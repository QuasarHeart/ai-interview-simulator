package org.buhuiqiming.fuchuang.controller.jpa;

import lombok.extern.slf4j.Slf4j;
import org.buhuiqiming.fuchuang.VO.InterviewVO;
import org.buhuiqiming.fuchuang.dto.CreateInterviewDTO;
import org.buhuiqiming.fuchuang.dto.Result;
import org.buhuiqiming.fuchuang.dto.SubmitAnswerTextDTO;
import org.buhuiqiming.fuchuang.service.InterviewService;
import org.buhuiqiming.fuchuang.util.ASR;
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

        // 具体返回结果构造
        Map<String, Object> data = new HashMap<>();
        data.put("interviewId", interviewId);
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
     * 目前处理的方法有三种：
     * 首先是针对1分钟以内，3MB大小的音频文件的getAudioToTextSimpleASR -- 同步
     * 其次是无限制的录音文件识别，这个需要进行音频文件的云端存储，异步执行
     * 最后是极速的录音文件识别，100MB以下，2小时以下，同步执行 目前来说最好的选择
     */
    @PostMapping("/{interviewId}/ans/voice")
    public SseEmitter submitAnswerVoice(@PathVariable String interviewId, @RequestParam("file") MultipartFile voiceAnswer) throws Exception{
        // String audioAns = interviewService.getAudioToTextSimpleASR(voiceAnswer);
        // interviewService.getAudioToTextASR(voiceAnswer);
        // ToDo 这里需要等待腾讯云进行回调

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
        data.put("status", "FINISHED");
        data.put("reportStatus", "REPORTING");
        return Result.success(data);
    }

    /**
     * 获取用户所有的面试记录和对话详情（一次性返回）
     */
    @GetMapping("/all")
    public Result getAllInterviews() {

        // TODO: 从 Token 中解析出真实的 userId
        String mockUserId = "user_001";

        List<InterviewVO> data = interviewService.getInterviewHistoryList(mockUserId);

        return Result.success(data);
    }
}