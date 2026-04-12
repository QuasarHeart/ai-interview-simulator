# AI Interview 2.0 对接与联测文档

本文基于当前代码实现整理，目标是让前端、后端可以直接按文档完成 2.0 联调。

适用代码范围：
- `ml-service/app/agent.py`
- `ml-service/tests/test_agent_runtime.py`
- `ml-service/tests/test_agent_behavior_eval.py`

## 1. 当前是否可以联测

可以。

当前验证状态：
- 运行时单测通过（异常分支、清理、命令顺序、report 边界）
- 官方风格行为评测通过（JudgeGroup + judges）
- 2.0 runtime 已切换到 Google Gemini Live 插件，在线 smoke 走 Google/Gemini 配置

注意：
- 如果使用 LiveKit Inference 作为评测后端，需保证 `LIVEKIT_API_KEY/LIVEKIT_API_SECRET` 与模型权限正确；否则可能出现 401。
- 2.0 runtime 最终报告仍桥接到 1.0 报告接口（`/api/v1/interview/report`）。

## 2. 2.0 架构与职责

2.0 是 LiveKit-first 的双模型运行时：

- Realtime 模型：负责实时对话输出（低延迟）
- Reasoning 模型：负责阶段决策、评分、策略更新

关键点：
- 会话初始化来源是 LiveKit room metadata（不是旧 v2 init API）
- 每轮转写触发异步推理
- 推理结果通过命令队列驱动实时会话行为
- 到达 `end` 阶段后触发报告请求，发送到后端 1.0 报告接口

## 3. 对接数据契约

## 3.1 LiveKit 房间 metadata（后端创建房间时传）

2.0 优先从 `ctx.room.metadata` 读取会话资料，同时兼容 `ctx.metadata` 和 `ctx.job.metadata` 作为补充来源。支持 JSON 字符串或 dict。

推荐结构：

```json
{
  "session_id": "sess-20260402-001",
  "job_position": "Java后端工程师",
  "jd_summary": "熟悉 Spring Boot、MySQL、Redis、消息队列",
  "resume_content": "3年支付与交易系统经验",
  "interview_config": {
    "mode": "video",
    "interviewer_style": "expert",
    "difficulty": "hard",
    "company_context": "电商交易场景"
  }
}
```

字段说明：

| 字段 | 是否必填 | 说明 | 默认值/规则 |
|---|---|---|---|
| `session_id` | 建议必填 | 业务侧会话 ID | 若 `room.name` 只是 `room_<session_id>` 这类别名，运行时会自动归一化；若确实不同，运行时以 `session_id` 为准并告警 |
| `job_position` | 建议必填 | 岗位 | 默认空字符串 |
| `jd_summary` | 建议必填 | JD 摘要 | 默认空字符串 |
| `resume_content` | 建议必填 | 简历摘要 | 默认空字符串 |
| `interview_config.mode` | 可选 | `text/audio/video` | 默认来自环境变量 `INTERVIEW_MODE` |
| `interview_config.interviewer_style` | 可选 | `standard/friendly/aggressive/expert` | 默认 `INTERVIEWER_STYLE` |
| `interview_config.difficulty` | 可选 | `easy/medium/hard` | 默认 `INTERVIEW_DIFFICULTY` |
| `interview_config.company_context` | 可选 | 公司语境 | 默认 `COMPANY_CONTEXT` |

说明：
  - metadata 为空或 JSON 非法时，会降级为默认配置并记录 warning。
  - 如果房间 metadata 缺失，worker 会尝试读取 job metadata；因此上游 dispatch/job request 也可以继续携带同样的 JSON 契约。
语义约定：
- `mode=text`：1.0 语音/文本面试模式。
- `mode=audio`：2.0 仅语音通话。
- `mode=video`：2.0 语音通话 + 视频通话。

## 3.1.1 前端开场字段清单（建议必传）

前端/后端在创建房间并开始面试前，建议至少传以下字段到 `room.metadata`：

1. `session_id`
2. `job_position`
3. `jd_summary`
4. `resume_content`
5. `interview_config.mode`
6. `interview_config.interviewer_style`
7. `interview_config.difficulty`
8. `interview_config.company_context`
9. 不需要再传额外的视频开关字段

最小可用 payload（可直接给前端）：

```json
{
  "session_id": "sess-20260402-001",
  "job_position": "Java后端工程师",
  "jd_summary": "熟悉 Spring Boot、MySQL、Redis",
  "resume_content": "3年支付系统经验",
  "interview_config": {
    "mode": "video",
    "interviewer_style": "expert",
    "difficulty": "hard",
    "company_context": "电商交易场景"
  }
}
```

## 3.2 前端实时输入与事件

