package org.buhuiqiming.fuchuang.entity.jpa;

import jakarta.persistence.*;
import lombok.Data;
import org.buhuiqiming.fuchuang.dto.TurnEvaluationResult;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.type.SqlTypes;

import java.time.Duration;
import java.time.LocalDateTime;

@Entity
@Data
@Table(name = "interview_session")
public class InterviewEntity {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(unique = true, nullable = false)
    private String interviewId;

    // 岗位名称
    @Column(nullable = false)
    private String jobRole;

    // 难度
    @Column(nullable = false)
    private String difficulty;

    // 面试模式 （text / video）
    @Column(nullable = false)
    private String mode;

    // 会话状态: CREATED, RUNNING, FINISHED, REPORTING(正在生成报告), REPORTED(已经生成报告)
    @Column(nullable = false)
    private String interviewStatus;
    // CREATED -> RUNNING -> FINISHED -> REPORTING -> REPORTED

    // 简历总结
    @Column
    private String resumeSummary;

    // 上传简历Id
    @Column(unique = true)
    private String resumeAssetId;

    // 存储简历地址 / 云存储URL
    @Column(unique = true)
    private String resumeAssetAddress;

    // 目前面试轮次
    @Column
    private int turnsNumber;

    // 最终综合评分
    @Column
    private int totalScore;

    // 早期对话总结
    @Column
    private String historySummary;

    // 面试状态记录
    @Column
    private String stageTransition; // 阶段转换指令
    @Column
    private String targetStage; // 目标阶段

    // 具体提升建议
    @Column(columnDefinition = "TEXT")
    private String advice;

    // 相关推荐资料
    @Column
    private String learningAssetAddress;

    // 面试持续时间
    @Column
    private Duration duration;

    // 最终用于展示的评分记录
    // 评分维度：指定在数据库中以 JSON 格式存储
    @JdbcTypeCode(SqlTypes.JSON)
    @Column(columnDefinition = "json")
    private TurnEvaluationResult totalEvaluation;

    // ================= 审计四元组 =================

    // 1. 创建人 (归属用户 ID) - 关联系统里的 User
    @Column()
    private String userId;

    // 2. 创建时间 (一旦创建不可修改)，可作为面试开始时间
    @Column(nullable = false, updatable = false)
    private LocalDateTime createTime;

    // 3. 更新时间
    @Column(nullable = false)
    private LocalDateTime updateTime;

    // 4. 更新方 -- 一般为创建人
    @Column()
    private String updateBy;

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

    public InterviewEntity() {}

    public InterviewEntity(String interviewId, String jobRole, String difficulty, String mode, String interviewStatus) {
        this.interviewId = interviewId;
        this.jobRole = jobRole;
        this.difficulty = difficulty;
        this.mode = mode;
        this.interviewStatus = interviewStatus;
        this.turnsNumber = 0;
    }

}
