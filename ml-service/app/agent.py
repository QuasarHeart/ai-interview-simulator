"""Official LiveKit interview runtime.

This module only keeps the thin job entrypoint and metadata parsing needed to
start the official workflow agent.
"""

from __future__ import annotations

import asyncio
import inspect
import json
import logging
import os
import time
from dataclasses import dataclass
from typing import Any
from uuid import uuid4

from dotenv import load_dotenv

from livekit import agents, rtc
from livekit.agents import AgentServer, AgentSession, room_io
import livekit.plugins.google as google

try:
    from app.official_workflow import InterviewContext, InterviewWorkflowAgent, OfficialPromptRegistry
except ModuleNotFoundError:
    from official_workflow import InterviewContext, InterviewWorkflowAgent, OfficialPromptRegistry

load_dotenv(os.getenv("ML_SERVICE_ENV_FILE", ".env.ml-service"))
logger = logging.getLogger("ml-service.agent")

STYLE_SET = {"standard", "friendly", "aggressive", "expert"}
DIFFICULTY_SET = {"easy", "medium", "hard"}
MODE_SET = {"text", "audio", "video"}


@dataclass(slots=True)
class SessionProfile:
    interviewer_style: str = "standard"
    difficulty: str = "medium"
    company_context: str = "通用科技公司文化"
    mode: str = "video"
    job_position: str = ""
    jd_summary: str = ""
    resume_content: str = ""


@dataclass(slots=True)
class ModelConfig:
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-native-audio-preview-12-2025")
    gemini_voice: str = os.getenv("GEMINI_VOICE", "Puck")
    gemini_temperature: float = float(os.getenv("GEMINI_TEMPERATURE", "0.8"))
    google_api_key: str = os.getenv("GOOGLE_API_KEY", "").strip()
    google_use_vertexai: bool = os.getenv("GOOGLE_USE_VERTEXAI", "false").strip().lower() in {"1", "true", "yes", "on"}
    google_cloud_project: str = os.getenv("GOOGLE_CLOUD_PROJECT", "").strip()
    google_cloud_location: str = os.getenv("GOOGLE_CLOUD_LOCATION", "").strip()
    interviewer_style: str = os.getenv("INTERVIEWER_STYLE", "standard")
    difficulty: str = os.getenv("INTERVIEW_DIFFICULTY", "medium")
    company_context: str = os.getenv("COMPANY_CONTEXT", "通用科技公司文化")
    interview_mode: str = os.getenv("INTERVIEW_MODE", "video")


config = ModelConfig()
server = AgentServer()


def _build_google_realtime_model(config_obj: ModelConfig) -> google.realtime.RealtimeModel:
    model_kwargs: dict[str, Any] = {
        "model": config_obj.gemini_model,
        "voice": config_obj.gemini_voice,
        "temperature": config_obj.gemini_temperature,
        
    }

    if config_obj.google_use_vertexai:
        model_kwargs["vertexai"] = True
        if config_obj.google_cloud_project:
            model_kwargs["project"] = config_obj.google_cloud_project
        if config_obj.google_cloud_location:
            model_kwargs["location"] = config_obj.google_cloud_location
    else:
        model_kwargs["api_key"] = config_obj.google_api_key

    if not config_obj.google_use_vertexai and not config_obj.google_api_key:
        raise ValueError("GOOGLE_API_KEY 未配置，或未启用 GOOGLE_USE_VERTEXAI")

    return google.realtime.RealtimeModel(**model_kwargs)


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


def _coerce_metadata_dict(raw_metadata: Any) -> dict[str, Any] | None:
    if raw_metadata is None:
        return None
    if isinstance(raw_metadata, dict):
        return dict(raw_metadata)
    if isinstance(raw_metadata, str):
        text = raw_metadata.strip()
        if not text:
            return None
        try:
            parsed = json.loads(text)
        except Exception:
            return {"_raw_metadata": text}
        if isinstance(parsed, dict):
            return parsed
        return {"_raw_metadata": text, "_raw_metadata_parsed": parsed}
    return None


