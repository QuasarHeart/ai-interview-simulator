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

import yaml
from jinja2 import Environment, StrictUndefined

from livekit.agents import Agent, AgentTask, CloseReason, llm
from livekit.agents.beta.workflows import TaskCompletedEvent, TaskGroup

try:
    from app.official_reporting import OfficialReportService
except ModuleNotFoundError:
    from official_reporting import OfficialReportService

logger = logging.getLogger("ml-service.official_workflow")
_OFFICIAL_PROMPT_DIR = Path(__file__).resolve().parent / "prompts" / "official"

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

STAGE_ORDER = ["intro", "resume_deep_dive", "tech_general", "tech_scenario", "reverse_qa", "end"]


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

STAGE_CONFIG: dict[str, dict[str, Any]] = {
    "intro": {
        "min_turns": 1,
        "max_turns": 2,
        "description": "开场与背景确认",
        "goal": "先完成简短身份确认，再引导候选人自我介绍，然后切入岗位和候选人背景。",
        "opening": "先用一句很短的话完成面试官身份确认，点出当前是 {job_position} 岗位面试，并自然带到公司文化；然后马上给候选人一个明确的问题，让他先自我介绍，重点说清最近做过什么和最有代表性的项目。不要停在话题描述上，也不要使用固定模板化台词。",
        "focus": "先让候选人自我介绍，再结合岗位、简历和最近项目快速建立面试信号，避免空泛开场。",
    },
    "resume_deep_dive": {
        "min_turns": 1,
        "max_turns": 3,
        "description": "项目深挖",
        "goal": "围绕最近项目、职责和技术取舍深挖。",
        "opening": "围绕候选人最近项目深挖，先从简历里挑一个具体项目或职责点，马上提出一个具体问题，追问职责、难点、结果或取舍，不要只说要深挖。",
        "focus": "把候选人的项目背景、规模、职责和结果问清楚。",
    },
    "tech_general": {
        "min_turns": 1,
        "max_turns": 3,
        "description": "通用技术追问",
        "goal": "围绕岗位核心技术点追问基础原理和关键知识。",
        "opening": "围绕岗位要求，先选一个具体技术点，马上提出一个基础原理、关键机制或常见取舍的具体问题，不要只概括方向。",
        "focus": "确认候选人对岗位关键技术点是否真正理解。",
    },
    "tech_scenario": {
        "min_turns": 1,
        "max_turns": 3,
        "description": "场景与权衡",
        "goal": "围绕复杂场景、边界条件和系统权衡追问。",
        "opening": "给出一个更复杂的场景，并马上提出一个具体问题，追问边界条件、异常处理、性能瓶颈或系统取舍，不要只说要讨论场景。",
        "focus": "看候选人是否能在真实约束下做出判断。",
    },
    "reverse_qa": {
        "min_turns": 1,
        "max_turns": 2,
        "description": "候选人反问",
        "goal": "留出候选人反问并进行简洁回答。",
        "opening": "现在留给你反问时间，如果没有问题也可以直接说没有了。",
        "focus": "回答候选人的问题并准备收尾。",
    },
    "end": {
        "min_turns": 0,
        "max_turns": 0,
        "description": "结束语",
        "goal": "自然结束本轮面试。",
        "opening": "感谢你的时间，今天的面试先到这里。",
        "focus": "礼貌收尾，不再展开新问题。",
    },
}


def _get_next_stage(stage_name: str) -> str:
    try:
        current_index = STAGE_ORDER.index(stage_name)
    except ValueError:
        return "end"
    if current_index + 1 < len(STAGE_ORDER):
        return STAGE_ORDER[current_index + 1]
    return "end"


def _no_more_questions(text: str) -> bool:
    normalized = _compact_text(text)
    if not normalized:
        return False
    markers = {
        "没问题了",
        "没有问题了",
        "没有了",
        "暂时没有了",
        "先没有了",
        "就这些",
        "没啥了",
        "不用了",
        "noquestions",
        "nomorequestions",
        "nothing",
        "none",
    }
    return any(marker in normalized for marker in markers)


