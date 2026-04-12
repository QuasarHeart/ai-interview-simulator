import asyncio
import json
import sys
from pathlib import Path
from types import SimpleNamespace
from typing import Any, cast

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import app.agent as agent_mod
import app.LLM_engine.engine as engine_mod
import app.main as main_mod
import app.official_workflow as workflow_mod
from app.schemas.schemas import AnalysisRequest, Background, ContentToAnalyze, FollowupRequest, FlowControl, HistoryData, InterviewConfig, RecentHistoryItem
from google.genai import types as google_types


def _make_ctx(
    room_name: str,
    metadata: str | dict | None = None,
    *,
    job_metadata: str | dict | None = None,
    ctx_metadata: str | dict | None = None,
):
    room = SimpleNamespace(name=room_name, metadata=metadata)
    job = SimpleNamespace(metadata=job_metadata)
    return SimpleNamespace(room=room, job=job, metadata=ctx_metadata)


def test_extract_session_profile_from_room_metadata_fixture():
    fixture_path = Path(__file__).resolve().parent / "fixtures" / "room_metadata_template.json"
    metadata = json.loads(fixture_path.read_text(encoding="utf-8"))
    ctx = _make_ctx(metadata["session_id"], json.dumps(metadata, ensure_ascii=False))

    profile = agent_mod._extract_session_profile(ctx, agent_mod.config)

    assert profile.interviewer_style == "expert"
    assert profile.difficulty == "hard"
    assert profile.mode == "video"
    assert profile.company_context == "电商交易场景"
    assert profile.job_position == "Java后端工程师"
    assert profile.jd_summary.startswith("熟悉 Spring Boot")
    assert profile.resume_content.startswith("3年支付与交易系统经验")


def test_extract_session_context_prefers_metadata_session_id_over_room_prefix(caplog):
    fixture_path = Path(__file__).resolve().parent / "fixtures" / "room_metadata_template.json"
    metadata = json.loads(fixture_path.read_text(encoding="utf-8"))
    ctx = _make_ctx(f"room_{metadata['session_id']}", json.dumps(metadata, ensure_ascii=False))

    with caplog.at_level("WARNING"):
        profile, session_metadata, metadata_source, resolved_session_id = agent_mod._extract_session_context(ctx, agent_mod.config)

    assert resolved_session_id == metadata["session_id"]
    assert session_metadata["session_id"] == metadata["session_id"]
    assert metadata_source == "room.metadata"
    assert profile.job_position == "Java后端工程师"
    assert not any("session_id mismatch" in record.message for record in caplog.records)


def test_extract_session_context_warns_on_true_session_id_mismatch(caplog):
    metadata = {
        "session_id": "sess-002",
        "job_position": "Python后端工程师",
        "jd_summary": "熟悉 FastAPI/Redis",
        "resume_content": "5年后端经验",
        "interview_config": {
            "mode": "audio",
            "interviewer_style": "friendly",
            "difficulty": "medium",
            "company_context": "内部平台",
        },
    }
    ctx = _make_ctx("room_789cb3fad3c94352a26f043ff94afbf9", json.dumps(metadata, ensure_ascii=False))

    with caplog.at_level("WARNING"):
        _, _, _, resolved_session_id = agent_mod._extract_session_context(ctx, agent_mod.config)

    assert resolved_session_id == "sess-002"
    assert any("session_id mismatch" in record.message for record in caplog.records)


def test_extract_session_profile_prefers_job_metadata():
    metadata = {
        "session_id": "s-002",
        "job_position": "Python后端工程师",
        "jd_summary": "熟悉 FastAPI/Redis",
        "resume_content": "5年后端经验",
        "interview_config": {
            "mode": "audio",
            "interviewer_style": "friendly",
            "difficulty": "medium",
            "company_context": "内部平台",
        },
    }
    ctx = _make_ctx("s-002", None, job_metadata=json.dumps(metadata, ensure_ascii=False))

    profile = agent_mod._extract_session_profile(ctx, agent_mod.config)

    assert profile.interviewer_style == "friendly"
    assert profile.difficulty == "medium"
    assert profile.mode == "audio"
    assert profile.job_position == "Python后端工程师"
    assert profile.jd_summary == "熟悉 FastAPI/Redis"
    assert profile.resume_content == "5年后端经验"


