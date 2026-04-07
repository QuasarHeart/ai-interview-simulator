from __future__ import annotations

import asyncio
import logging
import re
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml
from jinja2 import Environment, StrictUndefined

from livekit.agents import Agent, AgentTask, llm
from livekit.agents.beta.workflows import TaskCompletedEvent, TaskGroup

try:
    from app.official_reporting import OfficialReportService
except ModuleNotFoundError:
    from official_reporting import OfficialReportService

logger = logging.getLogger("ml-service.official_workflow")
_OFFICIAL_PROMPT_DIR = Path(__file__).resolve().parent / "prompts" / "official"

STAGE_ORDER = ["intro", "resume_deep_dive", "tech_general", "tech_scenario", "reverse_qa", "end"]

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
        self.agent_persona = self._load(_OFFICIAL_PROMPT_DIR / "agent_persona_v1.yaml")
        self.stage_control = self._load(_OFFICIAL_PROMPT_DIR / "stage_control_v1.yaml")
        self.turn_correction = self._load(_OFFICIAL_PROMPT_DIR / "turn_correction_v1.yaml")

    def _load(self, path: Path) -> PromptDoc:
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
        return "\n\n".join(part for part in [system_role, rules, fmt, input_context] if part.strip())

    def render_agent_persona(self, context: InterviewContext) -> str:
        return self._render(
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

    def render_stage_control(self, context: InterviewContext, stage_name: str) -> str:
        stage_cfg = STAGE_CONFIG[stage_name]
        return self._render(
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
        return self._render(
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
        super().__init__(instructions=self._prompts.render_stage_control(self._context, stage_name))

    async def on_enter(self) -> None:
        opening_text = self._stage_cfg["opening"].format(
            job_position=self._context.job_position or "岗位",
            company_context=self._context.company_context,
        )
        logger.info(
            "stage_enter session=%s stage=%s turns=%s",
            self._context.session_id,
            self._stage_name,
            self._turns,
        )
        if self._stage_name == "end":
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
        answer = (new_message.text_content or "").strip()
        question = _extract_last_assistant_message(turn_ctx, opening_text)
        history_summary = _build_history_summary(turn_ctx)
        stop_requested = _candidate_wants_to_stop(answer)
        no_more_questions = self._stage_name == "reverse_qa" and _no_more_questions(answer)

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
            logger.info(
                "stage_stop_requested session=%s stage=%s turns=%s answer=%s",
                self._context.session_id,
                self._stage_name,
                self._turns,
                answer[:120],
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
        self._turn_records.append(
            StageTurnRecord(
                stage=self._stage_name,
                turn_index=self._turns,
                question=question,
                user_answer=answer,
                history_summary=history_summary,
            )
        )
        logger.info(
            "stage_turn session=%s stage=%s turns=%s answer=%s",
            self._context.session_id,
            self._stage_name,
            self._turns,
            answer[:120],
        )

        if no_more_questions:
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
        self._report_service = OfficialReportService()
        self._latest_stage_results: list[StageResult] = []
        self._task_group: TaskGroup | None = None
        self._stop_requested = False

    def _request_stop(self) -> None:
        self._stop_requested = True
        if self._task_group is not None:
            self._task_group.cancel()

    async def _on_task_completed(self, event: TaskCompletedEvent) -> None:
        result = event.result
        if isinstance(result, StageResult):
            if result.stage != "end":
                self._latest_stage_results.append(result)
            logger.info(
                "stage_completed session=%s stage=%s turns=%s reason=%s summary=%s",
                self._context.session_id,
                result.stage,
                result.turns,
                result.completed_reason,
                result.history_summary[:120],
            )
            if result.completed_reason == "candidate_ended_interview":
                logger.info(
                    "workflow_stop_requested session=%s stage=%s",
                    self._context.session_id,
                    result.stage,
                )
                self._request_stop()

    async def on_enter(self) -> None:
        logger.info(
            "workflow_start session=%s stage_order=%s",
            self._context.session_id,
            STAGE_ORDER,
        )
        task_group = TaskGroup(chat_ctx=self.chat_ctx, on_task_completed=self._on_task_completed)
        self._task_group = task_group
        for stage_name in STAGE_ORDER:
            stage_description = STAGE_CONFIG[stage_name]["description"]
            task_group.add(
                lambda stage_name=stage_name: InterviewStageTask(stage_name, self._context, self._prompts),
                id=stage_name,
                description=stage_description,
            )

        results = None
        try:
            results = await task_group
            logger.info(
                "workflow_complete session=%s task_ids=%s",
                self._context.session_id,
                list(results.task_results.keys()),
            )
        except asyncio.CancelledError:
            logger.info(
                "workflow_cancelled session=%s stop_requested=%s",
                self._context.session_id,
                self._stop_requested,
            )
        finally:
            self._task_group = None

        if results is not None:
            ordered_stage_results = [
                results.task_results[stage_name]
                for stage_name in STAGE_ORDER
                if stage_name in results.task_results and stage_name != "end"
            ]
            if ordered_stage_results:
                self._latest_stage_results = [result for result in ordered_stage_results if isinstance(result, StageResult)]

        try:
            report_result = await self._report_service.generate_and_callback(self._context, self._latest_stage_results)
            logger.info(
                "report_generated session=%s status=%s callback_url=%s",
                self._context.session_id,
                report_result.get("status"),
                report_result.get("callback_url"),
            )
        finally:
            await self.session.aclose()

    async def on_exit(self) -> None:
        await self._report_service.aclose()
