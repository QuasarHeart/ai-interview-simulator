package org.buhuiqiming.fuchuang.VO;

import lombok.Builder;
import lombok.Data;

import java.util.List;

@Data
@Builder
public class GrowthCurveVO {
    private String jobRole;
    private float overallRating;
    private int interviewCount;
    private float bestScore;
    private float practiceTime;
    private List<Float> growthPoints;
    private List<String> strengths;
    private List<String> weaknesses;
    private DimensionDetails dimensionDetails;
    private DimensionScores dimensionScores;

    @Data
    @Builder
    public static class DimensionScores{
        private float professional;
        private float cognition;
        private float expression;
    }

    @Data
    @Builder
    public static class DimensionDetails{
        private Professional professional;
        private Cognition cognition;
        private Expression expression;
    }

    @Data
    @Builder
    public static class Professional {
        private  float technicalCorrectness;
        private  float knowledgeMatch;
        private  float jobMatch;
        private  float engineeringPractice;
    }

    @Data
    @Builder
    public static class Cognition {
        private  float logicStructure;
        private  float problemSolving;
        private  float systemThinking;
    }

    @Data
    @Builder
    public static class Expression {
        private  float clarity;
        private  float confidenceStability;
        private  float professionalMaturity;
    }
    

}
