import asyncio
import json
import sys
import time
from pathlib import Path
from types import SimpleNamespace
from typing import Any, cast

import pytest
from google.genai import types as google_types

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import app.agent as agent_mod
import app.official_workflow as workflow_mod


def _sample_report_json() -> str:
    return json.dumps(
        {
            "hiring_recommendation": "Hire",
            "executive_summary": "候选人整体表现稳定，技术栈与岗位匹配，具备较强工程实践能力。",
            "strengths": ["技术基础扎实", "表达清晰"],
            "weaknesses": ["深度案例还可再展开", "跨轮次复盘略少"],
            "ability_trend": "前中后段表现稳定，后半程有一定深挖空间但整体结论积极。",
            "detailed_recommendation": "建议录用，后续可在复杂系统设计和线上治理上继续培养。",
            "professional": {
                "technical_correctness": {
                    "reason": "回答整体准确，能覆盖关键技术点，但部分细节仍有继续追问空间。",
                    "score": 4.0,
                },
                "knowledge_match": {
                    "reason": "与岗位需要的 Spring Boot、MySQL、Redis 能较好对应。",
                    "score": 4.0,
                },
                "job_match": {
                    "reason": "能够结合后端岗位场景给出较贴近实际的回答。",
                    "score": 4.0,
                },
                "engineering_practice": {
                    "reason": "有实践经验描述，但复杂场景对比还可更充分。",
                    "score": 4.0,
                },
            },
            "cognition": {
                "logic_structure": {"reason": "回答分点清晰，结构完整。", "score": 4.0},
                "problem_solving": {"reason": "能给出可执行方案，但风险分析还可以更深入。", "score": 4.0},
                "system_thinking": {"reason": "有一定系统性，但全局权衡尚未完全展开。", "score": 4.0},
            },
            "expression": {
                "clarity": {"reason": "表达清晰，可直接理解。", "score": 4.0},
                "confidence_stability": {"reason": "整体稳定，没有明显失控或大幅跳跃。", "score": 4.0},
                "professional_maturity": {"reason": "语气与内容都保持专业。", "score": 4.0},
            },
        },
        ensure_ascii=False,
    )


def test_official_prompt_registry_renders_report_prompt_and_2_0_contract() -> None:
    context = workflow_mod.InterviewContext(
        session_id="sess-prompt-001",
        job_position="Java backend engineer",
        jd_summary="Spring Boot, MySQL, Redis",
        resume_content="3 years backend experience",
        interviewer_style="expert",
        difficulty="hard",
        company_context="internal platform",
        mode="video",
        metadata_source="room.metadata",
    )

    registry = workflow_mod.OfficialPromptRegistry()
    agent_prompt = registry.render_agent_persona(context)
    report_prompt = registry.render_report_generation_prompt(
        context,
        report_reason="finish_interview",
        conversation_summary="assistant: 请做个简单自我介绍\nuser: 我做过支付系统。",
        conversation_transcript="assistant: 请做个简单自我介绍\nuser: 我做过支付系统。",
    )

    assert "你是一位专业的大厂技术面试官" in agent_prompt
    assert "轮次保存类工具" not in agent_prompt
    assert "finish_interview" in agent_prompt
    assert "你是一位大厂技术面试的最终报告生成器" in report_prompt
    assert "hiring_recommendation" in report_prompt
    assert "technical_correctness" in report_prompt
    assert "conversation_transcript" in report_prompt
    assert "只输出一个 JSON 对象" in report_prompt
    assert '"overall_score":' not in report_prompt
    assert "不要输出 `overall_score`" in report_prompt


def test_build_google_realtime_model_injects_conservative_activity_detection(monkeypatch) -> None:
    captured_kwargs: dict[str, Any] = {}

    class FakeRealtimeModel:
        def __init__(self, **kwargs: Any) -> None:
            captured_kwargs.update(kwargs)

    monkeypatch.setattr(agent_mod.google.realtime, "RealtimeModel", FakeRealtimeModel)

    config = agent_mod.ModelConfig(
        gemini_model="test-gemini-model",
        gemini_voice="TestVoice",
        gemini_temperature=0.5,
        google_api_key="test-api-key",
        google_use_vertexai=False,
        google_enable_context_window_compression=False,
        google_enable_session_resumption=False,
        gemini_auto_activity_start_sensitivity="HIGH",
        gemini_auto_activity_end_sensitivity="LOW",
        gemini_auto_activity_prefix_padding_ms=420,
        gemini_auto_activity_silence_duration_ms=1800,
    )

    model = agent_mod._build_google_realtime_model(config)

    assert isinstance(model, FakeRealtimeModel)
    assert captured_kwargs["model"] == "test-gemini-model"
    assert captured_kwargs["voice"] == "TestVoice"
    assert captured_kwargs["temperature"] == 0.5
    assert captured_kwargs["api_key"] == "test-api-key"
    assert "context_window_compression" not in captured_kwargs
    assert "session_resumption" not in captured_kwargs

    realtime_input_config = captured_kwargs["realtime_input_config"]
    automatic_activity_detection = realtime_input_config.automatic_activity_detection
    assert automatic_activity_detection.disabled is False
    assert (
        automatic_activity_detection.start_of_speech_sensitivity
        == google_types.StartSensitivity.START_SENSITIVITY_HIGH
    )
    assert automatic_activity_detection.end_of_speech_sensitivity == google_types.EndSensitivity.END_SENSITIVITY_LOW
    assert automatic_activity_detection.prefix_padding_ms == 420
    assert automatic_activity_detection.silence_duration_ms == 1800


