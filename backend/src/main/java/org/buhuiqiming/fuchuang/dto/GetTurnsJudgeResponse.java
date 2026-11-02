package org.buhuiqiming.fuchuang.dto;

import lombok.Data;
import tools.jackson.databind.PropertyNamingStrategies;
import tools.jackson.databind.annotation.JsonNaming;

@Data
@JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
public class GetTurnsJudgeResponse {
    private String sessionId;
    private Integer roundId;
    private String question;
    private String userAnswer;
    private TurnEvaluationResult analysis;

}