def _candidate_wants_to_stop(text: str) -> bool:
    normalized = _compact_text(text)
    if not normalized:
        return False

    explicit_patterns = (
        r"(?:我|我们)?(?:不想|不要|暂时不|没必要|不打算|不准备)(?:再|继续)?(?:面试|聊|继续聊|继续问|问了)",
        r"(?:别(?:再)?)(?:面试|聊|继续聊|继续问|问了)(?:了|吧|啊|呀|嘛)",
        r"(?:结束|停止|终止|退出|中止|打住|算了)(?:面试|这次面试|本次面试|今天的面试|这轮面试|这次聊)?",
        r"(?:先|今天|这次|暂时)?(?:到这|到此为止|就这样|先这样|先到这里|就先这样|先结束吧|就先到这里|不聊了|不面了|不面试了)",
        r"(?:下次|改天|以后)(?:再|再说|再聊|再面|继续)?",
        r"(?:我|本人)?(?:有事|有点事|有事先走|临时有事|时间不够|赶时间|要忙了)(?:了|先|一下)?(?:先)?(?:结束|离开|退出|不面了|不聊了|告辞)?",
    )
    strong_stop_markers = (
        "不想面试",
        "不面试了",
        "不想继续面试",
        "不想继续了",
        "结束面试",
        "停止面试",
        "先结束吧",
        "到此为止",
        "不用继续了",
        "stopinterview",
        "endinterview",
        "quitinterview",
        "donotwanttointerview",
        "dontwanttointerview",
        "dontwanttocontinue",
        "iwanttostop",
        "iwanttoquit",
    )

    if any(marker in normalized for marker in strong_stop_markers):
        return True

    return any(re.search(pattern, normalized) for pattern in explicit_patterns)


def _compact_text(text: str) -> str:
    normalized = (text or "").strip().lower()
    if not normalized:
        return ""
    normalized = re.sub(r"[\s\u3000]+", "", normalized)
    normalized = re.sub(r"[，。！？；：、,.!?;:\"'“”‘’（）()\[\]{}<>…·—\-_/\\|]+", "", normalized)
    return normalized


@dataclass(slots=True)
class PromptDoc:
    system_role: str
    rules: str
    format_requirements: str
    input_context: str


class OfficialPromptRegistry:
    def __init__(self) -> None:
        self._env = Environment(undefined=StrictUndefined)
        _trace_log("prompt_registry_init", prompt_root=str(_OFFICIAL_PROMPT_DIR))
        self.agent_persona = self._load(_OFFICIAL_PROMPT_DIR / "agent_persona_v1.yaml")
        self.stage_control = self._load(_OFFICIAL_PROMPT_DIR / "stage_control_v1.yaml")
        self.turn_correction = self._load(_OFFICIAL_PROMPT_DIR / "turn_correction_v1.yaml")

    def _load(self, path: Path) -> PromptDoc:
        _trace_log("prompt_load", path=str(path))
        with path.open("r", encoding="utf-8") as handle:
            data = yaml.safe_load(handle)
        return PromptDoc(
            system_role=str(data["system_role"]),
            rules=str(data["rules"]),
            format_requirements=str(data["format_requirements"]),
            input_context=str(data["input_context"]),
        )

    def _render(self, doc: PromptDoc, **kwargs: Any) -> str:
        system_role = self._env.from_string(doc.system_role).render(**kwargs)
        rules = self._env.from_string(doc.rules).render(**kwargs)
        fmt = self._env.from_string(doc.format_requirements).render(**kwargs)
        input_context = self._env.from_string(doc.input_context).render(**kwargs)
        _trace_log(
            "prompt_render",
            kwargs=kwargs,
            system_role=system_role,
            rules=rules,
            format_requirements=fmt,
            input_context=input_context,
        )
        return "\n\n".join(part for part in [system_role, rules, fmt, input_context] if part.strip())

    def render_agent_persona(self, context: InterviewContext) -> str:
        rendered = self._render(
            self.agent_persona,
            session_id=context.session_id,
            metadata_source=context.metadata_source,
            job_position=context.job_position,
            jd_summary=context.jd_summary,
            resume_content=context.resume_content,
            interviewer_style=context.interviewer_style,
            difficulty=context.difficulty,
            company_context=context.company_context,
            mode=context.mode,
        )
        _trace_log("prompt_render_agent_persona", session_id=context.session_id, prompt=rendered)
        return rendered

    def render_stage_control(self, context: InterviewContext, stage_name: str) -> str:
        stage_cfg = STAGE_CONFIG[stage_name]
        rendered = self._render(
            self.stage_control,
            session_id=context.session_id,
            metadata_source=context.metadata_source,
            job_position=context.job_position,
            jd_summary=context.jd_summary,
            resume_content=context.resume_content,
            interviewer_style=context.interviewer_style,
            difficulty=context.difficulty,
            company_context=context.company_context,
            mode=context.mode,
            current_stage=stage_name,
            stage_goal=stage_cfg["goal"],
            stage_focus=stage_cfg["focus"],
            min_turns=stage_cfg["min_turns"],
            max_turns=stage_cfg["max_turns"],
            turn_index=1,
        )
        _trace_log("prompt_render_stage_control", session_id=context.session_id, stage_name=stage_name, prompt=rendered)
        return rendered

    def render_turn_correction(
        self,
        context: InterviewContext,
        *,
        stage_name: str,
        turn_index: int,
        question: str,
        user_answer: str,
        history_summary: str,
        no_more_questions: bool,
    ) -> str:
        next_stage = _get_next_stage(stage_name)
        stage_transition = "end" if stage_name == "end" else ("end" if stage_name == "reverse_qa" and no_more_questions else "continue")
        rendered = self._render(
            self.turn_correction,
            session_id=context.session_id,
            metadata_source=context.metadata_source,
            job_position=context.job_position,
            jd_summary=context.jd_summary,
            resume_content=context.resume_content,
            interviewer_style=context.interviewer_style,
            difficulty=context.difficulty,
            company_context=context.company_context,
            mode=context.mode,
            current_stage=stage_name,
            next_stage=next_stage,
            stage_transition=stage_transition,
            turn_index=turn_index,
            question=question,
            user_answer=user_answer,
            history_summary=history_summary,
            no_more_questions=str(no_more_questions).lower(),
        )
        _trace_log(
            "prompt_render_turn_correction",
            session_id=context.session_id,
            stage_name=stage_name,
            turn_index=turn_index,
            question=question,
            user_answer=user_answer,
            history_summary=history_summary,
            no_more_questions=no_more_questions,
            prompt=rendered,
        )
        return rendered


