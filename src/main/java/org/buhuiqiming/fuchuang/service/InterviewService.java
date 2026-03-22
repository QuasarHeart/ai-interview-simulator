package org.buhuiqiming.fuchuang.service;

import lombok.extern.slf4j.Slf4j;
import org.buhuiqiming.fuchuang.VO.InterviewTurnsVO;
import org.buhuiqiming.fuchuang.VO.InterviewVO;
import org.buhuiqiming.fuchuang.dto.*;
import org.buhuiqiming.fuchuang.entity.jpa.InterviewEntity;
import org.buhuiqiming.fuchuang.entity.jpa.InterviewTurnsEntity;
import org.buhuiqiming.fuchuang.exception.ServiceException;
import org.buhuiqiming.fuchuang.mapper.UserMapper;
import org.buhuiqiming.fuchuang.repository.InterviewRepository;
import org.buhuiqiming.fuchuang.repository.InterviewTurnsRepository;
import org.buhuiqiming.fuchuang.util.UserContext;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.client.RestClient;
import org.springframework.web.servlet.mvc.method.annotation.SseEmitter;
import tools.jackson.databind.JsonNode;
import tools.jackson.databind.ObjectMapper;

import java.time.Duration;
import java.time.LocalDateTime;
import java.util.*;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

@Slf4j
@Service
public class InterviewService {

    private final InterviewRepository interviewRepository;
    private final InterviewTurnsRepository interviewTurnsRepository;

    private final UserMapper userMapper;

    private final RestClient restClient;
    private final ExecutorService executorService = Executors.newVirtualThreadPerTaskExecutor();
    private final ObjectMapper objectMapper;

    public InterviewService(InterviewRepository interviewRepository,
                            InterviewTurnsRepository interviewTurnsRepository,
                            RestClient pythonClient,
                            ObjectMapper objectMapper,
                            UserMapper userMapper
    ) {
        this.interviewRepository = interviewRepository;
        this.interviewTurnsRepository = interviewTurnsRepository;
        this.restClient = pythonClient;
        this.objectMapper = objectMapper;
        this.userMapper = userMapper;
    }

    // 面试会话不存在错误码判断
    private InterviewEntity getInterviewOrElseThrow(String interviewId) {
        InterviewEntity interview = interviewRepository.findByInterviewId(interviewId);
        if (interview == null) {
            throw new ServiceException(404, "面试会话不存在");
        }
        return interview;
    }

    public String createInterview(CreateInterviewDTO dto) {
        System.out.println("createInterview");
        String interviewId = UUID.randomUUID().toString().replace("-", "");
        InterviewEntity interview = new InterviewEntity(interviewId, dto.getJobRole(), dto.getDifficulty(), dto.getMode(), "CREATED", dto.getJobInfo(), dto.getInterviewerStyle());
        interview.setUserId(UserContext.get());
        interviewRepository.save(interview);
        System.out.println("create interview success");
        return interviewId;
    }

    @Transactional(rollbackFor = Exception.class)
    public String startInterview(String interviewId){
        System.out.println("startInterview");
        InterviewEntity interview = getInterviewOrElseThrow(interviewId);
        if (!"CREATED".equals(interview.getInterviewStatus())) {
            throw new ServiceException(409, "状态不允许：面试已经开始或已结束");
        }
        InterviewStartRequest requestBody = InterviewStartRequest.builder()
                .sessionId(interviewId)
                .jobPosition(interview.getJobRole())
                .resumeContent(userMapper.getVitaContent(UserContext.get())) // 简历的解析文本
                .interviewConfig(InterviewStartRequest.InterviewConfig.builder()
                        .mode(interview.getMode())
                        .analyzeEmotion(false)
                        .interviewerStyle(interview.getInterviewerStyle())
                        .difficulty(interview.getDifficulty())
                        .build())
                .flowControl(InterviewStartRequest.FlowControl.builder()
                        .stageTransition("continue")
                        .targetStage("intro")
                        .build())
                .build();
        log.info("requestBody = {}", requestBody);
        Result response = restClient.post()
                .uri("/start")
                .body(requestBody)
                .retrieve()
                .body(Result.class);
        log.info("response={}", response);
        if (response == null || !Integer.valueOf(200).equals(response.getCode())) {
            throw new ServiceException(500, "ml服务启动异常: " + (response != null ? response.getMsg() : "无响应"));
        }

        StartInterviewQueDTO data = objectMapper.convertValue(
                response.getData(),
                StartInterviewQueDTO.class
        );
        if(data == null){
            // 服务器返回异常
            throw new ServiceException(500, "服务器返回异常: 返回值为空");
        }

        String interviewBeginQue = data.getQuestion();
        String stageTransition = data.getFlowControl().getStageTransition();
        String targetStage = data.getFlowControl().getTargetStage();

        interview.setStageTransition(stageTransition);
        interview.setTargetStage(targetStage);
        interview.setInterviewStatus("RUNNING");
        //第一轮特殊处理
        interview.setHistorySummary("当前为第一轮对话，暂无面试总结");
        int turnsNumber = interview.getTurnsNumber() + 1;
        interview.setTurnsNumber(turnsNumber);
        interviewRepository.save(interview);

        InterviewTurnsEntity interviewTurnsEntity = new InterviewTurnsEntity(interviewId, turnsNumber, interviewBeginQue, "");
        interviewTurnsRepository.save(interviewTurnsEntity);

        return interviewBeginQue;
    }