前端通过 LiveKit 音视频/文本进入房间后，运行时依赖如下事件：

- `user_state_changed`
  - `speaking` 时可能触发打断策略
- `user_input_transcribed`
  - 仅 `is_final=true` 的转写参与推理
  - 读取 `transcript`
  - 可选读取 `voice_metrics/face_metrics/emotion_signals`

无多模态信号时会降级到 transcript-only，并记录一次 warning。

## 3.3 运行时命令类型（内部行为，可用于观测）

推理后会进入命令队列，主要命令：

- `strategy_update`
  - 更新对话策略并触发动态指令刷新
- `assistant_soft_interrupt`
  - 轻打断并给出聚焦语句
- `interrupt_assistant`
  - 用户抢话时中断 assistant
- `pace_control`
  - 节奏/追问深度控制（静默应用，不额外发言）

## 3.4 报告回调（2.0 -> 后端）

当阶段到 `end` 且有 `round_results` 时，2.0 会在 worker 内部完成报告分析与生成，然后直接向 `REPORT_CALLBACK_URL_TEMPLATE` 对应地址发送最终回调。

回调 URL 规则：
- 模板来自 `REPORT_CALLBACK_URL_TEMPLATE`
- 使用 `{interviewId}` 占位符，值为 `session_id`（URL 编码后）

失败行为：
- 单次请求失败会记录异常日志
- `state.report_dispatched` 保持 `false`
- 当前无内置重试队列

## 4. 联调前准备

## 4.1 环境变量（`ml-service/.env.ml-service`）

至少确认：

- 模型与网关
  - `GOOGLE_API_KEY`
  - `GOOGLE_USE_VERTEXAI`
  - `GOOGLE_CLOUD_PROJECT`
  - `GOOGLE_CLOUD_LOCATION`
  - `GEMINI_MODEL`
  - `GEMINI_VOICE`
  - `GEMINI_LANGUAGE`
  - `GEMINI_TEMPERATURE`
- 报告评分模型
  - `REPORT_MODEL`，建议使用文本生成模型，例如 `gemini-3.1-flash-lite-preview`
- 报告流水日志
  - `REPORT_LOG_PIPELINE`，开启后打印 2.0 报告分析、生成、回调的详细流水日志，默认 `false`
  - `REPORT_LOG_PIPELINE_MAX_CHARS`，流水日志内容截断长度，避免单条日志过长
- 报告桥接
  - `REPORT_CALLBACK_URL_TEMPLATE`

如果跑 LiveKit Inference 评测：
- `LIVEKIT_API_KEY`
- `LIVEKIT_API_SECRET`
- `LIVEKIT_URL`

## 4.1.1 远端 LiveKit Server 场景（你当前就是这种）

如果这台机器只部署 agent，而 LiveKit Server 在另一台机器：

1. `LIVEKIT_URL` 必须配置成远端地址（不是本机 `127.0.0.1`，也不是 `host.docker.internal`）
2. `LIVEKIT_API_KEY` / `LIVEKIT_API_SECRET` 必须与远端 LiveKit Server 上配置一致
3. 远端机器防火墙/安全组需要放行对应端口

示例（按你的真实地址替换）：

```env
LIVEKIT_URL=ws://10.0.0.25:7880
LIVEKIT_API_KEY=your_livekit_key
LIVEKIT_API_SECRET=your_livekit_secret
```

如果是 TLS：

```env
LIVEKIT_URL=wss://livekit.your-domain.com
```

快速检查（在 agent 这台机器执行）：

```bash
curl -m 3 http://10.0.0.25:7880 || true
```

说明：
- 你现在日志里的 `Connect call failed ...:7880` 不是业务代码错误，而是 agent 到 LiveKit Server 的网络/地址配置问题。

## 4.2 启动 2.0 runtime

在仓库根目录执行：

```bash
cd ml-service
conda run -n ml-service python app/agent.py dev
```

说明：
- `python app/agent.py` 只会显示 CLI 帮助，不会真正启动 worker。
- `python app/agent.py dev` / `python app/agent.py start` 才会启动 agent worker。
- 启动后进程会前台常驻等待任务，这是正常现象，不是卡死。
- 联调时请新开一个终端执行前端/后端调用；需要停止时在该终端按 `Ctrl+C`。

## 5. 前后端联测流程（推荐）

## 5.1 后端步骤

1. 使用业务 `session_id` 创建 LiveKit room，建议 `room.name = session_id`
2. 在 room metadata 放入 3.1 的 JSON
3. 准备 report callback 接口，能按 `interviewId=session_id` 路由

说明：如果上游框架自动把房间名写成 `room_<session_id>`，运行时会自动把它归一化为业务 `session_id`，但仍建议后端创建房间时尽量直接使用同一个值。

