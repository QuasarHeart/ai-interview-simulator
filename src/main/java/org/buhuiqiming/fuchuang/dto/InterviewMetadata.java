package org.buhuiqiming.fuchuang.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.buhuiqiming.fuchuang.entity.jpa.InterviewEntity;
import org.buhuiqiming.fuchuang.mapper.UserMapper;
import org.springframework.beans.factory.annotation.Autowired;
import tools.jackson.databind.ObjectMapper;
import tools.jackson.databind.PropertyNamingStrategies;
import tools.jackson.databind.annotation.JsonNaming;

@Data
@AllArgsConstructor
@NoArgsConstructor
@JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
public class InterviewMetadata {
    private String sessionId;
    private String jobPosition;
    private String jdSummary;
    private String resumeContent;
    private InterviewConfig interviewConfig;
    @Autowired
    private UserMapper userMapper;
    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    @JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
    public static class InterviewConfig {
        private String mode;             // video / audio
        private String interviewerStyle; // expert / friendly
        private String difficulty;       // easy / hard
        private String companyContext;
        private boolean enableVideo;
    }

    // 辅助方法：快速转为 JSON 字符串
    public String toJson() {
        return new ObjectMapper().writeValueAsString(this);
    }
    public InterviewMetadata(InterviewEntity interviewEntity){
        this.sessionId = interviewEntity.getInterviewId();
        this.jobPosition = interviewEntity.getJobRole();
        this.jdSummary = interviewEntity.getJobInfo();
        this.resumeContent = userMapper.getVitaContent(interviewEntity.getUserId());
        this.interviewConfig = InterviewConfig.builder()
                .mode(interviewEntity.getMode())
                .interviewerStyle(interviewEntity.getInterviewerStyle())
                .difficulty(interviewEntity.getDifficulty())
                .companyContext(interviewEntity.getCompanyContext())
                .enableVideo(true)
                .build();
    }
}
