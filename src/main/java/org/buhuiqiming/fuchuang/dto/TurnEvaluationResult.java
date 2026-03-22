package org.buhuiqiming.fuchuang.dto;

import lombok.Data;
import tools.jackson.databind.PropertyNamingStrategies;
import tools.jackson.databind.annotation.JsonNaming;

import java.io.Serializable;
import java.util.List;

/**
 * 专门用于映射 InterviewTurnsEntity 中 evaluationResult 字段的 JSON 结构
 */
@Data
@JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
public class TurnEvaluationResult implements Serializable {

    private ProfessionalDetails professional;
    private CognitionDetails cognition;
    private ExpressionDetails expression;
    private DimensionScores dimensionScores;
    private float finalScore;
    private String overallFeedback;
    private List<String> improvementSuggestions;

    @Data
    public static class DimensionScores implements Serializable {
        private float professional;
        private float cognition;
        private float expression;
    }

    @Data
    @JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
    public static class ProfessionalDetails implements Serializable {
        private MetricDetail technicalCorrectness;
        private MetricDetail knowledgeMatch;
        private MetricDetail jobMatch;
        private MetricDetail engineeringPractice;
    }

    @Data
    @JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
    public static class CognitionDetails implements Serializable {
        private MetricDetail logicStructure;
        private MetricDetail problemSolving;
        private MetricDetail systemThinking;
    }

    @Data
    @JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
    public static class ExpressionDetails implements Serializable {
        private MetricDetail clarity;
        private MetricDetail confidenceStability;
        private MetricDetail professionalMaturity;
    }

    @Data
    public static class MetricDetail implements Serializable {
        private Integer score;
        private String reason;
    }
}