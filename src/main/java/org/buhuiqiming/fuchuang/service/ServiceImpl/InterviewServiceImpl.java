package org.buhuiqiming.fuchuang.service.ServiceImpl;

import lombok.extern.slf4j.Slf4j;
import org.buhuiqiming.fuchuang.VO.GrowthCurveVO;
import org.buhuiqiming.fuchuang.VO.InterviewVO;
import org.buhuiqiming.fuchuang.VO.InterviewTurnsVO;
import org.buhuiqiming.fuchuang.VO.ReportResultVO;
import org.buhuiqiming.fuchuang.config.RedisStreamConfig;
import org.buhuiqiming.fuchuang.dto.*;
import org.buhuiqiming.fuchuang.entity.jpa.InterviewEntity;
import org.buhuiqiming.fuchuang.entity.jpa.InterviewTurnsEntity;
import org.buhuiqiming.fuchuang.dto.TurnEvaluationResult;
import org.buhuiqiming.fuchuang.exception.ServiceException;
import org.buhuiqiming.fuchuang.mapper.UserMapper;
import org.buhuiqiming.fuchuang.repository.InterviewRepository;
import org.buhuiqiming.fuchuang.repository.InterviewTurnsRepository;
import org.buhuiqiming.fuchuang.service.InterviewService;
import org.buhuiqiming.fuchuang.util.UserContext;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Lazy;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.transaction.support.TransactionSynchronization;
import org.springframework.transaction.support.TransactionSynchronizationManager;
import org.springframework.web.client.RestClient;
import org.springframework.web.servlet.mvc.method.annotation.SseEmitter;

import tools.jackson.databind.ObjectMapper;
import tools.jackson.databind.JsonNode;

import java.time.Duration;
import java.time.LocalDateTime;
import java.util.*;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

@Slf4j
@Service
public class InterviewServiceImpl implements InterviewService {

    private final InterviewRepository interviewRepository;
    private final InterviewTurnsRepository interviewTurnsRepository;

    private final UserMapper userMapper;

    private final RestClient restClient;
    private final ExecutorService executorService = Executors.newVirtualThreadPerTaskExecutor();
    private final ObjectMapper objectMapper;
    private final StringRedisTemplate stringRedisTemplate;

    private final int historyTurnsCount = 4;
    private static final java.time.format.DateTimeFormatter TIME_FORMATTER =
            java.time.format.DateTimeFormatter.ofPattern("yyyy年MM月dd日HH:mm");

    @Autowired
    public InterviewServiceImpl(InterviewRepository interviewRepository,
                                InterviewTurnsRepository interviewTurnsRepository,
                                RestClient pythonClient,
                                ObjectMapper objectMapper,
                                UserMapper userMapper,
                                StringRedisTemplate stringRedisTemplate
    ) {
        this.interviewRepository = interviewRepository;
        this.interviewTurnsRepository = interviewTurnsRepository;
        this.restClient = pythonClient;
        this.objectMapper = objectMapper;
        this.userMapper = userMapper;
        this.stringRedisTemplate = stringRedisTemplate;
    }

    @Autowired
    @Lazy
    private InterviewService self;

    @Override
    public String getFormattedStartTime(String interviewId){
        InterviewEntity interview = getInterviewOrElseThrow(interviewId);
        return interview.getCreateTime().format(TIME_FORMATTER);
    }

    @Override
    public InterviewEntity getInterviewOrElseThrow(String interviewId) {
        InterviewEntity interview = interviewRepository.findByInterviewId(interviewId);
        if (interview == null) {
            throw new ServiceException(404, "面试会话不存在");
        }
        return interview;
    }

    @Override
    public String getInterviewStatus(String interviewId) {
        InterviewEntity interview = interviewRepository.findByInterviewId(interviewId);
        if (interview == null) {
            throw new ServiceException(404, "面试会话不存在");
        }
        return interview.getInterviewStatus();
    }

    @Override
    public String createInterview(CreateInterviewDTO dto) {
        System.out.println("createInterview");
        String interviewId = UUID.randomUUID().toString().replace("-", "");
        InterviewEntity interview = new InterviewEntity(interviewId, dto.getJobRole(), dto.getDifficulty(), dto.getMode(), "CREATED", dto.getJobInfo(), dto.getInterviewerStyle(), dto.getCompanyContext());
        interview.setUserId(UserContext.get());
        interviewRepository.save(interview);
        System.out.println("create interview success");
        return interviewId;
    }

    @Override
    public SseEmitter startInterviewStream(String interviewId){
        System.out.println("startInterviewStream");
        SseEmitter emitter = new SseEmitter(0L);
        InterviewEntity interview = getInterviewOrElseThrow(interviewId);
        if (!"CREATED".equals(interview.getInterviewStatus())) {
            throw new ServiceException(409, "状态不允许：面试已经开始或已结束");
        }

        log.info("当前流程，创建会话，阶段：请求ml");
        executorService.execute(() -> {
            try {
                InterviewStartRequest requestBody = InterviewStartRequest.builder()
                        .sessionId(interviewId)
                        .jobPosition(interview.getJobRole())
                        .jdSummary(interview.getJobInfo())
                        .resumeContent(userMapper.getVitaContent(UserContext.get())) // 简历的解析文本
                        .interviewConfig(InterviewStartRequest.InterviewConfig.builder()
                                .mode(interview.getMode())
                                .analyzeEmotion(false)
                                .interviewerStyle(interview.getInterviewerStyle())
                                .companyContext(interview.getCompanyContext())
                                .difficulty(interview.getDifficulty())
                                .build())
                        .flowControl(InterviewStartRequest.FlowControl.builder()
                                .stageTransition("continue")
                                .targetStage("intro")
                                .build())
                        .build();
                restClient.post()
                        .uri("/start/stream")
                        .accept(MediaType.TEXT_EVENT_STREAM)
                        .body(requestBody)
                        .exchange((request, response) -> {
                            if (response.getStatusCode().isError()) {
                                emitter.completeWithError(new RuntimeException("算法端响应异常: " + response.getStatusCode()));
                                return null;
                            }
                            StringBuilder queBuffer = new StringBuilder();
                            Map<String, Object> metaData = new HashMap<>();

                            try (java.io.BufferedReader reader = new java.io.BufferedReader(
                                    new java.io.InputStreamReader(response.getBody(), java.nio.charset.StandardCharsets.UTF_8))) {
                                String line;
                                while ((line = reader.readLine()) != null) {
                                    if (!line.startsWith("data: ")) {
                                        continue;
                                    }
                                    String jsonStr = line.substring(6).trim();
                                    JsonNode rootNode = objectMapper.readTree(jsonStr);
                                    String type = rootNode.path("type").asString();

                                    switch (type) {
                                        case "token":
                                            String field = rootNode.path("field").asString();
                                            String content = rootNode.path("content").asString();

                                            if ("question".equals(field)) {
                                                queBuffer.append(content);
                                            }

                                            emitter.send(content);
                                            break;

                                        case "meta":
                                            if (rootNode.has("flow_control")) {
                                                metaData.put("target_stage", rootNode.path("flow_control").path("target_stage").asString());
                                                metaData.put("stage_transition", rootNode.path("flow_control").path("stage_transition").asString());
                                            }
                                            break;

                                        case "done":
                                            emitter.send("[DONE]");
                                            startInterviewInfoHandle(interviewId, queBuffer.toString(), metaData);
                                            emitter.complete();
                                            break;

                                        case "error":
                                            emitter.send("[ERROR]");
                                            emitter.completeWithError(new RuntimeException("算法端流式生成出错"));
                                            break;

                                        default:
                                            break;
                                    }

                                    if ("done".equals(type) || "error".equals(type)) {
                                        break;
                                    }
                                }
                            }
                            return null;
                        });
            } catch (Exception e) {
                emitter.completeWithError(e);
            }
        });
        return emitter;
    }

