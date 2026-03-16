import sys
import io
import traceback
import uvicorn
import json
import json_repair

# 强制标准输出为 utf-8，避免 ascii 编码报错
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.responses import StreamingResponse

from app.schemas.schemas import StartRequest, FollowupRequest, AnalysisRequest, ReportRequest
from app.LLM_engine.engine import LLMEngine  # 你的实际路径

app = FastAPI(title="AI 面试官 ML-Service API")

# 全局初始化一次引擎
engine = LLMEngine()


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
async def start_interview(request: StartRequest):
    print(f"[Start] session={request.session_id}, job={request.job_position}")
    try:
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
        print(f"[Start][Error] {e}")
        raise HTTPException(status_code=500, detail=f"start接口调用失败: {str(e)}")


# ==========================================
# 接口 1-Stream：首轮问题流式（只给用户展示 question）
# ==========================================
@app.post("/api/v1/interview/start/stream")
async def start_interview_stream(request: StartRequest):
    print(f"[Start-Stream] session={request.session_id}, job={request.job_position}")

    async def event_gen():
        raw_acc = ""
        try:
            async for token in engine.stream_first_question(request):
                raw_acc += token

            parsed_raw = json_repair.loads(raw_acc)
            if not isinstance(parsed_raw, dict):
                raise ValueError(f"LLM返回不是JSON对象: {type(parsed_raw).__name__}")
            parsed: dict = parsed_raw

            question = str(parsed.get("question", ""))
            flow_control_raw = parsed.get("flow_control", {"stage_transition": "continue", "target_stage": "intro"})
            flow_control = flow_control_raw if isinstance(flow_control_raw, dict) else {
                "stage_transition": "continue",
                "target_stage": "intro"
            }

            # 用户可见字段：question（按块流式）
            async for evt in _yield_text_in_chunks(question, "question", chunk_size=12):
                yield evt

            # 非展示字段末尾一次性给前端
            yield f"data: {json.dumps({'type': 'meta', 'session_id': request.session_id, 'round_id': 1, 'flow_control': flow_control}, ensure_ascii=False)}\n\n"
            yield f"data: {json.dumps({'type': 'done'}, ensure_ascii=False)}\n\n"

        except Exception:
            err_trace = traceback.format_exc()
            print("\n[START_STREAM_ERROR_TRACE]\n" + err_trace)
            yield f"data: {json.dumps({'type': 'error', 'message': 'start stream failed, check server log'}, ensure_ascii=True)}\n\n"
            yield f"data: {json.dumps({'type': 'done'}, ensure_ascii=True)}\n\n"

    return StreamingResponse(event_gen(), media_type="text/event-stream")


# ==========================================
# 接口 2：生成追问问题（同步）
# ==========================================
@app.post("/api/v1/interview/followup")
async def followup_interview(request: FollowupRequest):
    print(f"[Followup] session={request.session_id}, round={request.round_id}")
    try:
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
        print(f"[Followup][Error] {e}")
        raise HTTPException(status_code=500, detail=f"followup接口调用失败: {str(e)}")


# ==========================================
# 接口 2-Stream：追问流式（展示 question + immediate_feedback）
# ==========================================
@app.post("/api/v1/interview/followup/stream")
async def followup_interview_stream(request: FollowupRequest):
    print(f"[Followup-Stream] session={request.session_id}, round={request.round_id}")

    async def event_gen():
        raw_acc = ""
        try:
            async for token in engine.stream_following_question(request):
                raw_acc += token

            parsed_raw = json_repair.loads(raw_acc)
            if not isinstance(parsed_raw, dict):
                raise ValueError(f"LLM返回不是JSON对象: {type(parsed_raw).__name__}")
            parsed: dict = parsed_raw

            question = str(parsed.get("question", ""))
            immediate_feedback = str(parsed.get("immediate_feedback", ""))
            updated_history_summary = str(parsed.get("updated_history_summary", ""))

            flow_control_raw = parsed.get(
                "flow_control",
                {"stage_transition": "continue", "target_stage": request.flow_control.target_stage}
            )
            flow_control = flow_control_raw if isinstance(flow_control_raw, dict) else {
                "stage_transition": "continue",
                "target_stage": request.flow_control.target_stage
            }

            # 用户可见字段按块流式
            async for evt in _yield_text_in_chunks(question, "question", chunk_size=12):
                yield evt
            async for evt in _yield_text_in_chunks(immediate_feedback, "immediate_feedback", chunk_size=12):
                yield evt

            # 非展示字段一次性返回
            yield f"data: {json.dumps({'type': 'meta', 'session_id': request.session_id, 'round_id': request.round_id, 'updated_history_summary': updated_history_summary, 'flow_control': flow_control}, ensure_ascii=False)}\n\n"
            yield f"data: {json.dumps({'type': 'done'}, ensure_ascii=False)}\n\n"

        except Exception:
            err_trace = traceback.format_exc()
            print("\n[FOLLOWUP_STREAM_ERROR_TRACE]\n" + err_trace)
            yield f"data: {json.dumps({'type': 'error', 'message': 'followup stream failed, check server log'}, ensure_ascii=True)}\n\n"
            yield f"data: {json.dumps({'type': 'done'}, ensure_ascii=True)}\n\n"

    return StreamingResponse(event_gen(), media_type="text/event-stream")


# ==========================================
# 接口 3：回答综合分析（同步）
# ==========================================
@app.post("/api/v1/interview/analysis")
async def analyze_answer(request: AnalysisRequest):
    print(f"[Analysis] session={request.session_id}")
    try:
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
        print(f"[Analysis][Error] {e}")
        raise HTTPException(status_code=500, detail=f"analysis接口调用失败: {str(e)}")


# ==========================================
# 接口 4：面试报告生成（异步任务受理）
# ==========================================
async def mock_async_report_task(session_id: str, callback_url: str):
    import asyncio
    print(f"[Report-Task] generating report for session={session_id}")
    await asyncio.sleep(5)
    print(f"[Report-Task] done, callback={callback_url}")
    # TODO: 用 httpx post 到 callback_url


@app.post("/api/v1/interview/report")
async def generate_report(request: ReportRequest, background_tasks: BackgroundTasks):
    print(f"[Report] session={request.session_id}")
    background_tasks.add_task(mock_async_report_task, request.session_id, request.callback_url)

    return {
        "code": 200,
        "message": "报告生成任务已受理",
        "data": {
            "session_id": request.session_id,
            "status": "processing",
            "message": "后台正在聚合各轮次评分并生成综合评估报告，完成后将推送到 callback_url。",
        },
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)