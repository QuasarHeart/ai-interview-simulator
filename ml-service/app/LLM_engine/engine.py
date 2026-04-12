"""
通用接入大模型的框架，适配面试过程中的不同流程
"""
import asyncio
import logging
import os
import yaml
import json_repair
from dataclasses import dataclass, field
from typing import Any, Dict
from jinja2 import Environment, StrictUndefined
from openai import AsyncOpenAI
from app.schemas.schemas import StartRequest, FollowupRequest, AnalysisRequest, ReportRequest
from typing import AsyncGenerator
from pathlib import Path

logger = logging.getLogger(__name__)

FOLLOWUP_STAGE_SEQUENCE = ["intro", "resume_deep_dive", "tech_general", "tech_scenario", "reverse_qa", "end"]

@dataclass
class Settings:
    professional_weight: float = 0.5
    cognition_weight: float = 0.3
    expression_weight: float = 0.2

    professional_subweights: Dict[str, float] = field(
        default_factory=lambda: {
            "technical_correctness": 0.20,
            "knowledge_match": 0.09,
            "job_match": 0.31,
            "engineering_practice": 0.40,
        }
    )
    cognition_subweights: Dict[str, float] = field(
        default_factory=lambda: {
            "logic_structure": 1/3,
            "problem_solving": 1/3,
            "system_thinking": 1/3,
        }
    )
    expression_subweights: Dict[str, float] = field(
        default_factory=lambda: {
            "clarity": 1/3,
            "confidence_stability": 1/3,
            "professional_maturity": 1/3,
        }
    )


settings = Settings()

FOLLOWUP_HISTORY_WINDOW = max(1, int(os.getenv("FOLLOWUP_HISTORY_WINDOW", "4")))
FOLLOWUP_HISTORY_FIELD_MAX_CHARS = max(32, int(os.getenv("FOLLOWUP_HISTORY_FIELD_MAX_CHARS", "160")))
ANALYSIS_CONTEXT_MAX_CHARS = max(256, int(os.getenv("ANALYSIS_CONTEXT_MAX_CHARS", "1200")))
ANALYSIS_HISTORY_SUMMARY_MAX_CHARS = max(256, int(os.getenv("ANALYSIS_HISTORY_SUMMARY_MAX_CHARS", "1000")))
ANALYSIS_QUESTION_MAX_CHARS = max(128, int(os.getenv("ANALYSIS_QUESTION_MAX_CHARS", "500")))
ANALYSIS_ANSWER_MAX_CHARS = max(128, int(os.getenv("ANALYSIS_ANSWER_MAX_CHARS", "1500")))
REPORT_RESULT_TEXT_MAX_CHARS = max(64, int(os.getenv("REPORT_RESULT_TEXT_MAX_CHARS", "180")))
REPORT_SUGGESTION_MAX_CHARS = max(48, int(os.getenv("REPORT_SUGGESTION_MAX_CHARS", "140")))
REPORT_REASON_MAX_CHARS = max(48, int(os.getenv("REPORT_REASON_MAX_CHARS", "120")))


def _truncate_text(value: Any, max_chars: int) -> str:
    text = str(value or "").strip()
    if max_chars <= 0 or len(text) <= max_chars:
        return text
    if max_chars <= 3:
        return text[:max_chars]
    return f"{text[:max_chars - 3].rstrip()}..."


def _history_item_value(item: Any, field_name: str, fallback: str = "") -> str:
    if isinstance(item, dict):
        value = item.get(field_name, fallback)
    else:
        value = getattr(item, field_name, fallback)
    if value is None:
        return fallback
    return str(value)


def _history_item_flow_value(item: Any, field_name: str, fallback: str = "") -> str:
    flow_control = None
    if isinstance(item, dict):
        flow_control = item.get("flow_control")
    else:
        flow_control = getattr(item, "flow_control", None)
    if isinstance(flow_control, dict):
        value = flow_control.get(field_name, fallback)
    else:
        value = getattr(flow_control, field_name, fallback) if flow_control is not None else fallback
    if value is None:
        return fallback
    return str(value)


