package org.buhuiqiming.fuchuang.entity;

import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

@Data
@NoArgsConstructor
public class MySession {
    private Long sessionId;
    private Long userId;
    private String title;
    private String sessionType;
    private Long latestSummaryId;
    private LocalDateTime createTime;
}
