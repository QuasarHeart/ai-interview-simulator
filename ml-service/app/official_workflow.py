"""version 2.0 official workflow"""
from __future__ import annotations

import asyncio
import json
import logging
import os
import re
import time
from dataclasses import asdict, dataclass, field, is_dataclass
from pathlib import Path
from typing import Any, cast
from urllib.parse import quote

import httpx
import google.genai as genai
import yaml
from jinja2 import Environment, StrictUndefined

from livekit.agents import Agent, CloseReason, llm

logger = logging.getLogger("ml-service.official_workflow")
_DEFAULT_REPORT_CALLBACK_URL_TEMPLATE = "https://nas.feixingxr.com/api/v1/interviews/{interviewId}/report-callback"
_REPORT_CALLBACK_MAX_ATTEMPTS = max(1, int(os.getenv("REPORT_CALLBACK_MAX_ATTEMPTS", "3")))
_REPORT_REQUEST_TIMEOUT_SECONDS = max(1.0, float(os.getenv("REPORT_REQUEST_TIMEOUT_SECONDS", "20")))
_REPORT_MODEL = (os.getenv("REPORT_MODEL", "gemini-2.5-flash-lite") or "gemini-2.5-flash-lite").strip()
_REPORT_TEMPERATURE = float(os.getenv("REPORT_TEMPERATURE", "0.2"))
_REPORT_MAX_OUTPUT_TOKENS = max(256, int(os.getenv("REPORT_MAX_OUTPUT_TOKENS", "4096")))

_REPORT_SCORE_REASON_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "reason": {"type": "string"},
        "score": {"type": "number", "minimum": 0, "maximum": 5, "multipleOf": 0.5},
    },
    "required": ["reason", "score"],
    "additionalProperties": False,
}

_REPORT_DIMENSION_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "technical_correctness": _REPORT_SCORE_REASON_SCHEMA,
        "knowledge_match": _REPORT_SCORE_REASON_SCHEMA,
        "job_match": _REPORT_SCORE_REASON_SCHEMA,
        "engineering_practice": _REPORT_SCORE_REASON_SCHEMA,
    },
    "required": ["technical_correctness", "knowledge_match", "job_match", "engineering_practice"],
    "additionalProperties": False,
}

_REPORT_COGNITION_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "logic_structure": _REPORT_SCORE_REASON_SCHEMA,
        "problem_solving": _REPORT_SCORE_REASON_SCHEMA,
        "system_thinking": _REPORT_SCORE_REASON_SCHEMA,
    },
    "required": ["logic_structure", "problem_solving", "system_thinking"],
    "additionalProperties": False,
}

_REPORT_EXPRESSION_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "clarity": _REPORT_SCORE_REASON_SCHEMA,
        "confidence_stability": _REPORT_SCORE_REASON_SCHEMA,
        "professional_maturity": _REPORT_SCORE_REASON_SCHEMA,
    },
    "required": ["clarity", "confidence_stability", "professional_maturity"],
    "additionalProperties": False,
}

_REPORT_RESPONSE_JSON_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "hiring_recommendation": {
            "type": "string",
            "enum": ["Strong Hire", "Hire", "Weak Hire", "No Hire"],
        },
        "executive_summary": {"type": "string"},
        "strengths": {"type": "array", "items": {"type": "string"}},
        "weaknesses": {"type": "array", "items": {"type": "string"}},
        "ability_trend": {"type": "string"},
        "detailed_recommendation": {"type": "string"},
        "professional": _REPORT_DIMENSION_SCHEMA,
        "cognition": _REPORT_COGNITION_SCHEMA,
        "expression": _REPORT_EXPRESSION_SCHEMA,
    },
    "required": [
        "hiring_recommendation",
        "executive_summary",
        "strengths",
        "weaknesses",
        "ability_trend",
        "detailed_recommendation",
        "professional",
        "cognition",
        "expression",
    ],
    "additionalProperties": False,
}

_TRACE_LOG_DETAIL = (
    os.getenv("INTERVIEW_TRACE_LOG_DETAIL")
    or os.getenv("OFFICIAL_TRACE_LOG_DETAIL")
    or "false"
).strip().lower() in {"1", "true", "yes", "on"}
_TRACE_LOG_MAX_CHARS = max(
    256,
    int(
        os.getenv(
            "INTERVIEW_TRACE_LOG_MAX_CHARS",
            os.getenv("OFFICIAL_TRACE_LOG_MAX_CHARS", "8000"),
        )
    ),
)


