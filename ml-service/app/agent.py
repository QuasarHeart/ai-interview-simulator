"""version 2.0
Official LiveKit interview runtime.

This module only keeps the thin job entrypoint and metadata parsing needed to
start the official workflow agent.
"""

from __future__ import annotations

import asyncio
import contextlib
import inspect
import importlib
import json
import logging
import os
import time
from dataclasses import asdict, dataclass, is_dataclass
from typing import Any, cast
from uuid import uuid4

from dotenv import load_dotenv

load_dotenv(os.getenv("ML_SERVICE_ENV_FILE", ".env.ml-service"))

from livekit import agents, rtc
from livekit.agents import AgentServer, AgentSession, TurnHandlingOptions, room_io
from google.genai import types as google_types
import livekit.plugins.google as google

try:
    anam = importlib.import_module("livekit.plugins.anam")
except ModuleNotFoundError:
    anam = None

try:
    from app.official_workflow import InterviewContext, InterviewWorkflowAgent, OfficialPromptRegistry
except ModuleNotFoundError:
    from official_workflow import InterviewContext, InterviewWorkflowAgent, OfficialPromptRegistry

logger = logging.getLogger("ml-service.agent")

_OFFICIAL_TRACE_LOG_DETAIL = (
    os.getenv("INTERVIEW_TRACE_LOG_DETAIL")
    or os.getenv("OFFICIAL_TRACE_LOG_DETAIL")
    or "false"
).strip().lower() in {"1", "true", "yes", "on"}
_OFFICIAL_TRACE_LOG_MAX_CHARS = max(
    256,
    int(
        os.getenv(
            "INTERVIEW_TRACE_LOG_MAX_CHARS",
            os.getenv("OFFICIAL_TRACE_LOG_MAX_CHARS", "8000"),
        )
    ),
)

STYLE_SET = {"standard", "friendly", "aggressive", "expert"}
DIFFICULTY_SET = {"easy", "medium", "hard"}
MODE_SET = {"text", "audio", "video"}


def _get_env_text(name: str, default: str = "") -> str:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip()


def _get_optional_int_env(name: str, default: int) -> int:
    raw_value = _get_env_text(name)
    if not raw_value:
        return default
    try:
        return int(raw_value)
    except ValueError:
        logger.warning("Invalid %s=%r; using default %s", name, raw_value, default)
        return default


def _get_optional_float_env(name: str, default: float) -> float:
    raw_value = _get_env_text(name)
    if not raw_value:
        return default
    try:
        return float(raw_value)
    except ValueError:
        logger.warning("Invalid %s=%r; using default %s", name, raw_value, default)
        return default


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
class AnamAccountConfig:
    api_key: str
    avatar_id: str
    api_url: str = ""
    avatar_name: str = "avatar"
    avatar_model: str = ""