@dataclass
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


@dataclass
class StageTurnRecord:
    stage: str
    turn_index: int
    question: str
    user_answer: str
    history_summary: str


@dataclass
class StageResult:
    stage: str
    turns: int
    question: str
    user_answer: str
    history_summary: str
    turn_records: list[StageTurnRecord]
    completed_reason: str


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


def _build_history_summary(turn_ctx: llm.ChatContext) -> str:
    items = list(getattr(turn_ctx, "items", []) or [])
    if not items:
        return ""
    lines: list[str] = []
    for item in items[-8:]:
        role = str(getattr(item, "role", "unknown")).strip() or "unknown"
        text = _message_text(item)
        if text:
            lines.append(f"{role}: {text}")
    return "\n".join(lines)


def _is_expected_workflow_cancellation(exc: BaseException, stop_requested: bool) -> bool:
    if stop_requested:
        return True
    if not isinstance(exc, llm.ToolError):
        return False
    return "cancel" in str(exc).lower()


class InterviewStageTask(AgentTask[StageResult]):
    def __init__(
        self,
        stage_name: str,
        interview_context: InterviewContext,
        prompts: OfficialPromptRegistry,
    ) -> None:
        self._stage_name = stage_name
        self._context = interview_context
        self._prompts = prompts
        self._turns = 0
        self._turn_records: list[StageTurnRecord] = []
        self._stage_cfg = STAGE_CONFIG[stage_name]
        _trace_log(
            "stage_task_init",
            session_id=self._context.session_id,
            stage_name=self._stage_name,
            stage_cfg=self._stage_cfg,
        )
        super().__init__(instructions=self._prompts.render_stage_control(self._context, stage_name))

    async def on_enter(self) -> None:
        opening_text = self._stage_cfg["opening"].format(
            job_position=self._context.job_position or "岗位",
            company_context=self._context.company_context,
        )
        _trace_log(
            "stage_enter",
            session_id=self._context.session_id,
            stage_name=self._stage_name,
            turns=self._turns,
            opening_text=opening_text,
            stage_focus=self._stage_cfg["focus"],
        )
        if self._stage_name == "end":
            _trace_log(
                "stage_complete_requested",
                session_id=self._context.session_id,
                stage_name=self._stage_name,
                turns=self._turns,
                reason="closing_stage",
                next_stage="end",
            )
            self.session.generate_reply(instructions=opening_text)
            self.complete(
                StageResult(
                    stage=self._stage_name,
                    turns=self._turns,
                    question=opening_text,
                    user_answer="",
                    history_summary=opening_text,
                    turn_records=[],
                    completed_reason="closing_stage",
                )
            )
            return

        _trace_log(
            "stage_enter_reply_requested",
            session_id=self._context.session_id,
            stage_name=self._stage_name,
            instructions=(
                f"{opening_text} "
                f"Follow the current stage strictly: {self._stage_cfg['focus']}"
            ),
        )
        self.session.generate_reply(
            instructions=(
                f"{opening_text} "
                f"Follow the current stage strictly: {self._stage_cfg['focus']}"
            )
        )

    async def on_user_turn_completed(self, turn_ctx: llm.ChatContext, new_message: llm.ChatMessage) -> None:
        opening_text = self._stage_cfg["opening"].format(
            job_position=self._context.job_position or "岗位",
            company_context=self._context.company_context,
        )
        self._turns += 1
        raw_answer = new_message.text_content or ""
        answer = raw_answer.strip()
        question = _extract_last_assistant_message(turn_ctx, opening_text)
        history_summary = _build_history_summary(turn_ctx)
        _trace_log(
            "stage_user_turn_received",
            session_id=self._context.session_id,
            stage_name=self._stage_name,
            turns=self._turns,
            raw_answer=raw_answer,
            answer=answer,
            question=question,
            history_summary=history_summary,
            chat_items=list(getattr(turn_ctx, "items", []) or []),
        )
        stop_requested = _candidate_wants_to_stop(answer)
        no_more_questions = self._stage_name == "reverse_qa" and _no_more_questions(answer)
        next_stage = _get_next_stage(self._stage_name)
        _trace_log(
            "stage_turn_decision",
            session_id=self._context.session_id,
            stage_name=self._stage_name,
            turns=self._turns,
            stop_requested=stop_requested,
            no_more_questions=no_more_questions,
            next_stage=next_stage,
        )

        if stop_requested:
            self._turn_records.append(
                StageTurnRecord(
                    stage=self._stage_name,
                    turn_index=self._turns,
                    question=question,
                    user_answer=answer,
                    history_summary=history_summary,
                )
            )
            _trace_log(
                "stage_stop_requested",
                session_id=self._context.session_id,
                stage_name=self._stage_name,
                turns=self._turns,
                answer=answer,
            )
            _trace_log(
                "stage_complete_requested",
                session_id=self._context.session_id,
                stage_name=self._stage_name,
                turns=self._turns,
                reason="candidate_ended_interview",
                next_stage=next_stage,
            )
            self.complete(
                StageResult(
                    stage=self._stage_name,
                    turns=self._turns,
                    question=question,
                    user_answer=answer,
                    history_summary=history_summary,
                    turn_records=list(self._turn_records),
                    completed_reason="candidate_ended_interview",
                )
            )
            return

        correction_note = self._prompts.render_turn_correction(
            self._context,
            stage_name=self._stage_name,
            turn_index=self._turns,
            question=question,
            user_answer=answer,
            history_summary=history_summary,
            no_more_questions=no_more_questions,
        )
        if correction_note.strip():
            turn_ctx.add_message(role="system", content=correction_note)
        _trace_log(
            "stage_turn_correction_applied",
            session_id=self._context.session_id,
            stage_name=self._stage_name,
            turns=self._turns,
            correction_note=correction_note,
        )
        self._turn_records.append(
            StageTurnRecord(
                stage=self._stage_name,
                turn_index=self._turns,
                question=question,
                user_answer=answer,
                history_summary=history_summary,
            )
        )
        _trace_log(
            "stage_turn_recorded",
            session_id=self._context.session_id,
            stage_name=self._stage_name,
            turns=self._turns,
            turn_record=self._turn_records[-1],
            turn_records=list(self._turn_records),
        )

        if no_more_questions:
            _trace_log(
                "stage_complete_requested",
                session_id=self._context.session_id,
                stage_name=self._stage_name,
                turns=self._turns,
                reason="candidate_has_no_questions",
                next_stage=next_stage,
            )
            self.complete(
                StageResult(
                    stage=self._stage_name,
                    turns=self._turns,
                    question=question,
                    user_answer=answer,
                    history_summary=history_summary,
                    turn_records=list(self._turn_records),
                    completed_reason="candidate_has_no_questions",
                )
            )
            return

        if self._turns >= self._stage_cfg["max_turns"]:
            _trace_log(
                "stage_complete_requested",
                session_id=self._context.session_id,
                stage_name=self._stage_name,
                turns=self._turns,
                reason="turn_limit_reached",
                next_stage=next_stage,
            )
            self.complete(
                StageResult(
                    stage=self._stage_name,
                    turns=self._turns,
                    question=question,
                    user_answer=answer,
                    history_summary=history_summary,
                    turn_records=list(self._turn_records),
                    completed_reason="turn_limit_reached",
                )
            )