def _trace_json_default(value: Any) -> Any:
    if is_dataclass(value):
        return asdict(cast(Any, value))
    if hasattr(value, "model_dump"):
        try:
            dumped = value.model_dump()
            if isinstance(dumped, dict):
                return dumped
        except Exception:
            pass
    return str(value)


def _trace_value(value: Any, max_chars: int = _TRACE_LOG_MAX_CHARS) -> str:
    if callable(value):
        try:
            value = value()
        except Exception as exc:  # pragma: no cover - defensive trace helper
            value = f"<trace-callable-error:{exc}>"

    if value is None:
        text = "null"
    elif isinstance(value, str):
        text = value
    else:
        try:
            text = json.dumps(value, ensure_ascii=False, default=_trace_json_default)
        except Exception:
            text = str(value)

    if max_chars > 0 and len(text) > max_chars:
        return f"{text[:max_chars]}...(truncated)"
    return text


def _trace_log(event: str, **fields: Any) -> None:
    if not _TRACE_LOG_DETAIL:
        return

    parts = [f"[Workflow-Trace] event={event}"]
    for key, value in fields.items():
        parts.append(f"{key}={_trace_value(value)}")
    logger.info(" ".join(parts))


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


@dataclass(slots=True)
class ReportModelConfig:
    report_model: str = _REPORT_MODEL
    report_temperature: float = _REPORT_TEMPERATURE
    report_max_output_tokens: int = _REPORT_MAX_OUTPUT_TOKENS
    google_api_key: str = os.getenv("GOOGLE_API_KEY", "").strip()
    google_use_vertexai: bool = os.getenv("GOOGLE_USE_VERTEXAI", "false").strip().lower() in {"1", "true", "yes", "on"}
    google_cloud_project: str = os.getenv("GOOGLE_CLOUD_PROJECT", "").strip()
    google_cloud_location: str = os.getenv("GOOGLE_CLOUD_LOCATION", "").strip()


def _build_report_model_client(config_obj: ReportModelConfig) -> genai.Client:
    _trace_log(
        "build_report_model_client_enter",
        model=config_obj.report_model,
        temperature=config_obj.report_temperature,
        use_vertexai=config_obj.google_use_vertexai,
        has_api_key=bool(config_obj.google_api_key),
    )

    if config_obj.google_use_vertexai:
        client = genai.Client(
            vertexai=True,
            project=config_obj.google_cloud_project or None,
            location=config_obj.google_cloud_location or None,
        )
    else:
        if not config_obj.google_api_key:
            raise ValueError("GOOGLE_API_KEY 未配置，或未启用 GOOGLE_USE_VERTEXAI")
        client = genai.Client(api_key=config_obj.google_api_key)

    _trace_log("build_report_model_client_exit", model=config_obj.report_model)
    return client


def _build_report_prompt_parts(
    context: InterviewContext,
    prompt_config: dict[str, Any],
    *,
    report_reason: str,
    conversation_summary: str,
    conversation_transcript: str,
) -> tuple[str, str, str]:
    render_kwargs = {
        "session_id": context.session_id,
        "metadata_source": context.metadata_source,
        "job_position": context.job_position,
        "jd_summary": context.jd_summary,
        "resume_content": context.resume_content,
        "interviewer_style": context.interviewer_style,
        "difficulty": context.difficulty,
        "company_context": context.company_context,
        "mode": context.mode,
        "report_reason": report_reason,
        "conversation_summary": conversation_summary,
        "conversation_transcript": conversation_transcript,
    }

    system_parts = [
        _render_prompt_block(prompt_config, "system_role", render_kwargs),
        _render_prompt_block(prompt_config, "rules", render_kwargs),
        _render_prompt_block(prompt_config, "format_requirements", render_kwargs),
    ]
    system_prompt = "\n\n".join(part for part in system_parts if part)
    user_prompt = _render_prompt_block(prompt_config, "input_context", render_kwargs)
    full_prompt = "\n\n".join(part for part in [system_prompt, user_prompt] if part)
    return system_prompt, user_prompt, full_prompt


