package org.buhuiqiming.fuchuang.dto;

import lombok.Builder;
import lombok.Data;
import tools.jackson.databind.PropertyNamingStrategies;
import tools.jackson.databind.annotation.JsonNaming;

@Data
@Builder
@JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
public class GetTurnsJudgeRequest {
    private String sessionId;
    private Integer roundId;
    private InterviewConfig interviewConfig;
    private ContentToAnalyze contentToAnalyze;
    private String currentStage;

    @Data
    @Builder
    @JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
    public static class InterviewConfig {
        private String mode;
        private String companyContext;
        private String interviewerStyle;
        private Boolean analyzeEmotion;
        private String difficulty;
    }

    @Data
    @Builder
    @JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
    public static class ContentToAnalyze {
        private String question;
        private String userAnswer;
        private String jobPosition;
        private String jbSummary;
        private String historySummary;
        private String resumeContent;
    }
}
