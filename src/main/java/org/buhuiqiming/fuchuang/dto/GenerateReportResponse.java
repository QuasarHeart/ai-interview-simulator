package org.buhuiqiming.fuchuang.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import tools.jackson.databind.PropertyNamingStrategies;
import tools.jackson.databind.annotation.JsonNaming;

import java.util.List;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
public class GenerateReportResponse {
    private String hiringRecommendation;
    private float overallScore;
    private String executiveSummary;
    private List<String> strengths;
    private List<String> weaknesses;
    private String abilityTrend;
    private String detailedRecommendation;
    
    private Professional professional;
    private Cognition cognition;
    private Expression expression;

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
    
}
