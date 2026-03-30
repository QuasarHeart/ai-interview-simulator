"""LiveKit 3.0 AI-native dual-model runtime (aligned to livekit-agents 1.5.1).

Implemented in this module:
- LiveKit-first session runtime using AgentServer + AgentSession
- Realtime model: qwen3-omni-flash-realtime
- Reasoning model: qwen-plus-2025-07-28
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
from livekit.plugins import openai


load_dotenv(".env.local")
logger = logging.getLogger("ml-service.agent")


@dataclass
class ModelConfig:
    realtime_model: str = os.getenv("REALTIME_MODEL", "qwen3-omni-flash-realtime")
    reasoning_model: str = os.getenv("REASONING_MODEL", "qwen-plus-2025-07-28")
    realtime_voice: str = os.getenv("REALTIME_VOICE", "Cherry")
    interviewer_style: str = os.getenv("INTERVIEWER_STYLE", "standard")
    enable_video_input: bool = os.getenv("VIDEO_INTERVIEW_ENABLED", "false").strip().lower() in {
        "1",
        "true",
        "yes",
        "on",
    }

    dashscope_api_key: str = os.getenv("DASHSCOPE_API_KEY", "").strip()
    dashscope_base_url: str = os.getenv(
        "DASHSCOPE_BASE_URL",
        "https://dashscope.aliyuncs.com/compatible-mode/v1",
    )

    reasoning_temperature: float = float(os.getenv("REASONING_TEMPERATURE", "0.2"))
    reasoning_timeout_sec: float = float(os.getenv("REASONING_TIMEOUT_SECONDS", "20"))
    reasoning_max_retries: int = int(os.getenv("REASONING_MAX_RETRIES", "2"))
    reasoning_retry_backoff_sec: float = float(os.getenv("REASONING_RETRY_BACKOFF_SECONDS", "0.6"))

    inference_worker_count: int = int(os.getenv("INFERENCE_WORKER_COUNT", "1"))
    command_queue_size: int = int(os.getenv("SESSION_COMMAND_QUEUE_SIZE", "256"))
    history_tail_size: int = int(os.getenv("SESSION_HISTORY_TAIL_SIZE", "10"))
    stale_decision_ttl_sec: int = int(os.getenv("STALE_DECISION_TTL_SECONDS", "30"))


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
        self.reasoning_stress = self._load(base / "reasoning" / "stress_mode_v1.yaml")

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
    realtime_instruction: dict[str, Any]


@dataclass
class RealtimeTurnEvent:
    session_id: str
    turn_id: str
    transcript: str
    assistant_text: str
    video_signals: dict[str, Any] = field(default_factory=dict)
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
    active_stage: str = "opening"
    latest_decision: Optional[StageDecision] = None
    history: list[dict[str, Any]] = field(default_factory=list)
    inference_queue: asyncio.Queue[InferenceTask] = field(default_factory=asyncio.Queue)
    command_queue: asyncio.Queue[dict[str, Any]] = field(default_factory=asyncio.Queue)
    user_is_speaking: bool = False
    lock: asyncio.Lock = field(default_factory=asyncio.Lock)


@dataclass
class RuntimeMetrics:
    inference_enqueued: int = 0
    inference_completed: int = 0
    inference_failed: int = 0
    user_interrupts: int = 0
    assistant_interrupts: int = 0
    stale_decisions_ignored: int = 0


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
        fallback = StageDecision(
            decision_version=decision_version,
            current_stage=task.context_snapshot.get("active_stage", "opening"),
            next_stage=task.context_snapshot.get("active_stage", "opening"),
            should_switch=False,
            confidence=0.0,
            analysis={
                "scores": {"professional": 0.0, "cognition": 0.0, "expression": 0.0},
                "risk_flags": ["reasoning_fallback"],
                "flow_rationale": "fallback",
            },
            realtime_instruction={
                "style": "neutral",
                "goal": "collect_more_signal",
                "interrupt_policy": "none",
                "priority": "normal",
            },
        )

        system_prompt, user_prompt = self.prompts.render(
            self.prompts.reasoning_stage,
            interviewer_style=self.config.interviewer_style,
            context_snapshot=json.dumps(task.context_snapshot, ensure_ascii=False),
            transcript=task.transcript,
            fallback_stage=fallback.current_stage,
        )

        # Guardrail and scoring prompts are attached as additional constraints.
        guardrail_system, guardrail_user = self.prompts.render(
            self.prompts.reasoning_guardrail,
            interviewer_style=self.config.interviewer_style,
            transcript=task.transcript,
        )
        scoring_system, scoring_user = self.prompts.render(
            self.prompts.reasoning_scoring,
            transcript=task.transcript,
            context_snapshot=json.dumps(task.context_snapshot, ensure_ascii=False),
        )

        if self.config.interviewer_style == "aggressive":
            stress_system, stress_user = self.prompts.render(
                self.prompts.reasoning_stress,
                transcript=task.transcript,
                context_snapshot=json.dumps(task.context_snapshot, ensure_ascii=False),
            )
        else:
            stress_system, stress_user = "", ""

        messages: Any = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
            {"role": "system", "content": guardrail_system},
            {"role": "user", "content": guardrail_user},
            {"role": "system", "content": scoring_system},
            {"role": "user", "content": scoring_user},
        ]
        if stress_system:
            messages.extend(
                [
                    {"role": "system", "content": stress_system},
                    {"role": "user", "content": stress_user},
                ]
            )

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

                current_stage = str(parsed.get("current_stage", fallback.current_stage))
                next_stage = str(parsed.get("next_stage", current_stage))

                return StageDecision(
                    decision_version=decision_version,
                    current_stage=current_stage,
                    next_stage=next_stage,
                    should_switch=bool(parsed.get("should_switch", False)),
                    confidence=float(parsed.get("confidence", 0.0)),
                    analysis=dict(parsed.get("analysis", fallback.analysis)),
                    realtime_instruction=dict(
                        parsed.get("realtime_instruction", fallback.realtime_instruction)
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

    def ensure_session(self, session_id: str) -> InterviewSessionState:
        state = self.sessions.get(session_id)
        if state:
            return state

        state = InterviewSessionState(session_id=session_id)
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

    async def get_next_command(self, session_id: str, timeout_sec: float = 0.2) -> dict[str, Any] | None:
        state = self.ensure_session(session_id)
        try:
            return await asyncio.wait_for(state.command_queue.get(), timeout=timeout_sec)
        except asyncio.TimeoutError:
            return None

    async def _emit_command(self, state: InterviewSessionState, command: dict[str, Any]) -> None:
        try:
            state.command_queue.put_nowait(command)
        except asyncio.QueueFull:
            logger.warning(
                "Command queue full, drop command session=%s type=%s",
                state.session_id,
                command.get("type"),
            )

    async def mark_user_speaking(self, session_id: str, speaking: bool) -> None:
        state = self.ensure_session(session_id)
        async with state.lock:
            if speaking and not state.user_is_speaking:
                self.metrics.user_interrupts += 1
                await self._emit_command(
                    state,
                    {"type": "interrupt_assistant", "reason": "user_barge_in", "ts": time.time()},
                )
            state.user_is_speaking = speaking

    async def on_realtime_turn(self, event: RealtimeTurnEvent) -> None:
        state = self.ensure_session(event.session_id)
        async with state.lock:
            state.context_version += 1
            state.history.append(
                {
                    "turn_id": event.turn_id,
                    "transcript": event.transcript,
                    "assistant_text": event.assistant_text,
                    "video_signals": event.video_signals,
                    "active_stage": state.active_stage,
                    "context_version": state.context_version,
                    "created_at": event.created_at,
                }
            )
            task = InferenceTask(
                session_id=event.session_id,
                turn_id=event.turn_id,
                transcript=event.transcript,
                context_snapshot={
                    "active_stage": state.active_stage,
                    "latest_decision": (
                        state.latest_decision.realtime_instruction if state.latest_decision else {}
                    ),
                    "history_tail": state.history[-self.config.history_tail_size :],
                    "context_version": state.context_version,
                },
            )
            await state.inference_queue.put(task)
            self.metrics.inference_enqueued += 1

    def get_realtime_instruction(self, session_id: str) -> dict[str, Any]:
        state = self.ensure_session(session_id)
        if state.latest_decision:
            return state.latest_decision.realtime_instruction
        return {
            "style": self.config.interviewer_style,
            "goal": "collect_more_signal",
            "interrupt_policy": "none",
            "priority": "normal",
        }

    async def _inference_worker(self, state: InterviewSessionState, worker_index: int) -> None:
        while True:
            item = await state.inference_queue.get()
            try:
                decision = await self.reasoning.decide_stage(
                    item,
                    decision_version=state.decision_version + 1,
                )
                async with state.lock:
                    if (time.time() - item.created_at) > self.config.stale_decision_ttl_sec:
                        self.metrics.stale_decisions_ignored += 1
                        continue
                    if decision.decision_version >= state.decision_version:
                        state.decision_version = decision.decision_version
                        state.latest_decision = decision
                        if decision.should_switch and decision.next_stage:
                            state.active_stage = decision.next_stage
                        await self._emit_command(
                            state,
                            {
                                "type": "strategy_update",
                                "decision_version": decision.decision_version,
                                "active_stage": state.active_stage,
                                "instruction": decision.realtime_instruction,
                                "analysis": decision.analysis,
                                "ts": time.time(),
                            },
                        )
                        if decision.realtime_instruction.get("interrupt_policy") == "hard" and state.user_is_speaking:
                            self.metrics.assistant_interrupts += 1
                            await self._emit_command(
                                state,
                                {
                                    "type": "assistant_soft_interrupt",
                                    "reason": "reasoning_policy_hard",
                                    "message": "我先帮你聚焦到最关键的信息点。",
                                    "ts": time.time(),
                                },
                            )

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
        system_prompt, user_prompt = self.prompts.render(
            self.prompts.realtime_policy,
            style=strategy.get("style", "standard"),
            goal=strategy.get("goal", "collect_more_signal"),
            interrupt_policy=strategy.get("interrupt_policy", "none"),
            priority=strategy.get("priority", "normal"),
        )
        return f"{system_prompt}\n\n{user_prompt}"

    async def apply_strategy_update(self, session: AgentSession, command: dict[str, Any]) -> None:
        decision_version = int(command.get("decision_version", 0))
        if decision_version <= self._last_instruction_version:
            return
        self._last_instruction_version = decision_version
        updated_instruction = await self.build_dynamic_instructions()
        try:
            session.generate_reply(instructions=updated_instruction)
        except Exception:
            logger.exception("Failed to apply strategy update")


class InferenceAssistant(Agent):
    def __init__(self) -> None:
        super().__init__(instructions="You are an asynchronous reasoning controller.")


config = ModelConfig()
prompts = PromptRegistry()
model_layer = InterviewModelLayer(config=config, prompts=prompts)
server = AgentServer()


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
        if cmd_type == "interrupt_assistant":
            try:
                interrupt_result = session.interrupt(force=True)
                if inspect.isawaitable(interrupt_result):
                    await interrupt_result
            except Exception:
                logger.warning("session.interrupt failed", exc_info=True)
        elif cmd_type == "strategy_update":
            await realtime_agent.apply_strategy_update(session, command)
        elif cmd_type == "assistant_soft_interrupt":
            msg = str(command.get("message", "我先补充一个关键点。"))
            try:
                session.generate_reply(instructions=msg)
            except Exception:
                logger.warning("assistant_soft_interrupt failed", exc_info=True)


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
        transcript = str(getattr(ev, "transcript", "") or "").strip()
        is_final = bool(getattr(ev, "is_final", False))
        if not transcript or not is_final:
            return
        asyncio.create_task(
            model_layer.on_realtime_turn(
                RealtimeTurnEvent(
                    session_id=session_id,
                    turn_id=str(uuid4()),
                    transcript=transcript,
                    assistant_text="",
                )
            )
        )

    @session.on("error")
    def _on_error(ev: Any) -> None:
        logger.error("AgentSession error session=%s ev=%s", session_id, ev)

    @session.on("close")
    def _on_close(ev: Any) -> None:
        logger.info("AgentSession close session=%s reason=%s", session_id, getattr(ev, "reason", None))


@server.rtc_session(agent_name="ai-interview-3")
async def ai_interview_session(ctx: agents.JobContext) -> None:
    session_id = getattr(getattr(ctx, "room", None), "name", None) or str(uuid4())
    model_layer.ensure_session(session_id)

    realtime_agent = RealtimeAssistant(model_layer=model_layer, prompts=prompts, session_id=session_id)
    initial_instruction = await realtime_agent.build_dynamic_instructions()

    session = AgentSession(
        llm=openai.realtime.RealtimeModel(
            model=config.realtime_model,
            voice=config.realtime_voice,
        )
    )

    room_options = room_io.RoomOptions(
        text_input=False,
        audio_input=room_io.AudioInputOptions(),
        video_input=room_io.VideoInputOptions() if config.enable_video_input else False,
        audio_output=room_io.AudioOutputOptions(),
        text_output=True,
    )

    await session.start(
        room=ctx.room,
        agent=realtime_agent,
        room_options=room_options,
    )

    _bind_session_events(session, session_id)

    # generate_reply is sync and returns SpeechHandle in livekit-agents 1.5.1
    session.generate_reply(instructions=initial_instruction)

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
