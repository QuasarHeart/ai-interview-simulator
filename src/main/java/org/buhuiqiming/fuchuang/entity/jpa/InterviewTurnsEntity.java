package org.buhuiqiming.fuchuang.entity.jpa;

import jakarta.persistence.*;
import lombok.Data;
import org.buhuiqiming.fuchuang.dto.TurnEvaluationResult;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.type.SqlTypes;

import java.time.LocalDateTime;

/**
 * 用于记录面试中每一轮的相关信息
 */
@Entity
@Data
public class InterviewTurnsEntity {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    // 对应面试的Id
    @Column(nullable = false)
    private String interviewId;

    // 当前轮次
    @Column(nullable = false)
    private int turnNumber;

    // 当前轮次AI面试官的提问
    @Column(columnDefinition = "TEXT", nullable = false)
    private String question;

    // 当前轮次用户的回答
    // 文本和音频两种形式
    // ToDo 两者的具体存储形式
    @Column(columnDefinition = "TEXT")
    private String answerText;

    @Column
    private String answerVoice;

    // 评分维度
    // 评分维度：指定在数据库中以 JSON 格式存储
    @JdbcTypeCode(SqlTypes.JSON)
    @Column(columnDefinition = "json")
    private TurnEvaluationResult evaluationResult;

    // ================= 审计四元组 =================

    // 1. 创建人 (归属用户 ID) - 关联系统里的 User
    @Column
    private String userId;

    // 2. 创建时间 (一旦创建不可修改)
    @Column(nullable = false, updatable = false)
    private LocalDateTime createTime;

    // 3. 更新时间
    @Column(nullable = false)
    private LocalDateTime updateTime;

    // 4. 更新方 -- 一般为创建人
    @Column
    private String updateBy;

    @Column
    private String stageTransition;

    @Column
    private String targetStage;
    /**
     * 在数据第一次插入数据库之前 (INSERT)，JPA 会自动调用这个方法
     */
    @PrePersist
    protected void onCreate() {
        LocalDateTime now = LocalDateTime.now();
        this.createTime = now;
        this.updateTime = now;
    }

    /**
     * 在数据每次更新之前 (UPDATE)，JPA 会自动调用这个方法
     */
    @PreUpdate
    protected void onUpdate() {
        this.updateTime = LocalDateTime.now();
    }

    public InterviewTurnsEntity() {}

    public InterviewTurnsEntity(String interviewId, int turnNumber, String question, String answerText) {
        this.interviewId = interviewId;
        this.turnNumber = turnNumber;
        this.question = question;
        this.answerText = answerText;
    }
}
