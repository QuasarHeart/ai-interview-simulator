package org.buhuiqiming.fuchuang.config;

import lombok.extern.slf4j.Slf4j;
import org.buhuiqiming.fuchuang.service.EvaluationStreamConsumer;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.redis.connection.RedisConnectionFactory;
import org.springframework.data.redis.connection.stream.Consumer;
import org.springframework.data.redis.connection.stream.MapRecord;
import org.springframework.data.redis.connection.stream.ReadOffset;
import org.springframework.data.redis.connection.stream.StreamOffset;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.data.redis.stream.StreamMessageListenerContainer;
import org.springframework.data.redis.stream.StreamMessageListenerContainer.StreamMessageListenerContainerOptions;
import org.springframework.data.redis.stream.Subscription;

import java.time.Duration;
import java.util.concurrent.Executors;

@Slf4j
@Configuration
public class RedisStreamConfig {

    public static final String EVAL_STREAM_KEY = "interview:eval:stream";
    public static final String EVAL_GROUP_NAME = "interview-eval-group";

    @Bean
    public StreamMessageListenerContainer<String, MapRecord<String, String, String>> streamMessageListenerContainer(
            RedisConnectionFactory connectionFactory,
            StringRedisTemplate stringRedisTemplate,
            EvaluationStreamConsumer streamConsumer) {

        // 初始化 Stream 和 Consumer Group
        initStreamAndGroup(stringRedisTemplate);

        // 配置监听器容器
        StreamMessageListenerContainerOptions<String, MapRecord<String, String, String>> options =
                StreamMessageListenerContainerOptions.builder()
                        .pollTimeout(Duration.ofSeconds(2)) // 如果没消息，最多等2秒再问一次
                        .executor(Executors.newVirtualThreadPerTaskExecutor())
                        .build();

        StreamMessageListenerContainer<String, MapRecord<String, String, String>> container =
                StreamMessageListenerContainer.create(connectionFactory, options);

        // 配置消费者：以组成员的身份，只读取最新分配给自己的消息 (">" 符号)
        Subscription subscription = container.receive(
                Consumer.from(EVAL_GROUP_NAME, "worker-" + System.currentTimeMillis()),
                StreamOffset.create(EVAL_STREAM_KEY, ReadOffset.lastConsumed()),
                streamConsumer
        );

        // 启动容器
        container.start();
        return container;
    }

    private void initStreamAndGroup(StringRedisTemplate stringRedisTemplate) {
        try {
            if (Boolean.FALSE.equals(stringRedisTemplate.hasKey(EVAL_STREAM_KEY))) {
                stringRedisTemplate.opsForStream().createGroup(EVAL_STREAM_KEY, EVAL_GROUP_NAME);
                log.info("成功创建 Redis Stream 和 Consumer Group: {}", EVAL_STREAM_KEY);
            } else {
                stringRedisTemplate.opsForStream().createGroup(EVAL_STREAM_KEY, EVAL_GROUP_NAME);
            }
        } catch (Exception e) {
            log.info("Consumer Group 已存在或初始化跳过: {}", e.getMessage());
        }
    }
}