@dataclass(slots=True)
class ModelConfig:
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-native-audio-preview-12-2025")
    gemini_voice: str = os.getenv("GEMINI_VOICE", "Puck")
    gemini_temperature: float = float(os.getenv("GEMINI_TEMPERATURE", "0.8"))
    google_api_key: str = os.getenv("GOOGLE_API_KEY", "").strip()
    google_use_vertexai: bool = os.getenv("GOOGLE_USE_VERTEXAI", "false").strip().lower() in {"1", "true", "yes", "on"}
    google_cloud_project: str = os.getenv("GOOGLE_CLOUD_PROJECT", "").strip()
    google_cloud_location: str = os.getenv("GOOGLE_CLOUD_LOCATION", "").strip()
    google_enable_context_window_compression: bool = (
        os.getenv("GOOGLE_ENABLE_CONTEXT_WINDOW_COMPRESSION", "true").strip().lower() in {"1", "true", "yes", "on"}
    )
    google_enable_session_resumption: bool = (
        os.getenv("GOOGLE_ENABLE_SESSION_RESUMPTION", "true").strip().lower() in {"1", "true", "yes", "on"}
    )
    gemini_auto_activity_start_sensitivity: str = os.getenv(
        "INTERVIEW_GEMINI_AUTO_ACTIVITY_START_SENSITIVITY",
        "HIGH",
    )
    gemini_auto_activity_end_sensitivity: str = os.getenv(
        "INTERVIEW_GEMINI_AUTO_ACTIVITY_END_SENSITIVITY",
        "LOW",
    )
    gemini_auto_activity_prefix_padding_ms: int = int(
        os.getenv("INTERVIEW_GEMINI_AUTO_ACTIVITY_PREFIX_PADDING_MS", "300")
    )
    gemini_auto_activity_silence_duration_ms: int = int(
        os.getenv("INTERVIEW_GEMINI_AUTO_ACTIVITY_SILENCE_DURATION_MS", "1500")
    )
    interviewer_style: str = os.getenv("INTERVIEWER_STYLE", "standard")
    difficulty: str = os.getenv("INTERVIEW_DIFFICULTY", "medium")
    company_context: str = os.getenv("COMPANY_CONTEXT", "通用科技公司文化")
    interview_mode: str = os.getenv("INTERVIEW_MODE", "video")
    anam_api_key: str = _get_env_text("ANAM_API_KEY")
    anam_api_url: str = _get_env_text("ANAM_API_URL")
    anam_avatar_id: str = _get_env_text("ANAM_AVATAR_ID")
    anam_avatar_name: str = _get_env_text("ANAM_AVATAR_NAME", "avatar")
    anam_avatar_model: str = _get_env_text("ANAM_AVATAR_MODEL")
    anam_accounts_json: str = _get_env_text("ANAM_ACCOUNTS_JSON")
    anam_api_keys: str = _get_env_text("ANAM_API_KEYS")
    anam_avatar_ids: str = _get_env_text("ANAM_AVATAR_IDS")
    anam_api_urls: str = _get_env_text("ANAM_API_URLS")
    anam_avatar_names: str = _get_env_text("ANAM_AVATAR_NAMES")
    anam_avatar_models: str = _get_env_text("ANAM_AVATAR_MODELS")
    anam_recycle_before_timeout_seconds: float = _get_optional_float_env(
        "ANAM_RECYCLE_BEFORE_TIMEOUT_SECONDS",
        165.0,
    )
    anam_restart_backoff_seconds: float = _get_optional_float_env(
        "ANAM_RESTART_BACKOFF_SECONDS",
        5.0,
    )


config = ModelConfig()
server = AgentServer()


def _trace_value(value: Any, max_chars: int = _OFFICIAL_TRACE_LOG_MAX_CHARS) -> str:
    if value is None:
        text = "null"
    elif isinstance(value, str):
        text = value
    elif is_dataclass(value):
        text = json.dumps(asdict(cast(Any, value)), ensure_ascii=False, default=str)
    elif hasattr(value, "model_dump"):
        text = json.dumps(value.model_dump(), ensure_ascii=False, default=str)
    else:
        try:
            text = json.dumps(value, ensure_ascii=False, default=str)
        except Exception:
            try:
                text = str(value)
            except Exception:
                text = "<unserializable>"

    if max_chars > 0 and len(text) > max_chars:
        return f"{text[:max_chars]}...(truncated)"
    return text


def _trace_log(event: str, **fields: Any) -> None:
    if not _OFFICIAL_TRACE_LOG_DETAIL:
        return

    parts = [f"[Official-Trace] function=agent event={event}"]
    for key, value in fields.items():
        if callable(value):
            value = value()
        parts.append(f"{key}={_trace_value(value)}")
    logger.info(" ".join(parts))


def _build_google_realtime_model(config_obj: ModelConfig) -> google.realtime.RealtimeModel:
    _trace_log(
        "build_google_realtime_model_enter",
        model=config_obj.gemini_model,
        voice=config_obj.gemini_voice,
        temperature=config_obj.gemini_temperature,
        use_vertexai=config_obj.google_use_vertexai,
        has_api_key=bool(config_obj.google_api_key),
    )
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

    if config_obj.google_enable_context_window_compression:
        model_kwargs["context_window_compression"] = google_types.ContextWindowCompressionConfig(
            sliding_window=google_types.SlidingWindow(),
        )

    if config_obj.google_enable_session_resumption:
        model_kwargs["session_resumption"] = google_types.SessionResumptionConfig()

    # Keep Gemini's built-in activity detection conservative so short pauses do not end the user's turn too early.
    model_kwargs["realtime_input_config"] = google_types.RealtimeInputConfig(
        automatic_activity_detection=google_types.AutomaticActivityDetection(
            disabled=False,
            start_of_speech_sensitivity=_resolve_google_start_sensitivity(
                config_obj.gemini_auto_activity_start_sensitivity
            ),
            end_of_speech_sensitivity=_resolve_google_end_sensitivity(
                config_obj.gemini_auto_activity_end_sensitivity
            ),
            prefix_padding_ms=config_obj.gemini_auto_activity_prefix_padding_ms,
            silence_duration_ms=config_obj.gemini_auto_activity_silence_duration_ms,
        )
    )

    if not config_obj.google_use_vertexai and not config_obj.google_api_key:
        raise ValueError("GOOGLE_API_KEY 未配置，或未启用 GOOGLE_USE_VERTEXAI")

    _trace_log(
        "build_google_realtime_model_exit",
        model_kwargs=model_kwargs,
    )
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


