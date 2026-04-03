import json
import asyncio
import contextlib
import sys
from types import SimpleNamespace
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import app.agent as agent_mod
from app.realtime import dashscope_realtime as dashscope_rt


def _make_ctx(room_name: str, metadata: str | dict | None):
    room = SimpleNamespace(name=room_name, metadata=metadata)
    return SimpleNamespace(room=room)


def test_compute_dimension_scores_v1_aligned_formula():
    details = {
        "professional": {
            "technical_correctness": {"reason": "", "score": 5.0},
            "knowledge_match": {"reason": "", "score": 4.0},
            "job_match": {"reason": "", "score": 3.0},
            "engineering_practice": {"reason": "", "score": 2.0},
        },
        "cognition": {
            "logic_structure": {"reason": "", "score": 4.0},
            "problem_solving": {"reason": "", "score": 4.0},
            "system_thinking": {"reason": "", "score": 4.0},
        },
        "expression": {
            "clarity": {"reason": "", "score": 3.0},
            "confidence_stability": {"reason": "", "score": 3.0},
            "professional_maturity": {"reason": "", "score": 3.0},
        },
    }

    scores, final_score = agent_mod._compute_dimension_scores(details)

    # professional = 5*0.2 + 4*0.09 + 3*0.31 + 2*0.4 = 3.09
    assert scores["professional"] == 3.1
    assert scores["cognition"] == 4.0
    assert scores["expression"] == 3.0

    expected_final = round((3.09 * 0.5 + 4.0 * 0.3 + 3.0 * 0.2) * 20, 1)
    assert final_score == expected_final


def test_compute_dimension_scores_abnormal_values_are_sanitized_and_clamped():
    details = {
        "professional": {
            "technical_correctness": {"reason": "", "score": "nan"},
            "knowledge_match": {"reason": "", "score": None},
            "job_match": {"reason": "", "score": "bad"},
            "engineering_practice": {"reason": "", "score": -9},
        },
        "cognition": {
            "logic_structure": {"reason": "", "score": 999},
            "problem_solving": {"reason": "", "score": float("inf")},
            "system_thinking": {"reason": "", "score": 5},
        },
        "expression": {
            "clarity": {"reason": "", "score": -1},
            "confidence_stability": {"reason": "", "score": 0},
            "professional_maturity": {"reason": "", "score": 2.5},
        },
    }

    scores, final_score = agent_mod._compute_dimension_scores(details)

    # Invalid numeric values are coerced to 0 and dimension scores are clamped to [0, 5].
    assert scores == {"professional": 0.0, "cognition": 5.0, "expression": 0.5}
    assert final_score == 32.0


def test_extract_session_profile_from_dispatch_metadata():
    metadata = {
        "session_id": "s-001",
        "job_position": "Java后端工程师",
        "jd_summary": "熟悉 Spring Boot/MySQL/Redis",
        "resume_content": "3年支付系统经验",
        "interview_config": {
            "mode": "video",
            "interviewer_style": "expert",
            "difficulty": "hard",
            "company_context": "字节跳动",
        },
    }
    ctx = _make_ctx("s-001", json.dumps(metadata, ensure_ascii=False))

    profile = agent_mod._extract_session_profile(ctx, agent_mod.config)

    assert profile.interviewer_style == "expert"
    assert profile.difficulty == "hard"
    assert profile.mode == "video"
    assert profile.company_context == "字节跳动"
    assert profile.job_position == "Java后端工程师"
    assert profile.jd_summary.startswith("熟悉")


def test_extract_session_profile_without_metadata_uses_defaults():
    ctx = _make_ctx("s-002", None)
    profile = agent_mod._extract_session_profile(ctx, agent_mod.config)

    assert profile.interviewer_style in {"standard", "friendly", "aggressive", "expert"}
    assert profile.difficulty in {"easy", "medium", "hard"}
    assert profile.job_position == ""
    assert profile.jd_summary == ""
    assert profile.resume_content == ""


def test_resolve_report_callback_url_uses_session_id_as_interview_id():
    template = "https://nas.feixingxr.com/api/v1/interviews/{interviewId}/report-callback"
    out = agent_mod._resolve_report_callback_url(template, "sess-001")
    assert out.endswith("/api/v1/interviews/sess-001/report-callback")


