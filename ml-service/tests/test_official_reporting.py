import asyncio
from types import SimpleNamespace
from typing import Any

import pytest

import app.official_reporting as reporting_mod
import app.official_workflow as workflow_mod


class _FakeEngine:
    def __init__(self) -> None:
        self.analysis_calls: list[object] = []
        self.report_calls: list[object] = []

    async def analyze_answer(self, request):
        self.analysis_calls.append(request)
        return {
            "dimension_details": {
                "professional": {
                    "technical_correctness": {"reason": "ok", "score": 4.0},
                    "knowledge_match": {"reason": "ok", "score": 4.0},
                    "job_match": {"reason": "ok", "score": 4.0},
                    "engineering_practice": {"reason": "ok", "score": 4.0},
                },
                "cognition": {
                    "logic_structure": {"reason": "ok", "score": 4.0},
                    "problem_solving": {"reason": "ok", "score": 4.0},
                    "system_thinking": {"reason": "ok", "score": 4.0},
                },
                "expression": {
                    "clarity": {"reason": "ok", "score": 4.0},
                    "confidence_stability": {"reason": "ok", "score": 4.0},
                    "professional_maturity": {"reason": "ok", "score": 4.0},
                },
            },
            "dimension_scores": {"professional": 4.0, "cognition": 4.0, "expression": 4.0},
            "final_score": 80.0,
            "overall_feedback": "good",
            "improvement_suggestions": ["more depth"],
        }

    async def generate_overall_report(self, request):
        self.report_calls.append(request)
        return {
            "hiring_recommendation": "Hire",
            "overall_score": 81.5,
            "executive_summary": "summary",
            "strengths": ["stable"],
            "weaknesses": ["deeper follow-up needed"],
            "ability_trend": "steady",
            "detailed_recommendation": "hire",
        }

    async def aclose(self):
        return None


@pytest.mark.asyncio
async def test_build_round_results_flattens_turn_records():
    engine: Any = _FakeEngine()
    service = reporting_mod.OfficialReportService(engine=engine, callback_url_template="http://example.com/{interviewId}")
    context = workflow_mod.InterviewContext(
        session_id="sess-100",
        job_position="Java后端工程师",
        jd_summary="Spring Boot",
        resume_content="3年后端经验",
        interviewer_style="expert",
        difficulty="hard",
        company_context="电商交易场景",
        mode="video",
        metadata_source="room.metadata",
    )
    stage_result = workflow_mod.StageResult(
        stage="tech_general",
        turns=2,
        question="你怎么设计缓存失效？",
        user_answer="我会结合过期时间和主动失效。",
        history_summary="assistant: 你怎么设计缓存失效？\nuser: 我会结合过期时间和主动失效。",
        turn_records=[
            workflow_mod.StageTurnRecord(
                stage="tech_general",
                turn_index=1,
                question="你怎么设计缓存失效？",
                user_answer="我会结合过期时间和主动失效。",
                history_summary="assistant: 你怎么设计缓存失效？\nuser: 我会结合过期时间和主动失效。",
            ),
            workflow_mod.StageTurnRecord(
                stage="tech_general",
                turn_index=2,
                question="如果双写失败怎么办？",
                user_answer="我会补偿重试并监控一致性。",
                history_summary="assistant: 如果双写失败怎么办？\nuser: 我会补偿重试并监控一致性。",
            ),
        ],
        completed_reason="turn_limit_reached",
    )

    round_results = await service.build_round_results(context, [stage_result])

    assert len(round_results) == 2
    assert round_results[0].round_id == 1
    assert round_results[0].current_stage == "tech_general"
    assert round_results[1].round_id == 2
    assert engine.analysis_calls

    await service.aclose()


