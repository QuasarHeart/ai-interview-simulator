"""version 2.0 report workflow"""
from __future__ import annotations

import asyncio
import json
from dataclasses import dataclass, field
import logging
import os
import time
from pathlib import Path
from typing import Any, Literal, cast
from urllib.parse import quote

import httpx
import json_repair
import yaml
import google.genai as genai
from google.genai import types as google_types
from jinja2 import Environment, StrictUndefined
from pydantic import BaseModel, Field

from app.schemas.schemas import (
    AnalysisRequest,
    CognitionDetails,
    ContentToAnalyze,
    DimensionDetails,
    DimensionScores,
    ExpressionDetails,
    InterviewConfig,
    InterviewContext as ReportInterviewContext,
    ProfessionalDetails,
    ReportRequest,
    RoundResultItem,
    ScoreReason,
)

logger = logging.getLogger("ml-service.official_reporting")

_DEFAULT_REPORT_CALLBACK_URL_TEMPLATE = "https://nas.feixingxr.com/api/v1/interviews/{interviewId}/report-callback"
_STYLE_SET = {"standard", "friendly", "aggressive", "expert"}
_DIFFICULTY_SET = {"easy", "medium", "hard"}
_MODE_SET = {"text", "audio", "video"}
_REPORT_ANALYSIS_CONCURRENCY = max(1, int(os.getenv("REPORT_ANALYSIS_CONCURRENCY", "3")))


def _env_bool(name: str, default: bool = False) -> bool:
    return os.getenv(name, str(default)).strip().lower() in {"1", "true", "yes", "on"}


def _env_int(name: str, default: int) -> int:
    return int(os.getenv(name, str(default)))


def _trace_enabled(default: bool = False) -> bool:
    raw_value = os.getenv("INTERVIEW_TRACE_LOG_DETAIL")
    if raw_value is not None:
        return raw_value.strip().lower() in {"1", "true", "yes", "on"}

    raw_value = os.getenv("OFFICIAL_TRACE_LOG_DETAIL")
    if raw_value is not None:
        return raw_value.strip().lower() in {"1", "true", "yes", "on"}

    raw_value = os.getenv("REPORT_LOG_PIPELINE")
    if raw_value is not None:
        return raw_value.strip().lower() in {"1", "true", "yes", "on"}

    return default


def _trace_max_chars(default: int = 12000) -> int:
    return max(
        256,
        int(
            os.getenv(
                "INTERVIEW_TRACE_LOG_MAX_CHARS",
                os.getenv("OFFICIAL_TRACE_LOG_MAX_CHARS", os.getenv("REPORT_LOG_PIPELINE_MAX_CHARS", str(default))),
            )
        ),
    )


def _serialize_log_value(value: Any, max_chars: int) -> str:
    if value is None:
        text = "null"
    elif isinstance(value, str):
        text = value
    else:
        if hasattr(value, "model_dump"):
            value = value.model_dump()
        try:
            text = json.dumps(value, ensure_ascii=False, default=str)
        except Exception as exc:  # pragma: no cover - extremely defensive
            text = f"<unserializable:{exc}>"

    if max_chars > 0 and len(text) > max_chars:
        return f"{text[:max_chars]}...(truncated)"
    return text


@dataclass(slots=True)
class Settings:
    professional_weight: float = 0.5
    cognition_weight: float = 0.3
    expression_weight: float = 0.2
    professional_subweights: dict[str, float] = field(
        default_factory=lambda: {
            "technical_correctness": 0.20,
            "knowledge_match": 0.09,
            "job_match": 0.31,
            "engineering_practice": 0.40,
        }
    )
    cognition_subweights: dict[str, float] = field(
        default_factory=lambda: {
            "logic_structure": 1 / 3,
            "problem_solving": 1 / 3,
            "system_thinking": 1 / 3,
        }
    )
    expression_subweights: dict[str, float] = field(
        default_factory=lambda: {
            "clarity": 1 / 3,
            "confidence_stability": 1 / 3,
            "professional_maturity": 1 / 3,
        }
    )


settings = Settings()


class _AnalysisSummary(BaseModel):
    overall_feedback: str = ""
    improvement_suggestions: list[str] = Field(default_factory=list)


class _AnalysisPromptOutput(BaseModel):
    professional: ProfessionalDetails
    cognition: CognitionDetails
    expression: ExpressionDetails
    summary: _AnalysisSummary