def test_apply_guardrail_interrupt_policy_mapping():
    fallback = {"interrupt_policy": "none", "style": "standard"}

    hard = agent_mod._apply_guardrail_interrupt_policy({"recommended_action": "hard_interrupt"}, fallback)
    assert hard["interrupt_policy"] == "hard"

    soft = agent_mod._apply_guardrail_interrupt_policy({"recommended_action": "soft_interrupt"}, fallback)
    assert soft["interrupt_policy"] == "soft"

    none = agent_mod._apply_guardrail_interrupt_policy({"recommended_action": "none"}, fallback)
    assert none["interrupt_policy"] == "none"


def test_normalize_dashscope_realtime_event_maps_event_names():
    audio = dashscope_rt.normalize_dashscope_realtime_event({"type": "response.audio.delta", "delta": "abc"})
    assert audio["type"] == "response.output_audio.delta"
    assert audio["delta"] == "abc"

    text = dashscope_rt.normalize_dashscope_realtime_event({"type": "response.text.delta", "delta": "hello"})
    assert text["type"] == "response.output_text.delta"

    item = dashscope_rt.normalize_dashscope_realtime_event({"type": "conversation.item.created", "item": {"id": "x"}})
    assert item["type"] == "conversation.item.added"

    missing = dashscope_rt.normalize_dashscope_realtime_event({"delta": "oops"})
    assert missing["type"] == "unknown"
    assert missing["delta"] == "oops"

    scalar = dashscope_rt.normalize_dashscope_realtime_event(["not", "a", "dict"])
    assert scalar["type"] == "unknown"
    assert scalar["payload"] == ["not", "a", "dict"]


def test_normalize_realtime_voice_falls_back_from_unsupported_value():
    assert dashscope_rt._normalize_realtime_voice("Tina") == "Cherry"
    assert dashscope_rt._normalize_realtime_voice("  ") == "Cherry"
    assert dashscope_rt._normalize_realtime_voice("Cherry") == "Cherry"

def test_derive_multimodal_summary_transcript_only_when_no_signals():
    summary = agent_mod._derive_multimodal_summary({}, {}, {})
    assert summary["source"] == "transcript_only"
    assert summary["signals_present"] == {"voice": False, "face": False, "emotion": False}
    assert 0.0 <= summary["nervousness_score"] <= 1.0


@pytest.mark.asyncio
async def test_emit_command_queue_drop_after_retries():
    prompts = agent_mod.PromptRegistry()
    layer = agent_mod.InterviewModelLayer(agent_mod.config, prompts)

    state = layer.ensure_session("test-overflow")
    # shrink queue for deterministic overflow
    state.command_queue = __import__("asyncio").Queue(maxsize=1)
    state.command_queue.put_nowait({"type": "dummy"})

    await layer._emit_command(state, {"type": "overflow"})

    assert layer.metrics.command_dropped >= 1

    await layer.close_session("test-overflow")
    await layer.reasoning.close()


def test_extract_session_profile_warns_on_session_id_mismatch(caplog):
    metadata = {
        "session_id": "meta-001",
        "job_position": "Java后端工程师",
        "interview_config": {
            "mode": "audio",
            "interviewer_style": "standard",
            "difficulty": "medium",
            "company_context": "字节跳动",
        },
    }
    ctx = _make_ctx("room-001", json.dumps(metadata, ensure_ascii=False))

    with caplog.at_level("WARNING"):
        profile = agent_mod._extract_session_profile(ctx, agent_mod.config)

    assert profile.mode == "audio"
    assert "session_id mismatch" in caplog.text


@pytest.mark.asyncio
async def test_dispatch_report_request_posts_expected_payload(monkeypatch):
    prompts = agent_mod.PromptRegistry()
    layer = agent_mod.InterviewModelLayer(agent_mod.config, prompts)

    state = layer.ensure_session("sess-rt-001")
    state.session_profile.job_position = "Java后端工程师"
    state.session_profile.jd_summary = "Spring Boot/MySQL/Redis"
    state.session_profile.resume_content = "3年支付系统经验"
    state.round_results.append(
        {
            "round_id": 1,
            "current_stage": "intro",
            "dimension_scores": {"professional": 3.1, "cognition": 3.0, "expression": 3.0},
            "dimension_details": {},
            "overall_feedback": "ok",
            "final_score": 62.0,
            "improvement_suggestions": ["继续补充证据"],
        }
    )

    sent = {}

    class _Resp:
        def raise_for_status(self):
            return None

    class _FakeClient:
        def __init__(self, *args, **kwargs):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            return False

        async def post(self, url, json):
            sent["url"] = url
            sent["json"] = json
            return _Resp()

    monkeypatch.setattr(agent_mod.httpx, "AsyncClient", _FakeClient)

    await layer._dispatch_report_request(state)

    assert state.report_dispatched is True
    assert sent["url"] == agent_mod.config.report_api_url
    assert sent["json"]["session_id"] == "sess-rt-001"
    assert sent["json"]["callback_url"].endswith("/api/v1/interviews/sess-rt-001/report-callback")
    assert sent["json"]["interview_context"]["job_position"] == "Java后端工程师"
    assert sent["json"]["round_results"][0]["round_id"] == 1

    await layer.close_session("sess-rt-001")
    await layer.reasoning.close()


