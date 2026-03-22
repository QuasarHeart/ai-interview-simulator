package org.buhuiqiming.fuchuang.dto;

import tools.jackson.databind.PropertyNamingStrategies;
import tools.jackson.databind.annotation.JsonNaming;
import lombok.Builder;
import lombok.Data;

@Data
@Builder
@JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
public class InterviewStartRequest {
    private String sessionId;
    private String jobPosition;
    private String resumeContent;
    private String jdSummary;
    private InterviewConfig interviewConfig;
    private FlowControl flowControl;

    @Data
    @Builder
    @JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
    public static class InterviewConfig{
        private String mode;
        private Boolean analyzeEmotion;
        private String interviewerStyle;
        private String companyContext;
        private String difficulty;
    }

    @Data
    @Builder
    @JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
    public static class FlowControl{
        private String stageTransition;
        private String targetStage;
    }

}