@pytest.mark.asyncio
async def test_ai_interview_session_wires_current_chain(monkeypatch):
    calls: list[str] = []
    fake_model = object()
    fake_room_options = SimpleNamespace(close_on_disconnect=False, delete_room_on_close=True)

    async def fake_connect() -> None:
        calls.append("connect")

    async def fake_wait_for_shutdown() -> None:
        calls.append("wait_for_shutdown")

    class FakeAgentSession:
        instances: list["FakeAgentSession"] = []

        def __init__(self, llm: Any, **kwargs: Any) -> None:
            self.llm = llm
            self.kwargs = kwargs
            self.started: dict[str, Any] | None = None
            FakeAgentSession.instances.append(self)

        async def start(self, *, room: Any, agent: Any, room_options: Any) -> None:
            calls.append("start")
            self.started = {"room": room, "agent": agent, "room_options": room_options}

    monkeypatch.setattr(agent_mod, "_build_google_realtime_model", lambda config_obj: fake_model)
    monkeypatch.setattr(agent_mod, "_build_room_options", lambda session_profile: fake_room_options)
    monkeypatch.setattr(agent_mod, "AgentSession", FakeAgentSession)

    session_metadata = {
        "session_id": "sess-001",
        "job_position": "Java backend engineer",
        "jd_summary": "Spring Boot, MySQL, Redis",
        "resume_content": "3 years backend experience",
        "interview_config": {
            "mode": "audio",
            "interviewer_style": "friendly",
            "difficulty": "hard",
            "company_context": "internal platform",
        },
    }
    ctx = SimpleNamespace(
        room=SimpleNamespace(name="room_sess-001", metadata=json.dumps(session_metadata, ensure_ascii=False)),
        job=SimpleNamespace(metadata=None),
        metadata=None,
        connect=fake_connect,
        wait_for_shutdown=fake_wait_for_shutdown,
    )

    await agent_mod.ai_interview_session(cast(Any, ctx))

    assert calls == ["connect", "start", "wait_for_shutdown"]
    assert FakeAgentSession.instances
    started = FakeAgentSession.instances[0].started
    assert started is not None
    assert started["room"].name == "room_sess-001"
    assert started["room_options"] is fake_room_options

    session_kwargs = FakeAgentSession.instances[0].kwargs
    assert session_kwargs["preemptive_generation"] is False
    assert session_kwargs["min_consecutive_speech_delay"] == float(
        agent_mod.os.getenv("INTERVIEW_MIN_CONSECUTIVE_SPEECH_DELAY", "4.0")
    )
    assert session_kwargs["turn_handling"]["turn_detection"] == "realtime_llm"
    assert session_kwargs["turn_handling"]["endpointing"]["min_delay"] == float(
        agent_mod.os.getenv("INTERVIEW_ENDPOINTING_MIN_DELAY", "4.0")
    )
    assert session_kwargs["turn_handling"]["endpointing"]["max_delay"] == float(
        agent_mod.os.getenv("INTERVIEW_ENDPOINTING_MAX_DELAY", "6.0")
    )
    assert "interruption" not in session_kwargs["turn_handling"]

    workflow_agent = started["agent"]
    assert isinstance(workflow_agent, workflow_mod.AINativeInterviewWorkflowAgent)
    assert workflow_agent._context.session_id == "sess-001"
    assert workflow_agent._context.job_position == "Java backend engineer"
    assert workflow_agent._context.mode == "audio"
    assert workflow_agent._context.metadata_source == "room.metadata"