def _resolve_google_start_sensitivity(value: Any) -> google_types.StartSensitivity:
    normalized = str(value or "").strip().upper()
    if normalized in {"HIGH", "START_SENSITIVITY_HIGH"}:
        return google_types.StartSensitivity.START_SENSITIVITY_HIGH
    if normalized in {"LOW", "START_SENSITIVITY_LOW"}:
        return google_types.StartSensitivity.START_SENSITIVITY_LOW
    if normalized in {"UNSPECIFIED", "START_SENSITIVITY_UNSPECIFIED", ""}:
        return google_types.StartSensitivity.START_SENSITIVITY_UNSPECIFIED

    logger.warning(
        "Invalid INTERVIEW_GEMINI_AUTO_ACTIVITY_START_SENSITIVITY=%s; falling back to START_SENSITIVITY_HIGH",
        value,
    )
    return google_types.StartSensitivity.START_SENSITIVITY_HIGH


def _resolve_google_end_sensitivity(value: Any) -> google_types.EndSensitivity:
    normalized = str(value or "").strip().upper()
    if normalized in {"HIGH", "END_SENSITIVITY_HIGH"}:
        return google_types.EndSensitivity.END_SENSITIVITY_HIGH
    if normalized in {"LOW", "END_SENSITIVITY_LOW"}:
        return google_types.EndSensitivity.END_SENSITIVITY_LOW
    if normalized in {"UNSPECIFIED", "END_SENSITIVITY_UNSPECIFIED", ""}:
        return google_types.EndSensitivity.END_SENSITIVITY_UNSPECIFIED

    logger.warning(
        "Invalid INTERVIEW_GEMINI_AUTO_ACTIVITY_END_SENSITIVITY=%s; falling back to END_SENSITIVITY_LOW",
        value,
    )
    return google_types.EndSensitivity.END_SENSITIVITY_LOW


def _coerce_metadata_dict(raw_metadata: Any) -> dict[str, Any] | None:
    _trace_log("coerce_metadata_dict_enter", raw_type=type(raw_metadata).__name__, raw_metadata=raw_metadata)
    if raw_metadata is None:
        _trace_log("coerce_metadata_dict_exit", result=None)
        return None
    if isinstance(raw_metadata, dict):
        result = dict(raw_metadata)
        _trace_log("coerce_metadata_dict_exit", result=result)
        return result
    if isinstance(raw_metadata, str):
        text = raw_metadata.strip()
        if not text:
            _trace_log("coerce_metadata_dict_exit", result=None)
            return None
        try:
            parsed = json.loads(text)
        except Exception:
            result = {"_raw_metadata": text}
            _trace_log("coerce_metadata_dict_exit", result=result)
            return result
        if isinstance(parsed, dict):
            _trace_log("coerce_metadata_dict_exit", result=parsed)
            return parsed
        result = {"_raw_metadata": text, "_raw_metadata_parsed": parsed}
        _trace_log("coerce_metadata_dict_exit", result=result)
        return result
    _trace_log("coerce_metadata_dict_exit", result=None)
    return None