@pytest.mark.asyncio
async def test_inference_worker_emits_pace_control_command():
    prompts = agent_mod.PromptRegistry()
    layer = agent_mod.InterviewModelLayer(agent_mod.config, prompts)
    state = layer.ensure_session("pace-001")

    decision = agent_mod.StageDecision(
        decision_version=1,
        current_stage="intro",
        next_stage="intro",
        should_switch=False,
        confidence=0.9,
        analysis={"scores": {"professional": 3, "cognition": 3, "expression": 3}, "risk_flags": [], "flow_rationale": "ok"},
        dimension_details=agent_mod._normalize_dimension_details({}),
        dimension_scores={"professional": 3.0, "cognition": 3.0, "expression": 3.0},
        final_score=60.0,
        realtime_instruction={
            "style": "standard",
            "goal": "probe_deeper",
            "interrupt_policy": "none",
            "priority": "normal",
            "pace": "slow",
            "probe_depth": "high",
            "focus_hint": "补充性能优化细节",
        },
    )

    class _FakeReasoning:
        async def decide_stage(self, task, decision_version):
            return decision

    layer.reasoning = _FakeReasoning()

    await state.inference_queue.put(
        agent_mod.InferenceTask(
            session_id="pace-001",
            turn_id="t1",
            transcript="我用过Redis",
            context_snapshot={"decision_ticket": 1},
        )
    )

    worker = asyncio.create_task(layer._inference_worker(state, 0))
    await state.inference_queue.join()
    worker.cancel()
    with contextlib.suppress(asyncio.CancelledError):
        await worker

    drained = []
    while not state.command_queue.empty():
        drained.append(state.command_queue.get_nowait())

    cmd_types = {item.get("type") for item in drained}
    assert agent_mod.CommandType.STRATEGY_UPDATE in cmd_types
    assert agent_mod.CommandType.PACE_CONTROL in cmd_types

    await layer.close_session("pace-001")


@pytest.mark.asyncio
async def test_safe_generate_reply_is_debounced_and_version_guarded(monkeypatch):
    prompts = agent_mod.PromptRegistry()
    layer = agent_mod.InterviewModelLayer(agent_mod.config, prompts)
    state = layer.ensure_session("reply-gate-001")
    state.min_reply_interval_sec = 10.0

    assistant = agent_mod.RealtimeAssistant(layer, prompts, "reply-gate-001")

    class _FakeSession:
        def __init__(self):
            self.calls = []

        def generate_reply(self, instructions):
            self.calls.append(instructions)

    fake = _FakeSession()

    await assistant.safe_generate_reply(fake, "first", version=1)
    await assistant.safe_generate_reply(fake, "debounced", version=2)
    assert fake.calls == ["first"]

    # lift debounce window and verify old version is ignored
    state.min_reply_interval_sec = 0.0
    await assistant.safe_generate_reply(fake, "old-version", version=1)
    await assistant.safe_generate_reply(fake, "new-version", version=2)
    assert fake.calls[-1] == "new-version"

    await layer.close_session("reply-gate-001")
    await layer.reasoning.close()


@pytest.mark.asyncio
async def test_run_command_loop_pace_control_is_silent(monkeypatch):
    stop_event = asyncio.Event()
    calls = {"session_generate": 0, "agent_generate": 0}

    class _FakeSession:
        def generate_reply(self, instructions):
            calls["session_generate"] += 1

        def interrupt(self, force=True):
            return None

    class _FakeAgent:
        async def apply_strategy_update(self, session, command):
            return None

        async def safe_generate_reply(self, session, msg, version=0):
            calls["agent_generate"] += 1

    commands = [
        {"type": agent_mod.CommandType.PACE_CONTROL, "message": "pace", "decision_version": 1},
    ]

    async def _fake_get_next_command(session_id, timeout_sec=0.2):
        if commands:
            return commands.pop(0)
        stop_event.set()
        return None

    monkeypatch.setattr(agent_mod.model_layer, "get_next_command", _fake_get_next_command)

    await agent_mod._run_command_loop(_FakeSession(), _FakeAgent(), "sid-1", stop_event)

    assert calls["session_generate"] == 0
    assert calls["agent_generate"] == 0


