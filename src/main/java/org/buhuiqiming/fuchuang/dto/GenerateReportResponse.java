package org.buhuiqiming.fuchuang.dto;

import jakarta.persistence.Column;
import lombok.Builder;
import lombok.Data;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.type.SqlTypes;
import tools.jackson.databind.PropertyNamingStrategies;
import tools.jackson.databind.annotation.JsonNaming;

import java.util.List;

@Data
@Builder
@JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
public class GenerateReportResponse {
    private String hiringRecommendation;
    private float overallScore;
    private String executiveSummary;
    private List<String> strengths;
    private List<String> weaknesses;
    private String abilityTrend;
    private String detailedRecommendation;
}