async def _generate_report_text_with_model(*, system_prompt: str, user_prompt: str) -> str:
    config_obj = ReportModelConfig()
    client = _build_report_model_client(config_obj)
    generation_config: Any = {
        "system_instruction": system_prompt,
        "temperature": config_obj.report_temperature,
        "max_output_tokens": config_obj.report_max_output_tokens,
        "response_mime_type": "application/json",
        "response_json_schema": _REPORT_RESPONSE_JSON_SCHEMA,
    }
    response = await asyncio.to_thread(
        client.models.generate_content,
        model=config_obj.report_model,
        contents=user_prompt,
        config=generation_config,
    )
    return str(getattr(response, "text", "") or "")


def _message_text(message: Any) -> str:
    if message is None:
        return ""
    text_content = getattr(message, "text_content", None)
    if isinstance(text_content, str) and text_content.strip():
        return text_content.strip()
    content = getattr(message, "content", None)
    if isinstance(content, list):
        parts = [str(item).strip() for item in content if str(item).strip()]
        return "".join(parts).strip()
    if isinstance(content, str):
        return content.strip()
    return str(content or "").strip()


def _extract_last_assistant_message(turn_ctx: llm.ChatContext, fallback: str) -> str:
    items = list(getattr(turn_ctx, "items", []) or [])
    for item in reversed(items):
        if str(getattr(item, "role", "")).strip().lower() != "assistant":
            continue
        text = _message_text(item)
        if text:
            return text
    return fallback


def _extract_last_user_message(turn_ctx: llm.ChatContext, fallback: str = "") -> str:
    items = list(getattr(turn_ctx, "items", []) or [])
    for item in reversed(items):
        if str(getattr(item, "role", "")).strip().lower() != "user":
            continue
        text = _message_text(item)
        if text:
            return text
    return fallback


def _build_history_summary(turn_ctx: llm.ChatContext, max_items: int = 8) -> str:
    items = list(getattr(turn_ctx, "items", []) or [])
    if not items:
        return ""
    lines: list[str] = []
    for item in items[-max_items:]:
        role = str(getattr(item, "role", "unknown")).strip() or "unknown"
        text = _message_text(item)
        if text:
            lines.append(f"{role}: {text}")
    return "\n".join(lines)


def _build_conversation_transcript(turn_ctx: llm.ChatContext, max_items: int = 40, max_chars: int = 12000) -> str:
    items = list(getattr(turn_ctx, "items", []) or [])
    if not items:
        return ""

    transcript_items = items[-max_items:] if max_items > 0 else items
    lines: list[str] = []
    for item in transcript_items:
        role = str(getattr(item, "role", "unknown")).strip() or "unknown"
        text = _message_text(item)
        if text:
            lines.append(f"{role}: {text}")

    transcript = "\n".join(lines)
    if max_chars > 0 and len(transcript) > max_chars:
        return f"{transcript[:max_chars]}...(truncated)"
    return transcript


def _extract_last_message_from_items(items: list[Any], role: str, fallback: str = "") -> str:
    for item in reversed(items or []):
        if str(getattr(item, "role", "")).strip().lower() != role:
            continue
        text = _message_text(item)
        if text:
            return text
    return fallback


def _extract_json_report(report_text: str) -> dict[str, Any] | None:
    text = str(report_text or "").strip()
    if not text:
        return None

    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
        text = re.sub(r"\s*```$", "", text)

    start_index = text.find("{")
    end_index = text.rfind("}")
    if start_index >= 0 and end_index > start_index:
        text = text[start_index : end_index + 1]

    try:
        parsed = json.loads(text)
    except Exception:
        return None

    return parsed if isinstance(parsed, dict) else None


def _safe_report_score(report_payload: dict[str, Any], section: str, key: str) -> float:
    try:
        section_payload = report_payload.get(section, {})
        value = section_payload.get(key, {})
        score = float(value.get("score", 0.0))
        if score < 0:
            return 0.0
        if score > 5:
            return 5.0
        return score
    except Exception:
        return 0.0


def _compute_report_score_summary(report_payload: dict[str, Any]) -> dict[str, Any]:
    professional = sum(
        _safe_report_score(report_payload, "professional", key) * weight
        for key, weight in settings.professional_subweights.items()
    )
    cognition = sum(
        _safe_report_score(report_payload, "cognition", key) * weight
        for key, weight in settings.cognition_subweights.items()
    )
    expression = sum(
        _safe_report_score(report_payload, "expression", key) * weight
        for key, weight in settings.expression_subweights.items()
    )

    overall_5_point = (
        professional * settings.professional_weight
        + cognition * settings.cognition_weight
        + expression * settings.expression_weight
    )
    return {
        "dimension_scores": {
            "professional": round(professional, 1),
            "cognition": round(cognition, 1),
            "expression": round(expression, 1),
        },
        "overall_score": round(overall_5_point * 20, 1),
    }


