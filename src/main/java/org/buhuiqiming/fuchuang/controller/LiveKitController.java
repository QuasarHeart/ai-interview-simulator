package org.buhuiqiming.fuchuang.controller;

import io.livekit.server.WebhookReceiver;
import livekit.LivekitWebhook;
import lombok.extern.slf4j.Slf4j;
import org.buhuiqiming.fuchuang.service.LiveKitService;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RestController;

@Slf4j
@RestController("/api/livekit")
public class LiveKitController {
    private  final LiveKitService liveKitService;
    private final WebhookReceiver webhookReceiver;
    public LiveKitController(LiveKitService liveKitService, WebhookReceiver webhookReceiver) {
        this.liveKitService = liveKitService;
        this.webhookReceiver = webhookReceiver;
    }


    @PostMapping("/webhook")
    public ResponseEntity<String> handleWebhook(
            @RequestHeader("Authorization") String authHeader,
            @RequestBody String body) {

        try {
            // 1. 验证签名（这是 0.12.1 的标准用法）
            // 如果 Authorization Header 为空或签名不匹配，会抛出异常
            LivekitWebhook.WebhookEvent event = webhookReceiver.receive(body, authHeader);

            // 2. 提取基础信息
            String eventName = event.getEvent();
            String roomName = event.getRoom().getName(); // 你的 session_id

            log.info("收到 LiveKit 事件: [{}], 房间: [{}]", eventName, roomName);

            // 3. 业务分发处理
            dispatchStep(event);

            // 4. 无论如何，必须返回 200 OK，否则 LiveKit 会一直重试推送
            return ResponseEntity.ok("Success");

        } catch (Exception e) {
            log.error("Webhook 验证失败或逻辑异常: {}", e.getMessage());
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body("Unauthorized");
        }
    }

    private void dispatchStep(LivekitWebhook.WebhookEvent event) {
        switch (event.getEvent()) {
            case "participant_joined":
                onParticipantJoined(event);
                break;
            case "participant_left":
                onParticipantLeft(event);
                break;
            case "room_finished":
                onRoomFinished(event);
                break;
            default:
                // 对于不关心的事件，静默跳过
                log.debug("忽略事件类型: {}", event.getEvent());
                break;
        }
    }

    private void onParticipantJoined(LivekitWebhook.WebhookEvent event) {
        String identity = event.getParticipant().getIdentity();
        // 逻辑：如果是面试者进入，标记面试开始
        if (!isAgent(identity)) {
            log.info("面试者 [{}] 进入房间，面试正式开始。", identity);
            // 这里执行你的数据库更新操作：UPDATE interview_table SET status='IN_PROGRESS' ...
        }
    }

    private void onParticipantLeft(LivekitWebhook.WebhookEvent event) {
        String identity = event.getParticipant().getIdentity();
        if (!isAgent(identity)) {
            log.warn("面试者 [{}] 离开了房间。可能发生了断网或手动关闭。", identity);
            // 逻辑：可以在这里开启一个延迟任务，检查 1 分钟后是否重连
        }
    }

    private void onRoomFinished(LivekitWebhook.WebhookEvent event) {
        log.info("房间 [{}] 已彻底关闭。正在进行收尾工作...", event.getRoom().getName());
        // 逻辑：清理缓存，统计面试时长等
    }

    // 简单的判断逻辑，假设你的 Agent Identity 包含 "agent" 字样
    private boolean isAgent(String identity) {
        return identity != null && identity.toLowerCase().contains("agent");
    }
}