def _extract_session_context(
    ctx: Any,
    config_obj: ModelConfig,
) -> tuple[SessionProfile, dict[str, Any], str]:
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

    metadata_sources: list[tuple[str, Any]] = [
        ("job.metadata", getattr(getattr(ctx, "job", None), "metadata", None)),
        ("ctx.metadata", getattr(ctx, "metadata", None)),
        ("room.metadata", getattr(room, "metadata", None)),
    ]

    metadata_dict: dict[str, Any] = {}
    metadata_source_names: list[str] = []
    for source_name, raw_metadata in metadata_sources:
        parsed_metadata = _coerce_metadata_dict(raw_metadata)
        if not parsed_metadata:
            continue
        metadata_dict.update(parsed_metadata)
        metadata_source_names.append(source_name)

    metadata_source = "+".join(metadata_source_names) if metadata_source_names else "defaults"
    if not metadata_dict:
        logger.warning("No dispatch/job/room metadata provided; interview context fields remain empty")
        return default_profile, {}, metadata_source

    interview_config = metadata_dict.get("interview_config")
    cfg_dict: dict[str, Any] = interview_config if isinstance(interview_config, dict) else metadata_dict

    incoming_session_id = str(metadata_dict.get("session_id") or cfg_dict.get("session_id") or "").strip()
    if incoming_session_id and room_session_id and incoming_session_id != room_session_id:
        logger.warning(
            "session_id mismatch: room.name=%s metadata.session_id=%s; room.name will be treated as runtime session_id",
            room_session_id,
            incoming_session_id,
        )

    return (
        SessionProfile(
            interviewer_style=_sanitize_style(cfg_dict.get("interviewer_style"), default_profile.interviewer_style),
            difficulty=_sanitize_difficulty(cfg_dict.get("difficulty"), default_profile.difficulty),
            company_context=str(cfg_dict.get("company_context") or default_profile.company_context).strip()
            or default_profile.company_context,
            mode=_sanitize_mode(cfg_dict.get("mode"), default_profile.mode),
            job_position=str(metadata_dict.get("job_position") or cfg_dict.get("job_position") or "").strip(),
            jd_summary=str(metadata_dict.get("jd_summary") or cfg_dict.get("jd_summary") or "").strip(),
            resume_content=str(metadata_dict.get("resume_content") or cfg_dict.get("resume_content") or "").strip(),
        ),
        metadata_dict,
        metadata_source,
    )


def _extract_session_profile(ctx: Any, config_obj: ModelConfig) -> SessionProfile:
    profile, _, _ = _extract_session_context(ctx, config_obj)
    return profile


def _build_room_options(session_profile: SessionProfile) -> room_io.RoomOptions:
    negotiated_video = session_profile.mode == "video"
    return room_io.RoomOptions(
        text_input=False,
        audio_input=room_io.AudioInputOptions(),
        video_input=room_io.VideoInputOptions() if negotiated_video else False,
        audio_output=room_io.AudioOutputOptions(),
        text_output=session_profile.mode == "text",
        close_on_disconnect=False,
        delete_room_on_close=True,
    )


@server.rtc_session(agent_name="ai-interview-3")
async def ai_interview_session(ctx: agents.JobContext) -> None:
    session_id = getattr(getattr(ctx, "room", None), "name", None) or str(uuid4())
    connect_fn = getattr(ctx, "connect", None)
    if callable(connect_fn):
        connect_result = connect_fn()
        if inspect.isawaitable(connect_result):
            await connect_result

    session_profile, session_metadata, metadata_source = _extract_session_context(ctx, config)
    interview_context = InterviewContext(
        session_id=session_id,
        job_position=session_profile.job_position,
        jd_summary=session_profile.jd_summary,
        resume_content=session_profile.resume_content,
        interviewer_style=session_profile.interviewer_style,
        difficulty=session_profile.difficulty,
        company_context=session_profile.company_context,
        mode=session_profile.mode,
        metadata_source=metadata_source,
    )
    prompts = OfficialPromptRegistry()
    workflow_agent = InterviewWorkflowAgent(interview_context=interview_context, prompts=prompts)

    session = AgentSession(llm=_build_google_realtime_model(config))
    room_options = _build_room_options(session_profile)

    await session.start(
        room=ctx.room,
        agent=workflow_agent,
        room_options=room_options,
    )

    logger.info(
        "official_session_started session=%s metadata_source=%s metadata_keys=%s",
        session_id,
        metadata_source,
        sorted(session_metadata.keys()) if isinstance(session_metadata, dict) else [],
    )

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


if __name__ == "__main__":
    agents.cli.run_app(server)
