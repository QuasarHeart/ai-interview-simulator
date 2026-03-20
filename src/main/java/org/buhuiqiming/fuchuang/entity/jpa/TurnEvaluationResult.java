package org.buhuiqiming.fuchuang.entity.jpa;

import lombok.Data;
import reactor.netty.channel.MeterKey;

import java.io.Serializable;

/**
 * 专门用于映射 InterviewTurnsEntity 中 evaluationResult 字段的 JSON 结构
 */
@Data
public class TurnEvaluationResult implements Serializable {

    private DimensionScores dimensionScores;
    private DimensionDetails dimensionDetails;

    @Data
    public static class DimensionScores implements Serializable {
        private Double professional;
        private Integer cognition;
        private Double expression;
    }

    @Data
    public static class DimensionDetails implements Serializable {
        private ProfessionalDetails professional;
        private CognitionDetails cognition;
        private ExpressionDetails expression;
    }

    @Data
    public static class ProfessionalDetails implements Serializable {
        private MetricDetail technicalCorrectness;
        private MetricDetail knowledgeMatch;
        private MetricDetail jobMatch;
        private MetricDetail engineeringPractice;
    }

    @Data
    public static class CognitionDetails implements Serializable {
        private MetricDetail logicStructure;
        private MetricDetail problemSolving;
        private MetricDetail systemThinking;
    }

    @Data
    public static class ExpressionDetails implements Serializable {
        private MetricDetail clarity;
        private MetricDetail confidence_stability;
        private MetricDetail professional_maturity;
    }

    @Data
    public static class MetricDetail implements Serializable {
        private Double score;
        private String reason;
    }
}