## 5.2 前端步骤

1. 入会同一个 room（token 与 room 匹配）
2. 打开麦克风（视频面试则打开摄像头）
3. 正常进行多轮问答，观察：
   - 是否实时发问
   - 是否在偏题/冗长时出现软打断
   - 末轮后是否触发报告流程

## 5.3 验收点

必验：

1. metadata 正确生效（岗位/JD/简历可影响提问）
2. stage 发生推进（`intro -> ... -> end`）
3. 报告请求成功发到后端（收到完整 `round_results`）
4. callback URL 中 `interviewId` 与 `session_id` 一致
5. 会话关闭后无残留 worker/session（已加测试验证）

## 6. 测试方法（基于当前代码）

## 6.1 本地回归测试

```bash
cd ml-service
conda run -n ml-service pytest -q
```

覆盖内容包括：
- reasoning 抛异常
- `_compute_dimension_scores` 异常输入
- `close_session` 清理
- 多命令顺序一致性
- `REPORT_CALLBACK_URL_TEMPLATE` 边界行为

## 6.2 官方风格行为评测（离线稳定）

```bash
cd ml-service
conda run -n ml-service pytest -q tests/test_agent_behavior_eval.py -q
```

特点：
- 使用 `JudgeGroup + built-in judges + custom judge`
- 默认使用 mock judge，适合 CI 稳定回归

## 6.3 官方风格行为评测（真实在线）

推荐使用 Google/Gemini 作为在线 smoke 的默认模型配置：

```bash
cd ml-service
set -a && source .env.ml-service >/dev/null 2>&1 && set +a
LIVEKIT_BEHAVIOR_EVAL_ONLINE=1 \
conda run -n ml-service pytest -q tests/test_agent_behavior_eval.py::test_behavior_eval_online_smoke -q
```

全量在线回归：

```bash
cd ml-service
set -a && source .env.ml-service >/dev/null 2>&1 && set +a
LIVEKIT_BEHAVIOR_EVAL_ONLINE=1 \
conda run -n ml-service pytest -q
```

## 7. 常见问题与排查

## 7.1 在线评测 401

现象：`object cannot be found` 或鉴权失败。

处理：
- 若走 LiveKit Inference：检查 `LIVEKIT_API_KEY/LIVEKIT_API_SECRET` 与模型权限
- 若走 Google Gemini：检查 `GOOGLE_API_KEY`，或确认 Vertex AI 的 `GOOGLE_USE_VERTEXAI/GOOGLE_CLOUD_PROJECT/GOOGLE_CLOUD_LOCATION` 配置正确

## 7.2 metadata 不生效

处理：
- 确认 metadata 是合法 JSON
- 确认字段放在 `room.metadata`，或者至少放在 `ctx.job.metadata` / `ctx.metadata` 的兼容 JSON 中
- 检查日志中是否有 `No valid metadata JSON` / `session_id mismatch`

## 7.3 report 未下发

处理：
- 确认阶段是否进入 `end`
- 确认 `round_results` 非空
- 检查报告回调地址可达
- 查看日志中 report callback 发送结果

## 8. 联调结论建议

当前版本可进入前后端联调和灰度验证。

建议联调完成后优先补两项：

1. report 失败重试/补偿机制（当前为单次尝试）

## 9. 2.0 Docker 部署（对应你 1.0 的 Docker 方式）

可以，2.0 也可以放到 Docker。

说明：
- 你现有的 `Dockerfile` 是 1.0 FastAPI 用的（`uvicorn app.main:app`）。
- 2.0 是 LiveKit worker 常驻进程，启动命令不同，建议使用新增的 `Dockerfile.agent2`。

## 9.1 构建 2.0 镜像

```bash
cd ml-service
docker build -f Dockerfile.agent2 -t ai-interview-2-runtime:latest .
```

## 9.2 运行 2.0 容器

```bash
cd ml-service
docker run --rm -it \
  --env-file .env.ml-service \
  --name ai-interview-2-runtime \
  ai-interview-2-runtime:latest
```

说明：
- 这是前台常驻 worker，日志持续输出是正常行为。
- 停止容器使用 `Ctrl+C`（前台）或 `docker stop ai-interview-2-runtime`（后台）。

## 9.3 容器联测要点

1. 确认容器内可访问 LiveKit 与 Google/Gemini 模型网关。
2. room metadata 契约保持与 3.1 一致。
3. 回调地址必须在容器内可达，建议使用宿主机域名、服务名或内网地址。

## 9.4 可选：本地调试模式

若需要容器内 `dev` 模式：

```bash
docker run --rm -it \
  --env-file .env.ml-service \
  --entrypoint python \
  ai-interview-2-runtime:latest app/agent.py dev
```

