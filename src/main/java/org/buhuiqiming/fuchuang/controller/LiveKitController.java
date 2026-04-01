package org.buhuiqiming.fuchuang.controller;

import io.livekit.server.WebhookReceiver;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestHeader;

@PostMapping("/livekit/webhook")
public void LiveKitController(@RequestHeader("Authorization") String auth, @RequestBody String body) {
    WebhookReceiver receiver = new WebhookReceiver(apiKey, apiSecret);
    WebhookEvent event = receiver.receive(body, auth);

    // 监听 AI 是否成功“自动进入”了房间
    if ("participant_joined".equals(event.getEvent())) {
        String identity = event.getParticipant().getIdentity();
        if (identity.startsWith("ai_agent")) { // 假设你在 Python 端定义的 ID
            System.out.println("业务通知：AI 面试官已就位，面试正式开始！");
        }
    }

    // 监听面试结束
    if ("room_finished".equals(event.getEvent())) {
        // 更新数据库，标记面试已完成，触发 AI 生成评价报告
        saveInterviewResult(event.getRoom().getName());
    }
}