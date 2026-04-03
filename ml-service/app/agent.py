"""LiveKit 3.0 AI-native dual-model runtime (aligned to livekit-agents 1.5.1).

Implemented in this module:
- LiveKit-first session runtime using AgentServer + AgentSession
- Realtime model: qwen3-omni-flash-realtime
- Reasoning model: qwen3-max-preview
- Non-blocking dual-model orchestration with per-session queues
- Exact AgentSession event binding for user_state_changed/user_input_transcribed
"""

from __future__ import annotations

import asyncio
import contextlib
import inspect
import json
import logging
import os
import time
import math
import httpx
from urllib.parse import quote
from enum import StrEnum
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional
from uuid import uuid4

import json_repair
import yaml
from dotenv import load_dotenv
from jinja2 import Environment, StrictUndefined
from openai import AsyncOpenAI

from livekit import agents
from livekit.agents import Agent, AgentServer, AgentSession, room_io
try:
    from app.realtime.dashscope_realtime import build_dashscope_realtime_model
except ModuleNotFoundError:
    from realtime.dashscope_realtime import build_dashscope_realtime_model


load_dotenv(os.getenv("ML_SERVICE_ENV_FILE", ".env.ml-service"))
logger = logging.getLogger("ml-service.agent")

_MULTIMODAL_UNAVAILABLE_WARNED = False

STAGE_SEQUENCE = ["intro", "resume_deep_dive", "tech_general", "tech_scenario", "reverse_qa", "end"]
STAGE_SET = set(STAGE_SEQUENCE)
STYLE_SET = {"standard", "friendly", "aggressive", "expert"}
DIFFICULTY_SET = {"easy", "medium", "hard"}
MODE_SET = {"text", "audio", "video"}


class CommandType(StrEnum):
    INTERRUPT_ASSISTANT = "interrupt_assistant"
    STRATEGY_UPDATE = "strategy_update"
    ASSISTANT_SOFT_INTERRUPT = "assistant_soft_interrupt"
    PACE_CONTROL = "pace_control"

# Keep 2.0 scoring strictly aligned with 1.0 weight system.
PROFESSIONAL_SUBWEIGHTS: dict[str, float] = {
    "technical_correctness": 0.20,
    "knowledge_match": 0.09,
    "job_match": 0.31,
    "engineering_practice": 0.40,
}
COGNITION_SUBWEIGHTS: dict[str, float] = {
    "logic_structure": 1 / 3,
    "problem_solving": 1 / 3,
    "system_thinking": 1 / 3,
}
EXPRESSION_SUBWEIGHTS: dict[str, float] = {
    "clarity": 1 / 3,
    "confidence_stability": 1 / 3,
    "professional_maturity": 1 / 3,
}
DIMENSION_WEIGHTS: dict[str, float] = {
    "professional": 0.5,
    "cognition": 0.3,
    "expression": 0.2,
}


def _safe_float(value: Any, fallback: float = 0.0) -> float:
    try:
        if value is None:
            return fallback
        out = float(value)
        if math.isnan(out) or math.isinf(out):
            return fallback
        return out
    except Exception:
        return fallback


def _clamp_score_0_5(value: float) -> float:
    return max(0.0, min(5.0, value))


