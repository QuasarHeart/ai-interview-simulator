package org.buhuiqiming.fuchuang.VO;

import lombok.Data;

@Data
public class InterviewTurnsVO {
    // 轮次编号
    private int turnNumber;

    // 用户的回答内容
    private String userContent;

    // AI 面试官的提问内容
    private String assistantContent;
}