def _resolve_session_id(room_name: str, metadata_session_id: str | None) -> str:
    _trace_log("resolve_session_id_enter", room_name=room_name, metadata_session_id=metadata_session_id)
    normalized_room_name = str(room_name or "").strip()
    if normalized_room_name.startswith("room_"):
        stripped_room_name = normalized_room_name.removeprefix("room_").strip()
        if stripped_room_name:
            normalized_room_name = stripped_room_name

    session_id = str(metadata_session_id or "").strip()
    if session_id:
        if normalized_room_name and session_id not in {normalized_room_name, str(room_name or "").strip()}:
            logger.warning(
                "session_id mismatch: room.name=%s metadata.session_id=%s; metadata.session_id will be treated as runtime session_id",
                room_name,
                session_id,
            )
        return session_id

    if normalized_room_name:
        _trace_log("resolve_session_id_exit", resolved_session_id=normalized_room_name, reason="room_name")
        return normalized_room_name

    room_name = str(room_name or "").strip()
    if room_name:
        _trace_log("resolve_session_id_exit", resolved_session_id=room_name, reason="raw_room_name")
        return room_name

    resolved = str(uuid4())
    _trace_log("resolve_session_id_exit", resolved_session_id=resolved, reason="generated_uuid")
    return resolved


def _extract_session_context(
    ctx: Any,
    config_obj: ModelConfig,
) -> tuple[SessionProfile, dict[str, Any], str, str]:
    _trace_log(
        "extract_session_context_enter",
        room_name=getattr(getattr(ctx, "room", None), "name", None),
        job_metadata=getattr(getattr(ctx, "job", None), "metadata", None),
        ctx_metadata=getattr(ctx, "metadata", None),
        room_metadata=getattr(getattr(ctx, "room", None), "metadata", None),
    )
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
        _trace_log(
            "extract_session_context_exit",
            metadata_source=metadata_source,
            resolved_session_id=_resolve_session_id(room_session_id, None),
            profile=default_profile,
            metadata_keys=[],
        )
        return default_profile, {}, metadata_source, _resolve_session_id(room_session_id, None)

    interview_config = metadata_dict.get("interview_config")
    cfg_dict: dict[str, Any] = interview_config if isinstance(interview_config, dict) else metadata_dict

    incoming_session_id = str(metadata_dict.get("session_id") or cfg_dict.get("session_id") or "").strip()
    resolved_session_id = _resolve_session_id(room_session_id, incoming_session_id)

    profile = SessionProfile(
        interviewer_style=_sanitize_style(cfg_dict.get("interviewer_style"), default_profile.interviewer_style),
        difficulty=_sanitize_difficulty(cfg_dict.get("difficulty"), default_profile.difficulty),
        company_context=str(cfg_dict.get("company_context") or default_profile.company_context).strip()
        or default_profile.company_context,
        mode=_sanitize_mode(cfg_dict.get("mode"), default_profile.mode),
        job_position=str(metadata_dict.get("job_position") or cfg_dict.get("job_position") or "").strip(),
        jd_summary=str(metadata_dict.get("jd_summary") or cfg_dict.get("jd_summary") or "").strip(),
        resume_content=str(metadata_dict.get("resume_content") or cfg_dict.get("resume_content") or "").strip(),
    )

    _trace_log(
        "extract_session_context_exit",
        metadata_source=metadata_source,
        resolved_session_id=resolved_session_id,
        profile=profile,
        metadata_keys=sorted(metadata_dict.keys()),
    )

    return (
        profile,
        metadata_dict,
        metadata_source,
        resolved_session_id,
    )


def _extract_session_profile(ctx: Any, config_obj: ModelConfig) -> SessionProfile:
    profile, _, _, _ = _extract_session_context(ctx, config_obj)
    return profile


def _build_room_options(session_profile: SessionProfile) -> room_io.RoomOptions:
    _trace_log("build_room_options_enter", session_profile=session_profile)
    negotiated_video = session_profile.mode == "video"
    room_options = room_io.RoomOptions(
        text_input=False,
        audio_input=room_io.AudioInputOptions(),
        video_input=room_io.VideoInputOptions() if negotiated_video else False,
        audio_output=room_io.AudioOutputOptions(),
        text_output=session_profile.mode == "text",
        close_on_disconnect=False,
        delete_room_on_close=True,
    )
    _trace_log("build_room_options_exit", room_options=room_options)
    return room_options


