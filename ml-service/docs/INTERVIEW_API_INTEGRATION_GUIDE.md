# AI Interview ML-Service 接口调用指南（后端联调版）

本文面向后端同学，描述 `ml-service/app` 当前可用接口、调用顺序、请求/响应格式、SSE 解析方式与报告回调协议。

## 1. 基础信息

- 服务默认地址：`http://<ml-service-host>:8000`
- 健康检查：`GET /health`
- 内容类型：`Content-Type: application/json; charset=utf-8`
- 当前版本接口统一返回结构：
  - 成功：`{"code":200,"message":"success|...","data":{...}}`
  - 异常：HTTP `500` + `{"detail":"..."}`

> 说明：当前版本要求通过环境变量注入 `DASHSCOPE_API_KEY`，未配置时服务会启动失败。

---

## 2. 推荐调用时序

1. `POST /api/v1/interview/start` 或 `/start/stream` 获取首轮问题
2. 用户回答后，调用 `POST /api/v1/interview/analysis` 做该轮评估
3. 基于轮次推进，循环调用 `POST /api/v1/interview/followup` 或 `/followup/stream`
4. 面试结束后调用 `POST /api/v1/interview/report` 异步生成最终报告
5. 等待回调接口接收报告结果

---

## 3. 接口明细

## 3.1 首轮问题（同步）

- 路径：`POST /api/v1/interview/start`
- 用途：返回首轮提问与初始流程控制

### 请求示例

```bash
curl -X POST 'http://127.0.0.1:8000/api/v1/interview/start' \
  -H 'Content-Type: application/json' \
  -d '{
    "session_id":"sess-001",
    "job_position":"Java后端工程师",
    "jd_summary":"熟悉 Spring Boot、MySQL、Redis",
    "resume_content":"3年支付系统开发经验",
    "interview_config":{
      "mode":"text",
      "interviewer_style":"standard",
      "difficulty":"medium",
      "company_context":"互联网ToB场景",
      "analyze_emotion":false
    },
    "flow_control":{
      "stage_transition":"continue",
      "target_stage":"intro"
    }
  }'
```

### 响应示例

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "session_id": "sess-001",
    "round_id": 1,
    "question": "...",
    "flow_control": {
      "stage_transition": "continue",
      "target_stage": "intro"
    }
  }
}
```

---

## 3.2 首轮问题（流式 SSE）

- 路径：`POST /api/v1/interview/start/stream`
- 用途：前端可边收边展示 question
- 返回 `text/event-stream`

### 事件格式

- token 事件（可多次）
```json
{"type":"token","field":"question","content":"分块文本"}
```

- meta 事件（一次）
```json
{"type":"meta","session_id":"sess-001","round_id":1,"flow_control":{...}}
```

- done 事件（一次，表示结束）
```json
{"type":"done"}
```

- error 事件（失败场景）
```json
{"type":"error","message":"start stream failed, check server log"}
```

### 调用示例

```bash
curl -N -X POST 'http://127.0.0.1:8000/api/v1/interview/start/stream' \
  -H 'Content-Type: application/json' \
  -d @start_payload.json
```

---

## 3.3 追问（同步）

- 路径：`POST /api/v1/interview/followup`
- 用途：根据历史对话生成下一问 + 即时反馈 + 更新摘要

### 请求示例（核心字段）

```json
{
  "session_id": "sess-001",
  "round_id": 2,
  "interview_config": {
    "mode": "text",
    "interviewer_style": "standard",
    "difficulty": "medium",
    "company_context": "互联网ToB场景",
    "analyze_emotion": false
  },
  "background": {
    "job_position": "Java后端工程师",
    "resume_content": "3年支付系统开发经验",
    "jd_summary": "熟悉 Spring Boot、MySQL、Redis"
  },
  "history_data": {
    "history_summary": "已完成开场，开始技术深入",
    "recent_history": [
      {
        "round_id": 1,
        "assistant_content": "请自我介绍",
        "user_content": "我负责过支付核心链路",
        "flow_control": {
          "stage_transition": "continue",
          "target_stage": "intro"
        }
      }
    ]
  }
}
```

### 响应关键字段

- `question`
- `updated_history_summary`
- `immediate_feedback`
- `flow_control`

---

## 3.4 追问（流式 SSE）

- 路径：`POST /api/v1/interview/followup/stream`
- 用途：边展示 `question` 和 `immediate_feedback`

### 事件格式

- token 事件（可多次）
```json
{"type":"token","field":"question","content":"..."}
```
或
```json
{"type":"token","field":"immediate_feedback","content":"..."}
```

- meta 事件（一次）
```json
{
  "type":"meta",
  "session_id":"sess-001",
  "round_id":2,
  "updated_history_summary":"...",
  "flow_control":{...}
}
```

- done/error 同上

### 调用示例

```bash
curl -N -X POST 'http://127.0.0.1:8000/api/v1/interview/followup/stream' \
  -H 'Content-Type: application/json' \
  -d @followup_payload.json
