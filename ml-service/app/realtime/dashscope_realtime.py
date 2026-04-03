"""DashScope Qwen-Omni realtime adapter for LiveKit AgentSession.

This module keeps all protocol translation outside the business runtime.
It intentionally avoids depending on DashScope's Python SDK so the LiveKit
runtime can speak the raw websocket protocol directly.
"""

from __future__ import annotations

import asyncio
import base64
import json
import time
from dataclasses import dataclass
from uuid import uuid4
from typing import Any

import aiohttp

from livekit import rtc
from livekit.agents import NOT_GIVEN, llm
from livekit.agents import utils as lk_utils
from livekit.agents.utils.images import EncodeOptions, ResizeOptions, encode
from livekit.plugins.openai.realtime.realtime_model import RealtimeModel as OpenAIRealtimeModel
from livekit.plugins.openai.realtime.realtime_model import RealtimeSession as OpenAIRealtimeSession


_DASHSCOPE_EVENT_TYPE_MAP: dict[str, str] = {
    "response.text.delta": "response.output_text.delta",
    "response.text.done": "response.output_text.done",
    "response.audio.delta": "response.output_audio.delta",
    "response.audio.done": "response.output_audio.done",
    "response.audio_transcript.delta": "response.output_audio_transcript.delta",
    "conversation.item.created": "conversation.item.added",
}


def _normalize_realtime_voice(voice: str | None) -> str:
    normalized = str(voice or "").strip()
    if not normalized:
        return "Cherry"
    if normalized.lower() == "tina":
        return "Cherry"
    return normalized


def normalize_dashscope_realtime_event(event: Any) -> dict[str, Any]:
    if isinstance(event, dict):
        normalized = dict(event)
        event_type = str(normalized.get("type") or normalized.get("event") or "").strip()
        normalized["type"] = _DASHSCOPE_EVENT_TYPE_MAP.get(event_type, event_type or "unknown")
        return normalized

    return {"type": "unknown", "payload": event}


@dataclass(slots=True)
class _NormalizedWSMessage:
    type: Any
    data: str
    extra: Any = None


class _DashScopeWebSocketProxy:
    def __init__(self, ws_conn: aiohttp.ClientWebSocketResponse) -> None:
        self._ws_conn = ws_conn

    async def receive(self) -> Any:
        msg = await self._ws_conn.receive()
        if msg.type != aiohttp.WSMsgType.TEXT:
            return msg

        try:
            payload = json.loads(msg.data)
        except Exception:
            return msg

        normalized = normalize_dashscope_realtime_event(payload)
        return _NormalizedWSMessage(
            type=aiohttp.WSMsgType.TEXT,
            data=json.dumps(normalized, ensure_ascii=False),
            extra=getattr(msg, "extra", None),
        )

    async def send_str(self, data: str) -> Any:
        return await self._ws_conn.send_str(data)

    async def close(self) -> Any:
        return await self._ws_conn.close()

    def __getattr__(self, name: str) -> Any:
        return getattr(self._ws_conn, name)