    /**
     * 接收Python部分传递过来的SSE流
     */
    public SseEmitter streamPythonResponse(String interviewId, String answerText){
        SseEmitter emitter = new SseEmitter(0L);
        InterviewEntity interview = getInterviewOrElseThrow(interviewId);

        int currentTurn = interview.getTurnsNumber();
        InterviewTurnsEntity interviewTurnsEntity = interviewTurnsRepository.findByInterviewIdAndTurnNumber(interviewId, currentTurn);
        interviewTurnsEntity.setAnswerText(answerText);
        // ToDo 进行具体的回答的分析，评价   --   这个针对单一轮次评价的还需要吗？

        interviewTurnsRepository.save(interviewTurnsEntity);

        executorService.execute(() -> {
            try{
                var config = InterviewFollowByRequest.InterviewConfig.builder()
                        .mode(interview.getMode())
                        .interviewerStyle(interview.getInterviewerStyle())
                        .difficulty(interview.getDifficulty())
                        .analyzeEmotion(false)
                        .build();
                var background = InterviewFollowByRequest.Background.builder()
                        .jobPosition(interview.getJobRole())
                        .resumeSummary(userMapper.getVitaContent(UserContext.get()))
                        .jdSummary(interview.getJobInfo()) //职位描述
                        .build();

                // ToDo 历史会话
                List<InterviewFollowByRequest.HistoryData.HistoryItem> historyItems = List.of(
                        InterviewFollowByRequest.HistoryData.HistoryItem.builder()
                                .role("assistant")
                                .content("无")
                                .build()
                );

                var history = InterviewFollowByRequest.HistoryData.builder()
                        .historySummary(interview.getHistorySummary())
                        .recentHistory(historyItems)
                        .build();
                var flow = InterviewFollowByRequest.FlowControl.builder()
                        .stageTransition("continue")
                        .targetStage("tech_general")
                        .build();
                InterviewFollowByRequest requestBody = InterviewFollowByRequest.builder()
                        .sessionId(interviewId)
                        .roundId(interview.getTurnsNumber())
                        .interviewConfig(config)
                        .background(background)
                        .historyData(history)
                        .flowControl(flow)
                        .build();

                restClient.post()
                        .uri("http://%s:%s/followup/stream",System.getenv("ML_SERVICE_HOST"),System.getenv("ML_SERVICE_PORT"))
                        .accept(MediaType.TEXT_EVENT_STREAM)
                        .body(requestBody)
                        .exchange((request, response) ->{
                            if (response.getStatusCode().isError()) {
                                emitter.completeWithError(new RuntimeException("算法端响应异常: " + response.getStatusCode()));
                                return null;
                            }
                            StringBuilder queBuffer = new StringBuilder();
                            StringBuilder feeBuffer = new StringBuilder();
                            Map<String, Object> metaData = new HashMap<>();

                            try (java.io.BufferedReader reader = new java.io.BufferedReader(
                                    new java.io.InputStreamReader(response.getBody(), java.nio.charset.StandardCharsets.UTF_8))){
                                String line;
                                while((line = reader.readLine()) != null){
                                    if (!line.startsWith("data: ")) {
                                        continue; // 忽略非数据行（比如空行）
                                    }
                                    // 提取 JSON 字符串
                                    String jsonStr = line.substring(6).trim();

                                    // 解析 JSON 节点
                                    JsonNode rootNode = objectMapper.readTree(jsonStr); // 直接用 JsonNode 接收
                                    String type = rootNode.path("type").asString();

                                    // 进行具体处理
                                    switch (type) {
                                        case "token":
                                            String field = rootNode.path("field").asString();
                                            String content = rootNode.path("content").asString();

                                            // 后台拼装记录
                                            if ("question".equals(field)) {
                                                queBuffer.append(content);
                                            } else if ("immediate_feedback".equals(field)) {
                                                feeBuffer.append(content);
                                            }

                                            // ToDo 现在是直接透传文字，前端需要什么结构化组织吗？
                                            emitter.send(content);
                                            break;

                                        case "meta":
                                            // 提取并暂存需要的元数据，比如 updated_history_summary 或 flow_control
                                            if (rootNode.has("updated_history_summary")) {
                                                metaData.put("history_summary", rootNode.path("updated_history_summary").asString());
                                            }
                                            if (rootNode.has("flow_control")) {
                                                metaData.put("target_stage", rootNode.path("flow_control").path("target_stage").asString());
                                                metaData.put("stage_transition", rootNode.path("flow_control").path("stage_transition").asString());
                                            }
                                            break;

                                        case "done":
                                            // 告诉前端结束了
                                            emitter.send("[DONE]");
                                            emitter.complete();

                                            // 结束后执行数据库落库操作
                                            saveTurnMetaData(interviewId, queBuffer.toString(), metaData);
                                            break;

                                        case "error":
                                            // 发生错误，通知前端并结束
                                            emitter.send("[ERROR]");
                                            emitter.completeWithError(new RuntimeException("算法端流式生成出错"));
                                            break;

                                        default:
                                            // 未知类型，可以记录日志忽略
                                            break;
                                    }

                                    // 如果遇到 done 或 error，退出 while 循环，停止读取
                                    if ("done".equals(type) || "error".equals(type)) {
                                        break;
                                    }
                                }
                            }
                            return null;
                        });
            } catch (Exception e) {
                // 捕获网络异常等
                emitter.completeWithError(e);
            }
        });
        return emitter;
    }