@pytest.mark.asyncio
async def test_run_command_loop_interrupt_calls_session_interrupt(monkeypatch):
    stop_event = asyncio.Event()
    calls = {"interrupt": 0}

    class _FakeSession:
        def generate_reply(self, instructions):
            return None

        async def _async_interrupt(self):
            calls["interrupt"] += 1

        def interrupt(self, force=True):
            return self._async_interrupt()

    class _FakeAgent:
        async def apply_strategy_update(self, session, command):
            return None

        async def safe_generate_reply(self, session, msg, version=0):
            return None

    commands = [{"type": agent_mod.CommandType.INTERRUPT_ASSISTANT}]

    async def _fake_get_next_command(session_id, timeout_sec=0.2):
        if commands:
            return commands.pop(0)
        stop_event.set()
        return None

    monkeypatch.setattr(agent_mod.model_layer, "get_next_command", _fake_get_next_command)

    await agent_mod._run_command_loop(_FakeSession(), _FakeAgent(), "sid-2", stop_event)
    assert calls["interrupt"] == 1


@pytest.mark.asyncio
async def test_run_command_loop_preserves_multi_command_order(monkeypatch):
    stop_event = asyncio.Event()
    events = []

    class _FakeSession:
        def generate_reply(self, instructions):
            return None

        def interrupt(self, force=True):
            events.append("interrupt")
            return None

    class _FakeAgent:
        async def apply_strategy_update(self, session, command):
            events.append("strategy")

        async def safe_generate_reply(self, session, msg, version=0):
            events.append("soft")

    commands = [
        {"type": agent_mod.CommandType.STRATEGY_UPDATE, "decision_version": 1},
        {"type": agent_mod.CommandType.ASSISTANT_SOFT_INTERRUPT, "message": "focus", "decision_version": 1},
        {"type": agent_mod.CommandType.INTERRUPT_ASSISTANT},
    ]

    async def _fake_get_next_command(session_id, timeout_sec=0.2):
        if commands:
            return commands.pop(0)
        stop_event.set()
        return None

    monkeypatch.setattr(agent_mod.model_layer, "get_next_command", _fake_get_next_command)

    await agent_mod._run_command_loop(_FakeSession(), _FakeAgent(), "sid-order", stop_event)
    assert events == ["strategy", "soft", "interrupt"]


@pytest.mark.asyncio
async def test_dispatch_report_request_is_idempotent(monkeypatch):
    prompts = agent_mod.PromptRegistry()
    layer = agent_mod.InterviewModelLayer(agent_mod.config, prompts)
    state = layer.ensure_session("sess-idem")
    state.round_results.append({"round_id": 1})

    sent = {"count": 0}

    class _Resp:
        def raise_for_status(self):
            return None

    class _FakeClient:
        def __init__(self, *args, **kwargs):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            return False

        async def post(self, url, json):
            sent["count"] += 1
            return _Resp()

    monkeypatch.setattr(agent_mod.httpx, "AsyncClient", _FakeClient)

    await layer._dispatch_report_request(state)
    await layer._dispatch_report_request(state)

    assert sent["count"] == 1
    assert state.report_dispatched is True

    await layer.close_session("sess-idem")
    await layer.reasoning.close()


@pytest.mark.asyncio
async def test_dispatch_report_request_with_none_report_api_url_keeps_undispatched(monkeypatch):
    prompts = agent_mod.PromptRegistry()
    layer = agent_mod.InterviewModelLayer(agent_mod.config, prompts)
    state = layer.ensure_session("sess-none-url")
    state.round_results.append({"round_id": 1})

    original_url = layer.config.report_api_url
    layer.config.report_api_url = None

    sent = {"url": "unset"}

    class _FakeClient:
        def __init__(self, *args, **kwargs):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            return False

        async def post(self, url, json):
            sent["url"] = url
            raise RuntimeError("invalid-url")

    monkeypatch.setattr(agent_mod.httpx, "AsyncClient", _FakeClient)

    await layer._dispatch_report_request(state)

    assert sent["url"] is None
    assert state.report_dispatched is False

    layer.config.report_api_url = original_url
    await layer.close_session("sess-none-url")
    await layer.reasoning.close()