def _build_turn_handling_options() -> TurnHandlingOptions:
    turn_handling = TurnHandlingOptions(
        turn_detection="realtime_llm",
        endpointing={
            "min_delay": float(os.getenv("INTERVIEW_ENDPOINTING_MIN_DELAY", "4.0")),
            "max_delay": float(os.getenv("INTERVIEW_ENDPOINTING_MAX_DELAY", "6.0")),
        },
    )
    _trace_log("build_turn_handling_options_exit", turn_handling=turn_handling)
    return turn_handling


def _split_env_items(raw_value: str) -> list[str]:
    text = raw_value.strip()
    if not text:
        return []

    try:
        parsed = json.loads(text)
    except Exception:
        parsed = None

    if isinstance(parsed, list):
        return [str(item).strip() for item in parsed if str(item).strip()]

    normalized = text.replace("\n", ",").replace(";", ",")
    return [item.strip() for item in normalized.split(",") if item.strip()]


def _value_for_index(values: list[str], index: int, default: str = "") -> str:
    if not values:
        return default
    if index < len(values):
        return values[index]
    if len(values) == 1:
        return values[0]
    return default


def _resolve_anam_accounts(config_obj: ModelConfig) -> list[AnamAccountConfig]:
    accounts: list[AnamAccountConfig] = []

    raw_accounts_json = config_obj.anam_accounts_json.strip()
    if raw_accounts_json:
        try:
            parsed_accounts = json.loads(raw_accounts_json)
        except Exception:
            logger.warning("Invalid ANAM_ACCOUNTS_JSON; ignoring it", exc_info=True)
        else:
            if isinstance(parsed_accounts, list):
                for index, item in enumerate(parsed_accounts):
                    if not isinstance(item, dict):
                        logger.warning("Ignoring ANAM_ACCOUNTS_JSON entry %s because it is not an object", index)
                        continue

                    api_key = str(
                        item.get("api_key") or item.get("apiKey") or item.get("key") or ""
                    ).strip()
                    avatar_id = str(
                        item.get("avatar_id") or item.get("avatarId") or item.get("id") or ""
                    ).strip()
                    if not api_key or not avatar_id:
                        logger.warning(
                            "Ignoring ANAM_ACCOUNTS_JSON entry %s because api_key or avatar_id is missing",
                            index,
                        )
                        continue

                    accounts.append(
                        AnamAccountConfig(
                            api_key=api_key,
                            avatar_id=avatar_id,
                            api_url=str(item.get("api_url") or item.get("apiUrl") or "").strip(),
                            avatar_name=str(item.get("avatar_name") or item.get("avatarName") or item.get("name") or "avatar").strip() or "avatar",
                            avatar_model=str(item.get("avatar_model") or item.get("avatarModel") or "").strip(),
                        )
                    )
            else:
                logger.warning("ANAM_ACCOUNTS_JSON must be a JSON list; ignoring it")

    if accounts:
        return accounts

    numbered_accounts: list[AnamAccountConfig] = []
    for index in range(1, 11):
        api_key = _get_env_text(f"ANAM_ACCOUNT_{index}_API_KEY")
        avatar_id = _get_env_text(f"ANAM_ACCOUNT_{index}_AVATAR_ID")
        api_url = _get_env_text(f"ANAM_ACCOUNT_{index}_API_URL")
        avatar_name = _get_env_text(f"ANAM_ACCOUNT_{index}_AVATAR_NAME")
        avatar_model = _get_env_text(f"ANAM_ACCOUNT_{index}_AVATAR_MODEL")

        if not api_key and not avatar_id and not api_url and not avatar_name and not avatar_model:
            continue

        if not api_key or not avatar_id:
            logger.warning(
                "Skipping ANAM_ACCOUNT_%s because api_key or avatar_id is missing",
                index,
            )
            continue

        numbered_accounts.append(
            AnamAccountConfig(
                api_key=api_key,
                avatar_id=avatar_id,
                api_url=api_url,
                avatar_name=avatar_name or config_obj.anam_avatar_name or "avatar",
                avatar_model=avatar_model,
            )
        )

    if numbered_accounts:
        return numbered_accounts

    api_keys = _split_env_items(config_obj.anam_api_keys)
    avatar_ids = _split_env_items(config_obj.anam_avatar_ids)
    api_urls = _split_env_items(config_obj.anam_api_urls)
    avatar_names = _split_env_items(config_obj.anam_avatar_names)
    avatar_models = _split_env_items(config_obj.anam_avatar_models)

    explicit_account_count = max(
        len(api_keys),
        len(avatar_ids),
        len(api_urls),
        len(avatar_names),
        len(avatar_models),
    )
    for index in range(explicit_account_count):
        api_key = _value_for_index(api_keys, index)
        avatar_id = _value_for_index(avatar_ids, index)
        if not api_key or not avatar_id:
            logger.warning(
                "Skipping Anam account %s because api_key or avatar_id is missing",
                index + 1,
            )
            continue

        accounts.append(
            AnamAccountConfig(
                api_key=api_key,
                avatar_id=avatar_id,
                api_url=_value_for_index(api_urls, index),
                avatar_name=_value_for_index(avatar_names, index, config_obj.anam_avatar_name or "avatar") or "avatar",
                avatar_model=_value_for_index(avatar_models, index, config_obj.anam_avatar_model),
            )
        )

    if accounts:
        return accounts

    if not config_obj.anam_api_key or not config_obj.anam_avatar_id:
        return []

    return [
        AnamAccountConfig(
            api_key=config_obj.anam_api_key,
            avatar_id=config_obj.anam_avatar_id,
            api_url=config_obj.anam_api_url,
            avatar_name=config_obj.anam_avatar_name or "avatar",
            avatar_model=config_obj.anam_avatar_model,
        )
    ]


