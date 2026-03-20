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
    private FlowControl flowControl;

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
        private String resumeSummary;
        private String jdSummary;
    }

    @Data
    @Builder
    @JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
    public static class HistoryData {
        private String historySummary;
        private List<HistoryItem> recentHistory; // 如果有具体结构可以再建个类

        @Data
        @Builder
        @JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
        public static class HistoryItem {
            private String role; // assistant, user
            private String content;
        }
    }

    @Data
    @Builder
    @JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
    public static class FlowControl {
        private String stageTransition; // continue, switch, end
        private String targetStage;      // intro, resume_deep_dive, etc.
    }
}
