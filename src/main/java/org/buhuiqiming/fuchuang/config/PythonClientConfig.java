package org.buhuiqiming.fuchuang.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.client.SimpleClientHttpRequestFactory;
import org.springframework.web.client.RestClient;

import java.time.Duration;

@Configuration
public class PythonClientConfig {

    @Bean
    public RestClient pythonClient(){
        SimpleClientHttpRequestFactory factory = new SimpleClientHttpRequestFactory();
        factory.setConnectTimeout((int) Duration.ofSeconds(300).toMillis()); // 连接超时 5 秒
        factory.setReadTimeout((int) Duration.ofSeconds(300).toMillis()); // 读取超时 30 秒

        return RestClient.builder()
                .requestFactory(factory)
                .baseUrl("https://ml.feixingxr.com/api/v1/interview")
                .defaultHeader("Content-Type", "application/json")
                .build();
    }
}
