package org.buhuiqiming.fuchuang.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import tools.jackson.databind.PropertyNamingStrategies;
import tools.jackson.databind.annotation.JsonNaming;

import java.util.List;

/**
 * 生成最终面试报告的请求体 DTO
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
public class GenerateReportRequest {

    private String sessionId;
    private String callbackUrl;
    private InterviewContext interviewContext;
    private List<RoundResult> roundResults;
    private InterviewConfig interviewConfig;

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    @JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
    public static class InterviewContext {
        private String jobPosition;
        private String jdSummary;
        private Integer totalRounds;
        private Integer interviewDurationSeconds;
        private String resumeContent;
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    @JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
    public static class RoundResult {
        private Integer roundId;
        private String currentStage;
        private DimensionScores dimensionScores;
        private DimensionDetails dimensionDetails;
        // ToDo 文档中 final_score 的类型是 string，这里严格按照文档映射为 String
        private String finalScore;
        private String overallFeedback;
        private List<String> improvementSuggestions;
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    @JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
    public static class DimensionScores {
        private Double professional;
        private Integer cognition;
        private Double expression;
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    @JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
    public static class DimensionDetails {
        private Professional professional;
        private Cognition cognition;
        private Expression expression;
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    @JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
    public static class Professional {
        private MetricDetail technicalCorrectness;
        private MetricDetail knowledgeMatch;
        private MetricDetail jobMatch;
        private MetricDetail engineeringPractice;
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    @JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
    public static class Cognition {
        private MetricDetail logicStructure;
        private MetricDetail problemSolving;
        private MetricDetail systemThinking;
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    @JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
    public static class Expression {
        private MetricDetail clarity;
        private MetricDetail confidenceStability;
        private MetricDetail professionalMaturity;
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    @JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
    public static class MetricDetail {
        private String reason;
        private Integer score;
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    @JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
    public static class InterviewConfig {
        private String mode;
        private Boolean analyzeEmotion;
        private String interviewerStyle;
        private String companyContext;
        private String difficulty;
    }
}