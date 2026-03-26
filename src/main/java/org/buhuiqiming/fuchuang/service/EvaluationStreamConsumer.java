package org.buhuiqiming.fuchuang.service;

import lombok.extern.slf4j.Slf4j;
import org.buhuiqiming.fuchuang.entity.jpa.InterviewEntity;
import org.buhuiqiming.fuchuang.entity.jpa.InterviewTurnsEntity;
import org.buhuiqiming.fuchuang.mapper.UserMapper;
import org.buhuiqiming.fuchuang.repository.InterviewTurnsRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.connection.stream.MapRecord;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.data.redis.stream.StreamListener;
import org.springframework.stereotype.Component;

@Slf4j
@Component
public class EvaluationStreamConsumer implements StreamListener<String, MapRecord<String, String, String>> {

    @Autowired
    private InterviewService interviewService;
    @Autowired
    private InterviewTurnsRepository interviewTurnsRepository;
    @Autowired
    private UserMapper userMapper;
    @Autowired
    private StringRedisTemplate stringRedisTemplate;

    @Override
    public void onMessage(MapRecord<String, String, String> message) {
        String interviewId = message.getValue().get("interviewId");
        int turnNumber = Integer.parseInt(message.getValue().get("turnNumber"));

        log.info("MQ 消费者接单: 开始执行评价任务, interviewId: {}, turnNumber: {}", interviewId, turnNumber);

        try {
            InterviewEntity interview = interviewService.getInterviewOrElseThrow(interviewId);
            InterviewTurnsEntity turn = interviewTurnsRepository.findByInterviewIdAndTurnNumber(interviewId, turnNumber);
            String resumeContent = userMapper.getVitaContent(interview.getUserId());

            interviewService.getTurnsJudgement(interview, turn, resumeContent);

            interviewTurnsRepository.save(turn);

            // 通知 Redis 任务结束，清除对应 PEL
            stringRedisTemplate.opsForStream().acknowledge("interview-eval-group", message);
            log.info("MQ 消费者完工并 ACK: interviewId: {}, turnNumber: {}", interviewId, turnNumber);
            stringRedisTemplate.opsForStream().delete("interview:eval:stream", message.getId());

            // 尝试生成报告
            interviewService.tryTriggerReportGeneration(interviewId);

        } catch (Exception e) {
            log.error("MQ 消费者执行评价异常, interviewId: {}, turnNumber: {}", interviewId, turnNumber, e);
            // 抛出异常后，这条消息会被留在 Redis 的 PEL 里，等待救援机制重试。
        }
    }
}