def _score_reason(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return {
            "reason": str(value.get("reason", "")).strip(),
            "score": _clamp_score_0_5(_safe_float(value.get("score"), 0.0)),
        }
    return {"reason": "", "score": 0.0}


def _normalize_dimension_details(raw: Any) -> dict[str, Any]:
    src = raw if isinstance(raw, dict) else {}
    professional_raw = src.get("professional")
    cognition_raw = src.get("cognition")
    expression_raw = src.get("expression")
    professional: dict[str, Any] = professional_raw if isinstance(professional_raw, dict) else {}
    cognition: dict[str, Any] = cognition_raw if isinstance(cognition_raw, dict) else {}
    expression: dict[str, Any] = expression_raw if isinstance(expression_raw, dict) else {}

    return {
        "professional": {
            "technical_correctness": _score_reason(professional.get("technical_correctness")),
            "knowledge_match": _score_reason(professional.get("knowledge_match")),
            "job_match": _score_reason(professional.get("job_match")),
            "engineering_practice": _score_reason(professional.get("engineering_practice")),
        },
        "cognition": {
            "logic_structure": _score_reason(cognition.get("logic_structure")),
            "problem_solving": _score_reason(cognition.get("problem_solving")),
            "system_thinking": _score_reason(cognition.get("system_thinking")),
        },
        "expression": {
            "clarity": _score_reason(expression.get("clarity")),
            "confidence_stability": _score_reason(expression.get("confidence_stability")),
            "professional_maturity": _score_reason(expression.get("professional_maturity")),
        },
    }


def _compute_dimension_scores(details: dict[str, Any]) -> tuple[dict[str, float], float]:
    professional = sum(
        _safe_float(details["professional"][k]["score"]) * w for k, w in PROFESSIONAL_SUBWEIGHTS.items()
    )
    cognition = sum(_safe_float(details["cognition"][k]["score"]) * w for k, w in COGNITION_SUBWEIGHTS.items())
    expression = sum(_safe_float(details["expression"][k]["score"]) * w for k, w in EXPRESSION_SUBWEIGHTS.items())

    scores = {
        "professional": round(_clamp_score_0_5(professional), 1),
        "cognition": round(_clamp_score_0_5(cognition), 1),
        "expression": round(_clamp_score_0_5(expression), 1),
    }
    final_5 = (
        _clamp_score_0_5(professional) * DIMENSION_WEIGHTS["professional"]
        + _clamp_score_0_5(cognition) * DIMENSION_WEIGHTS["cognition"]
        + _clamp_score_0_5(expression) * DIMENSION_WEIGHTS["expression"]
    )
    return scores, round(final_5 * 20, 1)


def _sanitize_stage(stage: Any, fallback: str) -> str:
    stage_name = str(stage or "").strip()
    if stage_name in STAGE_SET:
        return stage_name
    return fallback


def _sanitize_style(style: Any, fallback: str) -> str:
    value = str(style or "").strip().lower()
    if value in STYLE_SET:
        return value
    return fallback


def _sanitize_difficulty(difficulty: Any, fallback: str) -> str:
    value = str(difficulty or "").strip().lower()
    if value in DIFFICULTY_SET:
        return value
    return fallback


def _sanitize_mode(mode: Any, fallback: str) -> str:
    value = str(mode or "").strip().lower()
    if value in MODE_SET:
        return value
    return fallback


@dataclass
class SessionProfile:
    interviewer_style: str = "standard"
    difficulty: str = "medium"
    company_context: str = "通用科技公司文化"
    mode: str = "video"
    job_position: str = ""
    jd_summary: str = ""
    resume_content: str = ""


@dataclass
class ModelConfig:
    realtime_model: str = os.getenv("REALTIME_MODEL", "qwen3-omni-flash-realtime")
    reasoning_model: str = os.getenv("REASONING_MODEL", "qwen3-max-preview")
    realtime_voice: str = os.getenv("REALTIME_VOICE", "Cherry")
    interviewer_style: str = os.getenv("INTERVIEWER_STYLE", "standard")
    difficulty: str = os.getenv("INTERVIEW_DIFFICULTY", "medium")
    company_context: str = os.getenv("COMPANY_CONTEXT", "通用科技公司文化")
    interview_mode: str = os.getenv("INTERVIEW_MODE", "video")

    dashscope_api_key: str = os.getenv("DASHSCOPE_API_KEY", "").strip()
    dashscope_base_url: str = os.getenv(
        "DASHSCOPE_BASE_URL",
        "https://dashscope.aliyuncs.com/compatible-mode/v1",
    )
    realtime_api_key: str = os.getenv("REALTIME_API_KEY", os.getenv("DASHSCOPE_API_KEY", "")).strip()
    realtime_base_url: str = os.getenv(
        "REALTIME_BASE_URL",
        os.getenv("DASHSCOPE_BASE_URL", "wss://dashscope.aliyuncs.com/api-ws/v1/realtime"),
    ).strip()

    reasoning_temperature: float = float(os.getenv("REASONING_TEMPERATURE", "0.2"))
    reasoning_timeout_sec: float = float(os.getenv("REASONING_TIMEOUT_SECONDS", "20"))
    reasoning_max_retries: int = int(os.getenv("REASONING_MAX_RETRIES", "2"))
    reasoning_retry_backoff_sec: float = float(os.getenv("REASONING_RETRY_BACKOFF_SECONDS", "0.6"))

    inference_worker_count: int = int(os.getenv("INFERENCE_WORKER_COUNT", "1"))
    command_queue_size: int = int(os.getenv("SESSION_COMMAND_QUEUE_SIZE", "256"))
    history_tail_size: int = int(os.getenv("SESSION_HISTORY_TAIL_SIZE", "10"))
    stale_decision_ttl_sec: int = int(os.getenv("STALE_DECISION_TTL_SECONDS", "30"))
    min_reply_interval_sec: float = float(os.getenv("MIN_REPLY_INTERVAL_SECONDS", "0.8"))
    user_interrupt_cooldown_sec: float = float(os.getenv("USER_INTERRUPT_COOLDOWN_SECONDS", "0.8"))
    report_api_url: str = os.getenv("REPORT_API_URL", "http://127.0.0.1:8000/api/v1/interview/report").strip()
    report_callback_url_template: str = os.getenv(
        "REPORT_CALLBACK_URL_TEMPLATE",
        "https://nas.feixingxr.com/api/v1/interviews/{interviewId}/report-callback",
    ).strip()
    report_request_timeout_sec: float = float(os.getenv("REPORT_REQUEST_TIMEOUT_SECONDS", "20"))


@dataclass
class PromptDoc:
    system_role: str
    rules: str
    format_requirements: str
    input_context: str


class PromptRegistry:
    def __init__(self) -> None:
        self._env = Environment(undefined=StrictUndefined)
        base = Path(__file__).resolve().parent / "prompts"
        self.realtime_policy = self._load(base / "realtime" / "realtime_policy_v1.yaml")
        self.reasoning_stage = self._load(base / "reasoning" / "stage_decision_v1.yaml")
        self.reasoning_scoring = self._load(base / "reasoning" / "scoring_v1.yaml")
        self.reasoning_guardrail = self._load(base / "reasoning" / "guardrail_v1.yaml")
        self.reasoning_style_policy = self._load(base / "reasoning" / "style_policy_v1.yaml")

    def _load(self, path: Path) -> PromptDoc:
        with path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return PromptDoc(
            system_role=str(data["system_role"]),
            rules=str(data["rules"]),
            format_requirements=str(data["format_requirements"]),
            input_context=str(data["input_context"]),
        )

    def render(self, doc: PromptDoc, **kwargs: Any) -> tuple[str, str]:
        system_role = self._env.from_string(doc.system_role).render(**kwargs)
        rules = self._env.from_string(doc.rules).render(**kwargs)
        fmt = self._env.from_string(doc.format_requirements).render(**kwargs)
        user_ctx = self._env.from_string(doc.input_context).render(**kwargs)
        return f"{system_role}\n\n{rules}\n\n{fmt}", user_ctx


@dataclass
class StageDecision:
    decision_version: int
    current_stage: str
    next_stage: str
    should_switch: bool
    confidence: float
    analysis: dict[str, Any]
    dimension_details: dict[str, Any]
    dimension_scores: dict[str, float]
    final_score: float
    realtime_instruction: dict[str, Any]


@dataclass
class RealtimeTurnEvent:
    session_id: str
    turn_id: str
    transcript: str
    assistant_text: str
    video_signals: dict[str, Any] = field(default_factory=dict)
    voice_metrics: dict[str, Any] = field(default_factory=dict)
    face_metrics: dict[str, Any] = field(default_factory=dict)
    emotion_signals: dict[str, Any] = field(default_factory=dict)
    created_at: float = field(default_factory=time.time)


@dataclass
class InferenceTask:
    session_id: str
    turn_id: str
    transcript: str
    context_snapshot: dict[str, Any]
    created_at: float = field(default_factory=time.time)


@dataclass
class InterviewSessionState:
    session_id: str
    context_version: int = 0
    decision_version: int = 0
    active_stage: str = "intro"
    latest_decision: Optional[StageDecision] = None
    history: list[dict[str, Any]] = field(default_factory=list)
    inference_queue: asyncio.Queue[InferenceTask] = field(default_factory=asyncio.Queue)
    command_queue: asyncio.Queue[dict[str, Any]] = field(default_factory=asyncio.Queue)
    user_is_speaking: bool = False
    next_decision_ticket: int = 0
    session_profile: SessionProfile = field(default_factory=SessionProfile)
    round_results: list[dict[str, Any]] = field(default_factory=list)
    report_dispatched: bool = False
    started_at: float = field(default_factory=time.time)
    lock: asyncio.Lock = field(default_factory=asyncio.Lock)
    reply_lock: asyncio.Lock = field(default_factory=asyncio.Lock)
    last_reply_ts: float = 0.0
    last_reply_version: int = 0
    min_reply_interval_sec: float = 0.8
    last_user_interrupt_ts: float = 0.0


@dataclass
class RuntimeMetrics:
    inference_enqueued: int = 0
    inference_completed: int = 0
    inference_failed: int = 0
    user_interrupts: int = 0
    assistant_interrupts: int = 0
    stale_decisions_ignored: int = 0
    stage_switches: int = 0
    command_retry_count: int = 0
    command_dropped: int = 0


@dataclass
class ArbitrationDecision:
    should_interrupt: bool
    reason: str = ""
    message: str = ""


class ConversationArbitrationEngine:
    @staticmethod
    def evaluate(
        transcript: str,
        profile: SessionProfile,
        realtime_instruction: dict[str, Any],
    ) -> ArbitrationDecision:
        text = transcript.lower()
        off_topic = len(text) > 300 or "不知道" in transcript or "跑题" in transcript
        if off_topic:
            return ArbitrationDecision(
                should_interrupt=True,
                reason="off_topic_redirect",
                message="我先打断一下，我们回到刚刚的问题核心。",
            )

        return ArbitrationDecision(should_interrupt=False)


class RealtimeProviderFactory:
    @staticmethod
    def build(config_obj: ModelConfig) -> Any:
        return build_dashscope_realtime_model(config_obj)


class StableSessionFactory:
    @staticmethod
    def build(config_obj: ModelConfig) -> AgentSession:
        return AgentSession(llm=RealtimeProviderFactory.build(config_obj))


def _resolve_report_callback_url(template: str, session_id: str) -> str:
    interview_id = quote(str(session_id or "").strip(), safe="")
    tpl = str(template or "").strip()
    if "{interviewId}" in tpl:
        return tpl.replace("{interviewId}", interview_id)
    return tpl


def _derive_multimodal_summary(
    voice_metrics: dict[str, Any],
    face_metrics: dict[str, Any],
    emotion_signals: dict[str, Any],
) -> dict[str, Any]:
    # Prefer explicit model-provided values; otherwise infer a conservative nervousness score.
    pause_ratio = _safe_float(voice_metrics.get("pause_ratio"), 0.0)
    speech_rate = _safe_float(voice_metrics.get("speech_rate"), 0.0)
    jitter = _safe_float(voice_metrics.get("jitter"), 0.0)
    gaze_aversion = _safe_float(face_metrics.get("gaze_aversion"), 0.0)
    blink_rate = _safe_float(face_metrics.get("blink_rate"), 0.0)
    emotion_label = str(emotion_signals.get("label") or "unknown").strip().lower()

    explicit_nervous = emotion_signals.get("nervousness_score")
    if explicit_nervous is not None:
        nervousness = max(0.0, min(1.0, _safe_float(explicit_nervous, 0.0)))
    else:
        rate_component = 0.0
        if speech_rate > 0:
            if speech_rate < 2.0:
                rate_component = 0.25
            elif speech_rate > 6.5:
                rate_component = 0.25
        nervousness = max(
            0.0,
            min(1.0, pause_ratio * 0.35 + jitter * 0.25 + gaze_aversion * 0.25 + blink_rate * 0.15 + rate_component),
        )

    has_voice = bool(voice_metrics)
    has_face = bool(face_metrics)
    has_emotion = bool(emotion_signals)
    source = "event_multimodal" if (has_voice or has_face or has_emotion) else "transcript_only"

    return {
        "nervousness_score": round(nervousness, 3),
        "emotion_label": emotion_label,
        "source": source,
        "signals_present": {
            "voice": has_voice,
            "face": has_face,
            "emotion": has_emotion,
        },
    }


def _parse_json_object(raw: str) -> dict[str, Any]:
    try:
        value: Any = json_repair.loads(raw)
        if isinstance(value, tuple):
            value = value[0]
        if isinstance(value, dict):
            return value
    except Exception:
        logger.warning("JSON parse failed", exc_info=True)
    return {}


def _apply_guardrail_interrupt_policy(
    parsed: dict[str, Any],
    fallback_instruction: dict[str, Any],
) -> dict[str, Any]:
    base_raw = parsed.get("realtime_instruction")
    base_instruction = dict(base_raw) if isinstance(base_raw, dict) else dict(fallback_instruction)

    recommended_action = str(parsed.get("recommended_action") or "").strip().lower()
    action_map = {
        "none": "none",
        "soft_interrupt": "soft",
        "hard_interrupt": "hard",
    }
    mapped = action_map.get(recommended_action)
    if mapped:
        base_instruction["interrupt_policy"] = mapped

    return base_instruction


class ReasoningModelAdapter:
    def __init__(self, config: ModelConfig, prompts: PromptRegistry) -> None:
        if not config.dashscope_api_key:
            raise ValueError("DASHSCOPE_API_KEY is required")
        self.config = config
        self.prompts = prompts
        self.client = AsyncOpenAI(
            api_key=config.dashscope_api_key,
            base_url=config.dashscope_base_url,
        )

    async def close(self) -> None:
        await self.client.close()

    async def decide_stage(self, task: InferenceTask, decision_version: int) -> StageDecision:
        session_style = _sanitize_style(task.context_snapshot.get("interviewer_style"), self.config.interviewer_style)
        session_difficulty = _sanitize_difficulty(task.context_snapshot.get("difficulty"), self.config.difficulty)
        session_company_context = (
            str(task.context_snapshot.get("company_context") or self.config.company_context).strip()
            or self.config.company_context
        )
        session_mode = _sanitize_mode(task.context_snapshot.get("mode"), self.config.interview_mode)
        default_details = _normalize_dimension_details({})
        default_dimension_scores, default_final_score = _compute_dimension_scores(default_details)
        fallback = StageDecision(
            decision_version=decision_version,
            current_stage=task.context_snapshot.get("active_stage", "intro"),
            next_stage=task.context_snapshot.get("active_stage", "intro"),
            should_switch=False,
            confidence=0.0,
            analysis={
                "scores": {"professional": 0.0, "cognition": 0.0, "expression": 0.0},
                "risk_flags": ["reasoning_fallback"],
                "flow_rationale": "fallback",
            },
            dimension_details=default_details,
            dimension_scores=default_dimension_scores,
            final_score=default_final_score,
            realtime_instruction={
                "style": "standard",
                "goal": "collect_more_signal",
                "interrupt_policy": "none",
                "priority": "normal",
                "pace": "adaptive",
                "probe_depth": "medium",
                "focus_hint": "",
            },
        )

        system_prompt, user_prompt = self.prompts.render(
            self.prompts.reasoning_stage,
            interviewer_style=session_style,
            difficulty=session_difficulty,
            company_context=session_company_context,
            mode=session_mode,
            context_snapshot=json.dumps(task.context_snapshot, ensure_ascii=False),
            transcript=task.transcript,
            fallback_stage=fallback.current_stage,
            scoring_contract=json.dumps(
                {
                    "dimension_weights": DIMENSION_WEIGHTS,
                    "professional_subweights": PROFESSIONAL_SUBWEIGHTS,
                    "cognition_subweights": COGNITION_SUBWEIGHTS,
                    "expression_subweights": EXPRESSION_SUBWEIGHTS,
                },
                ensure_ascii=False,
            ),
        )

        # Guardrail and scoring prompts are attached as additional constraints.
        guardrail_system, guardrail_user = self.prompts.render(
            self.prompts.reasoning_guardrail,
            interviewer_style=session_style,
            transcript=task.transcript,
        )
        scoring_system, scoring_user = self.prompts.render(
            self.prompts.reasoning_scoring,
            transcript=task.transcript,
            context_snapshot=json.dumps(task.context_snapshot, ensure_ascii=False),
        )
        style_system, style_user = self.prompts.render(
            self.prompts.reasoning_style_policy,
            interviewer_style=session_style,
            difficulty=session_difficulty,
            mode=session_mode,
            transcript=task.transcript,
            context_snapshot=json.dumps(task.context_snapshot, ensure_ascii=False),
        )

        messages: Any = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
            {"role": "system", "content": guardrail_system},
            {"role": "user", "content": guardrail_user},
            {"role": "system", "content": scoring_system},
            {"role": "user", "content": scoring_user},
            {"role": "system", "content": style_system},
            {"role": "user", "content": style_user},
        ]

        last_exc: Exception | None = None
        for attempt in range(self.config.reasoning_max_retries + 1):
            try:
                response = await self.client.chat.completions.create(
                    model=self.config.reasoning_model,
                    messages=messages,
                    temperature=self.config.reasoning_temperature,
                    timeout=self.config.reasoning_timeout_sec,
                )
                raw = response.choices[0].message.content or "{}"
                parsed = _parse_json_object(raw)

                current_stage = _sanitize_stage(parsed.get("current_stage"), fallback.current_stage)
                next_stage = _sanitize_stage(parsed.get("next_stage"), current_stage)
                parsed_details = _normalize_dimension_details(parsed.get("dimension_details"))
                parsed_dimension_scores, parsed_final_score = _compute_dimension_scores(parsed_details)

                return StageDecision(
                    decision_version=decision_version,
                    current_stage=current_stage,
                    next_stage=next_stage,
                    should_switch=bool(parsed.get("should_switch", False)),
                    confidence=max(0.0, min(1.0, _safe_float(parsed.get("confidence"), 0.0))),
                    analysis=dict(parsed.get("analysis", fallback.analysis)),
                    dimension_details=parsed_details,
                    dimension_scores=parsed_dimension_scores,
                    final_score=parsed_final_score,
                    realtime_instruction=_apply_guardrail_interrupt_policy(
                        parsed,
                        fallback.realtime_instruction,
                    ),
                )
            except Exception as exc:
                last_exc = exc
                if attempt >= self.config.reasoning_max_retries:
                    break
                await asyncio.sleep(self.config.reasoning_retry_backoff_sec * (2**attempt))

        logger.exception("Reasoning model call failed after retries: %s", last_exc)
        return fallback