class DashScopeRealtimeSession(OpenAIRealtimeSession):
    def __init__(self, realtime_model: OpenAIRealtimeModel) -> None:
        self._chat_ctx = llm.ChatContext.empty()
        self._video_last_sent_at = 0.0
        self._video_min_interval_sec = 1.0
        self._audio_started = False
        self._tool_choice: Any = None
        super().__init__(realtime_model)

    @property
    def chat_ctx(self) -> llm.ChatContext:
        return self._chat_ctx.copy()

    @property
    def tools(self) -> llm.ToolContext:
        return self._tools.copy()

    def _build_session_update_payload(self, *, instructions: str | None = None) -> dict[str, Any]:
        opts = self._realtime_model._opts
        turn_detection = {
            "type": "server_vad",
            "threshold": 0.2,
            "prefix_padding_ms": 300,
            "silence_duration_ms": 800,
        }

        session: dict[str, Any] = {
            "modalities": list(opts.modalities),
            "voice": opts.voice,
            "input_audio_format": "pcm16",
            "output_audio_format": "pcm16",
            "input_audio_transcription": {"model": "gummy-realtime-v1"},
            "turn_detection": turn_detection,
        }

        if instructions is not None:
            session["instructions"] = instructions
        elif self._instructions is not None:
            session["instructions"] = self._instructions

        return {
            "type": "session.update",
            "event_id": uuid4().hex,
            "session": session,
        }

    async def _create_ws_conn(self) -> Any:
        ws_conn = await super()._create_ws_conn()
        return _DashScopeWebSocketProxy(ws_conn)

    def _create_session_update_event(self) -> dict[str, Any]:
        return self._build_session_update_payload()

    async def update_instructions(self, instructions: str) -> None:
        self._instructions = instructions
        self.send_event(self._build_session_update_payload(instructions=instructions))

    async def update_chat_ctx(self, chat_ctx: llm.ChatContext) -> None:
        async with self._update_chat_ctx_lock:
            self._chat_ctx = chat_ctx.copy(
                exclude_handoff=True,
                exclude_config_update=True,
            )

    async def update_tools(self, tools: list[llm.Tool]) -> None:
        # DashScope realtime client events documented so far do not expose a tool schema.
        # Keep the local tool context in sync and avoid sending unsupported websocket events.
        self._tools = llm.ToolContext([tool for tool in tools])

    def update_options(self, *, tool_choice: llm.ToolChoice | None = None) -> None:
        self._tool_choice = tool_choice

    def push_audio(self, frame: rtc.AudioFrame) -> None:
        for f in self._resample_audio(frame):
            data = f.data.tobytes()
            for nf in self._bstream.write(data):
                self._audio_started = True
                self.send_event(
                    {
                        "type": "input_audio_buffer.append",
                        "event_id": uuid4().hex,
                        "audio": base64.b64encode(nf.data).decode("utf-8"),
                    }
                )
                self._pushed_duration_s += nf.duration

    def push_video(self, frame: rtc.VideoFrame) -> None:
        if not self._audio_started:
            return

        now = time.monotonic()
        if (now - self._video_last_sent_at) < self._video_min_interval_sec:
            return

        image_bytes = encode(
            frame,
            EncodeOptions(
                format="JPEG",
                resize_options=ResizeOptions(
                    width=640,
                    height=640,
                    strategy="scale_aspect_fit",
                ),
                quality=75,
            ),
        )
        self.send_event(
            {
                "type": "input_image_buffer.append",
                "event_id": uuid4().hex,
                "image": base64.b64encode(image_bytes).decode("utf-8"),
            }
        )
        self._video_last_sent_at = now

    def commit_audio(self) -> None:
        if self._pushed_duration_s > 0.1:
            self.send_event({"type": "input_audio_buffer.commit", "event_id": uuid4().hex})
            self._pushed_duration_s = 0

    def clear_audio(self) -> None:
        self.send_event({"type": "input_audio_buffer.clear", "event_id": uuid4().hex})

    def interrupt(self) -> None:
        if not self.has_active_generation:
            return
        self.send_event({"type": "response.cancel", "event_id": uuid4().hex})

    def generate_reply(
        self, *, instructions: llm.NotGivenOr[str] = NOT_GIVEN
    ) -> asyncio.Future[llm.GenerationCreatedEvent]:
        event_id = uuid4().hex
        fut = asyncio.Future[llm.GenerationCreatedEvent]()
        self._response_created_futures[event_id] = fut

        if lk_utils.is_given(instructions):
            self._instructions = instructions
            self.send_event(self._build_session_update_payload(instructions=instructions))

        self.send_event(
            {
                "type": "response.create",
                "event_id": event_id,
                "response": {
                    "instructions": instructions if lk_utils.is_given(instructions) else self._instructions,
                    "modalities": list(self._realtime_model._opts.modalities),
                },
            }
        )

        def _on_timeout() -> None:
            self._response_created_futures.pop(event_id, None)
            if fut and not fut.done():
                fut.set_exception(llm.RealtimeError("generate_reply timed out."))

        handle = asyncio.get_event_loop().call_later(10.0, _on_timeout)
        fut.add_done_callback(lambda _: handle.cancel())
        return fut

    def truncate(
        self,
        *,
        message_id: str,
        modalities: list[str],
        audio_end_ms: int,
        audio_transcript: llm.NotGivenOr[str] = NOT_GIVEN,
    ) -> None:
        # DashScope's documented client events do not expose conversation item truncation.
        # Keep the local chat context consistent so the higher-level session state stays sane.
        if "audio" in modalities:
            return

        if lk_utils.is_given(audio_transcript):
            chat_ctx = self._chat_ctx.copy(
                exclude_handoff=True,
                exclude_config_update=True,
            )
            if (idx := chat_ctx.index_by_id(message_id)) is not None:
                new_item = chat_ctx.items[idx].model_copy(deep=True)
                if getattr(new_item, "type", None) == "message":
                    new_item.content = [audio_transcript]
                    chat_ctx.items[idx] = new_item
                    self._chat_ctx = chat_ctx

    def _handle_response_created(self, event: Any) -> None:
        if (
            getattr(event, "response", None) is not None
            and getattr(event.response, "metadata", None) is None
            and self._response_created_futures
        ):
            pending_event_id = next(iter(self._response_created_futures))
            event.response.metadata = {"client_event_id": pending_event_id}
        super()._handle_response_created(event)


class DashScopeRealtimeModel(OpenAIRealtimeModel):
    def session(self) -> DashScopeRealtimeSession:
        sess = DashScopeRealtimeSession(self)
        self._sessions.add(sess)
        return sess


def build_dashscope_realtime_model(config_obj: Any) -> DashScopeRealtimeModel:
    realtime_base_url = str(config_obj.realtime_base_url or "").strip()
    if realtime_base_url.endswith("/api-ws/v1/inference"):
        realtime_base_url = realtime_base_url[: -len("/inference")] + "/realtime"

    voice = _normalize_realtime_voice(getattr(config_obj, "realtime_voice", None))

    return DashScopeRealtimeModel(
        model=config_obj.realtime_model,
        voice=voice,
        base_url=realtime_base_url or "wss://dashscope.aliyuncs.com/api-ws/v1/realtime",
        api_key=config_obj.realtime_api_key,
    )