def _build_anam_avatar_session_for_account(
    config_obj: ModelConfig,
    session_profile: SessionProfile,
    account: AnamAccountConfig,
) -> Any:
    if anam is None:
        raise RuntimeError(
            "Anam avatar requested, but livekit-agents[anam] is not installed. "
            "Install livekit-agents[images,anam]~=1.5 to enable video avatars."
        )

    api_url = account.api_url.strip() or config_obj.anam_api_url.strip()
    if not api_url:
        api_url = getattr(anam, "DEFAULT_API_URL", "https://api.anam.ai")

    persona_config_kwargs: dict[str, Any] = {
        "name": account.avatar_name or config_obj.anam_avatar_name or "avatar",
        "avatarId": account.avatar_id,
    }
    avatar_model = account.avatar_model.strip() or config_obj.anam_avatar_model.strip()
    if avatar_model:
        persona_config_kwargs["avatarModel"] = avatar_model

    avatar_kwargs: dict[str, Any] = {
        "persona_config": anam.PersonaConfig(**persona_config_kwargs),
        "api_key": account.api_key,
        "api_url": api_url,
    }

    return anam.AvatarSession(**avatar_kwargs)


def _build_anam_avatar_session(config_obj: ModelConfig, session_profile: SessionProfile) -> Any | None:
    if session_profile.mode != "video":
        return None

    accounts = _resolve_anam_accounts(config_obj)
    if not accounts:
        logger.info(
            "Video mode is enabled but no Anam accounts are configured; continuing without digital avatar"
        )
        return None

    return _build_anam_avatar_session_for_account(config_obj, session_profile, accounts[0])


