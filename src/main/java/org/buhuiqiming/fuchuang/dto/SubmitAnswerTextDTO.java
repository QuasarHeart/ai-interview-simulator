package org.buhuiqiming.fuchuang.dto;

import lombok.Data;

@Data
public class SubmitAnswerTextDTO {
    private String type; // 前端传的 "text"

    private String content; // 前端传的具体文本
}