```

---

## 3.5 单轮分析（同步）

- 路径：`POST /api/v1/interview/analysis`
- 用途：返回维度打分、总分、反馈与建议

### 请求关键字段

- `session_id`
- `round_id`
- `current_stage`
- `interview_config`
- `content_to_analyze`（包含 `question`、`user_answer`、简历/JD/历史摘要）

### 响应关键字段

- `analysis.professional|cognition|expression`
- `analysis.dimension_scores`
- `analysis.final_score`
- `analysis.overall_feedback`
- `analysis.improvement_suggestions`

---

## 3.6 生成最终报告（异步受理 + 回调）

- 路径：`POST /api/v1/interview/report`
- 用途：受理任务，后台生成最终报告并回调

### 重要规则（已实现）

回调地址使用固定模板：

`https://nas.feixingxr.com/api/v1/interviews/{interviewId}/report-callback`

其中：

- `interviewId = session_id`
- 即 `session_id=sess-001` 时，实际回调地址为：
  `https://nas.feixingxr.com/api/v1/interviews/sess-001/report-callback`

> 注：请求体中的 `callback_url` 字段当前保留用于兼容，但实际回调以固定模板拼接地址为准。
> 即使传入 `callback_url`，也不会改变最终回调目标地址。

### 受理响应示例

```json
{
  "code": 200,
  "message": "报告生成任务已受理",
  "data": {
    "interviewId": "sess-001",
    "session_id": "sess-001",
    "status": "processing",
    "callback_target_url": "https://nas.feixingxr.com/api/v1/interviews/sess-001/report-callback",
    "message": "后台正在聚合各轮次评分并生成综合评估报告，完成后将推送到固定回调地址模板（interviewId=session_id）。"
  }
}
```

### 回调报文（成功）

```json
{
  "code": 200,
  "message": "report_generated",
  "data": {
    "interviewId": "sess-001",
    "session_id": "sess-001",
    "status": "completed",
    "report": {
      "hiring_recommendation": "Hire",
      "overall_score": 86.0,
      "executive_summary": "...",
      "strengths": ["..."],
      "weaknesses": ["..."],
      "ability_trend": "...",
      "detailed_recommendation": "..."
    }
  }
}
```

### 回调报文（失败）

```json
{
  "code": 500,
  "message": "report_generation_failed",
  "data": {
    "interviewId": "sess-001",
    "session_id": "sess-001",
    "status": "failed",
    "error": "具体错误信息"
  }
}
```

---

## 4. 错误码与重试建议

- `200`：业务成功
- `422`：请求体结构或字段枚举不合法（Pydantic 校验失败）
- `500`：ML 服务内部处理异常（LLM 调用失败、JSON 解析失败、回调失败等）

建议：

1. 同步接口失败时，后端可按幂等键（`session_id + round_id`）重试 1~2 次。
2. SSE 接口如果未收到 `done`，视为失败中断，按当前轮次重试。
3. 报告回调接收端应保证幂等（同一 `session_id` 重复回调可覆盖或去重）。

---

## 5. 联调检查清单

1. `GET /health` 返回 `{"status":"ok"}`
2. `/start`、`/followup`、`/analysis` 返回 `code=200`
3. `/start/stream`、`/followup/stream` 能收到 `done` 事件
4. `/report` 返回 `callback_target_url` 且 URL 中 `interviewId=session_id`
5. 回调接收端能收到 `report_generated` 或 `report_generation_failed`

---

## 6. 当前运行结论（本地烟测）

已在 `ml-service` 环境完成烟测：

- `/start` ✅
- `/followup` ✅
- `/analysis` ✅
- `/report` ✅
- `/start/stream` ✅（包含 `done`）
- `/followup/stream` ✅（包含 `done`）
- 回调 URL 映射 ✅：`https://nas.feixingxr.com/api/v1/interviews/sess-001/report-callback`
