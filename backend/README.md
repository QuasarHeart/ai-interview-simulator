# Backend

Spring Boot 业务服务，为前端和 ML Service 提供用户、面试会话、文件、实时通信和报告编排能力。

## 技术栈

- Java 25
- Spring Boot
- Spring MVC、WebSocket、WebFlux
- MySQL、Redis
- MyBatis、JPA
- LiveKit Server SDK
- Maven Wrapper

## 本地启动

先准备 MySQL、Redis、邮件、对象存储、LiveKit 和 ML Service 的运行环境，并通过环境变量注入凭证。不要把真实密钥写入 `src/main/resources/application.yaml`。

```bash
cd backend
./mvnw clean package -DskipTests
./mvnw spring-boot:run
```

默认服务端口由 `application.yaml` 决定。健康检查和监控端点由 Spring Boot Actuator 提供。

## 主要职责

- 用户注册、登录和 Token 校验；
- 面试会话、问题、回答和历史报告；
- 简历与附件上传、解析和对象存储；
- LiveKit 房间创建、Token 签发和回调；
- 与 `ml-service` 的 HTTP、SSE 和 WebSocket 通信；
- Redis Stream 评价任务和失败恢复。

## 配置原则

生产环境应使用 Secret Manager、CI/CD Secrets 或部署平台环境变量提供：

```text
DEEPSEEK_API_KEY
LIVEKIT_API_KEY
LIVEKIT_API_SECRET
数据库连接与密码
Redis 连接信息
邮件与对象存储凭证
```

测试中需要调用外部模型的用例也必须通过 `DEEPSEEK_API_KEY` 获取凭证，禁止硬编码 API Key。

## 构建

```bash
./mvnw clean package -DskipTests
docker build -t bole-ai-backend .
```

CI/CD 配置位于 [`.github/workflows/java-deploy.yml`](../.github/workflows/java-deploy.yml)。
