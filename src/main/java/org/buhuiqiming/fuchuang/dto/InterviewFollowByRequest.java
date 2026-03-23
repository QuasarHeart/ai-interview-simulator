package org.buhuiqiming.fuchuang.dto;

import tools.jackson.databind.PropertyNamingStrategies;
import tools.jackson.databind.annotation.JsonNaming;
import lombok.Builder;
import lombok.Data;
import java.util.List;

@Data
@Builder
@JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
public class InterviewFollowByRequest {
    private String sessionId;
    private Integer roundId;
    private InterviewConfig interviewConfig;
    private Background background;
    private HistoryData historyData;

    @Data
    @Builder
    @JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
    public static class InterviewConfig {
        private String mode; // 固定 "text"
        private String companyContext;
        private String interviewerStyle; // standard, friendly, aggressive, expert
        private Boolean analyzeEmotion;
        private String difficulty;
    }

    @Data
    @Builder
    @JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
    public static class Background {
        private String jobPosition;
        private String resumeContent;
        private String jdSummary;
    }

    @Data
    @Builder
    @JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
    public static class HistoryData {
        private String historySummary;
        private List<HistoryItem> recentHistory;

        @Data
        @Builder
        @JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
        public static class HistoryItem {
            private Integer roundId;
            private String assistantContent; // assistant, user
            private String userContent;
            private FlowControl flowControl;

            @Data
            @Builder
            @JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
            public static class FlowControl {
                private String stageTransition; // continue, switch, end
                private String targetStage;      // intro, resume_deep_dive, etc.
            }
        }
    }


}
