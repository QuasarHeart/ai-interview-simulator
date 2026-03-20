package org.buhuiqiming.fuchuang.repository;

import org.buhuiqiming.fuchuang.entity.jpa.InterviewEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface InterviewRepository extends JpaRepository<InterviewEntity,Long> {



    InterviewEntity findByInterviewId(String interviewId);
    // 按UserId进行检索，再按CreateTime进行递减排序
    List<InterviewEntity> findAllByUserIdOrderByCreateTimeDesc(String userId);
}