    private void startInterviewInfoHandle(String interviewId, String question, Map<String, Object> metaData){
        InterviewEntity interview = getInterviewOrElseThrow(interviewId);
        int turnsNum = interview.getTurnsNumber() + 1;
        interview.setTurnsNumber(turnsNum);
        interview.setInterviewStatus("RUNNING");
        interview.setHistorySummary("当前为第一轮对话，暂无面试总结");

        InterviewTurnsEntity interviewTurns = new InterviewTurnsEntity(interviewId, turnsNum, question, "");
        if(metaData.containsKey("target_stage") && metaData.containsKey("stage_transition")){
            interviewTurns.setStageTransition(metaData.get("stage_transition").toString());
            interviewTurns.setTargetStage(metaData.get("target_stage").toString());
        }

        interviewRepository.save(interview);
        interviewTurnsRepository.save(interviewTurns);

    }

    @Override
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
                .jdSummary(interview.getJobInfo())
                .resumeContent(userMapper.getVitaContent(UserContext.get())) // 简历的解析文本
                .interviewConfig(InterviewStartRequest.InterviewConfig.builder()
                        .mode(interview.getMode())
                        .analyzeEmotion(false)
                        .interviewerStyle(interview.getInterviewerStyle())
                        .companyContext(interview.getCompanyContext())
                        .difficulty(interview.getDifficulty())
                        .build())
                .flowControl(InterviewStartRequest.FlowControl.builder()
                        .stageTransition("continue")
                        .targetStage("intro")
                        .build())
                .build();
        log.info("当前流程，创建会话，阶段：请求ml");
        Result response = restClient.post()
                .uri("/start")
                .body(requestBody)
                .retrieve()
                .body(Result.class);
        log.info("当前流程，创建会话，阶段：收到ml回复");
        if (response == null || !Integer.valueOf(200).equals(response.getCode())) {
            throw new ServiceException(500, "ml服务启动异常: " + (response != null ? response.getMsg() : "无响应"));
        }

        StartInterviewQueResponse data = objectMapper.convertValue(
                response.getData(),
                StartInterviewQueResponse.class
        );
        if(data == null){
            throw new ServiceException(500, "服务器返回异常: 返回值为空");
        }

        String interviewBeginQue = data.getQuestion();

        interview.setInterviewStatus("RUNNING");
        //第一轮特殊处理
        interview.setHistorySummary("当前为第一轮对话，暂无面试总结");
        int turnsNumber = interview.getTurnsNumber() + 1;
        interview.setTurnsNumber(turnsNumber);

        interviewRepository.save(interview);

        InterviewTurnsEntity interviewTurnsEntity = new InterviewTurnsEntity(interviewId, turnsNumber, interviewBeginQue, "");
        interviewTurnsEntity.setStageTransition("continue");
        interviewTurnsEntity.setTargetStage("intro");
        interviewTurnsRepository.save(interviewTurnsEntity);