def _ensure_string_list(value: Any) -> list[str]:
    if isinstance(value, (list, tuple)):
        return [str(item).strip() for item in value if str(item).strip()]
    text = str(value or "").strip()
    return [text] if text else []


def _build_report_summary_payload(report_payload: dict[str, Any]) -> dict[str, Any]:
    score_summary = _compute_report_score_summary(report_payload)
    normalized_payload = dict(report_payload)
    normalized_payload["overall_score"] = score_summary["overall_score"]
    return normalized_payload


def _build_callback_report_payload(report_payload: dict[str, Any]) -> dict[str, Any]:
    normalized_report = _build_report_summary_payload(report_payload)
    normalized_report["hiring_recommendation"] = str(normalized_report.get("hiring_recommendation", "")).strip()
    normalized_report["executive_summary"] = str(normalized_report.get("executive_summary", "")).strip()
    normalized_report["strengths"] = _ensure_string_list(normalized_report.get("strengths", []))
    normalized_report["weaknesses"] = _ensure_string_list(normalized_report.get("weaknesses", []))
    normalized_report["ability_trend"] = str(normalized_report.get("ability_trend", "")).strip()
    normalized_report["detailed_recommendation"] = str(normalized_report.get("detailed_recommendation", "")).strip()
    return normalized_report


def _resolve_report_callback_url(session_id: str) -> str:
    safe_interview_id = quote(str(session_id or "").strip(), safe="")
    template = os.getenv("REPORT_CALLBACK_URL_TEMPLATE", _DEFAULT_REPORT_CALLBACK_URL_TEMPLATE).strip()
    if "{interviewId}" in template:
        return template.replace("{interviewId}", safe_interview_id)
    return template


def _build_report_callback_body(*, session_id: str, report_payload: dict[str, Any]) -> dict[str, Any]:
    _ = session_id
    return _build_callback_report_payload(report_payload)


def _build_report_failure_callback_body(*, session_id: str, error: str) -> dict[str, Any]:
    return {
        "code": 500,
        "message": "report_generation_failed",
        "data": {
            "interviewId": session_id,
            "session_id": session_id,
            "status": "failed",
            "error": error,
        },
    }


async def _post_callback_with_retry(session_id: str, callback_url: str, payload: dict[str, Any], max_attempts: int = _REPORT_CALLBACK_MAX_ATTEMPTS) -> None:
    timeout = httpx.Timeout(connect=5.0, read=_REPORT_REQUEST_TIMEOUT_SECONDS, write=10.0, pool=5.0)
    async with httpx.AsyncClient(timeout=timeout) as client:
        for attempt in range(1, max_attempts + 1):
            try:
                logger.info(
                    "report_callback_attempt session_id=%s url=%s attempt=%s/%s body=%s",
                    session_id,
                    callback_url,
                    attempt,
                    max_attempts,
                    _trace_value(payload, 6000),
                )
                response = await client.post(callback_url, json=payload)
                if 200 <= response.status_code < 300:
                    logger.info(
                        "report_callback_success session_id=%s url=%s status=%s attempt=%s/%s",
                        session_id,
                        callback_url,
                        response.status_code,
                        attempt,
                        max_attempts,
                    )
                    return
                raise RuntimeError(f"callback status={response.status_code}, body={response.text[:300]}")
            except Exception as exc:
                if attempt >= max_attempts:
                    logger.exception(
                        "report_callback_failed session_id=%s url=%s attempts=%s",
                        session_id,
                        callback_url,
                        max_attempts,
                    )
                    raise RuntimeError(f"callback failed after {max_attempts} attempts: {exc}") from exc
                sleep_seconds = 2 ** (attempt - 1)
                logger.warning(
                    "report_callback_retry session_id=%s url=%s attempt=%s/%s sleep=%ss error=%s",
                    session_id,
                    callback_url,
                    attempt,
                    max_attempts,
                    sleep_seconds,
                    str(exc),
                )
                await asyncio.sleep(sleep_seconds)


@dataclass(slots=True)
class InterviewContext:
    session_id: str
    job_position: str
    jd_summary: str
    resume_content: str
    interviewer_style: str
    difficulty: str
    company_context: str
    mode: str
    metadata_source: str = "defaults"
    started_at: float = field(default_factory=time.time)


