package org.buhuiqiming.fuchuang.VO;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.Map;

@Data
public class InterviewVO {
    private String interviewId;
    private String jobRole;
    private String difficulty;
    private String mode;
    private Long duration;
    private float score; // 对应实体类里的 totalScore
    private String startTime;
}
