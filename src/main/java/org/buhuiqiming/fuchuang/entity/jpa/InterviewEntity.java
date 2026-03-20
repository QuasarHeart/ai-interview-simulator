package org.buhuiqiming.fuchuang.entity.jpa;

import jakarta.persistence.*;
import lombok.Data;

import java.time.Duration;
import java.time.LocalDateTime;

@Entity
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

    // 会话状态: CREATED, RUNNING, FINISHED
    @Column(nullable = false)
    private String interviewStatus;

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

    // ======= 该轮次回答的各维度具体评分 ========
    /**
     * 具体内容的相关评分维度
     */
    // 技术正确性
    @Column
    private int correctness;

    // 知识深度
    @Column
    private int profundity;

    // 逻辑严谨性
    @Column
    private int rigour;

    // 岗位匹配度
    @Column
    private int fit;

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


    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getInterviewId() {
        return interviewId;
    }

    public void setInterviewId(String interviewId) {
        this.interviewId = interviewId;
    }

    public String getJobRole() {
        return jobRole;
    }

    public void setJobRole(String jobRole) {
        this.jobRole = jobRole;
    }

    public String getDifficulty() {
        return difficulty;
    }

    public void setDifficulty(String difficulty) {
        this.difficulty = difficulty;
    }

    public String getMode() {
        return mode;
    }

    public void setMode(String mode) {
        this.mode = mode;
    }

    public String getInterviewStatus() {
        return interviewStatus;
    }

    public void setInterviewStatus(String interviewStatus) {
        this.interviewStatus = interviewStatus;
    }

    public String getResumeSummary() {
        return resumeSummary;
    }

    public void setResumeSummary(String resumeSummary) {
        this.resumeSummary = resumeSummary;
    }

    public String getResumeAssetId() {
        return resumeAssetId;
    }

    public void setResumeAssetId(String resumeAssetId) {
        this.resumeAssetId = resumeAssetId;
    }

    public String getResumeAssetAddress() {
        return resumeAssetAddress;
    }

    public void setResumeAssetAddress(String resumeAssetAddress) {
        this.resumeAssetAddress = resumeAssetAddress;
    }

    public int getTurnsNumber() {
        return turnsNumber;
    }

    public void setTurnsNumber(int turnsNumber) {
        this.turnsNumber = turnsNumber;
    }

    public int getTotalScore() {
        return totalScore;
    }

    public void setTotalScore(int totalScore) {
        this.totalScore = totalScore;
    }

    public String getHistorySummary() {
        return historySummary;
    }

    public void setHistorySummary(String historySummary) {
        this.historySummary = historySummary;
    }

    public String getStageTransition() {
        return stageTransition;
    }

    public void setStageTransition(String stageTransition) {
        this.stageTransition = stageTransition;
    }

    public String getTargetStage() {
        return targetStage;
    }

    public void setTargetStage(String targetStage) {
        this.targetStage = targetStage;
    }

    public String getAdvice() {
        return advice;
    }

    public void setAdvice(String advice) {
        this.advice = advice;
    }

    public String getLearningAssetAddress() {
        return learningAssetAddress;
    }

    public void setLearningAssetAddress(String learningAssetAddress) {
        this.learningAssetAddress = learningAssetAddress;
    }

    public Duration getDuration() {
        return duration;
    }

    public void setDuration(Duration duration) {
        this.duration = duration;
    }

    public int getCorrectness() {
        return correctness;
    }

    public void setCorrectness(int correctness) {
        this.correctness = correctness;
    }

    public int getProfundity() {
        return profundity;
    }

    public void setProfundity(int profundity) {
        this.profundity = profundity;
    }

    public int getRigour() {
        return rigour;
    }

    public void setRigour(int rigour) {
        this.rigour = rigour;
    }

    public int getFit() {
        return fit;
    }

    public void setFit(int fit) {
        this.fit = fit;
    }

    public String getUserId() {
        return userId;
    }

    public void setUserId(String userId) {
        this.userId = userId;
    }

    public LocalDateTime getCreateTime() {
        return createTime;
    }

    public void setCreateTime(LocalDateTime createTime) {
        this.createTime = createTime;
    }

    public LocalDateTime getUpdateTime() {
        return updateTime;
    }

    public void setUpdateTime(LocalDateTime updateTime) {
        this.updateTime = updateTime;
    }

    public String getUpdateBy() {
        return updateBy;
    }

    public void setUpdateBy(String updateBy) {
        this.updateBy = updateBy;
    }

    @Override
    public String toString() {
        return "jobRole=" + jobRole;
    }
}
