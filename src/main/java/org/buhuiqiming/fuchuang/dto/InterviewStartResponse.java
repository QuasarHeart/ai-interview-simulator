package org.buhuiqiming.fuchuang.dto;

import tools.jackson.databind.annotation.JsonNaming;
import lombok.Data;
import tools.jackson.databind.PropertyNamingStrategies;

@Data
@JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
public class InterviewStartResponse {
    private String sessionId;
    private Integer roundId;
    private String question;
    private FlowControl flowControl;

    @Data
    @JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
    public static class FlowControl {
        private String stageTransition;
        private String targetStage;
    }
}