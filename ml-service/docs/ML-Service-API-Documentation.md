## ml-service-api-documentation

**Version**: 1.0.0
**Last Updated**: 2026-02-25

------

## 一、文档信息

本服务接口文档旨在详细描述面试模拟系统中 ML 模块的接口，包括首轮问题生成、追问问题生成、回答分析及面试报告生成等功能。

------

## 二、服务概述

本服务提供以下功能：

- **面试问题生成**：根据用户输入，生成首轮问题及追问问题。
- **回答评分与分析**：对用户的面试回答进行综合分析与评分。
- **情感分析**：分析用户回答中的情感特征（如自信度、语速等）。
- **面试报告生成**：基于面试过程中的数据生成最终的面试报告。

------

## 三、通用规范

- **请求格式**：所有请求必须使用 `application/json` 格式。
- **响应格式**：返回内容为 JSON 格式。
- **版本控制**：所有接口均应包含在 `/api/v1/` 路径中。
- **错误处理**：所有错误通过 `error_code` 和 `message` 返回，确保前端能够正确处理。
- **流式返回**：对于追问问题生成、回答分析等功能，使用 **流式响应**，采用 `text/event-stream` 类型。
- **Session 管理**：所有请求均需要有效的 `session_id`，该 ID 用于管理每次面试会话。

------

## 四、接口列表

------

### 1. 接口名称：生成首轮面试问题

#### 方法：`POST`

#### URL：

```
/api/v1/interview/start
```

#### 功能说明：

该接口用于根据用户选择的职位和面试难度生成首轮面试问题。

#### 请求参数：

```json
{
  "session_id": "string",     // 会话ID，后端生成并传递给ML服务
  "job_position": "string",   // 面试职位，例如 "backend developer"
  "difficulty": "string"      // 面试难度，支持 "easy", "medium", "hard"
}
```

#### 返回参数：

```json
{
  "question": "string",       // 生成的面试问题，例如 "请介绍一下你的项目经验"
  "session_id": "string"      // 会话ID，保持一致
}
```

#### 错误码：

```json
{
  "error_code": "INVALID_REQUEST",
  "message": "Invalid job position or difficulty level."
}
```

------

### 2. 接口名称：生成追问问题

#### 方法：`POST`

#### URL：

```
/api/v1/interview/followup
```

#### 功能说明：

该接口用于生成追问问题，根据用户上一个问题的回答进行生成。

#### 请求参数：

```json
{
  "session_id": "string",    // 会话ID
  "user_answer": "string"    // 用户的回答内容
}
```

#### 返回参数（流式）：

- `Content-Type: text/event-stream`

```json
data: "请详细说明你在项目中的角色和贡献"
```

- 最后标志：

```json
data: [DONE]
```

#### 错误码：

```json
{
  "error_code": "SESSION_NOT_FOUND",
  "message": "Session not found."
}
```

------

### 3. 接口名称：回答综合分析

#### 方法：`POST`

#### URL：

```
/api/v1/interview/analysis
```

#### 功能说明：

该接口用于对用户的回答进行综合分析，包括评分、逻辑严密性、自信度等。

#### 请求参数：

```json
{
  "session_id": "string",    // 会话ID
  "user_answer": "string"    // 用户的回答内容
}
```

#### 返回参数（流式）：

- `Content-Type: text/event-stream`

```json
data: "你的回答很好，逻辑清晰，缺少对项目细节的补充。"
```

- 最后标志：

```json
data: [DONE]
```

#### 错误码：

```json
{
  "error_code": "INVALID_ANSWER",
  "message": "User answer is too short."
}
```

------

### 4. 接口名称：面试报告生成

#### 方法：`POST`

#### URL：

```
/api/v1/interview/report
```

#### 功能说明：

该接口用于生成面试总结报告，返回报告生成的任务ID，用户可以使用该ID查询最终报告。

#### 请求参数：

```json
{
  "session_id": "string"   // 会话ID
}
```

#### 返回参数：

```json
{
  "task_id": "string",    // 生成的任务ID，用于查询报告状态
  "status": "pending"     // 当前任务状态，可能为 "pending" 或 "completed"
}
```

------

### 5. 查询面试报告

#### 方法：`GET`

#### URL：

```
/api/v1/interview/report/{task_id}
```

#### 功能说明：

根据 `task_id` 查询面试报告的生成状态和最终结果。

#### 返回参数（状态查询）：

```json
{
  "task_id": "string",      // 任务ID
  "status": "pending"       // 状态，"pending" 或 "completed"
}
```

#### 返回参数（已完成报告）：

```json
{
  "task_id": "string",      // 任务ID
  "status": "completed",    // 状态
  "report": {
    "overall_score": 85,    // 总体评分
    "technical_score": 90,  // 技术评分
    "communication_score": 80, // 沟通评分
    "strengths": "..."      // 优势
    "weaknesses": "..."     // 劣势
  }
}
```

#### 错误码：

```json
{
  "error_code": "REPORT_NOT_FOUND",
  "message": "Report not found for the given task ID."
}
```

------

## 五、错误码规范

| 错误码            | 描述                   |
| ----------------- | ---------------------- |
| INVALID_REQUEST   | 请求参数无效           |
| SESSION_NOT_FOUND | 会话ID未找到           |
| MODEL_BUSY        | 模型繁忙，无法处理请求 |
| INTERNAL_ERROR    | 内部服务器错误         |
| REPORT_NOT_FOUND  | 无法找到报告           |

------

## 六、数据结构定义

### Session 结构

```json
{
  "session_id": "string"  // 会话唯一标识符
}
```

### 面试报告结构

```json
{
  "overall_score": "int",      // 总体评分
  "technical_score": "int",    // 技术评分
  "communication_score": "int", // 沟通评分
  "strengths": "string",       // 优势
  "weaknesses": "string",      // 劣势
  "suggestions": "string"      // 改进建议
}
```

------

# 七、未来版本（待扩展功能）

- 情感分析（语音中的情感与语气）
- 多轮对话支持（根据不同轮次动态调整问题）
- 语音转写和音频分析
- 高级面试问题生成（AI 自适应问题生成）

