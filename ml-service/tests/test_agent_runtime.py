import json
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import app.agent as agent_mod
import app.official_workflow as workflow_mod


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
