package org.buhuiqiming.fuchuang.VO;

import lombok.Data;

@Data
public class InterviewVO {
    private String interviewId;
    private String jobRole;
    private String difficulty;
    private String mode;
    private Long duration;
    private String interviewStatus;
    private float score; // 对应实体类里的 totalScore
    private String startTime;
}