## 10. 1.0 + 2.0 同时上线（并行运行）

你的场景是可行的：
- 1.0 提供 HTTP API（`/api/v1/interview/*`）
- 2.0 是 LiveKit worker（常驻监听，不需要对外暴露 HTTP 端口）

两者可以在同一台机器、同一 Docker 网络里并行运行。

已提供编排文件：
- `ml-service/docker-compose.dual.yml`

该编排包含：
- `interview-api-v1`：基于 `Dockerfile`，对外 `8000`
- `interview-agent-v2`：基于 `Dockerfile.agent2`，负责 2.0 实时面试与报告回调

## 10.1 一键启动双版本

```bash
cd ml-service
docker compose -f docker-compose.dual.yml build
docker compose -f docker-compose.dual.yml up -d
```

开发期只重启容器（不重新构建）可用：

```bash
docker compose -f docker-compose.dual.yml up -d
```

查看状态：

```bash
docker compose -f docker-compose.dual.yml ps
docker compose -f docker-compose.dual.yml logs -f interview-agent-v2
```

停止：

```bash
docker compose -f docker-compose.dual.yml down
```

## 10.1.1 改代码后是否需要全量重建

不需要每次全量重建，按改动范围执行：

1. 只改 Python 代码（`app/*.py`、prompt、schema）
  - 执行：`docker compose -f docker-compose.dual.yml build interview-agent-v2`
  - 然后：`docker compose -f docker-compose.dual.yml up -d interview-agent-v2`
2. 只改 1.0 API 代码（`app/main.py` 或 1.0 路由逻辑）
  - 执行：`docker compose -f docker-compose.dual.yml build interview-api-v1`
  - 然后：`docker compose -f docker-compose.dual.yml up -d interview-api-v1`
3. 只改环境变量
  - 执行：`docker compose -f docker-compose.dual.yml up -d`
4. 改了依赖文件（`requirements.txt` 或 `requirements.agent2.txt`）
  - 对应服务必须 rebuild
5. 平时联调重启
  - 只需：`docker compose -f docker-compose.dual.yml up -d`

## 10.2 为什么能同时跑

1. 端口不冲突：
  - 1.0 占用并暴露 `8000`
  - 2.0 不暴露端口，仅内部常驻
2. 职责不冲突：
  - 1.0 继续承载你现有 API 能力
  - 2.0 负责实时面试 runtime 和策略控制
3. 报告由 worker 内部生成并直接回调：
  - 使用 `REPORT_CALLBACK_URL_TEMPLATE`
    - 不再依赖单独的报告桥接地址

## 10.3 与 cloudflared 共存建议

你当前 `cloudflared` 可继续保留，建议映射到 1.0 的 8000（即 `interview-api-v1`）。

推荐方式：
1. 公网请求 -> cloudflared -> 1.0 API
2. 2.0 走 LiveKit 通道，不要求被 cloudflared 直接暴露

说明：
- 如果 cloudflared 在 compose 外单独跑，确保它能访问宿主机 `8000`。
- 如果你想把 cloudflared 也纳入 compose，可后续再加第三个 service（取决于你当前 tunnel token/配置文件管理方式）。

## 10.4 上线切流建议

1. 先保持 1.0 全量在线（不变更公网入口）。
2. 启动 2.0，仅让指定房间或指定用户走 2.0（灰度）。
3. 观察以下指标：
  - 2.0 会话成功率
  - report 下发成功率
  - 端到端延迟与中断体验
4. 稳定后再逐步扩大 2.0 流量。

## 11. 为什么 Docker 会下载很多包

这是正常现象，原因是 2.0 依赖了 `livekit-agents` 生态。

主要原因：
1. `requirements.agent2.txt` 里有 `livekit-agents` 和 `livekit-plugins-google`。
2. 这两个包会带入一批传递依赖（例如 `numpy`、`av`、`opentelemetry-*`、`livekit-*`）。
3. 第一次 `docker build` 没有镜像缓存时，会完整下载并安装一次。

如何减少重复下载：
1. 不要每次都用 `up --build`，优先使用：
   - `docker compose -f docker-compose.dual.yml up -d`
2. 只有依赖文件变化时再重建：
   - `docker compose -f docker-compose.dual.yml build`
3. 保持 Dockerfile 的依赖层缓存（当前已按 `COPY requirements -> pip install -> COPY app` 处理）。

何时一定会重新下载：
1. 你改了 `app/requirements.agent2.txt`。
2. 你清理了本地 Docker 构建缓存。
3. 换了新机器或新 CI runner。

3. 若个别包无 wheel（极少数），会在导出或安装阶段暴露出来，再单独处理。