INTERVIEW_FLOW_SEQUENCE = ["intro", "resume_deep_dive", "tech_general", "tech_scenario", "reverse_qa", "end"]
_PROMPT_ROOT = Path(__file__).resolve().parent / "prompts" / "official"
_PROMPT_FILE = _PROMPT_ROOT / "agent_persona_v1.yaml"
_REPORT_PROMPT_FILE = _PROMPT_ROOT / "report_generation_v1.yaml"
_PROMPT_TEMPLATE_ENV = Environment(autoescape=False, trim_blocks=True, lstrip_blocks=True, undefined=StrictUndefined)


def _load_prompt_config(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as file:
        prompt_config = yaml.safe_load(file)
    if not isinstance(prompt_config, dict):
        raise ValueError(f"prompt config must be a mapping: {path}")
    return cast(dict[str, Any], prompt_config)


def _render_prompt_block(prompt_config: dict[str, Any], key: str, kwargs: dict[str, Any]) -> str:
    template = prompt_config.get(key)
    if not template:
        return ""
    return _PROMPT_TEMPLATE_ENV.from_string(str(template)).render(**kwargs).strip()


def _build_global_prompt(context: InterviewContext, prompt_config: dict[str, Any]) -> str:
    flow_summary = " -> ".join(INTERVIEW_FLOW_SEQUENCE)
    render_kwargs = {
        "session_id": context.session_id,
        "metadata_source": context.metadata_source,
        "job_position": context.job_position,
        "jd_summary": context.jd_summary,
        "resume_content": context.resume_content,
        "interviewer_style": context.interviewer_style,
        "difficulty": context.difficulty,
        "company_context": context.company_context,
        "mode": context.mode,
        "flow_summary": flow_summary,
    }

    prompt_parts = [
        _render_prompt_block(prompt_config, "system_role", render_kwargs),
        _render_prompt_block(prompt_config, "rules", render_kwargs),
        _render_prompt_block(prompt_config, "stage_strategy", render_kwargs),
        _render_prompt_block(prompt_config, "deep_dive_strategy", render_kwargs),
        _render_prompt_block(prompt_config, "turn_correction", render_kwargs),
        _render_prompt_block(prompt_config, "tool_contract", render_kwargs),
        _render_prompt_block(prompt_config, "anti_rush_control", render_kwargs),
        _render_prompt_block(prompt_config, "interviewer_style_policy", render_kwargs),
        _render_prompt_block(prompt_config, "format_requirements", render_kwargs),
        _render_prompt_block(prompt_config, "input_context", render_kwargs),
    ]
    return "\n\n".join(part for part in prompt_parts if part)


def _build_report_prompt(
    context: InterviewContext,
    prompt_config: dict[str, Any],
    *,
    report_reason: str,
    conversation_summary: str,
    conversation_transcript: str,
) -> str:
    _, _, full_prompt = _build_report_prompt_parts(
        context,
        prompt_config,
        report_reason=report_reason,
        conversation_summary=conversation_summary,
        conversation_transcript=conversation_transcript,
    )
    return full_prompt


class AINativeOfficialPromptRegistry:
    def __init__(self) -> None:
        self._prompt_config = _load_prompt_config(_PROMPT_FILE)
        self._report_prompt_config = _load_prompt_config(_REPORT_PROMPT_FILE)
        _trace_log(
            "prompt_registry_init",
            prompt_root=str(_PROMPT_ROOT),
            prompt_file=str(_PROMPT_FILE),
            report_prompt_file=str(_REPORT_PROMPT_FILE),
        )

    def render_agent_persona(self, context: InterviewContext) -> str:
        prompt = _build_global_prompt(context, self._prompt_config)
        _trace_log("prompt_render_agent_persona", session_id=context.session_id, prompt=prompt)
        return prompt

    def render_report_generation_prompt(
        self,
        context: InterviewContext,
        *,
        report_reason: str,
        conversation_summary: str,
        conversation_transcript: str,
    ) -> str:
        prompt = _build_report_prompt(
            context,
            self._report_prompt_config,
            report_reason=report_reason,
            conversation_summary=conversation_summary,
            conversation_transcript=conversation_transcript,
        )
        _trace_log(
            "prompt_render_report_generation",
            session_id=context.session_id,
            report_reason=report_reason,
            prompt=prompt,
        )
        return prompt


class AINativeInterviewWorkflowAgent(Agent):
    def __init__(self, interview_context: InterviewContext, prompts: AINativeOfficialPromptRegistry) -> None:
        super().__init__(instructions=prompts.render_agent_persona(interview_context))
        self._context = interview_context
        self._prompts = prompts
        self._state_lock = asyncio.Lock()
        self._finalization_requested = False
        self._finalization_reason = "model_requested_end"
        self._report_generation_started = False
        self._report_generation_completed = False
        self._report_generation_task: asyncio.Task[None] | None = None
        self._final_report_text = ""
        self._final_report_payload: dict[str, Any] | None = None
        self._final_report_callback_payload: dict[str, Any] | None = None
        _trace_log("workflow_agent_init", context=interview_context)

    def _request_session_close_after_report(self) -> None:
        try:
            session = self.session
        except RuntimeError:
            session = None

        close_soon = getattr(session, "_close_soon", None)
        if callable(close_soon):
            _trace_log(
                "workflow_room_close_requested",
                session_id=self._context.session_id,
                reason=CloseReason.TASK_COMPLETED.value,
            )
            close_soon(reason=CloseReason.TASK_COMPLETED)
            return

        aclose = getattr(session, "aclose", None)
        if callable(aclose):
            _trace_log("workflow_room_close_fallback", session_id=self._context.session_id, reason="session_missing_close_soon")
            close_result = aclose()
            if asyncio.iscoroutine(close_result):
                asyncio.create_task(close_result)

    def _build_report_generation_prompt(self, reason: str) -> str:
        conversation_summary = _build_history_summary(self.chat_ctx)
        conversation_transcript = _build_conversation_transcript(self.chat_ctx)
        return self._prompts.render_report_generation_prompt(
            self._context,
            report_reason=reason,
            conversation_summary=conversation_summary,
            conversation_transcript=conversation_transcript,
        )

    async def _finalize_report_generation(self, reason: str) -> None:
        session_id = self._context.session_id
        callback_url = _resolve_report_callback_url(session_id)
        system_prompt, user_prompt, report_prompt = _build_report_prompt_parts(
            self._context,
            self._prompts._report_prompt_config,
            report_reason=reason,
            conversation_summary=_build_history_summary(self.chat_ctx),
            conversation_transcript=_build_conversation_transcript(self.chat_ctx),
        )
        callback_body: dict[str, Any] | None = None

        _trace_log(
            "tool_finish_interview_report_model_request_started",
            session_id=session_id,
            reason=reason,
            report_prompt=report_prompt,
        )

        try:
            report_text = await _generate_report_text_with_model(system_prompt=system_prompt, user_prompt=user_prompt)
        except Exception as exc:
            report_text = ""
            self._final_report_text = report_text
            self._final_report_payload = {"_report_model_error": str(exc)}
            callback_body = _build_report_failure_callback_body(
                session_id=session_id,
                error=f"final report generation failed: {exc}",
            )
            logger.exception("report_generation_model_failed session=%s", session_id)
            _trace_log(
                "report_generation_model_failed",
                session_id=session_id,
                reason=reason,
                error=str(exc),
            )
        else:
            self._final_report_text = report_text
            report_payload = _extract_json_report(report_text)
            if report_payload is None:
                self._final_report_payload = {"_raw_report_text": report_text}
                callback_body = _build_report_failure_callback_body(
                    session_id=session_id,
                    error="final report JSON parse failed",
                )
                logger.warning("report_generation_json_parse_failed session=%s", session_id)
                _trace_log(
                    "report_generation_json_parse_failed",
                    session_id=session_id,
                    reason=reason,
                    report_text=report_text,
                )
            else:
                normalized_report = _build_report_summary_payload(report_payload)
                self._final_report_payload = normalized_report
                callback_body = _build_report_callback_body(session_id=session_id, report_payload=normalized_report)
                _trace_log(
                    "report_generation_score_summary",
                    session_id=session_id,
                    score_summary=_compute_report_score_summary(report_payload),
                )

        self._final_report_callback_payload = callback_body
        self._report_generation_completed = True
        _trace_log(
            "report_generation_completed",
            session_id=session_id,
            reason=reason,
            report_payload=self._final_report_payload,
            callback_body=callback_body,
        )

        if callback_body is not None:
            try:
                await _post_callback_with_retry(session_id, callback_url, callback_body)
            except Exception as exc:
                logger.exception("report_generation_callback_failed session=%s url=%s", session_id, callback_url)
                _trace_log(
                    "report_generation_callback_failed",
                    session_id=session_id,
                    callback_url=callback_url,
                    error=str(exc),
                )

        self._request_session_close_after_report()

    @llm.function_tool
    async def finish_interview(self, reason: str = "model_requested_end") -> dict[str, Any]:
        _trace_log(
            "tool_finish_interview_enter",
            session_id=self._context.session_id,
            reason=reason,
            finalization_requested=self._finalization_requested,
        )

        async with self._state_lock:
            self._finalization_requested = True
            self._finalization_reason = reason
            if self._report_generation_started:
                _trace_log(
                    "tool_finish_interview_report_generation_already_started",
                    session_id=self._context.session_id,
                    reason=reason,
                )
                return {
                    "status": "report_generation_already_started",
                    "reason": reason,
                    "report_generation_started": True,
                    "message": "最终报告生成已在进行中。",
                }
            self._report_generation_started = True

        report_prompt = self._build_report_generation_prompt(reason)
        _trace_log(
            "tool_finish_interview_report_prompt_prepared",
            session_id=self._context.session_id,
            reason=reason,
            report_prompt=report_prompt,
        )
        try:
            self._report_generation_task = asyncio.create_task(self._finalize_report_generation(reason))
        except Exception as exc:
            async with self._state_lock:
                self._report_generation_started = False
            logger.exception("report_generation_schedule_failed session=%s", self._context.session_id)
            _trace_log(
                "tool_finish_interview_report_generation_schedule_failed",
                session_id=self._context.session_id,
                reason=reason,
                error=str(exc),
            )
            return {
                "status": "report_generation_schedule_failed",
                "reason": reason,
                "report_generation_started": False,
                "error": str(exc),
            }
        _trace_log(
            "tool_finish_interview_report_generation_started",
            session_id=self._context.session_id,
            reason=reason,
            report_task=self._report_generation_task,
        )
        return {
            "status": "report_generation_started",
            "reason": reason,
            "report_generation_started": True,
            "message": "已提交最终报告生成任务，等待报告模型完成后自动结束房间。",
        }

    async def on_enter(self) -> None:
        _trace_log("workflow_start", session_id=self._context.session_id, mode="ai_native_tools")
        logger.info("workflow_start session=%s mode=ai_native_tools", self._context.session_id)
        generate_reply = getattr(self.session, "generate_reply", None)
        if callable(generate_reply):
            _trace_log(
                "workflow_start_generate_reply_requested",
                session_id=self._context.session_id,
                instructions="请根据全局提示自然开场并提出第一问；一次只问一个问题，问完就停住，等待用户完整回答后再继续。你需要自己判断面试阶段，但不能连续抛出多个问题。",
            )
            generate_reply(
                instructions=(
                    "请根据全局提示自然开场并提出第一问；一次只问一个问题，问完就停住，等待用户完整回答后再继续。你需要自己判断面试阶段，但不能连续抛出多个问题。"
                )
            )
        else:
            _trace_log("workflow_start_generate_reply_unavailable", session_id=self._context.session_id)

    async def on_exit(self) -> None:
        _trace_log(
            "workflow_on_exit",
            session_id=self._context.session_id,
            finalization_requested=self._finalization_requested,
            report_generation_started=self._report_generation_started,
            report_generation_completed=self._report_generation_completed,
        )
        _trace_log(
            "workflow_on_exit_snapshot_ready",
            session_id=self._context.session_id,
            round_count=len(getattr(self.chat_ctx, "items", []) or []),
            finalization_requested=self._finalization_requested,
            finalization_reason=self._finalization_reason,
            report_generation_started=self._report_generation_started,
            report_generation_completed=self._report_generation_completed,
        )

        if self._finalization_requested and not self._report_generation_started:
            logger.warning("workflow_on_exit_without_report_generation session=%s", self._context.session_id)
            _trace_log(
                "workflow_on_exit_without_report_generation",
                session_id=self._context.session_id,
                finalization_reason=self._finalization_reason,
            )

        if self._report_generation_task is not None and not self._report_generation_task.done():
            _trace_log(
                "workflow_on_exit_report_task_pending",
                session_id=self._context.session_id,
                finalization_reason=self._finalization_reason,
            )


OfficialPromptRegistry = cast(Any, AINativeOfficialPromptRegistry)
InterviewWorkflowAgent = cast(Any, AINativeInterviewWorkflowAgent)