@pytest.mark.asyncio
async def test_generate_and_callback_posts_report_payload():
    engine: Any = _FakeEngine()
    service = reporting_mod.OfficialReportService(engine=engine, callback_url_template="http://example.com/{interviewId}")
    context = SimpleNamespace(
        session_id="sess-200",
        job_position="Java后端工程师",
        jd_summary="Spring Boot",
        resume_content="3年后端经验",
        interviewer_style="expert",
        difficulty="hard",
        company_context="电商交易场景",
        mode="video",
        metadata_source="room.metadata",
        started_at=0.0,
    )
    stage_result = workflow_mod.StageResult(
        stage="intro",
        turns=1,
        question="请做个简单自我介绍",
        user_answer="我做过支付系统。",
        history_summary="assistant: 请做个简单自我介绍\nuser: 我做过支付系统。",
        turn_records=[
            workflow_mod.StageTurnRecord(
                stage="intro",
                turn_index=1,
                question="请做个简单自我介绍",
                user_answer="我做过支付系统。",
                history_summary="assistant: 请做个简单自我介绍\nuser: 我做过支付系统。",
            )
        ],
        completed_reason="turn_limit_reached",
    )

    posted = {}

    async def _fake_post_callback(callback_url: str, payload: dict, max_attempts: int = 3):
        posted["callback_url"] = callback_url
        posted["payload"] = payload

    service._post_callback_with_retry = _fake_post_callback  # type: ignore[method-assign]

    result = await service.generate_and_callback(context, [stage_result])

    assert result["status"] == "success"
    assert posted["callback_url"] == "http://example.com/sess-200"
    assert posted["payload"]["overall_score"] == 81.5
    assert engine.report_calls

    await service.aclose()


@pytest.mark.asyncio
async def test_generate_and_callback_times_out_report_generation():
    class _SlowReportEngine:
        async def analyze_answer(self, request):
            return {
                "dimension_details": {
                    "professional": {
                        "technical_correctness": {"reason": "ok", "score": 4.0},
                        "knowledge_match": {"reason": "ok", "score": 4.0},
                        "job_match": {"reason": "ok", "score": 4.0},
                        "engineering_practice": {"reason": "ok", "score": 4.0},
                    },
                    "cognition": {
                        "logic_structure": {"reason": "ok", "score": 4.0},
                        "problem_solving": {"reason": "ok", "score": 4.0},
                        "system_thinking": {"reason": "ok", "score": 4.0},
                    },
                    "expression": {
                        "clarity": {"reason": "ok", "score": 4.0},
                        "confidence_stability": {"reason": "ok", "score": 4.0},
                        "professional_maturity": {"reason": "ok", "score": 4.0},
                    },
                },
                "dimension_scores": {"professional": 4.0, "cognition": 4.0, "expression": 4.0},
                "final_score": 80.0,
                "overall_feedback": "good",
                "improvement_suggestions": ["more depth"],
            }

        async def generate_overall_report(self, request):
            await asyncio.Future()

        async def aclose(self):
            return None

    service = reporting_mod.OfficialReportService(
        engine=_SlowReportEngine(),
        callback_url_template="http://example.com/{interviewId}",
        report_analysis_timeout_sec=0.5,
        report_generation_timeout_sec=0.01,
    )
    context = SimpleNamespace(
        session_id="sess-201",
        job_position="Java后端工程师",
        jd_summary="Spring Boot",
        resume_content="3年后端经验",
        interviewer_style="expert",
        difficulty="hard",
        company_context="电商交易场景",
        mode="video",
        metadata_source="room.metadata",
        started_at=0.0,
    )
    stage_result = workflow_mod.StageResult(
        stage="intro",
        turns=1,
        question="请做个简单自我介绍",
        user_answer="我做过支付系统。",
        history_summary="assistant: 请做个简单自我介绍\nuser: 我做过支付系统。",
        turn_records=[
            workflow_mod.StageTurnRecord(
                stage="intro",
                turn_index=1,
                question="请做个简单自我介绍",
                user_answer="我做过支付系统。",
                history_summary="assistant: 请做个简单自我介绍\nuser: 我做过支付系统。",
            )
        ],
        completed_reason="turn_limit_reached",
    )

    posted = {}

    async def _fake_post_callback(callback_url: str, payload: dict, max_attempts: int = 3):
        posted["callback_url"] = callback_url
        posted["payload"] = payload

    service._post_callback_with_retry = _fake_post_callback  # type: ignore[method-assign]

    result = await service.generate_and_callback(context, [stage_result])

    assert result["status"] == "failed"
    assert posted["callback_url"] == "http://example.com/sess-201"
    assert posted["payload"]["message"] == "report_generation_failed"
    assert "timed out" in posted["payload"]["data"]["error"]

    await service.aclose()