def test_extract_session_profile_defaults_when_metadata_missing():
    ctx = _make_ctx("s-003", None)

    profile = agent_mod._extract_session_profile(ctx, agent_mod.config)

    assert profile.interviewer_style == agent_mod.config.interviewer_style
    assert profile.difficulty == agent_mod.config.difficulty
    assert profile.mode == agent_mod.config.interview_mode
    assert profile.job_position == ""
    assert profile.jd_summary == ""
    assert profile.resume_content == ""


def test_build_room_options_deletes_room_on_close():
    profile = agent_mod.SessionProfile(mode="video")

    room_options = agent_mod._build_room_options(profile)

    assert room_options.close_on_disconnect is False
    assert room_options.delete_room_on_close is True
    assert room_options.video_input is not False


def test_build_google_realtime_model_enables_live_session_management(monkeypatch):
    captured_kwargs: dict[str, object] = {}

    class _FakeRealtimeModel:
        def __init__(self, **kwargs):
            captured_kwargs.update(kwargs)

    monkeypatch.setattr(agent_mod.google.realtime, "RealtimeModel", _FakeRealtimeModel)

    config_obj = agent_mod.ModelConfig(
        google_api_key="test-key",
        google_enable_context_window_compression=True,
        google_enable_session_resumption=True,
    )

    agent_mod._build_google_realtime_model(config_obj)

    assert isinstance(captured_kwargs["context_window_compression"], google_types.ContextWindowCompressionConfig)
    assert isinstance(captured_kwargs["context_window_compression"].sliding_window, google_types.SlidingWindow)
    assert isinstance(captured_kwargs["session_resumption"], google_types.SessionResumptionConfig)


def test_recent_history_prompt_window_is_compact_and_tail_only():
    history = [
        SimpleNamespace(
            round_id=round_id,
            assistant_content="A" * 220,
            user_content="U" * 220,
            flow_control=SimpleNamespace(stage_transition="continue", target_stage="tech_general"),
        )
        for round_id in range(1, 7)
    ]

    prompt_text = engine_mod._format_recent_history_for_prompt(history)

    assert "[1]:" not in prompt_text
    assert "[2]:" not in prompt_text
    assert "[3]:" in prompt_text
    assert "[6]:" in prompt_text
    assert len(prompt_text) < 1600


def test_stream_field_prefix_extraction_prefers_feedback_before_question():
    raw_stream = '{"immediate_feedback":"上一轮回答抓住了核心，建议再补一点数据结果。","question":"请继续说明缓存失效后的补偿方案'

    feedback, feedback_closed = main_mod._extract_json_string_value_prefix(raw_stream, "immediate_feedback")
    question, question_closed = main_mod._extract_json_string_value_prefix(raw_stream, "question")

    assert feedback == "上一轮回答抓住了核心，建议再补一点数据结果。"
    assert feedback_closed is True
    assert question == "请继续说明缓存失效后的补偿方案"
    assert question_closed is False


def test_analysis_prompt_kwargs_are_compact():
    request = AnalysisRequest(
        session_id="sess-100",
        round_id=1,
        current_stage="tech_general",
        interview_config=InterviewConfig(
            mode="text",
            interviewer_style="standard",
            difficulty="medium",
            company_context="电商场景",
        ),
        content_to_analyze=ContentToAnalyze(
            job_position="Java后端工程师",
            jd_summary="J" * 1800,
            resume_content="R" * 4000,
            question="Q" * 1200,
            user_answer="A" * 2600,
            history_summary="H" * 1800,
        ),
    )

    kwargs = engine_mod._compact_analysis_prompt_kwargs(request)

    assert len(kwargs["jd_summary"]) <= engine_mod.ANALYSIS_CONTEXT_MAX_CHARS
    assert len(kwargs["resume_content"]) <= engine_mod.ANALYSIS_CONTEXT_MAX_CHARS
    assert len(kwargs["question"]) <= engine_mod.ANALYSIS_QUESTION_MAX_CHARS
    assert len(kwargs["user_answer"]) <= engine_mod.ANALYSIS_ANSWER_MAX_CHARS
    assert len(kwargs["history_summary"]) <= engine_mod.ANALYSIS_HISTORY_SUMMARY_MAX_CHARS