class InterviewModelLayer:
    def __init__(self, config: ModelConfig, prompts: PromptRegistry):
        self.config = config
        self.prompts = prompts
        self.reasoning = ReasoningModelAdapter(config, prompts)
        self.sessions: dict[str, InterviewSessionState] = {}
        self.workers: dict[str, list[asyncio.Task[Any]]] = {}
        self.metrics = RuntimeMetrics()

    def ensure_session(self, session_id: str, session_profile: SessionProfile | None = None) -> InterviewSessionState:
        state = self.sessions.get(session_id)
        if state:
            if session_profile:
                state.session_profile = session_profile
            return state

        state = InterviewSessionState(
            session_id=session_id,
            session_profile=session_profile
            or SessionProfile(
                interviewer_style=_sanitize_style(self.config.interviewer_style, "standard"),
                difficulty=_sanitize_difficulty(self.config.difficulty, "medium"),
                company_context=str(self.config.company_context or "通用科技公司文化").strip() or "通用科技公司文化",
                mode=_sanitize_mode(self.config.interview_mode, "video"),
            ),
            min_reply_interval_sec=max(0.0, self.config.min_reply_interval_sec),
        )
        state.command_queue = asyncio.Queue(maxsize=self.config.command_queue_size)
        self.sessions[session_id] = state
        self.workers[session_id] = [
            asyncio.create_task(self._inference_worker(state, i))
            for i in range(self.config.inference_worker_count)
        ]
        logger.info("Session initialized: %s", session_id)
        return state

    async def close(self) -> None:
        for session_id, tasks in self.workers.items():
            for task in tasks:
                task.cancel()
                with contextlib.suppress(asyncio.CancelledError):
                    await task
            logger.info("Stopped workers: %s", session_id)
        self.workers.clear()
        self.sessions.clear()
        await self.reasoning.close()

    async def close_session(self, session_id: str) -> None:
        tasks = self.workers.pop(session_id, [])
        for task in tasks:
            task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await task
        self.sessions.pop(session_id, None)
        logger.info("Session cleaned up: %s", session_id)

    def _to_round_result(self, state: InterviewSessionState, decision: StageDecision) -> dict[str, Any]:
        feedback = str(decision.analysis.get("flow_rationale", "")).strip()
        risk_flags = decision.analysis.get("risk_flags", [])
        if not isinstance(risk_flags, list):
            risk_flags = []
        suggestions = [str(x) for x in risk_flags if str(x).strip()]
        if not suggestions:
            suggestions = ["继续保持结构化表达并补充关键证据。"]

        return {
            "round_id": len(state.round_results) + 1,
            "current_stage": state.active_stage,
            "dimension_scores": decision.dimension_scores,
            "dimension_details": decision.dimension_details,
            "overall_feedback": feedback,
            "final_score": decision.final_score,
            "improvement_suggestions": suggestions,
        }

    async def _dispatch_report_request(self, state: InterviewSessionState) -> None:
        if state.report_dispatched:
            return

        profile = state.session_profile
        duration_seconds = int(max(1, time.time() - state.started_at))

        callback_url = _resolve_report_callback_url(self.config.report_callback_url_template, state.session_id)

        payload = {
            "session_id": state.session_id,
            "callback_url": callback_url,
            "interview_config": {
                "mode": profile.mode,
                "interviewer_style": profile.interviewer_style,
                "difficulty": profile.difficulty,
                "company_context": profile.company_context,
                "analyze_emotion": True,
            },
            "interview_context": {
                "job_position": profile.job_position,
                "jd_summary": profile.jd_summary,
                "resume_content": profile.resume_content,
                "total_rounds": len(state.round_results),
                "interview_duration_seconds": duration_seconds,
            },
            "round_results": state.round_results,
        }

        try:
            async with httpx.AsyncClient(timeout=httpx.Timeout(self.config.report_request_timeout_sec)) as client:
                resp = await client.post(self.config.report_api_url, json=payload)
                resp.raise_for_status()
            state.report_dispatched = True
            logger.info("Report request dispatched via 1.0 API session=%s", state.session_id)
        except Exception:
            logger.exception("Failed to dispatch report request session=%s", state.session_id)

    async def get_next_command(self, session_id: str, timeout_sec: float = 0.2) -> dict[str, Any] | None:
        state = self.ensure_session(session_id)
        try:
            return await asyncio.wait_for(state.command_queue.get(), timeout=timeout_sec)
        except asyncio.TimeoutError:
            return None

    async def _emit_command(self, state: InterviewSessionState, command: dict[str, Any]) -> None:
        for attempt in range(3):
            try:
                state.command_queue.put_nowait(command)
                if attempt > 0:
                    self.metrics.command_retry_count += attempt
                return
            except asyncio.QueueFull:
                if attempt >= 2:
                    self.metrics.command_dropped += 1
                    logger.error(
                        "Command queue full, drop command session=%s type=%s retries=%s",
                        state.session_id,
                        command.get("type"),
                        attempt,
                    )
                    return
                await asyncio.sleep(0.01 * (2**attempt))

    async def mark_user_speaking(self, session_id: str, speaking: bool) -> None:
        state = self.ensure_session(session_id)
        async with state.lock:
            if speaking and not state.user_is_speaking:
                now = time.time()
                if (now - state.last_user_interrupt_ts) >= max(0.0, self.config.user_interrupt_cooldown_sec):
                    state.last_user_interrupt_ts = now
                    self.metrics.user_interrupts += 1
                    await self._emit_command(
                        state,
                        {
                            "type": CommandType.INTERRUPT_ASSISTANT,
                            "reason": "user_barge_in",
                            "ts": now,
                        },
                    )
            state.user_is_speaking = speaking

    async def on_realtime_turn(self, event: RealtimeTurnEvent) -> None:
        state = self.ensure_session(event.session_id)
        async with state.lock:
            state.context_version += 1
            multimodal_summary = _derive_multimodal_summary(
                event.voice_metrics,
                event.face_metrics,
                event.emotion_signals,
            )
            state.history.append(
                {
                    "turn_id": event.turn_id,
                    "transcript": event.transcript,
                    "assistant_text": event.assistant_text,
                    "video_signals": event.video_signals,
                    "voice_metrics": event.voice_metrics,
                    "face_metrics": event.face_metrics,
                    "emotion_signals": event.emotion_signals,
                    "multimodal_summary": multimodal_summary,
                    "active_stage": state.active_stage,
                    "interviewer_style": state.session_profile.interviewer_style,
                    "difficulty": state.session_profile.difficulty,
                    "company_context": state.session_profile.company_context,
                    "mode": state.session_profile.mode,
                    "context_version": state.context_version,
                    "created_at": event.created_at,
                }
            )

            state.next_decision_ticket += 1
            decision_ticket = state.next_decision_ticket
            task = InferenceTask(
                session_id=event.session_id,
                turn_id=event.turn_id,
                transcript=event.transcript,
                context_snapshot={
                    "active_stage": state.active_stage,
                    "interviewer_style": state.session_profile.interviewer_style,
                    "difficulty": state.session_profile.difficulty,
                    "company_context": state.session_profile.company_context,
                    "mode": state.session_profile.mode,
                    "multimodal_summary": multimodal_summary,
                    "latest_decision": (
                        state.latest_decision.realtime_instruction if state.latest_decision else {}
                    ),
                    "history_tail": state.history[-self.config.history_tail_size :],
                    "context_version": state.context_version,
                    "decision_ticket": decision_ticket,
                },
            )
            await state.inference_queue.put(task)
            self.metrics.inference_enqueued += 1

    def get_realtime_instruction(self, session_id: str) -> dict[str, Any]:
        state = self.ensure_session(session_id)
        if state.latest_decision:
            return state.latest_decision.realtime_instruction
        return {
            "style": state.session_profile.interviewer_style,
            "goal": "collect_more_signal",
            "interrupt_policy": "none",
            "priority": "normal",
        }

    def get_session_profile(self, session_id: str) -> SessionProfile:
        state = self.ensure_session(session_id)
        return state.session_profile

    async def _inference_worker(self, state: InterviewSessionState, worker_index: int) -> None:
        while True:
            item = await state.inference_queue.get()
            try:
                decision = await self.reasoning.decide_stage(
                    item,
                    decision_version=int(item.context_snapshot.get("decision_ticket", 0)) or 1,
                )
                async with state.lock:
                    if (time.time() - item.created_at) > self.config.stale_decision_ttl_sec:
                        self.metrics.stale_decisions_ignored += 1
                        continue
                    if decision.decision_version >= state.decision_version:
                        state.decision_version = decision.decision_version
                        state.latest_decision = decision
                        if decision.should_switch and decision.next_stage:
                            previous_stage = state.active_stage
                            state.active_stage = decision.next_stage
                            if previous_stage != state.active_stage:
                                self.metrics.stage_switches += 1
                        await self._emit_command(
                            state,
                            {
                                "type": CommandType.STRATEGY_UPDATE,
                                "decision_version": decision.decision_version,
                                "active_stage": state.active_stage,
                                "instruction": decision.realtime_instruction,
                                "analysis": decision.analysis,
                                "dimension_scores": decision.dimension_scores,
                                "final_score": decision.final_score,
                                "ts": time.time(),
                            },
                        )

                        arbitration = ConversationArbitrationEngine.evaluate(
                            item.transcript,
                            state.session_profile,
                            decision.realtime_instruction,
                        )
                        if arbitration.should_interrupt:
                            self.metrics.assistant_interrupts += 1
                            await self._emit_command(
                                state,
                                {
                                    "type": CommandType.ASSISTANT_SOFT_INTERRUPT,
                                    "reason": arbitration.reason,
                                    "message": arbitration.message,
                                    "decision_version": decision.decision_version,
                                    "ts": time.time(),
                                },
                            )

                        state.round_results.append(self._to_round_result(state, decision))

                        pace = str(decision.realtime_instruction.get("pace", "adaptive")).strip().lower()
                        probe_depth = str(decision.realtime_instruction.get("probe_depth", "medium")).strip().lower()
                        focus_hint = str(decision.realtime_instruction.get("focus_hint", "")).strip()
                        if pace in {"slow", "fast", "adaptive"} or probe_depth in {"low", "medium", "high"} or focus_hint:
                            pace_message = f"节奏={pace or 'adaptive'}，追问深度={probe_depth or 'medium'}。"
                            if focus_hint:
                                pace_message += f" 重点聚焦：{focus_hint}"
                            await self._emit_command(
                                state,
                                {
                                    "type": CommandType.PACE_CONTROL,
                                    "message": pace_message,
                                    "decision_version": decision.decision_version,
                                    "ts": time.time(),
                                },
                            )
                        if decision.realtime_instruction.get("interrupt_policy") == "hard" and state.user_is_speaking:
                            self.metrics.assistant_interrupts += 1
                            await self._emit_command(
                                state,
                                {
                                    "type": CommandType.ASSISTANT_SOFT_INTERRUPT,
                                    "reason": "reasoning_policy_hard",
                                    "message": "我先帮你聚焦到最关键的信息点。",
                                    "ts": time.time(),
                                },
                            )

                        if state.active_stage == "end" and not state.report_dispatched and state.round_results:
                            asyncio.create_task(self._dispatch_report_request(state))

                self.metrics.inference_completed += 1
                logger.info(
                    "Decision applied session=%s worker=%s version=%s stage=%s->%s switch=%s",
                    state.session_id,
                    worker_index,
                    decision.decision_version,
                    decision.current_stage,
                    decision.next_stage,
                    decision.should_switch,
                )
            except Exception:
                self.metrics.inference_failed += 1
                logger.exception("Inference worker failed session=%s", state.session_id)
            finally:
                state.inference_queue.task_done()


