package org.buhuiqiming.fuchuang.service;

import org.buhuiqiming.fuchuang.VO.InterviewVO;
import org.buhuiqiming.fuchuang.VO.InterviewTurnsVO;
import org.buhuiqiming.fuchuang.VO.ReportResultVO;
import org.buhuiqiming.fuchuang.dto.CreateInterviewDTO;
import org.buhuiqiming.fuchuang.dto.GenerateReportResponse;
import org.buhuiqiming.fuchuang.dto.InterviewFollowByRequest;
import org.buhuiqiming.fuchuang.entity.jpa.InterviewEntity;
import org.buhuiqiming.fuchuang.entity.jpa.InterviewTurnsEntity;
import org.springframework.web.servlet.mvc.method.annotation.SseEmitter;

import java.util.List;

public interface InterviewService {

    // 面试会话不存在错误码判断
    InterviewEntity getInterviewOrElseThrow(String interviewId);

    // 获取对应面试会话当前状态
    String getInterviewStatus(String interviewId);

    // 创建面试
    String createInterview(CreateInterviewDTO dto);

    // 开始面试
    String startInterview(String interviewId);

    // 获取面试历史会话
    List<InterviewFollowByRequest.HistoryData.HistoryItem> getInterviewHistory(String interviewId);

    // 接收Python部分传递过来的SSE流
    SseEmitter streamPythonResponse(String interviewId, String answerText);

    // 结束面试会话
    void finishInterview(String interviewId);

    // 获取单轮回答评价
    void getTurnsJudgement(InterviewEntity interview, InterviewTurnsEntity interviewTurns, String context);

    // 获取历史面试列表
    List<InterviewVO> getInterviewHistoryList(Long userId);

    // 获取轮次具体信息
    List<InterviewTurnsVO> getInterviewTurns(String interviewId);

    // 获取某次面试的报告
    void getInterviewReport(String interviewId);

    // 处理生成报告的回调结果
    void handleInterviewReportCallback(String interviewId, GenerateReportResponse response);

    // 为前端处理报告数据
    ReportResultVO handleReportDataForFrontend(String interviewId);

    // 尝试触发报告生成
    void tryTriggerReportGeneration(String interviewId);
}