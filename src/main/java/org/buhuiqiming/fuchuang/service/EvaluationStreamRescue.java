package org.buhuiqiming.fuchuang.service;

import lombok.extern.slf4j.Slf4j;
import org.buhuiqiming.fuchuang.config.RedisStreamConfig;
import org.buhuiqiming.fuchuang.entity.jpa.InterviewTurnsEntity;
import org.buhuiqiming.fuchuang.repository.InterviewTurnsRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Range;
import org.springframework.data.redis.connection.stream.MapRecord;
import org.springframework.data.redis.connection.stream.PendingMessage;
import org.springframework.data.redis.connection.stream.PendingMessages;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

import java.time.Duration;
import java.util.List;

@Slf4j
@Component
public class EvaluationStreamRescue {
    private final StringRedisTemplate stringRedisTemplate;
    private final InterviewService interviewService;
    private final InterviewTurnsRepository interviewTurnsRepository;

    @Autowired
    public EvaluationStreamRescue(StringRedisTemplate stringRedisTemplate, InterviewService interviewService, InterviewTurnsRepository interviewTurnsRepository) {
        this.interviewTurnsRepository = interviewTurnsRepository;
        this.stringRedisTemplate = stringRedisTemplate;
        this.interviewService = interviewService;
    }

    private static final int MAX_RETRY_COUNT = 3; // 最大重试次数
    private static final long MAX_IDLE_MINUTES = 2; // 消息超过2分钟未ACK视为失败
    private static final long UP_TO_DELETE_MINUTES = 60; // 消息超过60分钟未ACK就直接删了

    /**
     * 每隔 1 分钟执行一次救援任务
     */
    @Scheduled(fixedDelay = 120000)
    public void rescuePendingMessages() {
        log.info("开始执行 Redis Stream PEL 救援任务...");

        try {
            // 查询 PEL 中最早的 10 条未 ACK 消息
            PendingMessages pendingMessages = stringRedisTemplate.opsForStream().pending(
                    RedisStreamConfig.EVAL_STREAM_KEY,
                    RedisStreamConfig.EVAL_GROUP_NAME,
                    Range.unbounded(),
                    10L
            );

            if (pendingMessages.isEmpty()) {
                log.debug("PEL 为空，没有需要救援的消息。");
                return;
            }

            for (PendingMessage pendingMessage : pendingMessages) {
                // 检查消息的空闲时间
                if (pendingMessage.getElapsedTimeSinceLastDelivery().compareTo(Duration.ofMinutes(MAX_IDLE_MINUTES)) > 0) {
                    String messageId = pendingMessage.getIdAsString();
                    long deliveryCount = pendingMessage.getTotalDeliveryCount();
                    boolean isTimeout = pendingMessage.getElapsedTimeSinceLastDelivery().compareTo(Duration.ofMinutes(UP_TO_DELETE_MINUTES)) > 0;

                    // 处理“毒药消息” (Poison Pill)：重试次数过多，放弃治疗
                    if (deliveryCount >= MAX_RETRY_COUNT || isTimeout) {
                        log.error("消息 {} 重试超过 {} 次，视为毒药消息，开始查询原始数据！", messageId, MAX_RETRY_COUNT);

                        // 根据 ID 去 Stream 里精确查找这条消息
                        List<MapRecord<String, Object, Object>> originalMessages = stringRedisTemplate.opsForStream().range(
                                RedisStreamConfig.EVAL_STREAM_KEY,
                                Range.closed(messageId, messageId) // 闭区间，只查这一个ID
                        );

                        if (originalMessages != null && !originalMessages.isEmpty()) {
                            // 拿到原始数据，解析参数
                            MapRecord<String, Object, Object> record = originalMessages.get(0);
                            String interviewId = (String) record.getValue().get("interviewId");
                            int turnNumber = Integer.parseInt((String) record.getValue().get("turnNumber"));

                            handlePoisonMessage(interviewId, turnNumber, messageId);
                        } else {
                            // 极端异常情况：PEL里有它，但Stream原队列里已经没它了
                            log.warn("毒药消息 {} 的原始数据丢失，直接进行 ACK 清理", messageId);
                            stringRedisTemplate.opsForStream().acknowledge(RedisStreamConfig.EVAL_STREAM_KEY, RedisStreamConfig.EVAL_GROUP_NAME, messageId);
                        }
                        continue;
                    }

                    // 使用 XCLAIM 认领消息并重新读取数据
                    log.info("认领超时消息 ID: {}, 已重试次数: {}", messageId, deliveryCount);
                    List<MapRecord<String, Object, Object>> claimedMessages = stringRedisTemplate.opsForStream().claim(
                            RedisStreamConfig.EVAL_STREAM_KEY,
                            RedisStreamConfig.EVAL_GROUP_NAME,
                            "rescuer-" + System.currentTimeMillis(), // 救援者作为新的消费者身份
                            Duration.ofMinutes(MAX_IDLE_MINUTES),
                            pendingMessage.getId()
                    );

                    // 重新执行消费逻辑
                    if (claimedMessages != null && !claimedMessages.isEmpty()) {
                        for (MapRecord<String, Object, Object> record : claimedMessages) {
                            String interviewId = (String) record.getValue().get("interviewId");
                            String turnNumberStr = (String) record.getValue().get("turnNumber");

                            log.info("开始重试执行评价任务: interviewId={}, turn={}", interviewId, turnNumberStr);

                            try {
                                interviewService.processEvaluationTask(interviewId, Integer.parseInt(turnNumberStr), messageId);

                                log.info("重试成功，已 ACK。");
                            } catch (Exception e) {
                                log.error("重试依然失败: {}", e.getMessage());
                                // 抛出异常后，它会继续留在 PEL 里，等待下一次被捞起，直到触发 MAX_RETRY_COUNT
                            }
                        }
                    }
                }
            }
        } catch (Exception e) {
            log.error("执行救援任务时发生异常", e);
        }
    }

    /**
     * 处理无法抢救的毒药消息
     */
    private void handlePoisonMessage(String interviewId, int turnNumber, String messageId) {
        InterviewTurnsEntity turn = interviewTurnsRepository.findByInterviewIdAndTurnNumber(interviewId, turnNumber);

        if (turn != null && turn.getEvaluationResult() == null) {
            // 修改 targetStage 绕过死锁统计
            turn.setTargetStage("failedEvaluation");
            interviewTurnsRepository.save(turn);
            log.warn("毒药消息处理：已将 interviewId: {}, turn: {} 标记为 failedEvaluation", interviewId, turnNumber);

            // 尝试触发生成报告 (因为上面改了状态，此时 countUnEvaluatedTurns 可能会归零，从而触发报告生成)
            interviewService.tryTriggerReportGeneration(interviewId);
        }

        // 将这颗毒药从 PEL 中 ACK 掉并删除，防止永远卡在这里
        stringRedisTemplate.opsForStream().acknowledge(
                RedisStreamConfig.EVAL_STREAM_KEY,
                RedisStreamConfig.EVAL_GROUP_NAME,
                messageId
        );
        stringRedisTemplate.opsForStream().delete(RedisStreamConfig.EVAL_STREAM_KEY, messageId);
        log.info("毒药消息 {} 已被强制 ACK 并清除", messageId);
    }

}
