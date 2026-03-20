package org.buhuiqiming.fuchuang.repository;

import org.buhuiqiming.fuchuang.entity.jpa.InterviewTurnsEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface InterviewTurnsRepository extends JpaRepository<InterviewTurnsEntity, Long> {

    InterviewTurnsEntity findByInterviewIdAndTurnNumber(String interviewId, int turnsNumber);

    // 按照interviewId中的轮次顺序先后排序后返回interviewTurnsEntity
    List<InterviewTurnsEntity> findByInterviewIdOrderByTurnNumberAsc(String interviewId);
}