package org.buhuiqiming.fuchuang.dto;

import lombok.Data;

@Data
public class CreateInterviewDTO {
    // 岗位类型
    private String jobRole;

    // 难度(easy, mid , hard)
    private String difficulty;

    // 输入模式(text, voice)
    private String mode;

    // 职位描述
    private String jobInfo;

    // 面试官风格
    private String interviewerStyle;

    // 公司简述
    private String companyContext;
}
