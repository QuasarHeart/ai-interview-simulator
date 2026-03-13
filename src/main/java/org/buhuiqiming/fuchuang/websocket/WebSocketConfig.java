package org.buhuiqiming.fuchuang.websocket;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.socket.config.annotation.EnableWebSocket;
import org.springframework.web.socket.config.annotation.WebSocketConfigurer;
import org.springframework.web.socket.config.annotation.WebSocketHandlerRegistry;
import org.springframework.web.socket.server.standard.ServletServerContainerFactoryBean;

@EnableWebSocket
@Configuration
public class WebSocketConfig implements WebSocketConfigurer {

    @Autowired
    private AudioInterviewHandler audioInterviewHandler;

    @Autowired
    private WebSocketAuthInterceptor webSocketAuthInterceptor;

    @Override
    public void registerWebSocketHandlers(WebSocketHandlerRegistry registry){
        registry.addHandler(audioInterviewHandler, "/ws/interview/audio")
                .addInterceptors(webSocketAuthInterceptor)
                .setAllowedOrigins("*"); // ToDo 测试需要允许所有来源，后续需指定域名
    }

    @Bean
    public ServletServerContainerFactoryBean createWebSocketContainer() {
        ServletServerContainerFactoryBean container = new ServletServerContainerFactoryBean();
        // 设置文本消息最大限制 (1MB)
        container.setMaxTextMessageBufferSize(1024 * 1024);
        // 设置二进制消息最大限制 (10MB，足够容纳好几分钟的连续清晰语音流)
        container.setMaxBinaryMessageBufferSize(10 * 1024 * 1024);
        return container;
    }
}