def test_resolve_report_callback_url_encodes_special_session_id():
    template = "https://nas.feixingxr.com/api/v1/interviews/{interviewId}/report-callback"
    out = agent_mod._resolve_report_callback_url(template, "sess/a b")
    assert out.endswith("/api/v1/interviews/sess%2Fa%20b/report-callback")


def test_apply_guardrail_interrupt_policy_keeps_existing_when_missing_action():
    fallback = {"interrupt_policy": "none", "style": "standard"}
    parsed = {"realtime_instruction": {"interrupt_policy": "soft", "style": "expert"}}
    out = agent_mod._apply_guardrail_interrupt_policy(parsed, fallback)
    assert out["interrupt_policy"] == "soft"
    assert out["style"] == "expert"


@pytest.mark.asyncio
async def test_inference_worker_ignores_stale_task(monkeypatch):
    prompts = agent_mod.PromptRegistry()
    layer = agent_mod.InterviewModelLayer(agent_mod.config, prompts)
    state = layer.ensure_session("stale-001")

    decision = agent_mod.StageDecision(
        decision_version=1,
        current_stage="intro",
        next_stage="tech_general",
        should_switch=True,
        confidence=0.9,
        analysis={"scores": {}, "risk_flags": [], "flow_rationale": "ok"},
        dimension_details=agent_mod._normalize_dimension_details({}),
        dimension_scores={"professional": 3.0, "cognition": 3.0, "expression": 3.0},
        final_score=60.0,
        realtime_instruction={"interrupt_policy": "none", "pace": "adaptive", "probe_depth": "medium"},
    )

    class _FakeReasoning:
        async def decide_stage(self, task, decision_version):
            return decision

    layer.reasoning = _FakeReasoning()

    old_ts = __import__("time").time() - (layer.config.stale_decision_ttl_sec + 5)
    await state.inference_queue.put(
        agent_mod.InferenceTask(
            session_id="stale-001",
            turn_id="t1",
            transcript="old",
            context_snapshot={"decision_ticket": 1},
            created_at=old_ts,
        )
    )

    worker = asyncio.create_task(layer._inference_worker(state, 0))
    await state.inference_queue.join()
    worker.cancel()
    with contextlib.suppress(asyncio.CancelledError):
        await worker

    assert layer.metrics.stale_decisions_ignored >= 1
    assert state.latest_decision is None

    await layer.close_session("stale-001")


@pytest.mark.asyncio
async def test_inference_worker_applies_stage_switch():
    prompts = agent_mod.PromptRegistry()
    layer = agent_mod.InterviewModelLayer(agent_mod.config, prompts)
    state = layer.ensure_session("switch-001")

    decision = agent_mod.StageDecision(
        decision_version=1,
        current_stage="intro",
        next_stage="tech_general",
        should_switch=True,
        confidence=0.9,
        analysis={"scores": {}, "risk_flags": [], "flow_rationale": "ok"},
        dimension_details=agent_mod._normalize_dimension_details({}),
        dimension_scores={"professional": 3.0, "cognition": 3.0, "expression": 3.0},
        final_score=60.0,
        realtime_instruction={
            "interrupt_policy": "none",
            "pace": "adaptive",
            "probe_depth": "medium",
            "focus_hint": "",
        },
    )

    class _FakeReasoning:
        async def decide_stage(self, task, decision_version):
            return decision

    layer.reasoning = _FakeReasoning()

    await state.inference_queue.put(
        agent_mod.InferenceTask(
            session_id="switch-001",
            turn_id="t1",
            transcript="ok",
            context_snapshot={"decision_ticket": 1},
        )
    )

    worker = asyncio.create_task(layer._inference_worker(state, 0))
    await state.inference_queue.join()
    worker.cancel()
    with contextlib.suppress(asyncio.CancelledError):
        await worker

    assert state.active_stage == "tech_general"
    assert layer.metrics.stage_switches >= 1
    assert state.latest_decision is not None

    await layer.close_session("switch-001")