class RealtimeAssistant(Agent):
    def __init__(self, model_layer: InterviewModelLayer, prompts: PromptRegistry, session_id: str) -> None:
        super().__init__(instructions="You are a realtime multimodal interviewer.")
        self.model_layer = model_layer
        self.prompts = prompts
        self.session_id = session_id
        self._last_instruction_version = 0

    async def build_dynamic_instructions(self) -> str:
        strategy = self.model_layer.get_realtime_instruction(self.session_id)
        session_profile = self.model_layer.get_session_profile(self.session_id)
        system_prompt, user_prompt = self.prompts.render(
            self.prompts.realtime_policy,
            style=strategy.get("style", "standard"),
            goal=strategy.get("goal", "collect_more_signal"),
            interrupt_policy=strategy.get("interrupt_policy", "none"),
            priority=strategy.get("priority", "normal"),
            pace=strategy.get("pace", "adaptive"),
            probe_depth=strategy.get("probe_depth", "medium"),
            focus_hint=strategy.get("focus_hint", ""),
            difficulty=session_profile.difficulty,
            company_context=session_profile.company_context,
            mode=session_profile.mode,
        )
        return f"{system_prompt}\n\n{user_prompt}"

    async def safe_generate_reply(
        self,
        session: AgentSession,
        instructions: str,
        version: int = 0,
    ) -> None:
        state = self.model_layer.ensure_session(self.session_id)
        async with state.reply_lock:
            now = time.time()
            if (now - state.last_reply_ts) < state.min_reply_interval_sec:
                return
            if version > 0 and version <= state.last_reply_version:
                return

            try:
                session.generate_reply(instructions=instructions)
                state.last_reply_ts = now
                if version > 0:
                    state.last_reply_version = version
            except Exception:
                logger.exception("safe_generate_reply failed")

    async def apply_strategy_update(self, session: AgentSession, command: dict[str, Any]) -> None:
        decision_version = int(command.get("decision_version", 0))
        if decision_version <= self._last_instruction_version:
            return
        self._last_instruction_version = decision_version
        updated_instruction = await self.build_dynamic_instructions()
        await self.safe_generate_reply(session, updated_instruction, version=decision_version)


