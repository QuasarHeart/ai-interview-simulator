package org.buhuiqiming.fuchuang.repository;

import org.buhuiqiming.fuchuang.entity.jpa.InterviewTurnsEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface InterviewTurnsRepository extends JpaRepository<InterviewTurnsEntity, Long> {

    InterviewTurnsEntity findByInterviewIdAndTurnNumber(String interviewId, int turnsNumber);

    // 按照interviewId中的轮次顺序先后排序后返回interviewTurnsEntity
    List<InterviewTurnsEntity> findByInterviewIdOrderByTurnNumberAsc(String interviewId);

    // 批量按轮次范围查询，避免 N+1
    List<InterviewTurnsEntity> findByInterviewIdAndTurnNumberBetweenOrderByTurnNumberDesc(String interviewId, int startTurn, int endTurn);

    // 统计某个面试中有多少还未评价的轮次（以evaluationResult是否为空为准）
    @Query("SELECT COUNT(t) FROM InterviewTurnsEntity t " +
            "WHERE t.interviewId = :interviewId " +
            "AND t.evaluationResult IS NULL " +
            "AND (t.targetStage IS NULL OR t.targetStage NOT IN ('end', 'failedEvaluation')) " +
            "AND (t.stageTransition IS NULL OR t.stageTransition != 'end')")
    int countUnEvaluatedTurns(@Param("interviewId") String interviewId);
}