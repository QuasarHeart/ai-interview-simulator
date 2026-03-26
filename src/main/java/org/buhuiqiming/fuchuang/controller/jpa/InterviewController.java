package org.buhuiqiming.fuchuang.controller.jpa;

import lombok.extern.slf4j.Slf4j;
import org.buhuiqiming.fuchuang.VO.InterviewTurnsVO;
import org.buhuiqiming.fuchuang.VO.InterviewVO;
import org.buhuiqiming.fuchuang.VO.ReportResultVO;
import org.buhuiqiming.fuchuang.dto.CreateInterviewDTO;
import org.buhuiqiming.fuchuang.dto.GenerateReportResponse;
import org.buhuiqiming.fuchuang.dto.Result;
import org.buhuiqiming.fuchuang.dto.SubmitAnswerTextDTO;
import org.buhuiqiming.fuchuang.exception.ServiceException;
import org.buhuiqiming.fuchuang.service.InterviewService;
import org.buhuiqiming.fuchuang.util.ASR;
import org.buhuiqiming.fuchuang.util.UserContext;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.servlet.mvc.method.annotation.SseEmitter;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * 面试相关接口
 * @moudle 面试会话相关
 */
@Slf4j
@RestController
@RequestMapping("/api/v1/interviews")
public class InterviewController {

    private final InterviewService interviewService;
    private final ASR asr;

    public InterviewController(InterviewService interviewService,
                               ASR asr) {
        this.interviewService = interviewService;
        this.asr = asr;
    }

    /**
     * 创建面试会话
     */
    @PostMapping
    public Result createInterview(@ModelAttribute CreateInterviewDTO dto) throws Exception{

        // 面试会话特征码 interviewId 的确定
        // 创建初步的数据库interview实体类记录
        String interviewId = interviewService.createInterview(dto);
        String firstQue = interviewService.startInterview(interviewId);
        String formattedTime = interviewService.getFormattedStartTime(interviewId);

        // 具体返回结果构造
        Map<String, Object> data = new HashMap<>();
        data.put("interviewId", interviewId);
        data.put("startTime", formattedTime);
        data.put("status", "RUNNING");
        data.put("question", firstQue);

        return Result.success(data);
    }

    /**
     * 提交文本回答并建立SSE连接
     */
    @PostMapping(value = "/{interviewId}/ans", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
    public SseEmitter submitAnswerText(@PathVariable String interviewId, @RequestBody SubmitAnswerTextDTO dto) throws Exception{
        return interviewService.streamPythonResponse(interviewId, dto.getContent());
    }

    /**
     * 提交音频回答
     * 首先是针对1分钟以内，3MB大小的音频文件的getAudioToTextSimpleASR -- 同步
     * 最后是极速的录音文件识别，100MB以下，2小时以下，同步执行 目前来说最好的选择
     */
    @PostMapping("/{interviewId}/ans/voice")
    public SseEmitter submitAnswerVoice(@PathVariable String interviewId, @RequestParam("file") MultipartFile voiceAnswer) throws Exception{
        // 短语音情况下的选择
        // String audioAns = interviewService.getAudioToTextSimpleASR(voiceAnswer);

        String audioAns = asr.getAudioToTextASRFast(voiceAnswer);
        return interviewService.streamPythonResponse(interviewId, audioAns);
    }

    @PostMapping(value = "/asr-callback", consumes = MediaType.APPLICATION_FORM_URLENCODED_VALUE)
    public String getAsrCallBack(@RequestParam Map<String, String> callbackData){
        String codeStr = callbackData.get("code");
        if (!"0".equals(codeStr)) {
            System.out.println("识别失败，原因：" + callbackData.get("message"));
            return "{\"code\": 0, \"message\": \"success\"}"; // 失败了也要回成功，不然腾讯云会一直重试
        }

        String result = callbackData.get("text");

        return "{\"code\": 0, \"message\": \"success\"}";
    }

    /**
     * 主动结束面试
     */
    @PostMapping("/{interviewId}/finish")
    public Result finishInterview(@PathVariable String interviewId) throws Exception{
        interviewService.finishInterview(interviewId);

        Map<String, Object> data = new HashMap<>();
        data.put("interviewId", interviewId);
        data.put("status", "FINISHED");
        return Result.success(data);
    }

    /**
     * 获取用户所有的面试记录（一次性返回）
     */
    @GetMapping("/all")
    public Result getAllInterviews() {

        Long currentUserId = UserContext.get();
        List<InterviewVO> data = interviewService.getInterviewHistoryList(currentUserId);

        return Result.success(data);
    }

    /**
     * 获取用户某一次面试的相关记录
     */
    @GetMapping("/{interviewId}/history")
    public Result getInterviewHistory(@PathVariable String interviewId) throws Exception{
        List<InterviewTurnsVO> data = interviewService.getInterviewTurns(interviewId);
        return Result.success(data);
    }

    /**
     * 面试报告回调
     */
    @PostMapping("/{interviewId}/report-callback")
    public void InterviewReportCallback(@PathVariable String interviewId, @RequestBody GenerateReportResponse response) throws Exception{
        if(response == null){
            log.info("返回报告为空");
            throw new ServiceException(500, "返回报告为空");
        }
        interviewService.handleInterviewReportCallback(interviewId, response);
    }

    /**
     * 获取面试报告
     */
    @GetMapping("/{interviewId}/report")
    public Result getInterviewReport(@PathVariable String interviewId) throws Exception{
        String status = interviewService.getInterviewStatus(interviewId);
        switch (status){
            case "FINISHED":
                return Result.error(409, "该面试会话已手动结束，无法生成报告");
            case "WAITING_REPORT":
                return Result.success(202, "正在评价回复，请稍候");
            case "REPORTING":
                return Result.success(202, "报告正在生成中，请稍候");
            case "REPORTED":
                ReportResultVO data = interviewService.handleReportDataForFrontend(interviewId);
                return Result.success(data);
            default:
                return Result.error(500, "面试会话状态异常，请联系管理员");
        }
    }

}