class InferenceAssistant(Agent):
    def __init__(self) -> None:
        super().__init__(instructions="You are an asynchronous reasoning controller.")


config = ModelConfig()
prompts = PromptRegistry()
model_layer = InterviewModelLayer(config=config, prompts=prompts)
server = AgentServer()


def _extract_session_profile(ctx: agents.JobContext, config_obj: ModelConfig) -> SessionProfile:
    room = getattr(ctx, "room", None)
    room_session_id = str(getattr(room, "name", "") or "")
    default_profile = SessionProfile(
        interviewer_style=_sanitize_style(config_obj.interviewer_style, "standard"),
        difficulty=_sanitize_difficulty(config_obj.difficulty, "medium"),
        company_context=(str(config_obj.company_context or "通用科技公司文化").strip() or "通用科技公司文化"),
        mode=_sanitize_mode(config_obj.interview_mode, "video"),
        job_position="",
        jd_summary="",
        resume_content="",
    )

    raw_metadata = getattr(room, "metadata", None)
    if not raw_metadata:
        logger.warning("No dispatch/room metadata provided; interview context fields remain empty")
        return default_profile

    metadata_dict: dict[str, Any] | None = None
    if isinstance(raw_metadata, dict):
        metadata_dict = raw_metadata
    elif isinstance(raw_metadata, str):
        text = raw_metadata.strip()
        if text:
            try:
                parsed = json.loads(text)
                if isinstance(parsed, dict):
                    metadata_dict = parsed
            except Exception:
                logger.warning("room metadata is not valid JSON, fallback to defaults")

    if not metadata_dict:
        logger.warning("No valid metadata JSON provided; interview context fields remain empty")
        return default_profile

    interview_config = metadata_dict.get("interview_config")
    cfg_dict: dict[str, Any] = interview_config if isinstance(interview_config, dict) else metadata_dict

    incoming_session_id = str(metadata_dict.get("session_id") or cfg_dict.get("session_id") or "").strip()
    if incoming_session_id and room_session_id and incoming_session_id != room_session_id:
        logger.warning(
            "session_id mismatch: room.name=%s metadata.session_id=%s; room.name will be treated as runtime session_id",
            room_session_id,
            incoming_session_id,
        )

    return SessionProfile(
        interviewer_style=_sanitize_style(cfg_dict.get("interviewer_style"), default_profile.interviewer_style),
        difficulty=_sanitize_difficulty(cfg_dict.get("difficulty"), default_profile.difficulty),
        company_context=str(cfg_dict.get("company_context") or default_profile.company_context).strip()
        or default_profile.company_context,
        mode=_sanitize_mode(cfg_dict.get("mode"), default_profile.mode),
        job_position=str(metadata_dict.get("job_position") or cfg_dict.get("job_position") or "").strip(),
        jd_summary=str(metadata_dict.get("jd_summary") or cfg_dict.get("jd_summary") or "").strip(),
        resume_content=str(metadata_dict.get("resume_content") or cfg_dict.get("resume_content") or "").strip(),
    )