class AnamAvatarManager:
    def __init__(
        self,
        *,
        config_obj: ModelConfig,
        session_profile: SessionProfile,
        session: AgentSession,
        room: rtc.Room,
    ) -> None:
        self._config = config_obj
        self._session_profile = session_profile
        self._session = session
        self._room = room
        self._accounts = _resolve_anam_accounts(config_obj)
        self._current_avatar_session: Any | None = None
        self._current_account_index = -1
        self._next_account_index = 0
        self._closed = False
        self._rotating = False
        self._switch_lock = asyncio.Lock()
        self._rotation_task: asyncio.Task[None] | None = None
        self._recycle_task: asyncio.Task[None] | None = None
        self._retry_task: asyncio.Task[None] | None = None

    async def start(self) -> None:
        if self._session_profile.mode != "video":
            return

        if not self._accounts:
            logger.info(
                "Video mode is enabled but no Anam accounts are configured; continuing without digital avatar"
            )
            return

        if anam is None:
            raise RuntimeError(
                "Anam avatar requested, but livekit-agents[anam] is not installed. "
                "Install livekit-agents[images,anam]~=1.5 to enable video avatars."
            )

        self._room.on("participant_disconnected", self._on_participant_disconnected)
        await self._rotate_avatar("initial avatar start")

    async def aclose(self) -> None:
        self._closed = True
        self._room.off("participant_disconnected", self._on_participant_disconnected)
        await self._cancel_task("_rotation_task")
        await self._cancel_task("_recycle_task")
        await self._cancel_task("_retry_task")

        async with self._switch_lock:
            self._rotating = True
            try:
                await self._close_current_avatar_session()
            finally:
                self._rotating = False

    def _on_participant_disconnected(self, participant: rtc.RemoteParticipant) -> None:
        if self._closed or self._rotating:
            return

        current_identity = getattr(self._current_avatar_session, "avatar_identity", None)
        if not current_identity or participant.identity != current_identity:
            return

        logger.info(
            "Anam avatar participant disconnected; switching to another account",
            extra={"participant": participant.identity, "room": self._room.name},
        )
        self.request_rotation("avatar participant disconnected")

    def request_rotation(self, reason: str) -> None:
        if self._closed:
            return
        if self._rotation_task is not None and not self._rotation_task.done():
            return
        self._rotation_task = asyncio.create_task(self._rotate_avatar(reason), name="anam_avatar_rotate")

    async def _cancel_task(self, attr_name: str) -> None:
        task = getattr(self, attr_name)
        if task is None:
            return
        setattr(self, attr_name, None)
        task.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await task

    async def _close_current_avatar_session(self) -> None:
        avatar_session = self._current_avatar_session
        self._current_avatar_session = None
        if avatar_session is None:
            return

        with contextlib.suppress(Exception):
            await avatar_session.aclose()

    async def _rotate_avatar(self, reason: str) -> None:
        async with self._switch_lock:
            if self._closed:
                return

            self._rotating = True
            try:
                await self._cancel_task("_recycle_task")
                await self._cancel_task("_retry_task")
                await self._close_current_avatar_session()

                if self._closed or not self._accounts:
                    return

                if await self._start_next_available_avatar(reason):
                    self._schedule_recycle_task()
                else:
                    self._schedule_retry_task(reason)
            finally:
                self._rotating = False
                self._rotation_task = None

    async def _start_next_available_avatar(self, reason: str) -> bool:
        if self._closed or not self._accounts:
            return False

        account_count = len(self._accounts)
        start_index = self._next_account_index % account_count
        last_error: Exception | None = None

        for offset in range(account_count):
            account_index = (start_index + offset) % account_count
            account = self._accounts[account_index]
            avatar_session = _build_anam_avatar_session_for_account(self._config, self._session_profile, account)
            try:
                await avatar_session.start(self._session, room=self._room)
            except Exception as exc:
                last_error = exc
                logger.exception(
                    "Anam avatar start failed; trying the next account",
                    extra={
                        "reason": reason,
                        "account_index": account_index,
                        "avatar_name": account.avatar_name,
                    },
                )
                with contextlib.suppress(Exception):
                    await avatar_session.aclose()
                self._next_account_index = (account_index + 1) % account_count
                continue

            self._current_avatar_session = avatar_session
            self._current_account_index = account_index
            self._next_account_index = (account_index + 1) % account_count
            logger.info(
                "Anam avatar session started",
                extra={
                    "reason": reason,
                    "account_index": account_index,
                    "avatar_name": account.avatar_name,
                    "room": self._room.name,
                },
            )
            return True

        if last_error is not None:
            logger.error(
                "All configured Anam accounts failed; the interview will continue without a digital avatar",
                extra={"reason": reason, "room": self._room.name},
            )
        return False

    def _schedule_recycle_task(self) -> None:
        if self._closed:
            return
        recycle_after_seconds = max(0.0, float(self._config.anam_recycle_before_timeout_seconds))
        if recycle_after_seconds <= 0:
            return

        self._recycle_task = asyncio.create_task(
            self._recycle_after_delay(recycle_after_seconds),
            name="anam_avatar_recycle",
        )

    async def _recycle_after_delay(self, recycle_after_seconds: float) -> None:
        try:
            await asyncio.sleep(recycle_after_seconds)
        except asyncio.CancelledError:
            return
        finally:
            self._recycle_task = None

        if self._closed:
            return

        self.request_rotation("scheduled recycle before timeout")

    def _schedule_retry_task(self, reason: str) -> None:
        if self._closed:
            return

        retry_after_seconds = max(0.0, float(self._config.anam_restart_backoff_seconds))
        if retry_after_seconds <= 0:
            return

        self._retry_task = asyncio.create_task(
            self._retry_after_delay(reason, retry_after_seconds),
            name="anam_avatar_retry",
        )

    async def _retry_after_delay(self, reason: str, retry_after_seconds: float) -> None:
        try:
            await asyncio.sleep(retry_after_seconds)
        except asyncio.CancelledError:
            return
        finally:
            self._retry_task = None

        if self._closed:
            return

        self.request_rotation(reason)


