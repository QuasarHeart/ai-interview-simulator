"""
通用接入大模型的框架，适配面试过程中的不同流程
"""
import os
import yaml
import json_repair
from dataclasses import dataclass, field
from typing import Dict
from jinja2 import Environment, StrictUndefined
from openai import AsyncOpenAI
from app.schemas.schemas import StartRequest, FollowupRequest, AnalysisRequest, ReportRequest
from typing import AsyncGenerator
from pathlib import Path

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


class LLMEngine:
    def __init__(self):
        #这里的在运行之前需要设置环境变量加上apikey或者硬编码apikey
        self.api_key = os.getenv("DASHSCOPE_API_KEY", "APIkey")
        self.base_url = os.getenv("DASHSCOPE_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")
        self.model = os.getenv("JUDGE_MODEL", "qwen-plus")
        self.temperature = float(os.getenv("SCORING_TEMPERATURE", "0.2"))

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

    def _load_yaml(self, path):
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Prompt file not found: {path}")
        with path.open("r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    async def _invoke_llm(self, prompt_config: dict, kwargs_dict: dict) -> dict:
        env = Environment(undefined=StrictUndefined)

        system_role = env.from_string(prompt_config["system_role"]).render(**kwargs_dict)
        rules = env.from_string(prompt_config["rules"]).render(**kwargs_dict)
        format_requirements = env.from_string(prompt_config["format_requirements"]).render(**kwargs_dict)
        user_prompt = env.from_string(prompt_config["input_context"]).render(**kwargs_dict)

        system_prompt = f"{system_role}\n\n{rules}\n\n{format_requirements}"

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=self.temperature
        )

        raw_text = response.choices[0].message.content or "{}"
        return json_repair.loads(raw_text)
    
    # 2) 把这两个方法加到 class LLMEngine 里（放在 _invoke_llm 后面最合适）

    async def stream_llm_raw_text(self, prompt_config: dict, kwargs_dict: dict) -> AsyncGenerator[str, None]:
        """
        流式返回模型原始文本 token（通常是 JSON 字符串片段）
        """
        env = Environment(undefined=StrictUndefined)

        system_role = env.from_string(prompt_config["system_role"]).render(**kwargs_dict)
        rules = env.from_string(prompt_config["rules"]).render(**kwargs_dict)
        format_requirements = env.from_string(prompt_config["format_requirements"]).render(**kwargs_dict)
        user_prompt = env.from_string(prompt_config["input_context"]).render(**kwargs_dict)
        system_prompt = f"{system_role}\n\n{rules}\n\n{format_requirements}"

        stream = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=self.temperature,
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
            "difficulty": req.interview_config.difficulty
        }
        async for t in self.stream_llm_raw_text(self.prompts["start"], kwargs):
            yield t


    async def stream_following_question(self, req: FollowupRequest) -> AsyncGenerator[str, None]:
        """
        followup 场景专用：返回原始 token 流
        """
        kwargs = {
            "current_stage": req.flow_control.target_stage,
            "jd_summary": req.background.jd_summary,
            "resume_summary": req.background.resume_summary,
            "interviewer_style": req.interview_config.interviewer_style,
            "company_context": req.interview_config.company_context,
            "difficulty": req.interview_config.difficulty,
            "history_summary": req.history_data.history_summary,
            "recent_history": "\n".join([f"[{item.role}]: {item.content}" for item in req.history_data.recent_history])
        }
        async for t in self.stream_llm_raw_text(self.prompts["followup"], kwargs):
            yield t

    async def generate_first_question(self, req: StartRequest) -> dict:
        kwargs = {
            "job_position": req.job_position,
            "resume_content": req.resume_content,
            "interviewer_style": req.interview_config.interviewer_style,
            "company_context": req.interview_config.company_context,
            "difficulty": req.interview_config.difficulty
        }
        return await self._invoke_llm(self.prompts["start"], kwargs)

    async def generate_following_question(self, req: FollowupRequest) -> dict:
        kwargs = {
            "current_stage": req.flow_control.target_stage,
            "jd_summary": req.background.jd_summary,
            "resume_summary": req.background.resume_summary,
            "interviewer_style": req.interview_config.interviewer_style,
            "company_context": req.interview_config.company_context,  # 补
            "difficulty": req.interview_config.difficulty,
            "history_summary": req.history_data.history_summary,
            "recent_history": "\n".join([f"[{item.role}]: {item.content}" for item in req.history_data.recent_history])
        }
        return await self._invoke_llm(self.prompts["followup"], kwargs)

    async def analyze_answer(self, req: AnalysisRequest) -> dict:
        kwargs = {
            "current_stage": req.current_stage,
            "job_position": req.content_to_analyze.job_position,
            "jd_summary": req.content_to_analyze.jd_summary,
            "resume_summary": req.content_to_analyze.resume_summary,
            "question": req.content_to_analyze.question,
            "user_answer": req.content_to_analyze.user_answer,
            "history_summary": req.content_to_analyze.history_summary,
            "difficulty": req.interview_config.difficulty,
        }

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
            print(f"[警告] 计算得分失败，依赖 AI 原生输出。错误: {e}")
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
            "job_position": req.interview_context.job_position,
            "jd_summary": req.interview_context.jd_summary,
            "resume_summary": req.interview_context.resume_summary,  # 补
            "difficulty": req.interview_config.difficulty,           # 补
            "total_rounds": req.interview_context.total_rounds,
            "interview_duration_seconds": req.interview_context.interview_duration_seconds,
            "round_results": [item.model_dump() for item in req.round_results]
        }
        return await self._invoke_llm(self.prompts["report"], kwargs)