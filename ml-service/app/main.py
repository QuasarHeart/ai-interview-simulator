import sys
import io
import traceback
import uvicorn
import json
import asyncio
import logging
import os
import json_repair
import httpx
from contextlib import asynccontextmanager
from typing import Any
from urllib.parse import quote

# 强制标准输出为 utf-8，避免 ascii 编码报错
try:
    stdout_reconfigure = getattr(sys.stdout, "reconfigure", None)
    stderr_reconfigure = getattr(sys.stderr, "reconfigure", None)
    if callable(stdout_reconfigure):
        stdout_reconfigure(encoding="utf-8")
    if callable(stderr_reconfigure):
        stderr_reconfigure(encoding="utf-8")
except Exception:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

from fastapi import FastAPI, BackgroundTasks, HTTPException, Request
from fastapi.responses import StreamingResponse

from app.schemas.schemas import StartRequest, FollowupRequest, AnalysisRequest, ReportRequest
from app.LLM_engine.engine import LLMEngine

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("ml-service.api")

REPORT_CALLBACK_URL_TEMPLATE = os.getenv(
    "REPORT_CALLBACK_URL_TEMPLATE",
    "https://nas.feixingxr.com/api/v1/interviews/{interviewId}/report-callback",
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("初始化 LLMEngine")
    engine = LLMEngine()
    app.state.engine = engine
    try:
        yield
    finally:
        logger.info("关闭 LLMEngine")
        await engine.aclose()


app = FastAPI(title="AI 面试官 ML-Service API", lifespan=lifespan)


def get_engine(request: Request) -> LLMEngine:
    return request.app.state.engine


def _sse_event(payload: dict, ensure_ascii: bool = False) -> str:
    return f"data: {json.dumps(payload, ensure_ascii=ensure_ascii)}\n\n"


def _try_parse_json_dict(raw: str) -> dict | None:
    if not raw.strip():
        return None
    try:
        parsed: Any = json_repair.loads(raw)
        if isinstance(parsed, tuple):
            parsed = parsed[0]
        if isinstance(parsed, dict):
            return parsed
        return None
    except Exception:
        return None


def _normalize_flow_control(value: Any, default_target_stage: str) -> dict:
    fallback = {
        "stage_transition": "continue",
        "target_stage": default_target_stage,
    }
    if not isinstance(value, dict):
        return fallback
    stage_transition = value.get("stage_transition")
    target_stage = value.get("target_stage")
    if stage_transition not in {"continue", "switch", "end"}:
        return fallback
    if target_stage not in {"intro", "resume_deep_dive", "tech_general", "tech_scenario", "reverse_qa", "end"}:
        return fallback
    return {
        "stage_transition": stage_transition,
        "target_stage": target_stage,
    }


def _resolve_report_callback_url(session_id: str) -> str:
    safe_interview_id = quote(session_id, safe="")
    template = REPORT_CALLBACK_URL_TEMPLATE.strip()
    if "{interviewId}" in template:
        return template.replace("{interviewId}", safe_interview_id)
    return template


# ========= 公共：按块发送 token（减少事件数量） =========
async def _yield_text_in_chunks(text: str, field: str, chunk_size: int = 12):
    buf = []
    for ch in text:
        buf.append(ch)
        if len(buf) >= chunk_size:
            part = "".join(buf)
            yield f"data: {json.dumps({'type': 'token', 'field': field, 'content': part}, ensure_ascii=False)}\n\n"
            buf = []
    if buf:
        part = "".join(buf)
        yield f"data: {json.dumps({'type': 'token', 'field': field, 'content': part}, ensure_ascii=False)}\n\n"


# ==========================================
# 接口 1：生成首轮面试问题（同步）
# ==========================================
@app.post("/api/v1/interview/start")
async def start_interview(request: StartRequest, http_request: Request):
    logger.info("[Start] session=%s job=%s", request.session_id, request.job_position)
    try:
        engine = get_engine(http_request)
        ai_result = await engine.generate_first_question(request)
        return {
            "code": 200,
            "message": "success",
            "data": {
                "session_id": request.session_id,
                "round_id": 1,
                "question": ai_result["question"],
                "flow_control": ai_result["flow_control"],
            },
        }
    except Exception as e:
        logger.exception("[Start][Error] session=%s", request.session_id)
        raise HTTPException(status_code=500, detail=f"start接口调用失败: {str(e)}")


# ==========================================
# 接口 1-Stream：首轮问题流式（只给用户展示 question）
# ==========================================
@app.post("/api/v1/interview/start/stream")
async def start_interview_stream(request: StartRequest, http_request: Request):
    logger.info("[Start-Stream] session=%s job=%s", request.session_id, request.job_position)
    engine = get_engine(http_request)

    async def event_gen():
        raw_acc = ""
        emitted_question = ""
        try:
            async for token in engine.stream_first_question(request):
                raw_acc += token

                parsed_partial = _try_parse_json_dict(raw_acc)
                if not parsed_partial:
                    continue

                question = str(parsed_partial.get("question", ""))
                if question.startswith(emitted_question) and len(question) > len(emitted_question):
                    delta = question[len(emitted_question):]
                    emitted_question = question
                    async for evt in _yield_text_in_chunks(delta, "question", chunk_size=12):
                        yield evt

            parsed_raw = json_repair.loads(raw_acc)
            if not isinstance(parsed_raw, dict):
                raise ValueError(f"LLM返回不是JSON对象: {type(parsed_raw).__name__}")
            parsed: dict = parsed_raw

            question = str(parsed.get("question", ""))
            if question.startswith(emitted_question) and len(question) > len(emitted_question):
                delta = question[len(emitted_question):]
                async for evt in _yield_text_in_chunks(delta, "question", chunk_size=12):
                    yield evt

            flow_control_raw = parsed.get("flow_control", {"stage_transition": "continue", "target_stage": "intro"})
            flow_control = _normalize_flow_control(flow_control_raw, default_target_stage="intro")

            # 非展示字段末尾一次性给后端
            yield _sse_event({'type': 'meta', 'session_id': request.session_id, 'round_id': 1, 'flow_control': flow_control}, ensure_ascii=False)
            yield _sse_event({'type': 'done'}, ensure_ascii=False)

        except Exception:
            err_trace = traceback.format_exc()
            logger.error("[START_STREAM_ERROR_TRACE] %s", err_trace)
            yield _sse_event({'type': 'error', 'message': 'start stream failed, check server log'}, ensure_ascii=True)
            yield _sse_event({'type': 'done'}, ensure_ascii=True)

    return StreamingResponse(
        event_gen(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


# ==========================================
# 接口 2：生成追问问题（同步）
# ==========================================
@app.post("/api/v1/interview/followup")
async def followup_interview(request: FollowupRequest, http_request: Request):
    logger.info("[Followup] session=%s round=%s", request.session_id, request.round_id)
    try:
        engine = get_engine(http_request)
        ai_result = await engine.generate_following_question(request)

        return {
            "code": 200,
            "message": "success",
            "data": {
                "session_id": request.session_id,
                "round_id": request.round_id,
                "question": ai_result["question"],
                "updated_history_summary": ai_result["updated_history_summary"],
                "immediate_feedback": ai_result["immediate_feedback"],
                "flow_control": ai_result["flow_control"],
            },
        }
    except Exception as e:
        logger.exception("[Followup][Error] session=%s round=%s", request.session_id, request.round_id)
        raise HTTPException(status_code=500, detail=f"followup接口调用失败: {str(e)}")


# ==========================================
# 接口 2-Stream：追问流式（展示 question + immediate_feedback）
# ==========================================
@app.post("/api/v1/interview/followup/stream")
async def followup_interview_stream(request: FollowupRequest, http_request: Request):
    logger.info("[Followup-Stream] session=%s round=%s", request.session_id, request.round_id)
    engine = get_engine(http_request)

    if request.history_data.recent_history:
        default_target_stage = request.history_data.recent_history[-1].flow_control.target_stage
    else:
        default_target_stage = "intro"

    async def event_gen():
        raw_acc = ""
        emitted_question = ""
        emitted_feedback = ""
        try:
            async for token in engine.stream_following_question(request):
                raw_acc += token

                parsed_partial = _try_parse_json_dict(raw_acc)
                if not parsed_partial:
                    continue

                question = str(parsed_partial.get("question", ""))
                if question.startswith(emitted_question) and len(question) > len(emitted_question):
                    delta = question[len(emitted_question):]
                    emitted_question = question
                    async for evt in _yield_text_in_chunks(delta, "question", chunk_size=12):
                        yield evt

                immediate_feedback = str(parsed_partial.get("immediate_feedback", ""))
                if immediate_feedback.startswith(emitted_feedback) and len(immediate_feedback) > len(emitted_feedback):
                    delta = immediate_feedback[len(emitted_feedback):]
                    emitted_feedback = immediate_feedback
                    async for evt in _yield_text_in_chunks(delta, "immediate_feedback", chunk_size=12):
                        yield evt

            parsed_raw = json_repair.loads(raw_acc)
            if not isinstance(parsed_raw, dict):
                raise ValueError(f"LLM返回不是JSON对象: {type(parsed_raw).__name__}")
            parsed: dict = parsed_raw

            question = str(parsed.get("question", ""))
            immediate_feedback = str(parsed.get("immediate_feedback", ""))
            updated_history_summary = str(parsed.get("updated_history_summary", ""))

            if question.startswith(emitted_question) and len(question) > len(emitted_question):
                delta = question[len(emitted_question):]
                async for evt in _yield_text_in_chunks(delta, "question", chunk_size=12):
                    yield evt
            if immediate_feedback.startswith(emitted_feedback) and len(immediate_feedback) > len(emitted_feedback):
                delta = immediate_feedback[len(emitted_feedback):]
                async for evt in _yield_text_in_chunks(delta, "immediate_feedback", chunk_size=12):
                    yield evt

            flow_control_raw = parsed.get("flow_control", {"stage_transition": "continue", "target_stage": default_target_stage})
            flow_control = _normalize_flow_control(flow_control_raw, default_target_stage=default_target_stage)

            # 非展示字段一次性返回
            yield _sse_event({'type': 'meta', 'session_id': request.session_id, 'round_id': request.round_id, 'updated_history_summary': updated_history_summary, 'flow_control': flow_control}, ensure_ascii=False)
            yield _sse_event({'type': 'done'}, ensure_ascii=False)

        except Exception:
            err_trace = traceback.format_exc()
            logger.error("[FOLLOWUP_STREAM_ERROR_TRACE] %s", err_trace)
            yield _sse_event({'type': 'error', 'message': 'followup stream failed, check server log'}, ensure_ascii=True)
            yield _sse_event({'type': 'done'}, ensure_ascii=True)

    return StreamingResponse(
        event_gen(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


# ==========================================
# 接口 3：回答综合分析（同步）
# ==========================================
@app.post("/api/v1/interview/analysis")
async def analyze_answer(request: AnalysisRequest, http_request: Request):
    logger.info("[Analysis] session=%s", request.session_id)
    try:
        engine = get_engine(http_request)
        ai_result = await engine.analyze_answer(request)

        if "dimension_details" in ai_result:
            professional = ai_result["dimension_details"]["professional"]
            cognition = ai_result["dimension_details"]["cognition"]
            expression = ai_result["dimension_details"]["expression"]
        else:
            professional = ai_result.get("professional", {})
            cognition = ai_result.get("cognition", {})
            expression = ai_result.get("expression", {})

        return {
            "code": 200,
            "message": "success",
            "data": {
                "session_id": request.session_id,
                "round_id": request.round_id,
                "question": request.content_to_analyze.question,
                "user_answer": request.content_to_analyze.user_answer,
                "analysis": {
                    "professional": professional,
                    "cognition": cognition,
                    "expression": expression,
                    "dimension_scores": ai_result.get("dimension_scores", {}),
                    "final_score": ai_result.get("final_score", 0),
                    "overall_feedback": ai_result.get("overall_feedback", ""),
                    "improvement_suggestions": ai_result.get("improvement_suggestions", []),
                },
            },
        }
    except Exception as e:
        logger.exception("[Analysis][Error] session=%s", request.session_id)
        raise HTTPException(status_code=500, detail=f"analysis接口调用失败: {str(e)}")


async def _post_callback_with_retry(callback_url: str, payload: dict, max_attempts: int = 3) -> None:
    timeout = httpx.Timeout(connect=5.0, read=20.0, write=10.0, pool=5.0)
    async with httpx.AsyncClient(timeout=timeout) as client:
        for attempt in range(1, max_attempts + 1):
            try:
                resp = await client.post(callback_url, json=payload)
                if 200 <= resp.status_code < 300:
                    logger.info("[Callback] 成功: url=%s status=%s", callback_url, resp.status_code)
                    return
                raise RuntimeError(f"callback status={resp.status_code}, body={resp.text[:300]}")
            except Exception as exc:
                if attempt >= max_attempts:
                    raise RuntimeError(f"回调失败，已重试 {max_attempts} 次: {exc}") from exc
                sleep_seconds = 2 ** (attempt - 1)
                logger.warning("[Callback] 失败重试: attempt=%s/%s sleep=%ss error=%s", attempt, max_attempts, sleep_seconds, str(exc))
                await asyncio.sleep(sleep_seconds)


async def _async_generate_report_and_callback(engine: LLMEngine, request: ReportRequest) -> None:
    logger.info("[Report-Task] start session=%s", request.session_id)
    callback_url = _resolve_report_callback_url(request.session_id)
    logger.info("[Report-Task] callback_url=%s", callback_url)
    try:
        report_payload = await engine.generate_overall_report(request)
        callback_payload = {
            "code": 200,
            "message": "report_generated",
            "data": {
                "session_id": request.session_id,
                "status": "completed",
                "report": report_payload,
            },
        }
        await _post_callback_with_retry(callback_url, callback_payload)
        logger.info("[Report-Task] done session=%s", request.session_id)
    except Exception as exc:
        logger.exception("[Report-Task] failed session=%s", request.session_id)
        failed_payload = {
            "code": 500,
            "message": "report_generation_failed",
            "data": {
                "session_id": request.session_id,
                "status": "failed",
                "error": str(exc),
            },
        }
        try:
            await _post_callback_with_retry(callback_url, failed_payload)
        except Exception:
            logger.exception("[Report-Task] failed-callback send failed session=%s", request.session_id)


@app.post("/api/v1/interview/report")
async def generate_report(request: ReportRequest, background_tasks: BackgroundTasks, http_request: Request):
    logger.info("[Report] session=%s", request.session_id)
    engine = get_engine(http_request)
    callback_url = _resolve_report_callback_url(request.session_id)
    background_tasks.add_task(_async_generate_report_and_callback, engine, request.model_copy(deep=True))

    return {
        "code": 200,
        "message": "报告生成任务已受理",
        "data": {
            "session_id": request.session_id,
            "status": "processing",
            "callback_target_url": callback_url,
            "message": "后台正在聚合各轮次评分并生成综合评估报告，完成后将推送到固定回调地址模板（interviewId=session_id）。",
        },
    }
# ==========================================
# 健康检查接口
# ==========================================

@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)