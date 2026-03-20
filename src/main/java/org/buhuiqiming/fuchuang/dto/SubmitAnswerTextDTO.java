package org.buhuiqiming.fuchuang.dto;

import lombok.Data;


public class SubmitAnswerTextDTO {
    private String type; // 前端传的 "text"

    private String content; // 前端传的具体文本

    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }

    public String getContent() {
        return content;
    }

    public void setContent(String content) {
        this.content = content;
    }

    @Override
    public String toString(){
        return "type:"+type+", content:"+content;
    }
}

