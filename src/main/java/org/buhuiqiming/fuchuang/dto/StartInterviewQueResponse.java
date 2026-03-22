package org.buhuiqiming.fuchuang.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;

@Data
public class StartInterviewQueResponse {
    @JsonProperty("session_id")
    private String sessionId;
    @JsonProperty("round_id")
    private Integer roundId;
    private String question;
    @JsonProperty("flow_control")
    private FlowControl flowControl;

    @Data
    public static class FlowControl {
        @JsonProperty("stage_transition")
        private String stageTransition;
        @JsonProperty("target_stage")
        private String targetStage;
    }
}