class _ReportPromptOutput(BaseModel):
    hiring_recommendation: Literal["Strong Hire", "Hire", "Weak Hire", "No Hire"]
    overall_score: float
    executive_summary: str
    strengths: list[str] = Field(default_factory=list)
    weaknesses: list[str] = Field(default_factory=list)
    ability_trend: str
    detailed_recommendation: str


@dataclass(slots=True)
class _GoogleReportModelConfig:
    model: str = os.getenv("REPORT_MODEL", "gemini-3.1-flash-lite-preview")
    temperature: float = float(os.getenv("SCORING_TEMPERATURE", "0.2"))
    google_api_key: str = os.getenv("GOOGLE_API_KEY", "").strip()
    google_use_vertexai: bool = os.getenv("GOOGLE_USE_VERTEXAI", "false").strip().lower() in {"1", "true", "yes", "on"}
    google_cloud_project: str = os.getenv("GOOGLE_CLOUD_PROJECT", "").strip()
    google_cloud_location: str = os.getenv("GOOGLE_CLOUD_LOCATION", "").strip()


class _GoogleReportEngine:
    def __init__(
        self,
        *,
        log_pipeline: bool | None = None,
        log_pipeline_max_chars: int | None = None,
    ) -> None:
        self._config = _GoogleReportModelConfig()
        self._template_env = Environment(undefined=StrictUndefined)
        self._prompt_root = Path(__file__).resolve().parent / "prompts"
        self._analysis_prompt = self._load_yaml(self._prompt_root / "analysis" / "scoring_v3.yaml")
        self._report_prompt = self._load_yaml(self._prompt_root / "report" / "report_v4.yaml")
        self._log_pipeline = _trace_enabled(False) if log_pipeline is None else log_pipeline
        self._log_pipeline_max_chars = max(
            256,
            int(log_pipeline_max_chars) if log_pipeline_max_chars is not None else _trace_max_chars(12000),
        )
        self._client = self._build_client()

    def _build_client(self) -> genai.Client:
        if self._config.google_use_vertexai:
            return genai.Client(
                vertexai=True,
                project=self._config.google_cloud_project or None,
                location=self._config.google_cloud_location or None,
            )
        if not self._config.google_api_key:
            raise ValueError("GOOGLE_API_KEY 未配置，或未启用 GOOGLE_USE_VERTEXAI")
        return genai.Client(api_key=self._config.google_api_key)

    @staticmethod
    def _load_yaml(path: Path) -> dict[str, Any]:
        if not path.exists():
            raise FileNotFoundError(f"Prompt file not found: {path}")
        with path.open("r", encoding="utf-8") as file:
            return yaml.safe_load(file)

    def _render_prompt(self, prompt_config: dict[str, Any], kwargs: dict[str, Any]) -> tuple[str, str]:
        system_role = self._template_env.from_string(prompt_config["system_role"]).render(**kwargs)
        rules = self._template_env.from_string(prompt_config["rules"]).render(**kwargs)
        format_requirements = self._template_env.from_string(prompt_config["format_requirements"]).render(**kwargs)
        user_prompt = self._template_env.from_string(prompt_config["input_context"]).render(**kwargs)
        return f"{system_role}\n\n{rules}\n\n{format_requirements}", user_prompt

    def _log_pipeline_event(
        self,
        stage: str,
        event: str,
        *,
        context: Any | None = None,
        payload: Any | None = None,
    ) -> None:
        if not self._log_pipeline:
            return

        if callable(context):
            context = context()
        if callable(payload):
            payload = payload()

        parts = [f"[Report-Pipeline] stage={stage}", f"event={event}"]
        if context is not None:
            parts.append(f"context={_serialize_log_value(context, 1024)}")
        if payload is not None:
            parts.append(f"payload={_serialize_log_value(payload, self._log_pipeline_max_chars)}")
        logger.info(" ".join(parts))

    @staticmethod
    def _parse_json_response(raw_text: str) -> dict[str, Any]:
        parsed: Any = json_repair.loads(raw_text)
        if isinstance(parsed, tuple):
            parsed = parsed[0]
        if not isinstance(parsed, dict):
            raise ValueError(f"LLM 返回结果不是 JSON 对象，实际类型: {type(parsed).__name__}")
        return parsed

    async def _generate_json(
        self,
        *,
        prompt_config: dict[str, Any],
        kwargs: dict[str, Any],
        schema: dict[str, Any],
        trace_stage: str,
        trace_context: Any | None = None,
    ) -> dict[str, Any]:
        self._log_pipeline_event(trace_stage, "input", context=trace_context, payload=kwargs)
        system_prompt, user_prompt = self._render_prompt(prompt_config, kwargs)
        self._log_pipeline_event(
            trace_stage,
            "rendered_prompts",
            context=trace_context,
            payload={"system_prompt": system_prompt, "user_prompt": user_prompt},
        )
        generation_config = google_types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=self._config.temperature,
            response_mime_type="application/json",
            response_json_schema=schema,
            thinking_config=google_types.ThinkingConfig(include_thoughts=False),
        )
        self._log_pipeline_event(
            trace_stage,
            "request",
            context=trace_context,
            payload={"model": self._config.model, "temperature": self._config.temperature},
        )
        try:
            response = await asyncio.to_thread(
                self._client.models.generate_content,
                model=self._config.model,
                contents=user_prompt,
                config=generation_config,
            )
            raw_text = getattr(response, "text", "") or "{}"
            self._log_pipeline_event(trace_stage, "response_raw", context=trace_context, payload=raw_text)
            parsed = self._parse_json_response(raw_text)
            self._log_pipeline_event(trace_stage, "response_parsed", context=trace_context, payload=parsed)
            return parsed
        except Exception as exc:
            self._log_pipeline_event(trace_stage, "error", context=trace_context, payload=str(exc))
            raise

    @staticmethod
    def _normalize_analysis_result(ai_result: dict[str, Any]) -> dict[str, Any]:
        if "dimension_details" in ai_result and isinstance(ai_result["dimension_details"], dict):
            details = ai_result["dimension_details"]
        else:
            details = {
                "professional": ai_result.get("professional", {}),
                "cognition": ai_result.get("cognition", {}),
                "expression": ai_result.get("expression", {}),
            }
            ai_result["dimension_details"] = details

        if "summary" in ai_result and isinstance(ai_result["summary"], dict):
            ai_result["overall_feedback"] = ai_result["summary"].get("overall_feedback", "")
            ai_result["improvement_suggestions"] = ai_result["summary"].get("improvement_suggestions", [])
        else:
            ai_result["overall_feedback"] = ai_result.get("overall_feedback", "")
            ai_result["improvement_suggestions"] = ai_result.get("improvement_suggestions", [])

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

        prof_score = sum(safe_score("professional", key) * weight for key, weight in settings.professional_subweights.items())
        cog_score = sum(safe_score("cognition", key) * weight for key, weight in settings.cognition_subweights.items())
        exp_score = sum(safe_score("expression", key) * weight for key, weight in settings.expression_subweights.items())

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
        return ai_result

    async def analyze_answer(self, req: AnalysisRequest) -> dict:
        kwargs = {
            "current_stage": req.current_stage,
            "job_position": req.content_to_analyze.job_position,
            "jd_summary": req.content_to_analyze.jd_summary,
            "resume_content": req.content_to_analyze.resume_content,
            "question": req.content_to_analyze.question,
            "user_answer": req.content_to_analyze.user_answer,
            "history_summary": req.content_to_analyze.history_summary,
            "difficulty": req.interview_config.difficulty,
        }
        trace_context = {
            "session_id": req.session_id,
            "round_id": req.round_id,
            "current_stage": req.current_stage,
        }
        ai_result = await self._generate_json(
            prompt_config=self._analysis_prompt,
            kwargs=kwargs,
            schema=_AnalysisPromptOutput.model_json_schema(),
            trace_stage="analysis",
            trace_context=trace_context,
        )
        normalized = self._normalize_analysis_result(ai_result)
        self._log_pipeline_event("analysis", "normalized_output", context=trace_context, payload=normalized)
        return normalized

    async def generate_overall_report(self, req: ReportRequest) -> dict:
        kwargs = {
            "job_position": req.interview_context.job_position,
            "jd_summary": req.interview_context.jd_summary,
            "resume_content": req.interview_context.resume_content,
            "difficulty": req.interview_config.difficulty,
            "total_rounds": req.interview_context.total_rounds,
            "interview_duration_seconds": req.interview_context.interview_duration_seconds,
            "round_results": [item.model_dump() for item in req.round_results],
        }
        trace_context = {
            "session_id": req.session_id,
            "total_rounds": req.interview_context.total_rounds,
            "interview_duration_seconds": req.interview_context.interview_duration_seconds,
        }
        report = await self._generate_json(
            prompt_config=self._report_prompt,
            kwargs=kwargs,
            schema=_ReportPromptOutput.model_json_schema(),
            trace_stage="report",
            trace_context=trace_context,
        )
        normalized = _ReportPromptOutput.model_validate(report).model_dump()
        self._log_pipeline_event("report", "normalized_output", context=trace_context, payload=normalized)
        return normalized

    async def aclose(self) -> None:
        return None