def _format_recent_history_for_prompt(recent_history: list[Any]) -> str:
    if not recent_history:
        return ""

    lines: list[str] = []
    for item in recent_history[-FOLLOWUP_HISTORY_WINDOW:]:
        round_id = _history_item_value(item, "round_id", "")
        assistant_content = _truncate_text(_history_item_value(item, "assistant_content", ""), FOLLOWUP_HISTORY_FIELD_MAX_CHARS)
        user_content = _truncate_text(_history_item_value(item, "user_content", ""), FOLLOWUP_HISTORY_FIELD_MAX_CHARS)
        stage_transition = _history_item_flow_value(item, "stage_transition", "continue")
        target_stage = _history_item_flow_value(item, "target_stage", "intro")
        lines.append(f"[{round_id}]: {assistant_content} | {user_content} | {stage_transition} -> {target_stage}")
    return "\n".join(lines)


def _compact_text_for_prompt(value: Any, max_chars: int) -> str:
    return _truncate_text(value, max_chars)


def _compact_analysis_prompt_kwargs(req: AnalysisRequest) -> dict[str, Any]:
    return {
        "current_stage": req.current_stage,
        "job_position": _compact_text_for_prompt(req.content_to_analyze.job_position, ANALYSIS_CONTEXT_MAX_CHARS),
        "jd_summary": _compact_text_for_prompt(req.content_to_analyze.jd_summary, ANALYSIS_CONTEXT_MAX_CHARS),
        "resume_content": _compact_text_for_prompt(req.content_to_analyze.resume_content, ANALYSIS_CONTEXT_MAX_CHARS),
        "question": _compact_text_for_prompt(req.content_to_analyze.question, ANALYSIS_QUESTION_MAX_CHARS),
        "user_answer": _compact_text_for_prompt(req.content_to_analyze.user_answer, ANALYSIS_ANSWER_MAX_CHARS),
        "history_summary": _compact_text_for_prompt(req.content_to_analyze.history_summary, ANALYSIS_HISTORY_SUMMARY_MAX_CHARS),
        "difficulty": req.interview_config.difficulty,
    }


def _compact_score_reason(reason: Any, max_chars: int = REPORT_REASON_MAX_CHARS) -> dict[str, Any]:
    if isinstance(reason, dict):
        return {
            "reason": _compact_text_for_prompt(reason.get("reason", ""), max_chars),
            "score": reason.get("score", 0.0),
        }
    return {"reason": _compact_text_for_prompt(reason, max_chars), "score": 0.0}