@pytest.mark.asyncio
async def test_generate_and_callback_falls_back_on_analysis_timeout():
    class _SlowAnalysisEngine:
        async def analyze_answer(self, request):
            await asyncio.Future()

        async def generate_overall_report(self, request):
            return {
                "hiring_recommendation": "Hire",
                "overall_score": 81.5,
                "executive_summary": "summary",
                "strengths": ["stable"],
                "weaknesses": ["deeper follow-up needed"],
                "ability_trend": "steady",
                "detailed_recommendation": "hire",
            }

        async def aclose(self):
            return None

    service = reporting_mod.OfficialReportService(
        engine=_SlowAnalysisEngine(),
        callback_url_template="http://example.com/{interviewId}",
        report_analysis_timeout_sec=1.0,
        report_generation_timeout_sec=1.0,
    )
    context = SimpleNamespace(
        session_id="sess-202",
        job_position="Java后端工程师",
        jd_summary="Spring Boot",
        resume_content="3年后端经验",
        interviewer_style="expert",
        difficulty="hard",
        company_context="电商交易场景",
        mode="video",
        metadata_source="room.metadata",
        started_at=0.0,
    )
    stage_result = workflow_mod.StageResult(
        stage="intro",
        turns=1,
        question="请做个简单自我介绍",
        user_answer="我做过支付系统。",
        history_summary="assistant: 请做个简单自我介绍\nuser: 我做过支付系统。",
        turn_records=[
            workflow_mod.StageTurnRecord(
                stage="intro",
                turn_index=1,
                question="请做个简单自我介绍",
                user_answer="我做过支付系统。",
                history_summary="assistant: 请做个简单自我介绍\nuser: 我做过支付系统。",
            )
        ],
        completed_reason="turn_limit_reached",
    )

    posted = {}

    async def _fake_post_callback(callback_url: str, payload: dict, max_attempts: int = 3):
        posted["callback_url"] = callback_url
        posted["payload"] = payload

    service._post_callback_with_retry = _fake_post_callback  # type: ignore[method-assign]

    result = await service.generate_and_callback(context, [stage_result])

    assert result["status"] == "success"
    assert posted["callback_url"] == "http://example.com/sess-202"
    assert posted["payload"]["overall_score"] == 81.5
    assert result["round_results"][0].final_score == 0.0
    assert "timeout" in result["round_results"][0].overall_feedback.lower()

    await service.aclose()


@pytest.mark.asyncio
async def test_report_engine_logs_pipeline_when_enabled(caplog, monkeypatch):
    class _FakeClient:
        def __init__(self, *args, **kwargs):
            self.models = SimpleNamespace(generate_content=self._generate_content)

        def _generate_content(self, *args, **kwargs):
            return SimpleNamespace(
                text=(
                    '{"hiring_recommendation":"Hire","overall_score":81.5,'
                    '"executive_summary":"summary","strengths":["stable"],'
                    '"weaknesses":["deeper follow-up needed"],"ability_trend":"steady",'
                    '"detailed_recommendation":"hire"}'
                )
            )

    monkeypatch.setattr(reporting_mod._GoogleReportEngine, "_build_client", lambda self: _FakeClient())

    engine = reporting_mod._GoogleReportEngine(log_pipeline=True, log_pipeline_max_chars=2048)
    request = reporting_mod.ReportRequest.model_validate(
        {
            "session_id": "sess-log",
            "callback_url": None,
            "interview_config": {
                "mode": "video",
                "interviewer_style": "expert",
                "difficulty": "hard",
                "company_context": "电商交易场景",
            },
            "interview_context": {
                "job_position": "Java后端工程师",
                "jd_summary": "Spring Boot",
                "resume_content": "3年后端经验",
                "total_rounds": 1,
                "interview_duration_seconds": 180,
            },
            "round_results": [
                {
                    "round_id": 1,
                    "current_stage": "tech_general",
                    "dimension_scores": {"professional": 4.0, "cognition": 4.0, "expression": 4.0},
                    "dimension_details": {
                        "professional": {
                            "technical_correctness": {"reason": "ok", "score": 4.0},
                            "knowledge_match": {"reason": "ok", "score": 4.0},
                            "job_match": {"reason": "ok", "score": 4.0},
                            "engineering_practice": {"reason": "ok", "score": 4.0},
                        },
                        "cognition": {
                            "logic_structure": {"reason": "ok", "score": 4.0},
                            "problem_solving": {"reason": "ok", "score": 4.0},
                            "system_thinking": {"reason": "ok", "score": 4.0},
                        },
                        "expression": {
                            "clarity": {"reason": "ok", "score": 4.0},
                            "confidence_stability": {"reason": "ok", "score": 4.0},
                            "professional_maturity": {"reason": "ok", "score": 4.0},
                        },
                    },
                    "overall_feedback": "good",
                    "final_score": 80.0,
                    "improvement_suggestions": ["more depth"],
                }
            ],
        }
    )

    with caplog.at_level("INFO"):
        result = await engine.generate_overall_report(request)

    assert result["overall_score"] == 81.5
    messages = [record.message for record in caplog.records]
    assert any("[Report-Pipeline] stage=report event=input" in message for message in messages)
    assert any("[Report-Pipeline] stage=report event=rendered_prompts" in message for message in messages)
    assert any("[Report-Pipeline] stage=report event=response_raw" in message for message in messages)
    assert any("[Report-Pipeline] stage=report event=response_parsed" in message for message in messages)


