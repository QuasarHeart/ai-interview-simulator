package org.buhuiqiming.fuchuang.VO;

import lombok.Builder;
import lombok.Data;
import org.buhuiqiming.fuchuang.dto.GenerateReportRequest;
import org.buhuiqiming.fuchuang.dto.TurnEvaluationResult;
import tools.jackson.databind.PropertyNamingStrategies;
import tools.jackson.databind.annotation.JsonNaming;

import java.io.Serializable;
import java.util.List;

@Data
@Builder
public class ReportResultVO {
    private String hiringRecommendation;
    private float overallScore;
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
    public static class Professional implements Serializable {
        private int technicalCorrectness;  
        private int knowledgeMatch;        
        private int jobMatch;              
        private int engineeringPractice;   
    }

    @Data
    @Builder
    public static class Cognition implements Serializable {
        private int logicStructure;        
        private int problemSolving;        
        private int systemThinking;        
    }

    @Data
    @Builder
    public static class Expression implements Serializable {
        private int clarity;               
        private int confidenceStability;   
        private int professionalMaturity;  
    }

    private String executiveSummary;
    private List<String> strengths;
    private List<String> weaknesses;
    private String abilityTrend;
    private String detailedRecommendation;
}
