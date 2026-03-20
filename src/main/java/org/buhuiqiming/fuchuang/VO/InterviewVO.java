package org.buhuiqiming.fuchuang.VO;

import lombok.Data;

import java.time.Duration;
import java.util.List;
import java.util.Map;

@Data
public class InterviewVO {
    private String interviewId;
    private String jobRole;
    private String difficulty;
    private String mode;
    private Duration duration;
    private Integer score; // 对应实体类里的 totalScore
    // 具体层面的得分
    private Map<String, Integer> scoresDelta;
    private List<InterviewTurnsVO> turns;
}
