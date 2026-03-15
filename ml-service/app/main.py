from fastapi import FastAPI, BackgroundTasks
import uvicorn
from app.schemas.schemas import StartRequest, FollowupRequest, AnalysisRequest, ReportRequest

app = FastAPI(title="AI 面试官 ML-Service API")

# ==========================================
# 接口 1：生成首轮面试问题
# ==========================================
@app.post("/api/v1/interview/start")
async def start_interview(request: StartRequest):
    print(f"[Start] 收到会话: {request.session_id}, 岗位: {request.job_position}")
    
    # TODO: 未来这里调用 engine.py
    # ai_result = await engine.generate_start(request)
    
    # 当前阶段：直接复制 Apifox 的返回示例，写死返回！
    return {
        "code": 200,
        "message": "success",
        "data": {
            "session_id": request.session_id,
            "round_id": 1,
            "question": "你好，请简单做个自我介绍，并说说你在上一个项目中承担的核心角色。",
            "flow_control": {
                "stage_transition": "continue",
                "target_stage": "intro"
            }
        }
    }

"""
测试指令，在ml-service目录下输入python -m app.main启动
curl --location --request POST 'http://0.0.0.0:8000/api/v1/interview/start' \
--header 'Content-Type: application/json' \
--data-raw '{
    "session_id": "adbe7f67-31bb-49a7-b4f2-54ee7183561e",
    "job_position": "java_backend",
    "resume_content": "精通Java，有分布式系统开发经验。",
    "interview_config": {
        "mode": "text",
        "analyze_emotion": false,
        "interviewer_style": "standard",
        "company_context": "字节跳动",
        "difficulty": "medium"
    },
    "flow_control": {
        "stage_transition": "continue",
        "target_stage": "intro"
    }
}'
"""
# ==========================================
# 接口 2：生成追问问题
# ==========================================
@app.post("/api/v1/interview/followup")
async def followup_interview(request: FollowupRequest):
    print(f"[Followup] 收到会话: {request.session_id}, 第 {request.round_id} 轮")
    
    # 直接写死返回复杂的假数据，应付前端和后端的联调
    return {
        "code": 200,
        "message": "success",
        "data": {
            "session_id": request.session_id,
            "round_id": request.round_id,
            "question": "既然你提到了Redis，如果节点宕机了你怎么保证数据不丢？",
            "updated_history_summary": "候选人完成了自我介绍，目前正在考察 Redis 持久化机制。",
            "immediate_feedback": "思路很清晰，我们往下深挖一下。",
            "flow_control": {
                "stage_transition": "continue",
                "target_stage": "tech_general"
            }
        }
    }

# ==========================================
# 接口 3：回答综合分析 (这个返回最复杂，直接贴假 JSON)
# ==========================================
@app.post("/api/v1/interview/analysis")
async def analyze_answer(request: AnalysisRequest):
    print(f"[Analysis] 分析请求: {request.session_id}")
    
    # 哪怕响应再复杂，在这里就是一坨硬编码的字典
    return {
        "code": 200,
        "message": "success",
        "data": {
            "session_id": request.session_id,
            "round_id": request.round_id,
            "question": request.content_to_analyze.question,
            "user_answer": request.content_to_analyze.user_answer,
            "analysis": {
                "dimension_scores": {
                    "professional": 4.2,
                    "cognition": 3.8,
                    "expression": 4.5
                },
                "dimension_details": {
                    "professional": {
                        "technical_correctness": {"score": 4, "reason": "回答正确"}
                        # ... 省略其他写死的字段，照着 Apifox 里的抄过来就行
                    },
                    "cognition": {
                        "logic_structure": {"score": 4, "reason": "逻辑严密"}
                    },
                    "expression": {
                        "clarity": {"score": 5, "reason": "表达极其清晰"}
                    }
                },
                "final_score": 85.5,
                "overall_feedback": "表现优异，基础扎实",
                "improvement_suggestions":["可以多增加一些底层源码的解析"]
            }
        }
    }

# ==========================================
# 接口 4：面试报告生成 (异步接口演示)
# ==========================================
async def mock_async_report_task(session_id: str, callback_url: str):
    """模拟后台慢慢写报告的任务"""
    import asyncio
    print(f"[后台任务] 正在为 {session_id} 生成报告...")
    await asyncio.sleep(5)  # 模拟大模型思考 5 秒钟
    print(f"[后台任务] 报告生成完毕！准备 POST 给回调地址: {callback_url}")
    # TODO: 未来这里用 httpx 库发送 POST 请求给业务后端

@app.post("/api/v1/interview/report")
async def generate_report(request: ReportRequest, background_tasks: BackgroundTasks):
    print(f"[Report] 收到生成报告请求: {request.session_id}")
    
    # 将耗时任务丢入后台运行，接口立刻返回！
    background_tasks.add_task(mock_async_report_task, request.session_id, request.callback_url)
    
    return {
        "code": 200,
        "message": "报告生成任务已受理",
        "data": {
            "session_id": request.session_id,
            "status": "processing",
            "message": "后台正在聚合各轮次评分并生成综合评估报告，完成后将推送到 callback_url。"
        }
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)