package org.buhuiqiming.fuchuang.config;

import io.livekit.server.WebhookReceiver;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class LiveKitConfig {

    private final String apiKey = System.getenv("LIVEKIT_API_KEY");
    private final String apiSecret = System.getenv("LIVEKIT_API_SECRET");
    @Bean
    public WebhookReceiver webhookReceiver() {

        if (apiKey == null || apiSecret == null) {
            throw new IllegalStateException("未检测到 LiveKit 环境变量，请检查配置！");
        }

        return new WebhookReceiver(apiKey, apiSecret);
    }
}