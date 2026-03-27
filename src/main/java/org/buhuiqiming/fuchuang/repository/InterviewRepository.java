package org.buhuiqiming.fuchuang.repository;

import org.buhuiqiming.fuchuang.entity.jpa.InterviewEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface InterviewRepository extends JpaRepository<InterviewEntity,Long> {



    InterviewEntity findByInterviewId(String interviewId);
    // 按UserId进行检索，再按CreateTime进行递减排序
    List<InterviewEntity> findAllByUserIdOrderByCreateTimeDesc(Long userId);

    // 只有当前状态是 oldState 时，才更新为 newState
    @Modifying
    @Query("UPDATE InterviewEntity i SET i.interviewStatus = :newState WHERE i.interviewId = :interviewId AND i.interviewStatus = :oldState")
    int updateStatusIfWaiting(@Param("interviewId") String interviewId, @Param("newState") String newState, @Param("oldState") String oldState);

    // 按 UserId 和 JobRole 检索，并按 CreateTime 升序排序（时间正序）
    List<InterviewEntity> findAllByUserIdAndJobRoleOrderByCreateTimeAsc(Long userId, String jobRole);
}