@pytest.mark.asyncio
async def test_inference_worker_reasoning_exception_is_captured():
    prompts = agent_mod.PromptRegistry()
    layer = agent_mod.InterviewModelLayer(agent_mod.config, prompts)
    state = layer.ensure_session("reasoning-err-001")

    class _FakeReasoning:
        async def decide_stage(self, task, decision_version):
            raise RuntimeError("reasoning-failed")

    layer.reasoning = _FakeReasoning()

    await state.inference_queue.put(
        agent_mod.InferenceTask(
            session_id="reasoning-err-001",
            turn_id="t1",
            transcript="hello",
            context_snapshot={"decision_ticket": 1},
        )
    )

    worker = asyncio.create_task(layer._inference_worker(state, 0))
    await state.inference_queue.join()
    worker.cancel()
    with contextlib.suppress(asyncio.CancelledError):
        await worker

    assert layer.metrics.inference_failed >= 1
    assert state.latest_decision is None

    await layer.close_session("reasoning-err-001")


@pytest.mark.asyncio
async def test_close_session_cleans_sessions_and_workers():
    prompts = agent_mod.PromptRegistry()
    layer = agent_mod.InterviewModelLayer(agent_mod.config, prompts)
    state = layer.ensure_session("cleanup-001")

    async def _pending_worker():
        await asyncio.sleep(60)

    extra_task = asyncio.create_task(_pending_worker())
    layer.workers["cleanup-001"].append(extra_task)

    assert "cleanup-001" in layer.sessions
    assert "cleanup-001" in layer.workers

    await layer.close_session("cleanup-001")

    assert "cleanup-001" not in layer.sessions
    assert "cleanup-001" not in layer.workers
    assert extra_task.cancelled() or extra_task.done()

    await layer.reasoning.close()


def test_extract_session_profile_invalid_metadata_json_warns_and_falls_back(caplog):
    ctx = _make_ctx("s-invalid", "{not-a-json")
    with caplog.at_level("WARNING"):
        profile = agent_mod._extract_session_profile(ctx, agent_mod.config)

    assert profile.job_position == ""
    assert "room metadata is not valid JSON" in caplog.text


@pytest.mark.asyncio
async def test_dispatch_report_request_failure_does_not_mark_dispatched(monkeypatch):
    prompts = agent_mod.PromptRegistry()
    layer = agent_mod.InterviewModelLayer(agent_mod.config, prompts)
    state = layer.ensure_session("sess-fail")
    state.round_results.append({"round_id": 1})

    class _FakeClient:
        def __init__(self, *args, **kwargs):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            return False

        async def post(self, url, json):
            raise RuntimeError("network-fail")

    monkeypatch.setattr(agent_mod.httpx, "AsyncClient", _FakeClient)

    await layer._dispatch_report_request(state)
    assert state.report_dispatched is False

    await layer.close_session("sess-fail")


@pytest.mark.asyncio
async def test_emit_command_retry_metric_increments_on_recovered_retry():
    prompts = agent_mod.PromptRegistry()
    layer = agent_mod.InterviewModelLayer(agent_mod.config, prompts)
    state = layer.ensure_session("retry-001")
    state.command_queue = asyncio.Queue(maxsize=1)

    await state.command_queue.put({"type": "occupy"})

    async def _free_slot():
        await asyncio.sleep(0.008)
        _ = await state.command_queue.get()
        state.command_queue.task_done()

    freer = asyncio.create_task(_free_slot())
    await layer._emit_command(state, {"type": "recovered"})
    await freer

    assert layer.metrics.command_retry_count >= 1

    await layer.close_session("retry-001")


@pytest.mark.asyncio
async def test_run_command_loop_routes_strategy_and_soft_interrupt(monkeypatch):
    stop_event = asyncio.Event()
    calls = {"apply": 0, "safe": 0}

    class _FakeSession:
        def generate_reply(self, instructions):
            return None

        def interrupt(self, force=True):
            return None

    class _FakeAgent:
        async def apply_strategy_update(self, session, command):
            calls["apply"] += 1

        async def safe_generate_reply(self, session, msg, version=0):
            calls["safe"] += 1

    commands = [
        {"type": agent_mod.CommandType.STRATEGY_UPDATE, "decision_version": 2},
        {"type": agent_mod.CommandType.ASSISTANT_SOFT_INTERRUPT, "message": "focus", "decision_version": 2},
    ]

    async def _fake_get_next_command(session_id, timeout_sec=0.2):
        if commands:
            return commands.pop(0)
        stop_event.set()
        return None

    monkeypatch.setattr(agent_mod.model_layer, "get_next_command", _fake_get_next_command)

    await agent_mod._run_command_loop(_FakeSession(), _FakeAgent(), "sid-3", stop_event)

    assert calls["apply"] == 1
    assert calls["safe"] == 1