    @Transactional
    // 异步读取结束后将完整的数据保存
    private void saveTurnMetaData(String interviewId, String queBuffer, Map<String, Object> metaData){
        InterviewEntity interview = getInterviewOrElseThrow(interviewId);
        int turnsNum = interview.getTurnsNumber() + 1;

        interview.setTurnsNumber(turnsNum);
        if(metaData.containsKey("history_summary")){
            interview.setHistorySummary(metaData.get("history_summary").toString());
        }
        if(metaData.containsKey("target_stage") && metaData.containsKey("stage_transition")){
            interview.setStageTransition(metaData.get("stage_transition").toString());
            interview.setTargetStage(metaData.get("target_stage").toString());
        }

        InterviewTurnsEntity interviewTurns = new InterviewTurnsEntity(interviewId, turnsNum, queBuffer, "");
        interviewRepository.save(interview);
        interviewTurnsRepository.save(interviewTurns);
    }

    /**
     * 获取当前面试轮次
     */
    public int getCurrentTurn(String interviewId){
        InterviewEntity interview = interviewRepository.findByInterviewId(interviewId);
        return interview.getTurnsNumber();
    }

    /**
     * 结束面试会话
     */
    @Transactional(rollbackFor = Exception.class)
    public void finishInterview(String interviewId){
        InterviewEntity interview = getInterviewOrElseThrow(interviewId);

        if (!"RUNNING".equals(interview.getInterviewStatus())) {
            throw new ServiceException(409, "状态不允许：当前会话不在进行中");
        }

        interview.setInterviewStatus("FINISHED");
        interview.setDuration(Duration.between(interview.getCreateTime(), LocalDateTime.now()));
        interviewRepository.save(interview);
    }

    // 获取历史面试列表（分页）
    public List<InterviewVO> getInterviewHistoryList(String userId){
        List<InterviewEntity> interviews = interviewRepository.findAllByUserIdOrderByCreateTimeDesc(userId);

        List<InterviewVO> resultList = new ArrayList<>();
        // ToDo 这里性能上后面肯定是要优化的
        for (InterviewEntity interview : interviews) {
            InterviewVO interviewVO = new InterviewVO();
            interviewVO.setInterviewId(interview.getInterviewId());
            interview.setJobRole(interview.getJobRole());
            interviewVO.setDifficulty(interview.getDifficulty());
            interviewVO.setMode(interview.getMode());
            interviewVO.setScore(interview.getTotalScore());
            interviewVO.setDuration(interview.getDuration());

            // ToDo 具体的评分维度要改
            Map<String, Integer> scoreMap = new HashMap<>();
            scoreMap.put("correctness", interview.getCorrectness());
            scoreMap.put("profundity", interview.getProfundity());
            scoreMap.put("rigour", interview.getRigour());
            scoreMap.put("fit",  interview.getFit());
            interviewVO.setScoresDelta(scoreMap);
            
            resultList.add(interviewVO);
        }
        return resultList;
    }

    // 获取轮次具体信息
    public List<InterviewTurnsVO> getInterviewTurns(String interviewId){
        getInterviewOrElseThrow(interviewId);

        List<InterviewTurnsEntity> turnsEntities = interviewTurnsRepository.findByInterviewIdOrderByTurnNumberAsc(interviewId);

        // 转换为 VO形式
        List<InterviewTurnsVO> voList = new ArrayList<>();
        for (InterviewTurnsEntity turnsEntity : turnsEntities) {
            InterviewTurnsVO interviewTurnVO = new InterviewTurnsVO();
            interviewTurnVO.setTurnNumber(turnsEntity.getTurnNumber());
            interviewTurnVO.setUserContent(turnsEntity.getAnswerText());
            interviewTurnVO.setAssistantContent(turnsEntity.getQuestion());

            voList.add(interviewTurnVO);
        }
        return voList;
    }
}