class OfficialReportService:
    def __init__(
        self,
        *,
        engine: Any | None = None,
        callback_url_template: str | None = None,
        report_request_timeout_sec: float | None = None,
        report_analysis_timeout_sec: float | None = None,
        report_generation_timeout_sec: float | None = None,
        log_pipeline: bool | None = None,
        log_pipeline_max_chars: int | None = None,
        log_callback_body: bool | None = None,
        log_callback_body_max_chars: int | None = None,
    ) -> None:
        self._engine = engine
        self._callback_url_template = (callback_url_template or os.getenv("REPORT_CALLBACK_URL_TEMPLATE", _DEFAULT_REPORT_CALLBACK_URL_TEMPLATE)).strip()
        self._report_request_timeout_sec = float(
            report_request_timeout_sec if report_request_timeout_sec is not None else os.getenv("REPORT_REQUEST_TIMEOUT_SECONDS", "20")
        )
        self._report_analysis_timeout_sec = max(
            1.0,
            float(
                report_analysis_timeout_sec if report_analysis_timeout_sec is not None else os.getenv(
                    "REPORT_ANALYSIS_TIMEOUT_SECONDS", "30"
                )
            ),
        )
        self._report_generation_timeout_sec = max(
            1.0,
            float(
                report_generation_timeout_sec if report_generation_timeout_sec is not None else os.getenv(
                    "REPORT_GENERATION_TIMEOUT_SECONDS", "90"
                )
            ),
        )
        self._log_pipeline = (
            log_pipeline
            if log_pipeline is not None
            else _trace_enabled(False)
        )
        self._log_pipeline_max_chars = max(
            256,
            int(
                log_pipeline_max_chars
                if log_pipeline_max_chars is not None
                else _trace_max_chars(12000)
            ),
        )
        self._log_callback_body = (
            log_callback_body
            if log_callback_body is not None
            else os.getenv("REPORT_LOG_CALLBACK_BODY", "true").strip().lower() in {"1", "true", "yes", "on"}
        )
        self._log_callback_body_max_chars = int(
            log_callback_body_max_chars if log_callback_body_max_chars is not None else os.getenv("REPORT_LOG_CALLBACK_BODY_MAX_CHARS", "20000")
        )

    async def aclose(self) -> None:
        if self._engine is None:
            return
        close = getattr(self._engine, "aclose", None)
        if callable(close):
            maybe_result = close()
            if asyncio.iscoroutine(maybe_result):
                await maybe_result
        self._engine = None

    def _ensure_engine(self) -> Any:
        if self._engine is None:
            self._engine = _GoogleReportEngine(
                log_pipeline=self._log_pipeline,
                log_pipeline_max_chars=self._log_pipeline_max_chars,
            )
        return self._engine

    def _log_pipeline_event(
        self,
        stage: str,
        event: str,
        *,
        context: Any | None = None,
        payload: Any | None = None,
    ) -> None:
        if not self._log_pipeline:
            return

        parts = [f"[Report-Pipeline] stage={stage}", f"event={event}"]
        if context is not None:
            parts.append(f"context={_serialize_log_value(context, 1024)}")
        if payload is not None:
            parts.append(f"payload={_serialize_log_value(payload, self._log_pipeline_max_chars)}")
        logger.info(" ".join(parts))

    def _resolve_report_callback_url(self, interview_id: str) -> str:
        safe_interview_id = quote(str(interview_id or "").strip(), safe="")
        template = self._callback_url_template
        if "{interviewId}" in template:
            return template.replace("{interviewId}", safe_interview_id)
        return template

    def _serialize_for_log(self, payload: dict[str, Any]) -> str:
        try:
            text = str(payload)
        except Exception as exc:  # pragma: no cover - extremely defensive
            text = f"<unserializable:{exc}>"
        if self._log_callback_body_max_chars > 0 and len(text) > self._log_callback_body_max_chars:
            return f"{text[:self._log_callback_body_max_chars]}...(truncated)"
        return text

    async def _post_callback_with_retry(self, callback_url: str, payload: dict[str, Any], max_attempts: int = 3) -> None:
        self._log_pipeline_event(
            "callback",
            "start",
            context={"callback_url": callback_url, "max_attempts": max_attempts},
            payload=payload,
        )
        timeout = httpx.Timeout(connect=5.0, read=self._report_request_timeout_sec, write=10.0, pool=5.0)
        async with httpx.AsyncClient(timeout=timeout) as client:
            for attempt in range(1, max_attempts + 1):
                try:
                    self._log_pipeline_event(
                        "callback",
                        "attempt",
                        context={"callback_url": callback_url, "attempt": attempt, "max_attempts": max_attempts},
                        payload=payload,
                    )
                    logger.info(
                        "[Report-Callback] sending attempt=%s/%s url=%s body=%s",
                        attempt,
                        max_attempts,
                        callback_url,
                        self._serialize_for_log(payload),
                    )
                    response = await client.post(callback_url, json=payload)
                    if 200 <= response.status_code < 300:
                        self._log_pipeline_event(
                            "callback",
                            "success",
                            context={"callback_url": callback_url, "attempt": attempt, "status_code": response.status_code},
                            payload=payload,
                        )
                        logger.info(
                            "[Report-Callback] sent successfully url=%s status=%s attempt=%s/%s",
                            callback_url,
                            response.status_code,
                            attempt,
                            max_attempts,
                        )
                        return
                    raise RuntimeError(f"callback status={response.status_code}, body={response.text[:300]}")
                except Exception as exc:
                    self._log_pipeline_event(
                        "callback",
                        "error",
                        context={"callback_url": callback_url, "attempt": attempt, "max_attempts": max_attempts},
                        payload=str(exc),
                    )
                    if attempt >= max_attempts:
                        logger.error(
                            "[Report-Callback] send failed url=%s attempts=%s error=%s",
                            callback_url,
                            max_attempts,
                            str(exc),
                        )
                        raise RuntimeError(f"callback failed after {max_attempts} attempts: {exc}") from exc
                    sleep_seconds = 2 ** (attempt - 1)
                    logger.warning(
                        "[Report-Callback] retry attempt=%s/%s sleep=%ss error=%s",
                        attempt,
                        max_attempts,
                        sleep_seconds,
                        str(exc),
                    )
                    await asyncio.sleep(sleep_seconds)

    @staticmethod
    def _zero_reason(message: str) -> ScoreReason:
        return ScoreReason(reason=message, score=0.0)

    @classmethod
    def _fallback_round_result(cls, *, round_id: int, stage: str, reason: str) -> RoundResultItem:
        zero_detail = DimensionDetails(
            professional=ProfessionalDetails(
                technical_correctness=cls._zero_reason(reason),
                knowledge_match=cls._zero_reason(reason),
                job_match=cls._zero_reason(reason),
                engineering_practice=cls._zero_reason(reason),
            ),
            cognition=CognitionDetails(
                logic_structure=cls._zero_reason(reason),
                problem_solving=cls._zero_reason(reason),
                system_thinking=cls._zero_reason(reason),
            ),
            expression=ExpressionDetails(
                clarity=cls._zero_reason(reason),
                confidence_stability=cls._zero_reason(reason),
                professional_maturity=cls._zero_reason(reason),
            ),
        )
        return RoundResultItem(
            round_id=round_id,
            current_stage=stage,
            dimension_scores=DimensionScores(professional=0.0, cognition=0.0, expression=0.0),
            dimension_details=zero_detail,
            overall_feedback=reason,
            final_score=0.0,
            improvement_suggestions=[reason],
        )

    @staticmethod
    def _get_attr_value(obj: Any, name: str, fallback: Any = "") -> Any:
        value = getattr(obj, name, fallback)
        if value is None:
            return fallback
        return value

    @staticmethod
    def _sanitize_mode(value: Any, fallback: str = "video") -> str:
        text = str(value or "").strip().lower()
        return text if text in _MODE_SET else fallback

    @staticmethod
    def _sanitize_style(value: Any, fallback: str = "standard") -> str:
        text = str(value or "").strip().lower()
        return text if text in _STYLE_SET else fallback

    @staticmethod
    def _sanitize_difficulty(value: Any, fallback: str = "medium") -> str:
        text = str(value or "").strip().lower()
        return text if text in _DIFFICULTY_SET else fallback

    @staticmethod
    def _to_interview_config(context: Any) -> InterviewConfig:
        return InterviewConfig(
            mode=cast(Any, OfficialReportService._sanitize_mode(OfficialReportService._get_attr_value(context, "mode", "video"))),
            interviewer_style=cast(
                Any,
                OfficialReportService._sanitize_style(
                    OfficialReportService._get_attr_value(context, "interviewer_style", "standard")
                ),
            ),
            difficulty=cast(
                Any,
                OfficialReportService._sanitize_difficulty(
                    OfficialReportService._get_attr_value(context, "difficulty", "medium")
                ),
            ),
            company_context=str(OfficialReportService._get_attr_value(context, "company_context", "")),
        )

    @staticmethod
    def _to_report_context(context: Any, *, total_rounds: int, interview_duration_seconds: int) -> ReportInterviewContext:
        return ReportInterviewContext(
            job_position=str(OfficialReportService._get_attr_value(context, "job_position", "")),
            jd_summary=str(OfficialReportService._get_attr_value(context, "jd_summary", "")),
            resume_content=str(OfficialReportService._get_attr_value(context, "resume_content", "")),
            total_rounds=total_rounds,
            interview_duration_seconds=interview_duration_seconds,
        )

    @staticmethod
    def _extract_round_text(stage_result: Any) -> tuple[str, str, str]:
        question = str(OfficialReportService._get_attr_value(stage_result, "question", "")).strip()
        user_answer = str(OfficialReportService._get_attr_value(stage_result, "user_answer", "")).strip()
        history_summary = str(OfficialReportService._get_attr_value(stage_result, "history_summary", "")).strip()
        return question, user_answer, history_summary

    @staticmethod
    def _extract_round_items(stage_result: Any) -> list[Any]:
        items = OfficialReportService._get_attr_value(stage_result, "turn_records", [])
        if isinstance(items, list):
            return items
        return []

    async def _score_round_result(
        self,
        *,
        engine: Any,
        analysis_request: AnalysisRequest,
        stage: str,
        round_id: int,
        semaphore: asyncio.Semaphore,
    ) -> RoundResultItem:
        async with semaphore:
            trace_context = {
                "session_id": analysis_request.session_id,
                "stage": stage,
                "round_id": round_id,
            }
            self._log_pipeline_event("analysis", "start", context=trace_context, payload=analysis_request)
            try:
                analysis = await asyncio.wait_for(
                    engine.analyze_answer(analysis_request),
                    timeout=self._report_analysis_timeout_sec,
                )
                self._log_pipeline_event("analysis", "done", context=trace_context, payload=analysis)
                dimension_details = analysis.get("dimension_details") or {
                    "professional": analysis.get("professional", {}),
                    "cognition": analysis.get("cognition", {}),
                    "expression": analysis.get("expression", {}),
                }
                return RoundResultItem(
                    round_id=round_id,
                    current_stage=stage,
                    dimension_scores=DimensionScores(**analysis.get("dimension_scores", {})),
                    dimension_details=DimensionDetails(**dimension_details),
                    overall_feedback=str(analysis.get("overall_feedback", "")),
                    final_score=float(analysis.get("final_score", 0.0)),
                    improvement_suggestions=list(analysis.get("improvement_suggestions", [])),
                )
            except asyncio.TimeoutError:
                logger.warning(
                    "[Report] stage analysis timeout session=%s stage=%s round=%s timeout=%ss",
                    analysis_request.session_id,
                    stage,
                    round_id,
                    self._report_analysis_timeout_sec,
                )
                self._log_pipeline_event(
                    "analysis",
                    "timeout",
                    context=trace_context,
                    payload={"timeout_seconds": self._report_analysis_timeout_sec},
                )
                return self._fallback_round_result(
                    round_id=round_id,
                    stage=stage,
                    reason=f"analysis timeout after {self._report_analysis_timeout_sec}s",
                )
            except Exception as exc:
                logger.exception("[Report] stage analysis failed session=%s stage=%s round=%s", analysis_request.session_id, stage, round_id)
                self._log_pipeline_event("analysis", "error", context=trace_context, payload=str(exc))
                return self._fallback_round_result(round_id=round_id, stage=stage, reason=f"analysis failed: {exc}")

    async def build_round_results(self, context: Any, stage_results: list[Any]) -> list[RoundResultItem]:
        engine = self._ensure_engine()
        interview_config = self._to_interview_config(context)
        self._log_pipeline_event(
            "build_round_results",
            "start",
            context={"session_id": self._get_attr_value(context, "session_id", ""), "stage_results": len(stage_results)},
            payload={"stage_results": [self._get_attr_value(item, "stage", "") for item in stage_results]},
        )

        semaphore = asyncio.Semaphore(_REPORT_ANALYSIS_CONCURRENCY)
        round_tasks: list[asyncio.Task[RoundResultItem]] = []
        round_id = 0
        for stage_result in stage_results:
            stage = str(self._get_attr_value(stage_result, "stage", "")).strip()
            if not stage or stage == "end":
                continue

            for turn_record in self._extract_round_items(stage_result) or [stage_result]:
                question, user_answer, history_summary = self._extract_round_text(turn_record)
                if not question:
                    question = str(self._get_attr_value(turn_record, "question", "")).strip()
                if not user_answer:
                    user_answer = str(self._get_attr_value(turn_record, "user_answer", "")).strip()
                if not history_summary:
                    history_summary = str(self._get_attr_value(turn_record, "history_summary", "")).strip()

                round_id += 1
                analysis_request = AnalysisRequest(
                    session_id=str(self._get_attr_value(context, "session_id", "")),
                    round_id=round_id,
                    current_stage=stage,
                    interview_config=interview_config,
                    content_to_analyze=ContentToAnalyze(
                        job_position=str(self._get_attr_value(context, "job_position", "")),
                        jd_summary=str(self._get_attr_value(context, "jd_summary", "")),
                        resume_content=str(self._get_attr_value(context, "resume_content", "")),
                        question=question or str(self._get_attr_value(stage_result, "question", "")),
                        user_answer=user_answer,
                        history_summary=history_summary or str(self._get_attr_value(stage_result, "history_summary", "")),
                    ),
                )
                round_tasks.append(
                    asyncio.create_task(
                        self._score_round_result(
                            engine=engine,
                            analysis_request=analysis_request,
                            stage=stage,
                            round_id=round_id,
                            semaphore=semaphore,
                        )
                    )
                )

        if not round_tasks:
            self._log_pipeline_event(
                "build_round_results",
                "empty",
                context={"session_id": self._get_attr_value(context, "session_id", "")},
                payload="no scored rounds collected",
            )
            return [self._fallback_round_result(round_id=1, stage="intro", reason="no scored rounds collected")]

        round_results = list(await asyncio.gather(*round_tasks))
        self._log_pipeline_event(
            "build_round_results",
            "done",
            context={"session_id": self._get_attr_value(context, "session_id", ""), "round_count": len(round_results)},
            payload=lambda: [item.model_dump() for item in round_results],
        )
        return round_results

    async def generate_and_callback(self, context: Any, stage_results: list[Any]) -> dict[str, Any]:
        session_id = str(self._get_attr_value(context, "session_id", ""))
        callback_url = self._resolve_report_callback_url(session_id)
        logger.info("[Report] start session=%s callback_url=%s", session_id, callback_url)
        self._log_pipeline_event(
            "report",
            "start",
            context={"session_id": session_id, "callback_url": callback_url, "stage_results": len(stage_results)},
            payload=[self._get_attr_value(item, "stage", "") for item in stage_results],
        )

        try:
            round_results = await self.build_round_results(context, stage_results)
            interview_duration_seconds = max(1, int(time.time() - float(self._get_attr_value(context, "started_at", time.time()))))
            interview_context = self._to_report_context(
                context,
                total_rounds=len(round_results),
                interview_duration_seconds=interview_duration_seconds,
            )
            interview_config = self._to_interview_config(context)
            report_request = ReportRequest(
                session_id=session_id,
                callback_url=None,
                interview_config=interview_config,
                interview_context=interview_context,
                round_results=round_results,
            )
            self._log_pipeline_event(
                "report",
                "generation_start",
                context={
                    "session_id": session_id,
                    "total_rounds": interview_context.total_rounds,
                    "interview_duration_seconds": interview_context.interview_duration_seconds,
                },
                payload=lambda: report_request.model_dump(),
            )
            report_payload = await asyncio.wait_for(
                self._ensure_engine().generate_overall_report(report_request),
                timeout=self._report_generation_timeout_sec,
            )
            self._log_pipeline_event(
                "report",
                "generation_done",
                context={"session_id": session_id},
                payload=report_payload,
            )
            logger.info(
                "[Report] prepared callback session=%s url=%s body=%s",
                session_id,
                callback_url,
                self._serialize_for_log(report_payload),
            )
            self._log_pipeline_event(
                "callback",
                "prepared",
                context={"session_id": session_id, "callback_url": callback_url},
                payload=report_payload,
            )
            await self._post_callback_with_retry(callback_url, report_payload)
            logger.info("[Report] callback completed successfully session=%s url=%s", session_id, callback_url)
            self._log_pipeline_event(
                "callback",
                "completed",
                context={"session_id": session_id, "callback_url": callback_url},
                payload={"status": "success"},
            )
            return {
                "status": "success",
                "callback_url": callback_url,
                "round_results": round_results,
                "report_payload": report_payload,
            }
        except asyncio.TimeoutError as exc:
            logger.warning(
                "[Report] generation timeout session=%s timeout=%ss url=%s",
                session_id,
                self._report_generation_timeout_sec,
                callback_url,
            )
            self._log_pipeline_event(
                "report",
                "generation_timeout",
                context={"session_id": session_id, "callback_url": callback_url},
                payload={"timeout_seconds": self._report_generation_timeout_sec},
            )
            failed_payload = {
                "code": 500,
                "message": "report_generation_failed",
                "data": {
                    "interviewId": session_id,
                    "session_id": session_id,
                    "status": "failed",
                    "error": f"report generation timed out after {self._report_generation_timeout_sec}s",
                },
            }
            try:
                logger.info(
                    "[Report] prepared failed callback session=%s url=%s body=%s",
                    session_id,
                    callback_url,
                    self._serialize_for_log(failed_payload),
                )
                self._log_pipeline_event(
                    "callback",
                    "prepared_failed",
                    context={"session_id": session_id, "callback_url": callback_url},
                    payload=failed_payload,
                )
                await self._post_callback_with_retry(callback_url, failed_payload)
                logger.info("[Report] failed callback delivered session=%s url=%s", session_id, callback_url)
                self._log_pipeline_event(
                    "callback",
                    "completed_failed",
                    context={"session_id": session_id, "callback_url": callback_url},
                    payload={"status": "failed"},
                )
            except Exception:
                logger.exception("[Report] failed callback send failed session=%s url=%s", session_id, callback_url)
            return {
                "status": "failed",
                "callback_url": callback_url,
                "error": failed_payload["data"]["error"],
                "failed_payload": failed_payload,
            }
        except Exception as exc:
            logger.exception("[Report] failed session=%s url=%s", session_id, callback_url)
            self._log_pipeline_event(
                "report",
                "error",
                context={"session_id": session_id, "callback_url": callback_url},
                payload=str(exc),
            )
            failed_payload = {
                "code": 500,
                "message": "report_generation_failed",
                "data": {
                    "interviewId": session_id,
                    "session_id": session_id,
                    "status": "failed",
                    "error": str(exc),
                },
            }
            try:
                logger.info(
                    "[Report] prepared failed callback session=%s url=%s body=%s",
                    session_id,
                    callback_url,
                    self._serialize_for_log(failed_payload),
                )
                self._log_pipeline_event(
                    "callback",
                    "prepared_failed",
                    context={"session_id": session_id, "callback_url": callback_url},
                    payload=failed_payload,
                )
                await self._post_callback_with_retry(callback_url, failed_payload)
                logger.info("[Report] failed callback delivered session=%s url=%s", session_id, callback_url)
                self._log_pipeline_event(
                    "callback",
                    "completed_failed",
                    context={"session_id": session_id, "callback_url": callback_url},
                    payload={"status": "failed"},
                )
            except Exception:
                logger.exception("[Report] failed callback send failed session=%s url=%s", session_id, callback_url)
            return {
                "status": "failed",
                "callback_url": callback_url,
                "error": str(exc),
                "failed_payload": failed_payload,
            }