@pytest.mark.asyncio
async def test_finish_interview_uses_report_model_and_closes_after_completion(monkeypatch):
    close_calls: list[str] = []
    generated_calls: dict[str, Any] = {}
    callback_calls: dict[str, Any] = {}
    close_event = asyncio.Event()

    class FakeSession:
        def generate_reply(self, *args: Any, **kwargs: Any) -> Any:
            raise AssertionError("finish_interview should not call realtime generate_reply for the final report")

    async def fake_generate_report_text_with_model(*, system_prompt: str, user_prompt: str) -> str:
        generated_calls["system_prompt"] = system_prompt
        generated_calls["user_prompt"] = user_prompt
        return _sample_report_json()

    async def fake_post_callback_with_retry(session_id: str, callback_url: str, payload: dict[str, Any], max_attempts: int = 3) -> None:
        callback_calls["session_id"] = session_id
        callback_calls["callback_url"] = callback_url
        callback_calls["payload"] = payload

    context = workflow_mod.InterviewContext(
        session_id="sess-finish-001",
        job_position="Java backend engineer",
        jd_summary="Spring Boot, MySQL, Redis",
        resume_content="3 years backend experience",
        interviewer_style="expert",
        difficulty="hard",
        company_context="internal platform",
        mode="audio",
        metadata_source="room.metadata",
    )
    agent = workflow_mod.AINativeInterviewWorkflowAgent(context, workflow_mod.OfficialPromptRegistry())
    chat_ctx = agent.chat_ctx.copy()
    chat_ctx.add_message(role="assistant", content="请做个简单自我介绍")
    chat_ctx.add_message(role="user", content="我做过支付系统。")
    await agent.update_chat_ctx(chat_ctx)
    monkeypatch.setattr(agent, "_get_activity_or_raise", lambda: SimpleNamespace(session=FakeSession()))
    monkeypatch.setattr(workflow_mod, "_generate_report_text_with_model", fake_generate_report_text_with_model)
    monkeypatch.setattr(workflow_mod, "_post_callback_with_retry", fake_post_callback_with_retry)
    monkeypatch.setattr(
        agent,
        "_request_session_close_after_report",
        lambda: (close_calls.append("close"), close_event.set()),
    )

    result = await cast(Any, agent).finish_interview(reason="candidate_requested_end")
    assert result["status"] == "report_generation_started"
    assert result["report_generation_started"] is True
    assert "最终报告生成任务" in result["message"]

    await asyncio.wait_for(close_event.wait(), timeout=1.0)
    await asyncio.sleep(0)

    assert close_calls == ["close"]
    assert "你是一位大厂技术面试的最终报告生成器" in generated_calls["system_prompt"]
    assert "只输出一个 JSON 对象" in generated_calls["system_prompt"]
    assert "conversation_transcript" in generated_calls["user_prompt"]
    assert "我做过支付系统。" in generated_calls["user_prompt"]
    assert agent._final_report_payload is not None
    assert agent._final_report_payload["hiring_recommendation"] == "Hire"
    assert agent._final_report_payload["professional"]["technical_correctness"]["score"] == 4.0
    assert agent._final_report_payload["dimension_scores"] == {
        "professional": 4.0,
        "cognition": 4.0,
        "expression": 4.0,
    }
    assert agent._final_report_payload["overall_score"] == 80.0
    assert callback_calls["callback_url"] == "https://nas.feixingxr.com/api/v1/interviews/sess-finish-001/report-callback"
    assert callback_calls["session_id"] == "sess-finish-001"
    assert callback_calls["payload"]["hiring_recommendation"] == "Hire"
    assert callback_calls["payload"]["executive_summary"] == "候选人整体表现稳定，技术栈与岗位匹配，具备较强工程实践能力。"
    assert callback_calls["payload"]["strengths"] == ["技术基础扎实", "表达清晰"]
    assert callback_calls["payload"]["weaknesses"] == ["深度案例还可再展开", "跨轮次复盘略少"]
    assert callback_calls["payload"]["ability_trend"].startswith("前中后段表现稳定")
    assert callback_calls["payload"]["detailed_recommendation"].startswith("建议录用")
    assert callback_calls["payload"]["professional"]["technical_correctness"]["score"] == 4.0
    assert callback_calls["payload"]["professional"]["knowledge_match"]["score"] == 4.0
    assert callback_calls["payload"]["cognition"]["logic_structure"]["score"] == 4.0
    assert callback_calls["payload"]["expression"]["clarity"]["score"] == 4.0
    assert callback_calls["payload"]["dimension_scores"] == {
        "professional": 4.0,
        "cognition": 4.0,
        "expression": 4.0,
    }
    assert callback_calls["payload"]["overall_score"] == 80.0