        return interviewBeginQue;
    }

    @Override
    public List<InterviewFollowByRequest.HistoryData.HistoryItem> getInterviewHistory(String interviewId) {
        List<InterviewFollowByRequest.HistoryData.HistoryItem> list = new ArrayList<>();

        InterviewEntity interview = getInterviewOrElseThrow(interviewId);
        int turnsNumber = interview.getTurnsNumber();
        int count = historyTurnsCount;

        while (count > 0 && turnsNumber > 0) {
            InterviewTurnsEntity interviewTurnsEntity = interviewTurnsRepository.findByInterviewIdAndTurnNumber(interviewId, turnsNumber);
            if (interviewTurnsEntity == null) {
                log.error("interviewTurnsEntity is null for interviewId: {}, turn: {}", interviewId, turnsNumber);
                throw new ServiceException(500, "存储流程出错，请重试");
            }

            String answerText = interviewTurnsEntity.getAnswerText() != null ? interviewTurnsEntity.getAnswerText() : "";
            String questionText = interviewTurnsEntity.getQuestion() != null ? interviewTurnsEntity.getQuestion() : "";

            InterviewFollowByRequest.HistoryData.HistoryItem.FlowControl historyFlowControl =
                    InterviewFollowByRequest.HistoryData.HistoryItem.FlowControl.builder()
                            .stageTransition(interviewTurnsEntity.getStageTransition())
                            .targetStage(interviewTurnsEntity.getTargetStage())
                            .build();

            InterviewFollowByRequest.HistoryData.HistoryItem item = InterviewFollowByRequest.HistoryData.HistoryItem.builder()
                    .roundId(turnsNumber)
                    .assistantContent(questionText)
                    .userContent(answerText)
                    .flowControl(historyFlowControl)
                    .build();

            list.add(0, item);

            turnsNumber--;
            count--;
        }
        return list;
    }

    @Override
    public SseEmitter streamPythonResponse(String interviewId, String answerText){
        SseEmitter emitter = new SseEmitter(0L);
        InterviewEntity interview = getInterviewOrElseThrow(interviewId);

        if(!"RUNNING".equals(interview.getInterviewStatus())){
            throw new ServiceException(409, "该面试会话为开始或已结束");
        }

        int currentTurn = interview.getTurnsNumber();
        InterviewTurnsEntity interviewTurnsEntity = interviewTurnsRepository.findByInterviewIdAndTurnNumber(interviewId, currentTurn);
        interviewTurnsEntity.setAnswerText(answerText);

        Long currentUserId = UserContext.get();
        String resumeContent = userMapper.getVitaContent(currentUserId);

        interviewTurnsRepository.save(interviewTurnsEntity);

        Map<String, String> messageBody = new HashMap<>();
        messageBody.put("interviewId", interviewId);
        messageBody.put("turnNumber", String.valueOf(currentTurn));

        var record = org.springframework.data.redis.connection.stream.StreamRecords.newRecord()
                .ofStrings(messageBody)
                .withStreamKey("interview:eval:stream");
        stringRedisTemplate.opsForStream().add(record);
        stringRedisTemplate.opsForStream().trim("interview:eval:stream", 1200);
        log.info("已将评价任务投递到 MQ, interviewId: {}, turn: {}", interviewId, currentTurn);

        executorService.execute(() -> {
            try{
                var config = InterviewFollowByRequest.InterviewConfig.builder()
                        .mode(interview.getMode())
                        .companyContext("字节")// ToDo: 公司背景
                        .interviewerStyle(interview.getInterviewerStyle())
                        .difficulty(interview.getDifficulty())
                        .analyzeEmotion(false)
                        .build();
                var background = InterviewFollowByRequest.Background.builder()
                        .jobPosition(interview.getJobRole())
                        .resumeContent(resumeContent)
                        .jdSummary(interview.getJobInfo())
                        .build();

                List<InterviewFollowByRequest.HistoryData.HistoryItem> historyItems = getInterviewHistory(interviewId);

                var history = InterviewFollowByRequest.HistoryData.builder()
                        .historySummary(interview.getHistorySummary())
                        .recentHistory(historyItems)
                        .build();
                InterviewFollowByRequest requestBody = InterviewFollowByRequest.builder()
                        .sessionId(interviewId)
                        .roundId(interview.getTurnsNumber())
                        .interviewConfig(config)
                        .background(background)
                        .historyData(history)
                        .build();

                restClient.post()
                        .uri("/followup/stream")
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
                                        continue;
                                    }
                                    String jsonStr = line.substring(6).trim();
                                    JsonNode rootNode = objectMapper.readTree(jsonStr);
                                    String type = rootNode.path("type").asString();

                                    switch (type) {
                                        case "token":
                                            String field = rootNode.path("field").asString();
                                            String content = rootNode.path("content").asString();

                                            if ("question".equals(field)) {
                                                queBuffer.append(content);
                                            } else if ("immediate_feedback".equals(field)) {
                                                feeBuffer.append(content);
                                            }

                                            emitter.send(content);
                                            break;

                                        case "meta":
                                            if (rootNode.has("updated_history_summary")) {
                                                metaData.put("history_summary", rootNode.path("updated_history_summary").asString());
                                            }
                                            if (rootNode.has("flow_control")) {
                                                metaData.put("target_stage", rootNode.path("flow_control").path("target_stage").asString());
                                                metaData.put("stage_transition", rootNode.path("flow_control").path("stage_transition").asString());
                                            }
                                            break;

                                        case "done":
                                            if(metaData.containsKey("target_stage") && metaData.get("target_stage").toString().equals("end")){
                                                emitter.send("[END]");
                                                saveTurnMetaData(interviewId, queBuffer.toString(), metaData);

                                                InterviewEntity endInterview = getInterviewOrElseThrow(interviewId);
                                                endInterview.setInterviewStatus("WAITING_REPORT");
                                                endInterview.setDuration(Duration.between(endInterview.getCreateTime(), LocalDateTime.now()));
                                                interviewRepository.save(endInterview);

                                                self.tryTriggerReportGeneration(interviewId);
                                            } else{
                                                emitter.send("[DONE]");
                                                saveTurnMetaData(interviewId, queBuffer.toString(), metaData);
                                            }

                                            emitter.complete();

                                            break;

                                        case "error":
                                            emitter.send("[ERROR]");
                                            emitter.completeWithError(new RuntimeException("算法端流式生成出错"));
                                            break;

                                        default:
                                            break;
                                    }

                                    if ("done".equals(type) || "error".equals(type)) {
                                        break;
                                    }
                                }
                            }
                            return null;
                        });
            } catch (Exception e) {
                emitter.completeWithError(e);
            }
        });
        return emitter;
    }

    private void saveTurnMetaData(String interviewId, String queBuffer, Map<String, Object> metaData){
        InterviewEntity interview = getInterviewOrElseThrow(interviewId);
        int turnsNum = interview.getTurnsNumber() + 1;

        interview.setTurnsNumber(turnsNum);
        if(metaData.containsKey("history_summary")){
            interview.setHistorySummary(metaData.get("history_summary").toString());
        }

        InterviewTurnsEntity interviewTurns = new InterviewTurnsEntity(interviewId, turnsNum, queBuffer, "");
        if(metaData.containsKey("target_stage") && metaData.containsKey("stage_transition")){
            interviewTurns.setStageTransition(metaData.get("stage_transition").toString());
            interviewTurns.setTargetStage(metaData.get("target_stage").toString());
            if("end".equals(metaData.get("stage_transition").toString())
                    || "end".equals(metaData.get("target_stage").toString())){
                interviewTurns.setEvaluationResult(null);
            }
        }

        interviewRepository.save(interview);
        interviewTurnsRepository.save(interviewTurns);
    }

    @Override
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

    @Override
    public void processEvaluationTask(String interviewId, int turnNumber, String messageId){
        InterviewEntity interview = getInterviewOrElseThrow(interviewId);
        InterviewTurnsEntity turn = interviewTurnsRepository.findByInterviewIdAndTurnNumber(interviewId, turnNumber);
        String resumeContent = userMapper.getVitaContent(interview.getUserId());

        getTurnsJudgement(interview, turn, resumeContent);
        interviewTurnsRepository.save(turn);

        stringRedisTemplate.opsForStream().acknowledge(
                RedisStreamConfig.EVAL_STREAM_KEY,
                RedisStreamConfig.EVAL_GROUP_NAME,
                messageId
        );
        stringRedisTemplate.opsForStream().delete(RedisStreamConfig.EVAL_STREAM_KEY, messageId);
        self.tryTriggerReportGeneration(interviewId);
    }

    @Override
    public void getTurnsJudgement(InterviewEntity interview, InterviewTurnsEntity interviewTurns, String context){
        var config = GetTurnsJudgeRequest.InterviewConfig.builder()
                .mode(interview.getMode())
                .analyzeEmotion(false)
                .companyContext("字节")// ToDo: 公司背景
                .interviewerStyle(interview.getInterviewerStyle())
                .difficulty(interview.getDifficulty())
                .build();
        var analyze = GetTurnsJudgeRequest.ContentToAnalyze.builder()
                .question(interviewTurns.getQuestion())
                .userAnswer(interviewTurns.getAnswerText())
                .jobPosition(interview.getJobRole())
                .jdSummary(interview.getJobInfo())
                .historySummary(interview.getHistorySummary())
                .resumeContent(context)
                .build();
        GetTurnsJudgeRequest getTurnsJudgeRequest = GetTurnsJudgeRequest.builder()
                .sessionId(interviewTurns.getInterviewId())
                .roundId(interviewTurns.getTurnNumber())
                .interviewConfig(config)
                .contentToAnalyze(analyze)
                .currentStage(interviewTurns.getTargetStage())
                .build();
        log.info("getTurnsJudgeRequest:{}", getTurnsJudgeRequest);
        Result response = restClient.post()
                .uri("/analysis")
                .body(getTurnsJudgeRequest)
                .retrieve()
                .body(Result.class);
        log.info("response={}", response);
        if (response == null || !Integer.valueOf(200).equals(response.getCode())) {
            throw new ServiceException(500, "评价服务异常: " + (response != null ? response.getMsg() : "无响应"));
        }

        GetTurnsJudgeResponse data = objectMapper.convertValue(
                response.getData(),
                GetTurnsJudgeResponse.class
        );
        if (data == null || data.getAnalysis() == null) {
            throw new ServiceException(500, "评价服务返回的数据结构异常");
        }

        TurnEvaluationResult evaluationResult = data.getAnalysis();
        interviewTurns.setEvaluationResult(evaluationResult);
    }

    @Override
    public List<InterviewVO> getInterviewHistoryList(Long userId){
        List<InterviewEntity> interviews = interviewRepository.findAllByUserIdOrderByCreateTimeDesc(userId);

        List<InterviewVO> resultList = new ArrayList<>();
        for (InterviewEntity interview : interviews) {
            InterviewVO interviewVO = new InterviewVO();
            String interviewId = interview.getInterviewId();
            interviewVO.setInterviewId(interviewId);
            interviewVO.setJobRole(interview.getJobRole()); // 修正这里的潜在问题
            interviewVO.setDifficulty(interview.getDifficulty());
            interviewVO.setMode(interview.getMode());
            interviewVO.setInterviewStatus(interview.getInterviewStatus());
            interviewVO.setScore(interview.getTotalScore());
            // 还在进行中的面试会话持续时间返回为 0
            interviewVO.setDuration(interview.getDuration() != null ? interview.getDuration().getSeconds() : 0L);
            interviewVO.setStartTime(getFormattedStartTime(interviewId));

            resultList.add(interviewVO);
        }
        return resultList;
    }

    @Override
    public List<InterviewTurnsVO> getInterviewTurns(String interviewId){
        InterviewEntity interview = getInterviewOrElseThrow(interviewId);
        if(!Objects.equals(interview.getUserId(), UserContext.get())){
            throw new ServiceException(500, "用户信息不匹配，请重试");
        }

        List<InterviewTurnsEntity> turnsEntities = interviewTurnsRepository.findByInterviewIdOrderByTurnNumberAsc(interviewId);

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

    private GenerateReportRequest buildGenerateReportRequest(InterviewEntity interview,
                                                             List<InterviewTurnsEntity> turnsEntities,
                                                             String callbackUrl) {
        var config = GenerateReportRequest.InterviewConfig.builder()
                .mode(interview.getMode())
                .analyzeEmotion(false)
                .interviewerStyle(interview.getInterviewerStyle())
                .companyContext("字节")
                .difficulty(interview.getDifficulty())
                .build();

        List<GenerateReportRequest.RoundResult> roundResults = new ArrayList<>();
        for (InterviewTurnsEntity turn : turnsEntities) {
            TurnEvaluationResult eval = turn.getEvaluationResult();
            if (eval == null) {
                continue;
            }

            GenerateReportRequest.DimensionScores scores = GenerateReportRequest.DimensionScores.builder()
                    .professional(eval.getDimensionScores().getProfessional())
                    .cognition(eval.getDimensionScores().getCognition())
                    .expression(eval.getDimensionScores().getExpression())
                    .build();


            GenerateReportRequest.DimensionDetails details = GenerateReportRequest.DimensionDetails.builder()
                    .professional(buildProfessional(eval.getProfessional()))
                    .cognition(buildCognition(eval.getCognition()))
                    .expression(buildExpression(eval.getExpression()))
                    .build();

            GenerateReportRequest.RoundResult roundResult = GenerateReportRequest.RoundResult.builder()
                    .roundId(turn.getTurnNumber())
                    .currentStage(turn.getTargetStage())
                    .dimensionScores(scores)
                    .dimensionDetails(details)
                    .finalScore(eval.getFinalScore())
                    .overallFeedback(eval.getOverallFeedback())
                    .improvementSuggestions(eval.getImprovementSuggestions())
                    .build();

            roundResults.add(roundResult);
        }

        var context = GenerateReportRequest.InterviewContext.builder()
                .jobPosition(interview.getJobRole())
                .jdSummary(interview.getJobInfo())
                .totalRounds(roundResults.size())
                .interviewDurationSeconds(interview.getDuration() != null ? (int) interview.getDuration().getSeconds() : 0)
                .resumeContent(userMapper.getVitaContent(interview.getUserId()))
                .build();

        return GenerateReportRequest.builder()
                .sessionId(interview.getInterviewId())
                .callbackUrl(callbackUrl)
                .interviewContext(context)
                .roundResults(roundResults)
                .interviewConfig(config)
                .build();
    }

    private GenerateReportRequest.Professional buildProfessional(TurnEvaluationResult.ProfessionalDetails source) {
        if (source == null) return null;
        return GenerateReportRequest.Professional.builder()
                .technicalCorrectness(mapMetric(source.getTechnicalCorrectness()))
                .knowledgeMatch(mapMetric(source.getKnowledgeMatch()))
                .jobMatch(mapMetric(source.getJobMatch()))
                .engineeringPractice(mapMetric(source.getEngineeringPractice()))
                .build();
    }

    private GenerateReportRequest.Cognition buildCognition(TurnEvaluationResult.CognitionDetails source) {
        if (source == null) return null;
        return GenerateReportRequest.Cognition.builder()
                .logicStructure(mapMetric(source.getLogicStructure()))
                .problemSolving(mapMetric(source.getProblemSolving()))
                .systemThinking(mapMetric(source.getSystemThinking()))
                .build();
    }

    private GenerateReportRequest.Expression buildExpression(TurnEvaluationResult.ExpressionDetails source) {
        if (source == null) return null;
        return GenerateReportRequest.Expression.builder()
                .clarity(mapMetric(source.getClarity()))
                .confidenceStability(mapMetric(source.getConfidenceStability()))
                .professionalMaturity(mapMetric(source.getProfessionalMaturity()))
                .build();
    }

    private GenerateReportRequest.MetricDetail mapMetric(TurnEvaluationResult.MetricDetail source) {
        if (source == null) return null;
        return GenerateReportRequest.MetricDetail.builder()
                .reason(source.getReason())
                .score(source.getScore())
                .build();
    }

    @Override
    public void getInterviewReport(String interviewId){
        InterviewEntity interview = getInterviewOrElseThrow(interviewId);
        if(!"REPORTING".equals(interview.getInterviewStatus())){
            throw new ServiceException(409, "当前面试会话未满足获取报告状态条件");
        }
        List<InterviewTurnsEntity> turnsEntities = interviewTurnsRepository.findByInterviewIdOrderByTurnNumberAsc(interviewId);
        String callbackUrl = "https://nas.feixingxr.com/api/v1/interviews/{interviewId}/report-callback";

        GenerateReportRequest requestBody = buildGenerateReportRequest(interview, turnsEntities, callbackUrl);
        log.debug("requestBody={}", requestBody);
        Result response = restClient.post()
                .uri("/report")
                .body(requestBody)
                .retrieve()
                .body(Result.class);
        if (response == null || !Integer.valueOf(200).equals(response.getCode())) {
            throw new ServiceException(500, "评价服务异常: " + (response != null ? response.getMsg() : "无响应"));
        }
    }

    @Override
    public void handleInterviewReportCallback(String interviewId, GenerateReportResponse response){
        if (response == null) {
            log.error("面试报告回调失败: 响应体为空, interviewId: {}", interviewId);
            throw new ServiceException(400, "回调响应体不能为空");
        }

        try {
            InterviewEntity interview = getInterviewOrElseThrow(interviewId);
            interview.setInterviewStatus("REPORTED");
            interview.setTotalScore(response.getOverallScore());
            interview.setHiringRecommendation(response.getHiringRecommendation());
            interview.setStrengths(response.getStrengths());
            interview.setWeaknesses(response.getWeaknesses());
            interview.setExecutiveSummary(response.getExecutiveSummary());
            interview.setDetailedRecommendation(response.getDetailedRecommendation());

            // 2.0 对应评分维度对应实现
            if (response.getProfessional() != null || response.getCognition() != null || response.getExpression() != null) {
                log.info("回调中包含各维度评价详情，直接映射数据, interviewId: {}", interviewId);
                TurnEvaluationResult totalEval = new TurnEvaluationResult();
                totalEval.setFinalScore(response.getOverallScore());

                // 映射 Professional
                if (response.getProfessional() != null) {
                    TurnEvaluationResult.ProfessionalDetails prof = new TurnEvaluationResult.ProfessionalDetails();
                    prof.setTechnicalCorrectness(mapReportMetricDetail(response.getProfessional().getTechnicalCorrectness()));
                    prof.setKnowledgeMatch(mapReportMetricDetail(response.getProfessional().getKnowledgeMatch()));
                    prof.setJobMatch(mapReportMetricDetail(response.getProfessional().getJobMatch()));
                    prof.setEngineeringPractice(mapReportMetricDetail(response.getProfessional().getEngineeringPractice()));
                    totalEval.setProfessional(prof);
                }

                // 映射 Cognition
                if (response.getCognition() != null) {
                    TurnEvaluationResult.CognitionDetails cog = new TurnEvaluationResult.CognitionDetails();
                    cog.setLogicStructure(mapReportMetricDetail(response.getCognition().getLogicStructure()));
                    cog.setProblemSolving(mapReportMetricDetail(response.getCognition().getProblemSolving()));
                    cog.setSystemThinking(mapReportMetricDetail(response.getCognition().getSystemThinking()));
                    totalEval.setCognition(cog);
                }

                // 映射 Expression
                if (response.getExpression() != null) {
                    TurnEvaluationResult.ExpressionDetails exp = new TurnEvaluationResult.ExpressionDetails();
                    exp.setClarity(mapReportMetricDetail(response.getExpression().getClarity()));
                    exp.setConfidenceStability(mapReportMetricDetail(response.getExpression().getConfidenceStability()));
                    exp.setProfessionalMaturity(mapReportMetricDetail(response.getExpression().getProfessionalMaturity()));
                    totalEval.setExpression(exp);
                }

                interview.setTotalEvaluation(totalEval);

            }

            // ToDo 这里用以区分 1.0 和 2.0 的是面试轮次具体内容的记录是否存在，
            //  目前由于2.0 中后端不进行具体记录（具体需求实现为音视频？），所以具体轮次记录为空。
            //  但是事实上最好还是分开新建接口实现，不过如果需求不变动的话，目前应该就是最高效的，加个提醒而已。
            List<InterviewTurnsEntity> turnsEntities = interviewTurnsRepository.findByInterviewIdOrderByTurnNumberAsc(interviewId);
            log.info("当前面试会话具体轮次是否为空: {}", (turnsEntities != null));
            if (turnsEntities != null && !turnsEntities.isEmpty()) {
                log.info("开始计算面试平均评价, interviewId: {}, 总轮次: {}", interviewId, turnsEntities.size());
                TurnEvaluationResult averageEvaluation = calculateAverageEvaluation(turnsEntities);
                interview.setTotalEvaluation(averageEvaluation);
            } else {
                log.warn("面试报告回调处理: 未找到对应的轮次记录, 无法计算平均分, interviewId: {}", interviewId);
            }

            interviewRepository.save(interview);
            log.info("面试报告回调处理完成并成功落库, interviewId: {}", interviewId);

        } catch (ServiceException se) {
            throw new ServiceException(se.getCode(), se.getMessage());
        } catch (Exception e) {
            log.error("处理面试报告回调时发生未知异常, interviewId: {}", interviewId, e);
            throw new ServiceException(500, "处理面试报告回调异常");
        }
    }

    /**
     * 辅助方法：将 GenerateReportResponse 中的 MetricDetail 映射为 TurnEvaluationResult 需要的 MetricDetail
     */
    private TurnEvaluationResult.MetricDetail mapReportMetricDetail(GenerateReportResponse.MetricDetail source) {
        if (source == null) {
            return null;
        }
        TurnEvaluationResult.MetricDetail target = new TurnEvaluationResult.MetricDetail();
        target.setScore(source.getScore());
        target.setReason(source.getReason());
        return target;
    }

    private TurnEvaluationResult calculateAverageEvaluation(List<InterviewTurnsEntity> turns) {
        log.info("开始执行 averageEvaluation 计算, 输入轮次数: {}", turns == null ? 0 : turns.size());
        TurnEvaluationResult totalEval = new TurnEvaluationResult();

        if (turns == null || turns.isEmpty()) {
            return totalEval;
        }

        try {
            int turnCount = 0;
            float finalScoreSum = 0;

            int dimCount = 0;
            float dimProfSum = 0, dimCogSum = 0, dimExpSum = 0;

            int[] techCorr = new int[2];
            int[] knowMatch = new int[2];
            int[] jobMatch = new int[2];
            int[] engPrac = new int[2];

            int[] logicStruct = new int[2];
            int[] probSolv = new int[2];
            int[] sysThink = new int[2];

            int[] clarity = new int[2];
            int[] confStab = new int[2];
            int[] profMat = new int[2];

            for (InterviewTurnsEntity turn : turns) {
                TurnEvaluationResult eval = turn.getEvaluationResult();
                if (eval == null) {
                    log.debug("轮次 {} 没有评价结果，跳过该轮计算", turn.getTurnNumber());
                    continue;
                }

                turnCount++;
                finalScoreSum += eval.getFinalScore();

                if (eval.getDimensionScores() != null) {
                    dimCount++;
                    dimProfSum += eval.getDimensionScores().getProfessional();
                    dimCogSum += eval.getDimensionScores().getCognition();
                    dimExpSum += eval.getDimensionScores().getExpression();
                }

                if (eval.getProfessional() != null) {
                    accumulateMetricScore(techCorr, eval.getProfessional().getTechnicalCorrectness());
                    accumulateMetricScore(knowMatch, eval.getProfessional().getKnowledgeMatch());
                    accumulateMetricScore(jobMatch, eval.getProfessional().getJobMatch());
                    accumulateMetricScore(engPrac, eval.getProfessional().getEngineeringPractice());
                }

                if (eval.getCognition() != null) {
                    accumulateMetricScore(logicStruct, eval.getCognition().getLogicStructure());
                    accumulateMetricScore(probSolv, eval.getCognition().getProblemSolving());
                    accumulateMetricScore(sysThink, eval.getCognition().getSystemThinking());
                }

                if (eval.getExpression() != null) {
                    accumulateMetricScore(clarity, eval.getExpression().getClarity());
                    accumulateMetricScore(confStab, eval.getExpression().getConfidenceStability());
                    accumulateMetricScore(profMat, eval.getExpression().getProfessionalMaturity());
                }
            }

            if (turnCount > 0) {
                totalEval.setFinalScore(finalScoreSum / turnCount);
                log.info("averageEvaluation 计算完成，有效参与打分轮次: {}, 最终平均分: {}", turnCount, totalEval.getFinalScore());
            } else {
                log.warn("averageEvaluation 计算结束，没有发现任何有效打分轮次");
            }

            if (dimCount > 0) {
                TurnEvaluationResult.DimensionScores dimScores = new TurnEvaluationResult.DimensionScores();
                dimScores.setProfessional(dimProfSum / dimCount);
                dimScores.setCognition(dimCogSum / dimCount);
                dimScores.setExpression(dimExpSum / dimCount);
                totalEval.setDimensionScores(dimScores);
            }

            TurnEvaluationResult.ProfessionalDetails profDetails = new TurnEvaluationResult.ProfessionalDetails();
            profDetails.setTechnicalCorrectness(buildAverageMetricDetail(techCorr));
            profDetails.setKnowledgeMatch(buildAverageMetricDetail(knowMatch));
            profDetails.setJobMatch(buildAverageMetricDetail(jobMatch));
            profDetails.setEngineeringPractice(buildAverageMetricDetail(engPrac));
            totalEval.setProfessional(profDetails);

            TurnEvaluationResult.CognitionDetails cogDetails = new TurnEvaluationResult.CognitionDetails();
            cogDetails.setLogicStructure(buildAverageMetricDetail(logicStruct));
            cogDetails.setProblemSolving(buildAverageMetricDetail(probSolv));
            cogDetails.setSystemThinking(buildAverageMetricDetail(sysThink));
            totalEval.setCognition(cogDetails);

            TurnEvaluationResult.ExpressionDetails expDetails = new TurnEvaluationResult.ExpressionDetails();
            expDetails.setClarity(buildAverageMetricDetail(clarity));
            expDetails.setConfidenceStability(buildAverageMetricDetail(confStab));
            expDetails.setProfessionalMaturity(buildAverageMetricDetail(profMat));
            totalEval.setExpression(expDetails);

            return totalEval;

        } catch (Exception e) {
            log.error("计算面试平均评价时发生严重异常", e);
            throw new ServiceException(500, "计算报告平均分内部异常");
        }
    }

    private void accumulateMetricScore(int[] stats, TurnEvaluationResult.MetricDetail detail) {
        if (stats == null || stats.length < 2) {
            log.warn("accumulateMetricScore 警告: 传入的 stats 数组无效");
            return;
        }
        if (detail != null && detail.getScore() != null) {
            stats[0] += detail.getScore();
            stats[1] += 1;
        }
    }

    private TurnEvaluationResult.MetricDetail buildAverageMetricDetail(int[] stats) {
        if (stats[1] == 0) {
            return null;
        }
        TurnEvaluationResult.MetricDetail avgDetail = new TurnEvaluationResult.MetricDetail();
        avgDetail.setScore(Math.round((float) stats[0] / stats[1]));
        return avgDetail;
    }

    @Override
    public ReportResultVO handleReportDataForFrontend(String interviewId) {
        log.info("准备为前端组装面试报告数据, interviewId: {}", interviewId);
        try {
            InterviewEntity interview = getInterviewOrElseThrow(interviewId);

            ReportResultVO.ReportResultVOBuilder voBuilder = ReportResultVO.builder()
                    .hiringRecommendation(interview.getHiringRecommendation())
                    .overallScore(interview.getTotalScore())
                    .executiveSummary(interview.getExecutiveSummary())
                    .strengths(interview.getStrengths())
                    .weaknesses(interview.getWeaknesses())
                    .abilityTrend(interview.getAbilityTrend())
                    .detailedRecommendation(interview.getDetailedRecommendation());

            TurnEvaluationResult totalEval = interview.getTotalEvaluation();
            if (totalEval != null) {
                if (totalEval.getDimensionScores() != null) {
                    voBuilder.dimensionScores(ReportResultVO.DimensionScores.builder()
                            .professional(totalEval.getDimensionScores().getProfessional())
                            .cognition(totalEval.getDimensionScores().getCognition())
                            .expression(totalEval.getDimensionScores().getExpression())
                            .build());
                }

                ReportResultVO.DimensionDetails.DimensionDetailsBuilder detailsBuilder = ReportResultVO.DimensionDetails.builder();

                if (totalEval.getProfessional() != null) {
                    detailsBuilder.professional(ReportResultVO.Professional.builder()
                            .technicalCorrectness(extractScoreForFrontend(totalEval.getProfessional().getTechnicalCorrectness()))
                            .knowledgeMatch(extractScoreForFrontend(totalEval.getProfessional().getKnowledgeMatch()))
                            .jobMatch(extractScoreForFrontend(totalEval.getProfessional().getJobMatch()))
                            .engineeringPractice(extractScoreForFrontend(totalEval.getProfessional().getEngineeringPractice()))
                            .build());
                }

                if (totalEval.getCognition() != null) {
                    detailsBuilder.cognition(ReportResultVO.Cognition.builder()
                            .logicStructure(extractScoreForFrontend(totalEval.getCognition().getLogicStructure()))
                            .problemSolving(extractScoreForFrontend(totalEval.getCognition().getProblemSolving()))
                            .systemThinking(extractScoreForFrontend(totalEval.getCognition().getSystemThinking()))
                            .build());
                }

                if (totalEval.getExpression() != null) {
                    detailsBuilder.expression(ReportResultVO.Expression.builder()
                            .clarity(extractScoreForFrontend(totalEval.getExpression().getClarity()))
                            .confidenceStability(extractScoreForFrontend(totalEval.getExpression().getConfidenceStability()))
                            .professionalMaturity(extractScoreForFrontend(totalEval.getExpression().getProfessionalMaturity()))
                            .build());
                }

                voBuilder.dimensionDetails(detailsBuilder.build());
            } else {
                log.warn("查询组装报告时发现: 该面试记录缺少综合评价数据(totalEvaluation为空), 可能尚未回调或回调计算失败, interviewId: {}", interviewId);
            }

            ReportResultVO resultVO = voBuilder.build();
            log.info("前端报告数据组装成功, interviewId: {}", interviewId);
            return resultVO;

        } catch (ServiceException se) {
            throw se;
        } catch (Exception e) {
            log.error("为前端组装报告数据时发生异常, interviewId: {}", interviewId, e);
            throw new ServiceException(500, "组装报告数据内部异常");
        }
    }

    private int extractScoreForFrontend(TurnEvaluationResult.MetricDetail metric) {
        if (metric != null && metric.getScore() != null) {
            return metric.getScore();
        }
        return 0;
    }

    @Override
    @Transactional
    public void tryTriggerReportGeneration(String interviewId){
        String status = getInterviewStatus(interviewId);
        if(!"WAITING_REPORT".equals(status)){
            return;
        }

        int unEvaluationTurns = interviewTurnsRepository.countUnEvaluatedTurns(interviewId);
        if(unEvaluationTurns > 0){
            log.info("还有 {} 轮面试轮次正在评分中", unEvaluationTurns);
            return;
        }

        int updateStatus = interviewRepository.updateStatusIfWaiting(interviewId, "REPORTING", "WAITING_REPORT");
        if(updateStatus > 0){
            log.info("已经完成所有面试轮次评价，开始生成报告");
            // 注册事务同步器：当前事务提交后，才去触发子线程
            TransactionSynchronizationManager.registerSynchronization(new TransactionSynchronization() {
                @Override
                public void afterCommit() {
                    executorService.execute(() -> getInterviewReport(interviewId));
                }
            });
        } else{
            log.info("已经完成所有面试轮次评价，但是更新面试会话状态失败, {}", interviewId);
        }
    }

    @Override
    public GrowthCurveVO getGrowthCurve(Long userId, String jobRole) {
        // 1. 获取按时间正序排列的面试记录
        List<InterviewEntity> interviews = interviewRepository.findAllByUserIdAndJobRoleAndInterviewStatusOrderByCreateTimeAsc(userId, jobRole, "REPORTED");

        // 2. 判空处理，交由 GlobalExceptionHandler 处理返回给前端的 Result.error
        if (interviews == null || interviews.isEmpty()) {
            throw new ServiceException(404, "该岗位暂无面试记录，无法生成成长曲线");
        }

        int interviewCount = interviews.size();
        float totalScoreSum = 0f;
        float bestScore = 0f;
        long totalDurationSeconds = 0L;
        List<Float> growthPoints = new ArrayList<>();

        // 用于计算 DimensionScores (大维度平均分) [0]存总和，[1]存有效计数
        float[] profScoreStat = new float[2];
        float[] cogScoreStat = new float[2];
        float[] expScoreStat = new float[2];

        // 用于计算 DimensionDetails (细则平均分) [0]存总和，[1]存有效计数
        float[] techCorr = new float[2];
        float[] knowMatch = new float[2];
        float[] jobMatch = new float[2];
        float[] engPrac = new float[2];

        float[] logicStruct = new float[2];
        float[] probSolv = new float[2];
        float[] sysThink = new float[2];

        float[] clarity = new float[2];
        float[] confStab = new float[2];
        float[] profMat = new float[2];

        // 3. 遍历聚合数据
        for (InterviewEntity interview : interviews) {
            float score = interview.getTotalScore();
            totalScoreSum += score;
            growthPoints.add(score); // 记录成长点（按时间正序）

            if (score > bestScore) {
                bestScore = score;
            }

            if (interview.getDuration() != null) {
                totalDurationSeconds += interview.getDuration().getSeconds();
            }

            // 累加评价维度分数
            TurnEvaluationResult eval = interview.getTotalEvaluation();
            if (eval != null) {
                // 累加大维度分数
                if (eval.getDimensionScores() != null) {
                    accumulateFloatStat(profScoreStat, eval.getDimensionScores().getProfessional());
                    accumulateFloatStat(cogScoreStat, eval.getDimensionScores().getCognition());
                    accumulateFloatStat(expScoreStat, eval.getDimensionScores().getExpression());
                }

                // 累加专业能力细则
                if (eval.getProfessional() != null) {
                    accumulateMetricStat(techCorr, eval.getProfessional().getTechnicalCorrectness());
                    accumulateMetricStat(knowMatch, eval.getProfessional().getKnowledgeMatch());
                    accumulateMetricStat(jobMatch, eval.getProfessional().getJobMatch());
                    accumulateMetricStat(engPrac, eval.getProfessional().getEngineeringPractice());
                }

                // 累加认知能力细则
                if (eval.getCognition() != null) {
                    accumulateMetricStat(logicStruct, eval.getCognition().getLogicStructure());
                    accumulateMetricStat(probSolv, eval.getCognition().getProblemSolving());
                    accumulateMetricStat(sysThink, eval.getCognition().getSystemThinking());
                }

                // 累加表达能力细则
                if (eval.getExpression() != null) {
                    accumulateMetricStat(clarity, eval.getExpression().getClarity());
                    accumulateMetricStat(confStab, eval.getExpression().getConfidenceStability());
                    accumulateMetricStat(profMat, eval.getExpression().getProfessionalMaturity());
                }
            }
        }

        // 4. 获取最近一次面试的优缺点（列表的最后一个元素）
        InterviewEntity latestInterview = interviews.get(interviews.size() - 1);
        List<String> latestStrengths = latestInterview.getStrengths() != null ? latestInterview.getStrengths() : new ArrayList<>();
        List<String> latestWeaknesses = latestInterview.getWeaknesses() != null ? latestInterview.getWeaknesses() : new ArrayList<>();

        // 5. 计算各项平均值
        float overallRating = totalScoreSum / interviewCount;
        // 练习时间：秒转为小时 (保留浮点精度)
        float practiceTimeHours = totalDurationSeconds / 3600.0f;

        // 构建大维度平均分对象
        GrowthCurveVO.DimensionScores avgDimensionScores = GrowthCurveVO.DimensionScores.builder()
                .professional(calculateAverage(profScoreStat))
                .cognition(calculateAverage(cogScoreStat))
                .expression(calculateAverage(expScoreStat))
                .build();

        // 构建细则平均分对象
        GrowthCurveVO.DimensionDetails avgDimensionDetails = GrowthCurveVO.DimensionDetails.builder()
                .professional(GrowthCurveVO.Professional.builder()
                        .technicalCorrectness(calculateAverage(techCorr))
                        .knowledgeMatch(calculateAverage(knowMatch))
                        .jobMatch(calculateAverage(jobMatch))
                        .engineeringPractice(calculateAverage(engPrac))
                        .build())
                .cognition(GrowthCurveVO.Cognition.builder()
                        .logicStructure(calculateAverage(logicStruct))
                        .problemSolving(calculateAverage(probSolv))
                        .systemThinking(calculateAverage(sysThink))
                        .build())
                .expression(GrowthCurveVO.Expression.builder()
                        .clarity(calculateAverage(clarity))
                        .confidenceStability(calculateAverage(confStab))
                        .professionalMaturity(calculateAverage(profMat))
                        .build())
                .build();

        // 6. 组装最终的 VO 并返回
        return GrowthCurveVO.builder()
                .jobRole(jobRole)
                .overallRating(overallRating)
                .interviewCount(interviewCount)
                .bestScore(bestScore)
                .practiceTime(practiceTimeHours)
                .growthPoints(growthPoints)
                .strengths(latestStrengths)
                .weaknesses(latestWeaknesses)
                .dimensionScores(avgDimensionScores)
                .dimensionDetails(avgDimensionDetails)
                .build();
    }

    /**
     * 辅助方法：用于累加 TurnEvaluationResult.MetricDetail 的整数分
     */
    private void accumulateMetricStat(float[] stat, TurnEvaluationResult.MetricDetail detail) {
        if (detail != null && detail.getScore() != null) {
            stat[0] += detail.getScore();
            stat[1] += 1;
        }
    }

    /**
     * 辅助方法：用于累加 float 类型的分数
     */
    private void accumulateFloatStat(float[] stat, float score) {
        if (score > 0) { // 假设0分代表未打分或无效
            stat[0] += score;
            stat[1] += 1;
        }
    }

    /**
     * 辅助方法：计算平均分（如果无有效打分，则默认返回 0f）
     */
    private float calculateAverage(float[] stat) {
        if (stat[1] == 0) {
            return 0f;
        }
        return stat[0] / stat[1];
    }
}