def _plain_object_to_dict(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return dict(value)
    if hasattr(value, "model_dump"):
        dumped = value.model_dump()
        if isinstance(dumped, dict):
            return dumped
    if hasattr(value, "__dict__"):
        return {key: nested for key, nested in vars(value).items() if not key.startswith("_")}
    return {}


def _compact_dimension_details(details: Any) -> dict[str, Any]:
    if not isinstance(details, dict):
        return {}

    compacted: dict[str, Any] = {}
    for section_name, section_value in details.items():
        if not isinstance(section_value, dict):
            compacted[section_name] = section_value
            continue

        compacted_section: dict[str, Any] = {}
        for key, value in section_value.items():
            compacted_section[key] = _compact_score_reason(value, REPORT_REASON_MAX_CHARS)
        compacted[section_name] = compacted_section
    return compacted


def _compact_round_results_for_report(round_results: list[Any]) -> list[dict[str, Any]]:
    compacted_results: list[dict[str, Any]] = []
    for item in round_results:
        round_result = _plain_object_to_dict(item)
        dimension_scores = _plain_object_to_dict(round_result.get("dimension_scores", {}))

        compacted_results.append(
            {
                "round_id": round_result.get("round_id"),
                "current_stage": round_result.get("current_stage", ""),
                "dimension_scores": dimension_scores,
                "dimension_details": _compact_dimension_details(round_result.get("dimension_details", {})),
                "overall_feedback": _compact_text_for_prompt(round_result.get("overall_feedback", ""), REPORT_RESULT_TEXT_MAX_CHARS),
                "final_score": round_result.get("final_score", 0.0),
                "improvement_suggestions": [
                    _compact_text_for_prompt(suggestion, REPORT_SUGGESTION_MAX_CHARS)
                    for suggestion in list(round_result.get("improvement_suggestions", []))[:3]
                ],
            }
        )
    return compacted_results


class LLMEngine:
    def __init__(self):
        self.api_key = os.getenv("DASHSCOPE_API_KEY", "").strip()
        if not self.api_key:
            raise ValueError("DASHSCOPE_API_KEY 未配置，服务无法启动")

        self.base_url = os.getenv("DASHSCOPE_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")
        self.model = os.getenv("JUDGE_MODEL", "qwen-turbo")
        self.temperature = float(os.getenv("SCORING_TEMPERATURE", "1.0"))
        self.request_timeout = float(os.getenv("LLM_REQUEST_TIMEOUT_SECONDS", "30"))
        self.max_retries = int(os.getenv("LLM_MAX_RETRIES", "1"))
        self.retry_backoff_seconds = float(os.getenv("LLM_RETRY_BACKOFF_SECONDS", "0.75"))

        self.template_env = Environment(undefined=StrictUndefined)

        self.client = AsyncOpenAI(api_key=self.api_key, base_url=self.base_url)
        # ===== 可移植路径：基于当前文件位置，不再硬编码 =====
        # engine.py 位于: ml-service/app/LLM_engine/engine.py
        # app 目录:       ml-service/app
        app_dir = Path(__file__).resolve().parent.parent

        self.prompts = {
            "start": self._load_yaml(app_dir / "prompts" / "start" / "start_v4.yaml"),
            "followup": self._load_yaml(app_dir / "prompts" / "follow_up" / "follow_up_v4.yaml"),
            "analysis": self._load_yaml(app_dir / "prompts" / "analysis" / "scoring_v3.yaml"),
            "report": self._load_yaml(app_dir / "prompts" / "report" / "report_v4.yaml"),
        }

    async def aclose(self) -> None:
        await self.client.close()

    def _load_yaml(self, path):
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Prompt file not found: {path}")
        with path.open("r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    @staticmethod
    def _derive_followup_stage_context(req: FollowupRequest) -> tuple[str, str]:
        current_stage = "intro"
        if req.history_data.recent_history:
            last_item = req.history_data.recent_history[-1]
            stage = last_item.flow_control.target_stage
            if stage in FOLLOWUP_STAGE_SEQUENCE:
                current_stage = stage

        idx = FOLLOWUP_STAGE_SEQUENCE.index(current_stage)
        next_stage = FOLLOWUP_STAGE_SEQUENCE[min(idx + 1, len(FOLLOWUP_STAGE_SEQUENCE) - 1)]
        return current_stage, next_stage

    def _build_prompts(self, prompt_config: dict, kwargs_dict: dict) -> tuple[str, str]:
        system_role = self.template_env.from_string(prompt_config["system_role"]).render(**kwargs_dict)
        rules = self.template_env.from_string(prompt_config["rules"]).render(**kwargs_dict)
        format_requirements = self.template_env.from_string(prompt_config["format_requirements"]).render(**kwargs_dict)
        user_prompt = self.template_env.from_string(prompt_config["input_context"]).render(**kwargs_dict)

        system_prompt = f"{system_role}\n\n{rules}\n\n{format_requirements}"
        return system_prompt, user_prompt

    @staticmethod
    def _loads_json_dict(raw_text: str) -> dict:
        parsed: Any = json_repair.loads(raw_text)
        if isinstance(parsed, tuple):
            parsed = parsed[0]
        if not isinstance(parsed, dict):
            raise ValueError(f"LLM 返回结果不是 JSON 对象，实际类型: {type(parsed).__name__}")
        return parsed

    async def _invoke_llm(self, prompt_config: dict, kwargs_dict: dict) -> dict:
        system_prompt, user_prompt = self._build_prompts(prompt_config, kwargs_dict)

        last_error: Exception | None = None
        for attempt in range(self.max_retries + 1):
            try:
                response = await self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=self.temperature,
                    timeout=self.request_timeout,
                )

                raw_text = response.choices[0].message.content or "{}"
                return self._loads_json_dict(raw_text)

            except Exception as exc:
                last_error = exc
                if attempt >= self.max_retries:
                    break
                sleep_seconds = self.retry_backoff_seconds * (2 ** attempt)
                logger.warning(
                    "LLM 调用失败，准备重试: attempt=%s/%s sleep=%.2fs error=%s",
                    attempt + 1,
                    self.max_retries + 1,
                    sleep_seconds,
                    str(exc),
                )
                await asyncio.sleep(sleep_seconds)

        raise RuntimeError(f"LLM 调用失败，已重试 {self.max_retries} 次: {last_error}")
    
    # 2) 把这两个方法加到 class LLMEngine 里（放在 _invoke_llm 后面最合适）

    async def stream_llm_raw_text(self, prompt_config: dict, kwargs_dict: dict) -> AsyncGenerator[str, None]:
        """
        流式返回模型原始文本 token（通常是 JSON 字符串片段）
        """
        system_prompt, user_prompt = self._build_prompts(prompt_config, kwargs_dict)

        stream = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=self.temperature,
            timeout=self.request_timeout,
            stream=True
        )

        async for chunk in stream:
            delta = None
            if chunk.choices and chunk.choices[0].delta:
                delta = chunk.choices[0].delta.content
            if delta:
                yield delta


    async def stream_first_question(self, req: StartRequest) -> AsyncGenerator[str, None]:
        """
        start 场景专用：返回原始 token 流
        """
        kwargs = {
            "job_position": req.job_position,
            "resume_content": req.resume_content,
            "interviewer_style": req.interview_config.interviewer_style,
            "company_context": req.interview_config.company_context,
            "difficulty": req.interview_config.difficulty,
            "jd_summary": req.jd_summary,
        }
        async for t in self.stream_llm_raw_text(self.prompts["start"], kwargs):
            yield t


    async def stream_following_question(
        self,
        req: FollowupRequest,
        forced_current_stage: str | None = None,
        forced_next_stage: str | None = None,
        forced_stage_round_index: int | None = None,
    ) -> AsyncGenerator[str, None]:
        """
        followup 场景专用：返回原始 token 流
        """
        current_stage, next_stage = self._derive_followup_stage_context(req)
        if forced_current_stage in FOLLOWUP_STAGE_SEQUENCE:
            current_stage = forced_current_stage
        if forced_next_stage in FOLLOWUP_STAGE_SEQUENCE:
            next_stage = forced_next_stage
        stage_round_index = forced_stage_round_index if isinstance(forced_stage_round_index, int) and forced_stage_round_index > 0 else 1
        kwargs = {
            "round_id": req.round_id,
            "job_position": req.background.job_position,
            "mode": req.interview_config.mode,
            "jd_summary": req.background.jd_summary,
            "resume_content": req.background.resume_content,
            "interviewer_style": req.interview_config.interviewer_style,
            "company_context": req.interview_config.company_context,
            "difficulty": req.interview_config.difficulty,
            "history_summary": req.history_data.history_summary,
            "current_stage": current_stage,
            "next_stage": next_stage,
            "stage_round_index": stage_round_index,
            "recent_history": _format_recent_history_for_prompt(req.history_data.recent_history),
        }
        async for t in self.stream_llm_raw_text(self.prompts["followup"], kwargs):
            yield t

    async def generate_first_question(self, req: StartRequest) -> dict:
        kwargs = {
            "job_position": req.job_position,
            "resume_content": req.resume_content,
            "interviewer_style": req.interview_config.interviewer_style,
            "company_context": req.interview_config.company_context,
            "difficulty": req.interview_config.difficulty,
            "jd_summary": req.jd_summary,
        }
        return await self._invoke_llm(self.prompts["start"], kwargs)

    async def generate_following_question(
        self,
        req: FollowupRequest,
        forced_current_stage: str | None = None,
        forced_next_stage: str | None = None,
        forced_stage_round_index: int | None = None,
    ) -> dict:
    # generate_following_question kwargs 补 mode，并统一 recent_history 格式
        current_stage, next_stage = self._derive_followup_stage_context(req)
        if forced_current_stage in FOLLOWUP_STAGE_SEQUENCE:
            current_stage = forced_current_stage
        if forced_next_stage in FOLLOWUP_STAGE_SEQUENCE:
            next_stage = forced_next_stage
        stage_round_index = forced_stage_round_index if isinstance(forced_stage_round_index, int) and forced_stage_round_index > 0 else 1
        kwargs = {
            "round_id": req.round_id,
            "job_position": req.background.job_position,
            "mode": req.interview_config.mode,  # 补上
            "jd_summary": req.background.jd_summary,
            "resume_content": req.background.resume_content,
            "interviewer_style": req.interview_config.interviewer_style,
            "company_context": req.interview_config.company_context,
            "difficulty": req.interview_config.difficulty,
            "history_summary": req.history_data.history_summary,
            "current_stage": current_stage,
            "next_stage": next_stage,
            "stage_round_index": stage_round_index,
            "recent_history": _format_recent_history_for_prompt(req.history_data.recent_history),
        }
        return await self._invoke_llm(self.prompts["followup"], kwargs)

    async def analyze_answer(self, req: AnalysisRequest) -> dict:
        kwargs = _compact_analysis_prompt_kwargs(req)

        ai_result = await self._invoke_llm(self.prompts["analysis"], kwargs)

        try:
            # 1) 兼容两种返回结构：
            # A. 新结构：{"dimension_details": {...}, "overall_feedback": "...", "improvement_suggestions": [...]}
            # B. 旧结构：{"professional": {...}, "cognition": {...}, "expression": {...}, "summary": {...}}
            if "dimension_details" in ai_result and isinstance(ai_result["dimension_details"], dict):
                details = ai_result["dimension_details"]
            else:
                details = {
                "professional": ai_result.get("professional", {}),
                "cognition": ai_result.get("cognition", {}),
                "expression": ai_result.get("expression", {}),
                }
                ai_result["dimension_details"] = details

            # 2) 兼容 summary 包裹层
            if "summary" in ai_result and isinstance(ai_result["summary"], dict):
                ai_result["overall_feedback"] = ai_result["summary"].get("overall_feedback", "")
                ai_result["improvement_suggestions"] = ai_result["summary"].get("improvement_suggestions", [])
            else:
                ai_result["overall_feedback"] = ai_result.get("overall_feedback", "")
                ai_result["improvement_suggestions"] = ai_result.get("improvement_suggestions", [])

            # 3) 安全读取 score（防止字符串、缺失、越界）
            def safe_score(section: str, key: str) -> float:
                try:
                    val = details[section][key]["score"]
                    val = float(val)
                    if val < 0:
                        return 0.0
                    if val > 5:
                        return 5.0
                    return val
                except Exception:
                    return 0.0

            # 4) 使用权重表 keys 来计算，避免模型漏字段导致 KeyError
            prof_score = sum(
                safe_score("professional", k) * w
                for k, w in settings.professional_subweights.items()
            )
            cog_score = sum(
                safe_score("cognition", k) * w
                for k, w in settings.cognition_subweights.items()
            )
            exp_score = sum(
                safe_score("expression", k) * w
                for k, w in settings.expression_subweights.items()
            )

            ai_result["dimension_scores"] = {
                "professional": round(prof_score, 1),
                "cognition": round(cog_score, 1),
                "expression": round(exp_score, 1),
            }

            total_5_point = (
                prof_score * settings.professional_weight
                + cog_score * settings.cognition_weight
                + exp_score * settings.expression_weight
            )
            ai_result["final_score"] = round(total_5_point * 20, 1)

        except Exception as e:
            logger.warning("计算得分失败，回退到兜底输出: %s", e)
            # 兜底，保证响应字段完整
            ai_result.setdefault("dimension_details", {
                "professional": {},
                "cognition": {},
                "expression": {},
            })
            ai_result.setdefault("dimension_scores", {
                "professional": 0.0,
                "cognition": 0.0,
                "expression": 0.0,
            })
            ai_result.setdefault("final_score", 0.0)
            ai_result.setdefault("overall_feedback", "")
            ai_result.setdefault("improvement_suggestions", [])

        return ai_result

    async def generate_overall_report(self, req: ReportRequest) -> dict:
        kwargs = {
            "job_position": _compact_text_for_prompt(req.interview_context.job_position, ANALYSIS_CONTEXT_MAX_CHARS),
            "jd_summary": _compact_text_for_prompt(req.interview_context.jd_summary, ANALYSIS_CONTEXT_MAX_CHARS),
            "resume_content": _compact_text_for_prompt(req.interview_context.resume_content, ANALYSIS_CONTEXT_MAX_CHARS),
            "difficulty": req.interview_config.difficulty,
            "total_rounds": req.interview_context.total_rounds,
            "interview_duration_seconds": req.interview_context.interview_duration_seconds,
            "round_results": _compact_round_results_for_report(req.round_results),
        }
        return await self._invoke_llm(self.prompts["report"], kwargs)