@server.rtc_session(agent_name="ai-interview-3")
async def ai_interview_session(ctx: agents.JobContext) -> None:
    _trace_log(
        "ai_interview_session_enter",
        room_name=getattr(getattr(ctx, "room", None), "name", None),
        room_metadata=getattr(getattr(ctx, "room", None), "metadata", None),
        job_metadata=getattr(getattr(ctx, "job", None), "metadata", None),
    )
    connect_fn = getattr(ctx, "connect", None)
    if callable(connect_fn):
        _trace_log("ai_interview_session_connect_enter")
        connect_result = connect_fn()
        if inspect.isawaitable(connect_result):
            await connect_result
        _trace_log("ai_interview_session_connect_exit")

    session_profile, session_metadata, metadata_source, session_id = _extract_session_context(ctx, config)
    _trace_log(
        "ai_interview_session_context_ready",
        session_id=session_id,
        metadata_source=metadata_source,
        session_profile=session_profile,
        metadata_keys=sorted(session_metadata.keys()) if isinstance(session_metadata, dict) else [],
    )
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

    session = AgentSession(
        llm=_build_google_realtime_model(config),
        turn_handling=_build_turn_handling_options(),
        preemptive_generation=False,
        min_consecutive_speech_delay=float(os.getenv("INTERVIEW_MIN_CONSECUTIVE_SPEECH_DELAY", "4.0")),
    )
    room_options = _build_room_options(session_profile)

    avatar_manager = AnamAvatarManager(
        config_obj=config,
        session_profile=session_profile,
        session=session,
        room=ctx.room,
    )
    add_shutdown_callback = getattr(ctx, "add_shutdown_callback", None)
    if callable(add_shutdown_callback):
        add_shutdown_callback(avatar_manager.aclose)

    _trace_log("ai_interview_session_avatar_start_enter", session_id=session_id, provider="anam")
    try:
        await avatar_manager.start()
    except Exception:
        logger.exception("Anam avatar manager failed to start; continuing without digital avatar")
    else:
        _trace_log("ai_interview_session_avatar_start_exit", session_id=session_id, provider="anam")

    _trace_log("ai_interview_session_before_start", room_options=room_options, interview_context=interview_context)

    try:
        await session.start(
            room=ctx.room,
            agent=workflow_agent,
            room_options=room_options,
        )
    except Exception:
        with contextlib.suppress(Exception):
            await avatar_manager.aclose()
        raise

    _trace_log("ai_interview_session_started", session_id=session_id, room_options=room_options)

    logger.info(
        "official_session_started session=%s metadata_source=%s metadata_keys=%s",
        session_id,
        metadata_source,
        sorted(session_metadata.keys()) if isinstance(session_metadata, dict) else [],
    )

    wait_for_shutdown = getattr(ctx, "wait_for_shutdown", None)
    shutdown_event = getattr(ctx, "shutdown_event", None)

    if callable(wait_for_shutdown):
        _trace_log("ai_interview_session_wait_for_shutdown_enter", session_id=session_id)
        result = wait_for_shutdown()
        if inspect.isawaitable(result):
            await result
        _trace_log("ai_interview_session_wait_for_shutdown_exit", session_id=session_id)
    elif shutdown_event is not None and hasattr(shutdown_event, "wait"):
        _trace_log("ai_interview_session_shutdown_event_wait_enter", session_id=session_id)
        await shutdown_event.wait()
        _trace_log("ai_interview_session_shutdown_event_wait_exit", session_id=session_id)
    else:
        _trace_log("ai_interview_session_fallback_sleep_loop_enter", session_id=session_id)
        while True:
            await asyncio.sleep(1.0)


if __name__ == "__main__":
    agents.cli.run_app(server)
