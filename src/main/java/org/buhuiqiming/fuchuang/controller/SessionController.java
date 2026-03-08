package org.buhuiqiming.fuchuang.controller;

import lombok.extern.slf4j.Slf4j;
import org.buhuiqiming.fuchuang.dto.MessageDTO;
import org.buhuiqiming.fuchuang.dto.Result;
import org.buhuiqiming.fuchuang.entity.MyMessage;
import org.buhuiqiming.fuchuang.entity.MySession;
import org.buhuiqiming.fuchuang.service.ChatService;
import org.buhuiqiming.fuchuang.service.SessionService;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.servlet.mvc.method.annotation.SseEmitter;

import java.time.LocalDateTime;
import java.util.List;
import java.util.UUID;
import java.util.concurrent.CompletableFuture;

@RestController
@RequestMapping("/session")
@Slf4j
public class SessionController {

    private  final ChatService chatService;
    private  final SessionService sessionService;

    public SessionController(ChatService chatService, SessionService sessionService) {
        this.chatService = chatService;
        this.sessionService = sessionService;
    }

    /**
     * 创建会话
     * @return 会话ID
     */
    @GetMapping
    public Result createSession(@RequestBody MySession  session) {
        return Result.success(sessionService.createSession(session));
    }


    /**
     * 流式对话接口
     * @param message 用户输入
     * @return SseEmitter 发射器
     */
    @GetMapping(value = "/chat", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
    public SseEmitter streamChat(@RequestBody MyMessage  message) {


        message.setCreateTime(LocalDateTime.now());
        message.setRole("user");
        chatService.saveMessage(message);

        // 1. 创建发射器，设置超时时间（例如 2 分钟）
        // 大厂实践中通常会设置一个较大的超时，避免 AI 思考太久被断开
        SseEmitter emitter = new SseEmitter(120_000L);

        // 2. 异步执行 AI 生成逻辑
        // 注意：这里必须异步，否则会阻塞 Tomcat 的主线程池
        CompletableFuture.runAsync(() -> {
            StringBuilder fullResponse = new StringBuilder();
            try {
                //获取上下文

                List<MessageDTO> messages = chatService.getMessage(message.getSessionId());
                log.info("获取上下文：{}",messages);


                // 模拟从 ML 接口获取数据（实际中你会调用 ML 提供的 Stream 接口）
                for (int i = 0; i < 5; i++) {
                    String chunk = "这是第 " + i + " 片段数据; ";

                    // 推送给前端
                    emitter.send(SseEmitter.event()
                            .id(UUID.randomUUID().toString()) // 每一片可以带个 ID
                            .data(chunk) // 核心内容
                            .reconnectTime(3000)); // 建议浏览器断线 3 秒重连

                    fullResponse.append(chunk);
                    Thread.sleep(500); // 模拟网络延迟和生成耗时
                }

                // 3. 推送结束标识（大厂常用 [DONE]）
                emitter.send(SseEmitter.event().data("[DONE]"));

                // 4. 全部成功后，调用 Service 异步存入数据库
                message.setCreateTime(LocalDateTime.now());
                message.setContent(fullResponse.toString());
                message.setMsgType("assistant");
                chatService.saveMessage(message);

                // 5. 完成流
                emitter.complete();

            } catch (Exception e) {
                // 如果中间报错，通知前端并结束
                emitter.completeWithError(e);
            }
        });

        // 立即返回 emitter 对象，连接已建立，主线程释放
        return emitter;
    }
}