@pytest.mark.asyncio
async def test_generate_and_callback_pipeline_logs_when_enabled(caplog):
    engine: Any = _FakeEngine()
    service = reporting_mod.OfficialReportService(
        engine=engine,
        callback_url_template="http://example.com/{interviewId}",
        log_pipeline=True,
        log_callback_body=False,
    )
    context = SimpleNamespace(
        session_id="sess-203",
        job_position="Java后端工程师",
        jd_summary="Spring Boot",
        resume_content="3年后端经验",
        interviewer_style="expert",
        difficulty="hard",
        company_context="电商交易场景",
        mode="video",
        metadata_source="room.metadata",
        started_at=0.0,
    )
    stage_result = workflow_mod.StageResult(
        stage="intro",
        turns=1,
        question="请做个简单自我介绍",
        user_answer="我做过支付系统。",
        history_summary="assistant: 请做个简单自我介绍\nuser: 我做过支付系统。",
        turn_records=[
            workflow_mod.StageTurnRecord(
                stage="intro",
                turn_index=1,
                question="请做个简单自我介绍",
                user_answer="我做过支付系统。",
                history_summary="assistant: 请做个简单自我介绍\nuser: 我做过支付系统。",
            )
        ],
        completed_reason="turn_limit_reached",
    )

    posted = {}

    async def _fake_post_callback(callback_url: str, payload: dict, max_attempts: int = 3):
        posted["callback_url"] = callback_url
        posted["payload"] = payload

    service._post_callback_with_retry = _fake_post_callback  # type: ignore[method-assign]

    with caplog.at_level("INFO"):
        result = await service.generate_and_callback(context, [stage_result])

    assert result["status"] == "success"
    assert posted["callback_url"] == "http://example.com/sess-203"
    assert posted["payload"]["overall_score"] == 81.5
    messages = [record.message for record in caplog.records]
    assert any("[Report-Pipeline] stage=report event=start" in message for message in messages)
    assert any("[Report-Pipeline] stage=analysis event=start" in message for message in messages)
    assert any("[Report-Pipeline] stage=callback event=completed" in message for message in messages)

    await service.aclose()


@pytest.mark.asyncio
async def test_generate_and_callback_pipeline_logs_when_disabled(caplog):
    engine: Any = _FakeEngine()
    service = reporting_mod.OfficialReportService(
        engine=engine,
        callback_url_template="http://example.com/{interviewId}",
        log_pipeline=False,
        log_callback_body=False,
    )
    context = SimpleNamespace(
        session_id="sess-204",
        job_position="Java后端工程师",
        jd_summary="Spring Boot",
        resume_content="3年后端经验",
        interviewer_style="expert",
        difficulty="hard",
        company_context="电商交易场景",
        mode="video",
        metadata_source="room.metadata",
        started_at=0.0,
    )
    stage_result = workflow_mod.StageResult(
        stage="intro",
        turns=1,
        question="请做个简单自我介绍",
        user_answer="我做过支付系统。",
        history_summary="assistant: 请做个简单自我介绍\nuser: 我做过支付系统。",
        turn_records=[
            workflow_mod.StageTurnRecord(
                stage="intro",
                turn_index=1,
                question="请做个简单自我介绍",
                user_answer="我做过支付系统。",
                history_summary="assistant: 请做个简单自我介绍\nuser: 我做过支付系统。",
            )
        ],
        completed_reason="turn_limit_reached",
    )

    async def _fake_post_callback(callback_url: str, payload: dict, max_attempts: int = 3):
        return None

    service._post_callback_with_retry = _fake_post_callback  # type: ignore[method-assign]

    with caplog.at_level("INFO"):
        result = await service.generate_and_callback(context, [stage_result])

    assert result["status"] == "success"
    assert not any("[Report-Pipeline]" in record.message for record in caplog.records)

    await service.aclose()