async def _run_command_loop(
    session: AgentSession,
    realtime_agent: RealtimeAssistant,
    session_id: str,
    stop_event: asyncio.Event,
) -> None:
    while not stop_event.is_set():
        command = await model_layer.get_next_command(session_id, timeout_sec=0.2)
        if not command:
            continue

        cmd_type = command.get("type")
        if cmd_type == CommandType.INTERRUPT_ASSISTANT:
            try:
                interrupt_result = session.interrupt(force=True)
                if inspect.isawaitable(interrupt_result):
                    await interrupt_result
            except Exception:
                logger.warning("session.interrupt failed", exc_info=True)
        elif cmd_type == CommandType.STRATEGY_UPDATE:
            await realtime_agent.apply_strategy_update(session, command)
        elif cmd_type == CommandType.ASSISTANT_SOFT_INTERRUPT:
            msg = str(command.get("message", "我先补充一个关键点。"))
            decision_version = int(command.get("decision_version", 0))
            await realtime_agent.safe_generate_reply(session, msg, version=decision_version)
        elif cmd_type == CommandType.PACE_CONTROL:
            # Keep pace control silent to avoid creating extra speech turns.
            logger.debug(
                "pace_control applied silently session=%s decision_version=%s msg=%s",
                session_id,
                command.get("decision_version"),
                command.get("message"),
            )


