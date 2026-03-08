package org.buhuiqiming.fuchuang.entity;

import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

@Data
@NoArgsConstructor
public class MyMessage {
    private Long messageId;
    private Long sessionId;
    private String role;
    private String content;
    private String msgType;
    private String parentId;
    private Integer tokens;
    private LocalDateTime createTime;

}