def test_round_results_are_compact_for_report_prompt():
    round_results = [
        SimpleNamespace(
            round_id=1,
            current_stage="tech_general",
            dimension_scores=SimpleNamespace(professional=4.0, cognition=3.5, expression=4.0),
            dimension_details={
                "professional": {
                    "technical_correctness": {"reason": "T" * 300, "score": 4.0},
                    "knowledge_match": {"reason": "K" * 300, "score": 4.0},
                },
                "cognition": {
                    "logic_structure": {"reason": "L" * 300, "score": 4.0},
                },
                "expression": {
                    "clarity": {"reason": "C" * 300, "score": 4.0},
                },
            },
            overall_feedback="O" * 500,
            final_score=82.0,
            improvement_suggestions=["S" * 400, "T" * 400, "U" * 400, "V" * 400],
        )
    ]

    compacted = engine_mod._compact_round_results_for_report(round_results)

    assert len(compacted) == 1
    assert len(compacted[0]["overall_feedback"]) <= engine_mod.REPORT_RESULT_TEXT_MAX_CHARS
    assert len(compacted[0]["improvement_suggestions"]) == 3
    assert all(len(item) <= engine_mod.REPORT_SUGGESTION_MAX_CHARS for item in compacted[0]["improvement_suggestions"])
    assert len(compacted[0]["dimension_details"]["professional"]["technical_correctness"]["reason"]) <= engine_mod.REPORT_REASON_MAX_CHARS


@pytest.mark.asyncio
async def test_followup_stream_emits_feedback_before_question():
    class _FakeStreamEngine:
        async def stream_following_question(self, request, *args, **kwargs):
            yield '{"immediate_feedback":"上一轮回答抓住了核心，'
            yield '建议再补一点数据结果。","question":"请继续说明缓存失效后的补偿方案","updated_history_summary":"已覆盖要点","flow_control":{"stage_transition":"continue","target_stage":"intro"}}'

    fake_engine = _FakeStreamEngine()
    http_request: Any = SimpleNamespace(app=SimpleNamespace(state=SimpleNamespace(engine=fake_engine)))
    followup_request = FollowupRequest(
        session_id="sess-001",
        round_id=2,
        interview_config=InterviewConfig(
            mode="text",
            interviewer_style="standard",
            difficulty="medium",
            company_context="电商场景",
        ),
        background=Background(
            job_position="Java后端工程师",
            resume_content="3年后端经验",
            jd_summary="熟悉 Spring Boot 和 MySQL",
        ),
        history_data=HistoryData(
            history_summary="上一轮已完成基础追问",
            recent_history=[
                RecentHistoryItem(
                    round_id=1,
                    assistant_content="请介绍一下项目经历",
                    user_content="我做过缓存优化",
                    flow_control=FlowControl(stage_transition="continue", target_stage="intro"),
                )
            ],
        ),
    )

    response = await cast(Any, main_mod.followup_interview_stream)(followup_request, http_request)

    chunks: list[str] = []
    async for chunk in response.body_iterator:
        chunks.append(chunk.decode("utf-8") if isinstance(chunk, bytes) else str(chunk))

    body = "".join(chunks)
    assert body.index('"field": "immediate_feedback"') < body.index('"field": "question"')


@pytest.mark.parametrize(
    "stage_name, expected",
    [
        ("intro", True),
        ("resume_deep_dive", True),
        ("tech_general", True),
        ("tech_scenario", True),
        ("reverse_qa", True),
        ("end", True),
    ],
)
def test_official_workflow_stage_order_contains_all_stages(stage_name: str, expected: bool):
    assert (stage_name in workflow_mod.STAGE_ORDER) is expected


@pytest.mark.parametrize(
    "answer, expected",
    [
        ("没问题了", True),
        ("暂时没有了，谢谢", True),
        ("还有问题", False),
        ("我想再问一个问题", False),
    ],
)
def test_no_more_questions_detection(answer: str, expected: bool):
    assert workflow_mod._no_more_questions(answer) is expected


@pytest.mark.parametrize(
    "answer, expected",
    [
        ("我不想面试了", True),
        ("咱们先结束吧", True),
        ("请继续追问", False),
        ("我只是想换个话题", False),
    ],
)
def test_candidate_wants_to_stop_detection(answer: str, expected: bool):
    assert workflow_mod._candidate_wants_to_stop(answer) is expected


@pytest.mark.parametrize(
    "answer, expected",
    [
        ("我今天有点事，先这样吧。", True),
        ("这次面试就到这里。", True),
        ("咱们今天先结束，我改天再来。", True),
        ("别面试了。", True),
        ("我想换个话题继续聊技术。", False),
        ("能不能先别面试，继续讲项目。", False),
    ],
)
def test_candidate_wants_to_stop_handles_paraphrases(answer: str, expected: bool):
    assert workflow_mod._candidate_wants_to_stop(answer) is expected