def _bind_session_events(session: AgentSession, session_id: str) -> None:
    # livekit-agents 1.5.1 exact event names from AgentSession EventTypes
    @session.on("user_state_changed")
    def _on_user_state_changed(ev: Any) -> None:
        new_state = getattr(ev, "new_state", None)
        if new_state == "speaking":
            asyncio.create_task(model_layer.mark_user_speaking(session_id, True))
        elif new_state in {"listening", "away"}:
            asyncio.create_task(model_layer.mark_user_speaking(session_id, False))

    @session.on("user_input_transcribed")
    def _on_user_input_transcribed(ev: Any) -> None:
        global _MULTIMODAL_UNAVAILABLE_WARNED

        transcript = str(getattr(ev, "transcript", "") or "").strip()
        is_final = bool(getattr(ev, "is_final", False))
        if not transcript or not is_final:
            return

        voice_metrics = getattr(ev, "voice_metrics", None)
        face_metrics = getattr(ev, "face_metrics", None)
        emotion_signals = getattr(ev, "emotion_signals", None)

        if not isinstance(voice_metrics, dict):
            voice_metrics = {}
        if not isinstance(face_metrics, dict):
            face_metrics = {}
        if not isinstance(emotion_signals, dict):
            emotion_signals = {}

        if (
            not _MULTIMODAL_UNAVAILABLE_WARNED
            and not voice_metrics
            and not face_metrics
            and not emotion_signals
        ):
            _MULTIMODAL_UNAVAILABLE_WARNED = True
            logger.warning(
                "No multimodal metrics found on user_input_transcribed event; "
                "fallback to transcript-only summary under current runtime."
            )

        video_signals = {}
        if isinstance(face_metrics, dict):
            video_signals = {"face_metrics": face_metrics}

        asyncio.create_task(
            model_layer.on_realtime_turn(
                RealtimeTurnEvent(
                    session_id=session_id,
                    turn_id=str(uuid4()),
                    transcript=transcript,
                    assistant_text="",
                    video_signals=video_signals,
                    voice_metrics=voice_metrics,
                    face_metrics=face_metrics,
                    emotion_signals=emotion_signals,
                )
            )
        )

    @session.on("error")
    def _on_error(ev: Any) -> None:
        logger.error("AgentSession error session=%s ev=%s", session_id, ev)

    @session.on("close")
    def _on_close(ev: Any) -> None:
        logger.info("AgentSession close session=%s reason=%s", session_id, getattr(ev, "reason", None))
        asyncio.create_task(model_layer.close_session(session_id))


