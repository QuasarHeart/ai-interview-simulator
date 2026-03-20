package org.buhuiqiming.fuchuang.versionOne;

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
        factory.setConnectTimeout((int) Duration.ofSeconds(5).toMillis()); // 连接超时 5 秒
        factory.setReadTimeout((int) Duration.ofSeconds(30).toMillis()); // 读取超时 30 秒

        return RestClient.builder()
                .requestFactory(factory)
                .baseUrl("http://localhost:8000/api/v1/interview") // ToDo 具体Python发布的域名或者本地运行
                .defaultHeader("Content-Type", "application/json")
                .build();
    }
}