class InterviewWorkflowAgent(Agent):
    def __init__(self, interview_context: InterviewContext, prompts: OfficialPromptRegistry) -> None:
        super().__init__(instructions=prompts.render_agent_persona(interview_context))
        self._context = interview_context
        self._prompts = prompts
        self._latest_stage_results: list[StageResult] = []
        self._task_group: TaskGroup | None = None
        self._report_task: asyncio.Task[None] | None = None
        self._stop_requested = False
        _trace_log("workflow_agent_init", context=interview_context)

    def _request_stop(self) -> None:
        self._stop_requested = True
        _trace_log("workflow_stop_requested", session_id=self._context.session_id, task_group_present=self._task_group is not None)
        if self._task_group is not None:
            self._task_group.cancel()

    def _clear_report_task_reference(self, task: asyncio.Task[None]) -> None:
        if self._report_task is task:
            self._report_task = None
            _trace_log("report_task_reference_cleared", session_id=self._context.session_id)

    async def _run_report_job(self, stage_results: list[StageResult]) -> None:
        report_service = OfficialReportService()
        try:
            _trace_log("report_job_started", session_id=self._context.session_id, stage_results=stage_results)
            logger.info(
                "report_job_started session=%s stage_results=%s",
                self._context.session_id,
                len(stage_results),
            )
            report_result = await report_service.generate_and_callback(self._context, stage_results)
            _trace_log("report_job_completed", session_id=self._context.session_id, report_result=report_result)
            logger.info(
                "report_job_completed session=%s status=%s callback_url=%s",
                self._context.session_id,
                report_result.get("status"),
                report_result.get("callback_url"),
            )
        except asyncio.CancelledError:
            _trace_log("report_job_cancelled", session_id=self._context.session_id)
            logger.warning("report_job_cancelled session=%s", self._context.session_id)
            return
        except Exception:
            _trace_log("report_job_failed", session_id=self._context.session_id)
            logger.exception("report_job_failed session=%s", self._context.session_id)
        finally:
            _trace_log("report_job_service_close", session_id=self._context.session_id)
            await report_service.aclose()

    def _start_report_job(self, stage_results: list[StageResult]) -> None:
        if self._report_task is not None and not self._report_task.done():
            _trace_log("report_job_already_running", session_id=self._context.session_id, report_task=self._report_task)
            logger.warning("report_job_already_running session=%s", self._context.session_id)
            return

        self._report_task = asyncio.create_task(self._run_report_job(list(stage_results)))
        self._report_task.add_done_callback(self._clear_report_task_reference)
        _trace_log("report_job_started_background", session_id=self._context.session_id, report_task=self._report_task, stage_results=stage_results)

    def _request_session_close_before_report(self) -> None:
        try:
            session = self.session
        except RuntimeError:
            session = None

        close_soon = getattr(session, "_close_soon", None)
        if callable(close_soon):
            _trace_log("workflow_room_close_requested", session_id=self._context.session_id, reason=CloseReason.TASK_COMPLETED.value)
            logger.info(
                "workflow_room_close_requested session=%s reason=%s",
                self._context.session_id,
                CloseReason.TASK_COMPLETED.value,
            )
            close_soon(reason=CloseReason.TASK_COMPLETED)
            return

        aclose = getattr(session, "aclose", None)
        if callable(aclose):
            _trace_log("workflow_room_close_fallback", session_id=self._context.session_id, reason="session_missing_close_soon")
            logger.warning(
                "workflow_room_close_fallback session=%s reason=session_missing_close_soon",
                self._context.session_id,
            )
            close_result = aclose()
            if asyncio.iscoroutine(close_result):
                asyncio.create_task(close_result)

    async def _on_task_completed(self, event: TaskCompletedEvent) -> None:
        result = event.result
        _trace_log("workflow_task_completed", session_id=self._context.session_id, result=result)
        if isinstance(result, StageResult):
            if result.stage != "end":
                self._latest_stage_results.append(result)
            _trace_log(
                "workflow_stage_result_recorded",
                session_id=self._context.session_id,
                stage_result=result,
                latest_stage_results=list(self._latest_stage_results),
            )
            logger.info(
                "stage_completed session=%s stage=%s turns=%s reason=%s summary=%s",
                self._context.session_id,
                result.stage,
                result.turns,
                result.completed_reason,
                result.history_summary[:120],
            )
            logger.info(
                "stage_transition session=%s from_stage=%s to_stage=%s reason=%s",
                self._context.session_id,
                result.stage,
                _get_next_stage(result.stage),
                result.completed_reason,
            )
            if result.completed_reason == "candidate_ended_interview":
                _trace_log("workflow_candidate_requested_stop", session_id=self._context.session_id, stage=result.stage)
                logger.info(
                    "workflow_stop_requested session=%s stage=%s",
                    self._context.session_id,
                    result.stage,
                )
                self._request_stop()

    async def on_enter(self) -> None:
        _trace_log("workflow_start", session_id=self._context.session_id, stage_order=STAGE_ORDER)
        logger.info(
            "workflow_start session=%s stage_order=%s",
            self._context.session_id,
            STAGE_ORDER,
        )
        task_group = TaskGroup(chat_ctx=self.chat_ctx, on_task_completed=self._on_task_completed)
        self._task_group = task_group
        for stage_name in STAGE_ORDER:
            stage_description = STAGE_CONFIG[stage_name]["description"]
            _trace_log("workflow_stage_task_added", session_id=self._context.session_id, stage_name=stage_name, stage_description=stage_description)
            task_group.add(
                lambda stage_name=stage_name: InterviewStageTask(stage_name, self._context, self._prompts),
                id=stage_name,
                description=stage_description,
            )

        results = None
        try:
            _trace_log("workflow_task_group_await_start", session_id=self._context.session_id)
            results = await task_group
            _trace_log("workflow_task_group_await_done", session_id=self._context.session_id, results=results)
            logger.info(
                "workflow_complete session=%s task_ids=%s",
                self._context.session_id,
                list(results.task_results.keys()),
            )
        except llm.ToolError as exc:
            _trace_log("workflow_tool_error", session_id=self._context.session_id, stop_requested=self._stop_requested, error=str(exc))
            if _is_expected_workflow_cancellation(exc, self._stop_requested):
                logger.info(
                    "workflow_cancelled session=%s stop_requested=%s reason=%s",
                    self._context.session_id,
                    self._stop_requested,
                    exc,
                )
            else:
                raise
        except asyncio.CancelledError:
            _trace_log("workflow_cancelled", session_id=self._context.session_id, stop_requested=self._stop_requested)
            logger.info(
                "workflow_cancelled session=%s stop_requested=%s",
                self._context.session_id,
                self._stop_requested,
            )
        finally:
            _trace_log("workflow_task_group_cleared", session_id=self._context.session_id)
            self._task_group = None

        if results is not None:
            ordered_stage_results = [
                results.task_results[stage_name]
                for stage_name in STAGE_ORDER
                if stage_name in results.task_results and stage_name != "end"
            ]
            if ordered_stage_results:
                self._latest_stage_results = [result for result in ordered_stage_results if isinstance(result, StageResult)]
            _trace_log("workflow_latest_stage_results_ready", session_id=self._context.session_id, latest_stage_results=list(self._latest_stage_results))

        self._request_session_close_before_report()
        self._start_report_job(list(self._latest_stage_results))
        _trace_log("workflow_report_job_kicked_off", session_id=self._context.session_id, latest_stage_results=list(self._latest_stage_results))

    async def on_exit(self) -> None:
        _trace_log("workflow_on_exit", session_id=self._context.session_id, report_task=self._report_task)
        if self._report_task is not None and not self._report_task.done():
            logger.info(
                "report_job_detached session=%s task_done=%s",
                self._context.session_id,
                self._report_task.done(),
            )
