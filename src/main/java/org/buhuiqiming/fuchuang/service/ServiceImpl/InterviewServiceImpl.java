package org.buhuiqiming.fuchuang.service.ServiceImpl;

import lombok.extern.slf4j.Slf4j;
import org.buhuiqiming.fuchuang.VO.InterviewVO;
import org.buhuiqiming.fuchuang.VO.InterviewTurnsVO;
import org.buhuiqiming.fuchuang.VO.ReportResultVO;
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
        InterviewEntity interview = new InterviewEntity(interviewId, dto.getJobRole(), dto.getDifficulty(), dto.getMode(), "CREATED", dto.getJobInfo(), dto.getInterviewerStyle());
        interview.setUserId(UserContext.get());
        interviewRepository.save(interview);
        System.out.println("create interview success");
        return interviewId;
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
                        .companyContext("字节")// ToDo: 公司背景
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

        int currentTurn = interview.getTurnsNumber();
        InterviewTurnsEntity interviewTurnsEntity = interviewTurnsRepository.findByInterviewIdAndTurnNumber(interviewId, currentTurn);
        interviewTurnsEntity.setAnswerText(answerText);

        Long currentUserId = UserContext.get();
        String resumeContent = userMapper.getVitaContent(currentUserId);
        interviewTurnsEntity.setStageTransition("continue");
        interviewTurnsEntity.setTargetStage("intro");

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
                                                InterviewEntity endInterview = getInterviewOrElseThrow(interviewId);
                                                endInterview.setInterviewStatus("WAITING_REPORT");
                                                interviewRepository.save(endInterview);

                                                self.tryTriggerReportGeneration(interviewId);
                                            } else{
                                                emitter.send("[DONE]");
                                            }
                                            emitter.complete();
                                            saveTurnMetaData(interviewId, queBuffer.toString(), metaData);
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
            interviewVO.setInterviewId(interview.getInterviewId());
            interviewVO.setJobRole(interview.getJobRole()); // 修正这里的潜在问题
            interviewVO.setDifficulty(interview.getDifficulty());
            interviewVO.setMode(interview.getMode());
            interviewVO.setScore(interview.getTotalScore());
            interviewVO.setDuration(interview.getDuration());

            resultList.add(interviewVO);
        }
        return resultList;
    }

    @Override
    public List<InterviewTurnsVO> getInterviewTurns(String interviewId){
        getInterviewOrElseThrow(interviewId);

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

        var context = GenerateReportRequest.InterviewContext.builder()
                .jobPosition(interview.getJobRole())
                .jdSummary(interview.getJobInfo())
                .totalRounds(interview.getTurnsNumber())
                .interviewDurationSeconds(interview.getDuration() != null ? (int) interview.getDuration().getSeconds() : 0)
                .resumeContent(userMapper.getVitaContent(UserContext.get()))
                .build();

        List<GenerateReportRequest.RoundResult> roundResults = new ArrayList<>();
        for (InterviewTurnsEntity turn : turnsEntities) {
            TurnEvaluationResult eval = turn.getEvaluationResult();
            if (eval == null) {
                continue;
            }

            GenerateReportRequest.DimensionScores scores = null;
            if (eval.getDimensionScores() != null) {
                scores = GenerateReportRequest.DimensionScores.builder()
                        .professional(eval.getDimensionScores().getProfessional())
                        .cognition(eval.getDimensionScores().getCognition())
                        .expression(eval.getDimensionScores().getExpression())
                        .build();
            }

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
        interview.setInterviewStatus("REPORTING");
        interviewRepository.save(interview);
        List<InterviewTurnsEntity> turnsEntities = interviewTurnsRepository.findByInterviewIdOrderByTurnNumberAsc(interviewId);
        String callbackUrl = "https://nas.feixingxr.com/api/v1/interviews/{interviewId}/report-callback";

        GenerateReportRequest requestBody = buildGenerateReportRequest(interview, turnsEntities, callbackUrl);

        Result result = restClient.post()
                .uri("/report")
                .body(requestBody)
                .retrieve()
                .body(Result.class);
    }

    @Override
    public void handleInterviewReportCallback(String interviewId, GenerateReportResponse response){
        log.info("接收到面试报告回调, interviewId: {}, response: {}", interviewId, response);

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

            List<InterviewTurnsEntity> turnsEntities = interviewTurnsRepository.findByInterviewIdOrderByTurnNumberAsc(interviewId);
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
            throw se;
        } catch (Exception e) {
            log.error("处理面试报告回调时发生未知异常, interviewId: {}", interviewId, e);
            throw new ServiceException(500, "处理面试报告回调异常");
        }
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
            executorService.execute(() -> getInterviewReport(interviewId));
        } else{
            log.info("已经完成所有面试轮次评价，但是更新面试会话状态失败, {}", interviewId);
        }
    }
}