@pytest.mark.parametrize(
    "exc, stop_requested, expected",
    [
        (workflow_mod.llm.ToolError("AgentTask interview_stage_task is cancelled"), False, True),
        (workflow_mod.llm.ToolError("AgentTask interview_stage_task is cancelled"), True, True),
        (RuntimeError("unexpected failure"), False, False),
    ],
)
def test_expected_workflow_cancellation_detection(exc: BaseException, stop_requested: bool, expected: bool):
    assert workflow_mod._is_expected_workflow_cancellation(exc, stop_requested) is expected


def test_request_session_close_before_report_uses_close_soon():
    context = workflow_mod.InterviewContext(
        session_id="sess-close-first",
        job_position="Java后端工程师",
        jd_summary="Spring Boot",
        resume_content="3年后端经验",
        interviewer_style="expert",
        difficulty="hard",
        company_context="电商交易场景",
        mode="video",
        metadata_source="room.metadata",
    )
    agent = workflow_mod.InterviewWorkflowAgent(context, workflow_mod.OfficialPromptRegistry())

    calls: list[tuple[str, object]] = []

    class _FakeSession:
        def _close_soon(self, *, reason, drain=False, error=None):
            calls.append(("close_soon", reason))

        async def aclose(self):
            calls.append(("aclose", None))

    agent._get_activity_or_raise = lambda: SimpleNamespace(session=_FakeSession())  # type: ignore[method-assign]

    agent._request_session_close_before_report()

    assert calls == [("close_soon", workflow_mod.CloseReason.TASK_COMPLETED)]


@pytest.mark.asyncio
async def test_on_enter_requests_close_before_background_report(monkeypatch):
    events: list[tuple[str, object]] = []
    report_finish = asyncio.Event()

    stage_result = workflow_mod.StageResult(
        stage="intro",
        turns=1,
        question="请做个简单自我介绍",
        user_answer="我做过支付系统。",
        history_summary="assistant: 请做个简单自我介绍\nuser: 我做过支付系统。",
        turn_records=[],
        completed_reason="turn_limit_reached",
    )

    class _FakeTaskGroup:
        def __init__(self, chat_ctx, on_task_completed):
            self._on_task_completed = on_task_completed

        def add(self, *args, **kwargs):
            events.append(("add", kwargs.get("id", "")))

        def cancel(self):
            events.append(("cancel", "task_group"))

        def __await__(self):
            async def _run():
                events.append(("task_group_await", "start"))
                return SimpleNamespace(task_results={"intro": stage_result})

            return _run().__await__()

    class _FakeReportService:
        def __init__(self):
            events.append(("report_service_init", "init"))

        async def generate_and_callback(self, context, stage_results):
            events.append(("report_start", len(stage_results)))
            await report_finish.wait()
            events.append(("report_finish", len(stage_results)))
            return {"status": "success", "callback_url": "http://example.com/report"}

        async def aclose(self):
            events.append(("report_service_close", "close"))

    class _FakeSession:
        def _close_soon(self, *, reason, drain=False, error=None):
            events.append(("close_soon", reason))

    monkeypatch.setattr(workflow_mod, "TaskGroup", _FakeTaskGroup)
    monkeypatch.setattr(workflow_mod, "OfficialReportService", _FakeReportService)

    context = workflow_mod.InterviewContext(
        session_id="sess-bg-report",
        job_position="Java后端工程师",
        jd_summary="Spring Boot",
        resume_content="3年后端经验",
        interviewer_style="expert",
        difficulty="hard",
        company_context="电商交易场景",
        mode="video",
        metadata_source="room.metadata",
    )
    agent = workflow_mod.InterviewWorkflowAgent(context, workflow_mod.OfficialPromptRegistry())
    agent._get_activity_or_raise = lambda: SimpleNamespace(session=_FakeSession())  # type: ignore[method-assign]

    await agent.on_enter()
    await asyncio.sleep(0)

    assert agent._report_task is not None
    assert not agent._report_task.done()

    close_index = next(index for index, item in enumerate(events) if item[0] == "close_soon")
    report_start_index = next(index for index, item in enumerate(events) if item[0] == "report_start")
    assert close_index < report_start_index
    assert events[report_start_index] == ("report_start", 1)

    report_finish.set()
    await asyncio.wait_for(agent._report_task, timeout=2.0)

    assert any(item[0] == "report_finish" for item in events)
    assert any(item[0] == "report_service_close" for item in events)
