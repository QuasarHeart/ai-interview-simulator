from fastapi import FastAPI, BackgroundTasks, HTTPException
import uvicorn

from app.schemas.schemas import StartRequest, FollowupRequest, AnalysisRequest, ReportRequest
from app.LLM_engine.engine import LLMEngine  # 确保路径与你实际文件一致

app = FastAPI(title="AI 面试官 ML-Service API")

# 全局初始化一次引擎
engine = LLMEngine()


# ==========================================
# 接口 1：生成首轮面试问题
# ==========================================
@app.post("/api/v1/interview/start")
async def start_interview(request: StartRequest):
    print(f"[Start] 收到会话: {request.session_id}, 岗位: {request.job_position}")
    try:
        ai_result = await engine.generate_first_question(request)

        return {
            "code": 200,
            "message": "success",
            "data": {
                "session_id": request.session_id,
                "round_id": 1,  # 首轮固定1
                "question": ai_result["question"],
                "flow_control": ai_result["flow_control"],
            },
        }
    except Exception as e:
        print(f"[Start][Error] {e}")
        raise HTTPException(status_code=500, detail=f"start接口调用失败: {str(e)}")


# ==========================================
# 接口 2：生成追问问题
# ==========================================
@app.post("/api/v1/interview/followup")
async def followup_interview(request: FollowupRequest):
    print(f"[Followup] 收到会话: {request.session_id}, 第 {request.round_id} 轮")
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
# 接口 3：回答综合分析
# ==========================================
@app.post("/api/v1/interview/analysis")
async def analyze_answer(request: AnalysisRequest):
    print(f"[Analysis] 分析请求: {request.session_id}")
    try:
        ai_result = await engine.analyze_answer(request)

        # 兼容你的报告结构：analysis 下放三大维度 + 分数 + 反馈
        # 如果 prompt 返回 dimension_details，则从里面拆
        if "dimension_details" in ai_result:
            professional = ai_result["dimension_details"]["professional"]
            cognition = ai_result["dimension_details"]["cognition"]
            expression = ai_result["dimension_details"]["expression"]
        else:
            # 兼容旧结构
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
# 接口 4：面试报告生成 (异步接口演示)
# ==========================================
async def mock_async_report_task(session_id: str, callback_url: str):
    import asyncio
    print(f"[后台任务] 正在为 {session_id} 生成报告...")
    await asyncio.sleep(5)
    print(f"[后台任务] 报告生成完毕！准备 POST 给回调地址: {callback_url}")
    # TODO: 用 httpx post 到 callback_url


@app.post("/api/v1/interview/report")
async def generate_report(request: ReportRequest, background_tasks: BackgroundTasks):
    print(f"[Report] 收到生成报告请求: {request.session_id}")

    # 可选：这里可以同步先调用一次 LLM 生成报告内容（当前先不阻塞接口）
    # report_result = await engine.generate_overall_report(request)
    # TODO: 把 report_result 在后台任务里推送到 callback_url

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