@server.rtc_session(agent_name="ai-interview-3")
async def ai_interview_session(ctx: agents.JobContext) -> None:
    session_id = getattr(getattr(ctx, "room", None), "name", None) or str(uuid4())
    session_profile = _extract_session_profile(ctx, config)
    model_layer.ensure_session(session_id, session_profile=session_profile)

    realtime_agent = RealtimeAssistant(model_layer=model_layer, prompts=prompts, session_id=session_id)
    initial_instruction = await realtime_agent.build_dynamic_instructions()

    session = StableSessionFactory.build(config)

    negotiated_video = session_profile.mode == "video"

    room_options = room_io.RoomOptions(
        text_input=False,
        audio_input=room_io.AudioInputOptions(),
        video_input=room_io.VideoInputOptions() if negotiated_video else False,
        audio_output=room_io.AudioOutputOptions(),
        text_output=True,
    )

    await session.start(
        room=ctx.room,
        agent=realtime_agent,
        room_options=room_options,
    )

    _bind_session_events(session, session_id)

    # Initial reply goes through gate to avoid immediate overlap with early strategy updates.
    await realtime_agent.safe_generate_reply(session, initial_instruction, version=1)

    stop_event = asyncio.Event()
    cmd_task = asyncio.create_task(
        _run_command_loop(
            session=session,
            realtime_agent=realtime_agent,
            session_id=session_id,
            stop_event=stop_event,
        )
    )

    try:
        wait_for_shutdown = getattr(ctx, "wait_for_shutdown", None)
        shutdown_event = getattr(ctx, "shutdown_event", None)

        if callable(wait_for_shutdown):
            result = wait_for_shutdown()
            if inspect.isawaitable(result):
                await result
        elif shutdown_event is not None and hasattr(shutdown_event, "wait"):
            await shutdown_event.wait()
        else:
            while True:
                await asyncio.sleep(1.0)
    finally:
        stop_event.set()
        cmd_task.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await cmd_task


if __name__ == "__main__":
    agents.cli.run_app(server)
