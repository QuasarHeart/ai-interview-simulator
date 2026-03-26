package org.buhuiqiming.fuchuang.service;

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
public class InterviewService {

    private final InterviewRepository interviewRepository;
    private final InterviewTurnsRepository interviewTurnsRepository;

    private final UserMapper userMapper;

    private final RestClient restClient;
    private final ExecutorService executorService = Executors.newVirtualThreadPerTaskExecutor();
    private final ObjectMapper objectMapper;
    private final StringRedisTemplate stringRedisTemplate;

    private final int historyTurnsCount = 4;

    @Autowired
    public InterviewService(InterviewRepository interviewRepository,
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

    // 面试会话不存在错误码判断
    public InterviewEntity getInterviewOrElseThrow(String interviewId) {
        InterviewEntity interview = interviewRepository.findByInterviewId(interviewId);
        if (interview == null) {
            throw new ServiceException(404, "面试会话不存在");
        }
        return interview;
    }

    // 获取对应面试会话当前状态
    public String getInterviewStatus(String interviewId) {
        InterviewEntity interview = interviewRepository.findByInterviewId(interviewId);
        if (interview == null) {
            throw new ServiceException(404, "面试会话不存在");
        }
        return interview.getInterviewStatus();
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

        StartInterviewQueResponse data = objectMapper.convertValue(
                response.getData(),
                StartInterviewQueResponse.class
        );
        if(data == null){
            // 服务器返回异常
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

    // 获取面试历史会话
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

            // 防止为 null
            String answerText = interviewTurnsEntity.getAnswerText() != null ? interviewTurnsEntity.getAnswerText() : "";
            String questionText = interviewTurnsEntity.getQuestion() != null ? interviewTurnsEntity.getQuestion() : "";

            // 1. 构建这一轮历史对话的 FlowControl
            InterviewFollowByRequest.HistoryData.HistoryItem.FlowControl historyFlowControl =
                    InterviewFollowByRequest.HistoryData.HistoryItem.FlowControl.builder()
                            .stageTransition(interviewTurnsEntity.getStageTransition())
                            .targetStage(interviewTurnsEntity.getTargetStage())
                            .build();

            // 2. 将一轮的 Q(assistant) 和 A(user) 合并到一个 HistoryItem 中
            InterviewFollowByRequest.HistoryData.HistoryItem item = InterviewFollowByRequest.HistoryData.HistoryItem.builder()
                    .roundId(turnsNumber)
                    .assistantContent(questionText)
                    .userContent(answerText)
                    .flowControl(historyFlowControl)
                    .build();

            // 3. 重点：使用头插法 (index: 0)，保证最终 List 中老对话在前，新对话在后。
            list.add(0, item);

            turnsNumber--;
            count--;
        }
        log.info("list={}", list);
        return list;
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
        stringRedisTemplate.opsForStream().trim("interview:eval:stream", 1200); // 最大容纳任务数为1200
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
                log.info("requestBody: {}", requestBody);
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
                                            if(metaData.containsKey("target_stage") && metaData.get("target_stage").toString().equals("end")){
                                                emitter.send("[END]");
                                                InterviewEntity endInterview = getInterviewOrElseThrow(interviewId);
                                                endInterview.setInterviewStatus("WAITING_REPORT");
                                                interviewRepository.save(endInterview);

                                                // 尝试触发报告生成
                                                self.tryTriggerReportGeneration(interviewId);
                                            } else{
                                                emitter.send("[DONE]");
                                            }
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

    // 异步读取结束后将完整的数据保存
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

    // 获取单轮回答评价
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
        log.info("getTurnsJudgeResponse:{}", data);
        if (data == null || data.getAnalysis() == null) {
            throw new ServiceException(500, "评价服务返回的数据结构异常");
        }

        TurnEvaluationResult evaluationResult = data.getAnalysis();
        interviewTurns.setEvaluationResult(evaluationResult);
    }

    // 获取历史面试列表
    public List<InterviewVO> getInterviewHistoryList(Long userId){
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

    private GenerateReportRequest buildGenerateReportRequest(InterviewEntity interview,
                                                             List<InterviewTurnsEntity> turnsEntities,
                                                             String callbackUrl) {
        // 1. 构建 InterviewConfig
        var config = GenerateReportRequest.InterviewConfig.builder()
                .mode(interview.getMode())
                .analyzeEmotion(false)        // ToDo: 后续如果有配置可替换
                .interviewerStyle(interview.getInterviewerStyle()) // ToDo: 默认风格
                .companyContext("字节")           // ToDo: 公司背景
                .difficulty(interview.getDifficulty())
                .build();

        // 2. 构建 InterviewContext
        var context = GenerateReportRequest.InterviewContext.builder()
                .jobPosition(interview.getJobRole())
                .jdSummary(interview.getJobInfo())
                .totalRounds(interview.getTurnsNumber())
                // 将 Duration 转换为秒数
                .interviewDurationSeconds(interview.getDuration() != null ? (int) interview.getDuration().getSeconds() : 0)
                .resumeContent(userMapper.getVitaContent(UserContext.get()))
                .build();

        // 3. 循环构建 RoundResults 列表
        List<GenerateReportRequest.RoundResult> roundResults = new ArrayList<>();
        for (InterviewTurnsEntity turn : turnsEntities) {
            TurnEvaluationResult eval = turn.getEvaluationResult();
            if (eval == null) {
                // 如果某轮因为异常没有生成评价，直接跳过或赋默认值
                continue;
            }

            // 3.1 映射 DimensionScores (注意类型转换：Double 转 Integer)
            GenerateReportRequest.DimensionScores scores = null;
            if (eval.getDimensionScores() != null) {
                scores = GenerateReportRequest.DimensionScores.builder()
                        .professional(eval.getDimensionScores().getProfessional())
                        .cognition(eval.getDimensionScores().getCognition())
                        .expression(eval.getDimensionScores().getExpression())
                        .build();
            }

            // 3.2 映射 DimensionDetails 的三个子维度
            GenerateReportRequest.DimensionDetails details = GenerateReportRequest.DimensionDetails.builder()
                    .professional(buildProfessional(eval.getProfessional()))
                    .cognition(buildCognition(eval.getCognition()))
                    .expression(buildExpression(eval.getExpression()))
                    .build();

            // 3.3 组装单轮 RoundResult
            GenerateReportRequest.RoundResult roundResult = GenerateReportRequest.RoundResult.builder()
                    .roundId(turn.getTurnNumber())
                    .currentStage(turn.getTargetStage()) // 也可以从 turn 扩展字段里取
                    .dimensionScores(scores)
                    .dimensionDetails(details)
                    .finalScore(eval.getFinalScore())
                    .overallFeedback(eval.getOverallFeedback())
                    .improvementSuggestions(eval.getImprovementSuggestions())
                    .build();

            roundResults.add(roundResult);
        }

        // 4. 组装最终请求体
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

    // 获取某次面试的报告
    public void getInterviewReport(String interviewId){
        InterviewEntity interview = getInterviewOrElseThrow(interviewId);
        interview.setInterviewStatus("FINISHED");
        interviewRepository.save(interview);
        List<InterviewTurnsEntity> turnsEntities = interviewTurnsRepository.findByInterviewIdOrderByTurnNumberAsc(interviewId);
        String callbackUrl = "https://nas.feixingxr.com/api/v1/interviews/{interviewId}/report-callback";

        GenerateReportRequest requestBody = buildGenerateReportRequest(interview, turnsEntities, callbackUrl);
        log.info("requestBody: {}", requestBody);
        Result result = restClient.post()
                .uri("/report")
                .body(requestBody)
                .retrieve()
                .body(Result.class);
        log.info("result: {}", result);
    }

    // 处理生成报告的回调结果
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

            // 具体各个评分维度的分数的确定（取InterviewTurnsEntity对应项的平均值）
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
            // 原样抛出业务异常
            throw se;
        } catch (Exception e) {
            log.error("处理面试报告回调时发生未知异常, interviewId: {}", interviewId, e);
            throw new ServiceException(500, "处理面试报告回调异常");
        }
    }

    /**
     * 计算所有轮次评价的平均值
     */
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

            // 使用数组累加具体细项分数: index 0 为 sum(总分), index 1 为 count(有效次数)
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

                // 1. 累加 DimensionScores
                if (eval.getDimensionScores() != null) {
                    dimCount++;
                    dimProfSum += eval.getDimensionScores().getProfessional();
                    dimCogSum += eval.getDimensionScores().getCognition();
                    dimExpSum += eval.getDimensionScores().getExpression();
                }

                // 2. 累加 ProfessionalDetails
                if (eval.getProfessional() != null) {
                    accumulateMetricScore(techCorr, eval.getProfessional().getTechnicalCorrectness());
                    accumulateMetricScore(knowMatch, eval.getProfessional().getKnowledgeMatch());
                    accumulateMetricScore(jobMatch, eval.getProfessional().getJobMatch());
                    accumulateMetricScore(engPrac, eval.getProfessional().getEngineeringPractice());
                }

                // 3. 累加 CognitionDetails
                if (eval.getCognition() != null) {
                    accumulateMetricScore(logicStruct, eval.getCognition().getLogicStructure());
                    accumulateMetricScore(probSolv, eval.getCognition().getProblemSolving());
                    accumulateMetricScore(sysThink, eval.getCognition().getSystemThinking());
                }

                // 4. 累加 ExpressionDetails
                if (eval.getExpression() != null) {
                    accumulateMetricScore(clarity, eval.getExpression().getClarity());
                    accumulateMetricScore(confStab, eval.getExpression().getConfidenceStability());
                    accumulateMetricScore(profMat, eval.getExpression().getProfessionalMaturity());
                }
            }

            // ================= 赋值平均分 =================
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

    /**
     * 辅助方法：累加单项的得分
     */
    private void accumulateMetricScore(int[] stats, TurnEvaluationResult.MetricDetail detail) {
        if (stats == null || stats.length < 2) {
            log.warn("accumulateMetricScore 警告: 传入的 stats 数组无效");
            return;
        }
        if (detail != null && detail.getScore() != null) {
            stats[0] += detail.getScore(); // sum
            stats[1] += 1;                 // count
        }
    }

    /**
     * 辅助方法：构造平均分的 MetricDetail，只设置 score 不设置 reason
     */
    private TurnEvaluationResult.MetricDetail buildAverageMetricDetail(int[] stats) {
        if (stats[1] == 0) {
            return null; // 如果没有任何一轮有该项打分，返回 null
        }
        TurnEvaluationResult.MetricDetail avgDetail = new TurnEvaluationResult.MetricDetail();
        // 取四舍五入的平均值（根据 MetricDetail 中 score 为 Integer 的要求）
        avgDetail.setScore(Math.round((float) stats[0] / stats[1]));
        // 不设置 reason，让其保持默认的 null 即可
        return avgDetail;
    }

    public ReportResultVO handleReportDataForFrontend(String interviewId) {
        log.info("准备为前端组装面试报告数据, interviewId: {}", interviewId);
        try {
            // 1. 获取面试实体
            InterviewEntity interview = getInterviewOrElseThrow(interviewId);

            // 2. 初始化 VO 的基础字段
            ReportResultVO.ReportResultVOBuilder voBuilder = ReportResultVO.builder()
                    .hiringRecommendation(interview.getHiringRecommendation())
                    .overallScore(interview.getTotalScore())
                    .executiveSummary(interview.getExecutiveSummary())
                    .strengths(interview.getStrengths())
                    .weaknesses(interview.getWeaknesses())
                    .abilityTrend(interview.getAbilityTrend())
                    .detailedRecommendation(interview.getDetailedRecommendation());

            // 3. 映射详细的评分维度 (totalEvaluation)
            TurnEvaluationResult totalEval = interview.getTotalEvaluation();
            if (totalEval != null) {
                // 3.1 映射大维度的得分 (DimensionScores)
                if (totalEval.getDimensionScores() != null) {
                    voBuilder.dimensionScores(ReportResultVO.DimensionScores.builder()
                            .professional(totalEval.getDimensionScores().getProfessional())
                            .cognition(totalEval.getDimensionScores().getCognition())
                            .expression(totalEval.getDimensionScores().getExpression())
                            .build());
                }

                // 3.2 映射细分维度的得分 (DimensionDetails)
                ReportResultVO.DimensionDetails.DimensionDetailsBuilder detailsBuilder = ReportResultVO.DimensionDetails.builder();

                // --- 专业能力 (Professional) ---
                if (totalEval.getProfessional() != null) {
                    detailsBuilder.professional(ReportResultVO.Professional.builder()
                            .technicalCorrectness(extractScoreForFrontend(totalEval.getProfessional().getTechnicalCorrectness()))
                            .knowledgeMatch(extractScoreForFrontend(totalEval.getProfessional().getKnowledgeMatch()))
                            .jobMatch(extractScoreForFrontend(totalEval.getProfessional().getJobMatch()))
                            .engineeringPractice(extractScoreForFrontend(totalEval.getProfessional().getEngineeringPractice()))
                            .build());
                }

                // --- 认知能力 (Cognition) ---
                if (totalEval.getCognition() != null) {
                    detailsBuilder.cognition(ReportResultVO.Cognition.builder()
                            .logicStructure(extractScoreForFrontend(totalEval.getCognition().getLogicStructure()))
                            .problemSolving(extractScoreForFrontend(totalEval.getCognition().getProblemSolving()))
                            .systemThinking(extractScoreForFrontend(totalEval.getCognition().getSystemThinking()))
                            .build());
                }

                // --- 表达能力 (Expression) ---
                if (totalEval.getExpression() != null) {
                    detailsBuilder.expression(ReportResultVO.Expression.builder()
                            .clarity(extractScoreForFrontend(totalEval.getExpression().getClarity()))
                            .confidenceStability(extractScoreForFrontend(totalEval.getExpression().getConfidenceStability()))
                            .professionalMaturity(extractScoreForFrontend(totalEval.getExpression().getProfessionalMaturity()))
                            .build());
                }

                // 将组装好的 details 放入 voBuilder
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

    /**
     * 辅助方法：安全地从 MetricDetail 中提取分数 (转为 int)
     */
    private int extractScoreForFrontend(TurnEvaluationResult.MetricDetail metric) {
        if (metric != null && metric.getScore() != null) {
            return metric.getScore(); // 返回 Integer，自动拆箱为 int
        }
        return 0; // 如果没有评分，默认给 0 分
    }

    // 尝试触发报告生成
    @Transactional
    public void tryTriggerReportGeneration(String interviewId){
        // 检查面试会话状态
        String status = getInterviewStatus(interviewId);
        if(!"WAITING_REPORT".equals(status)){
            return;
        }

        // 检查所有面试轮次是否都已经完成评分
        int unEvaluationTurns = interviewTurnsRepository.countUnEvaluatedTurns(interviewId);
        if(unEvaluationTurns > 0){
            log.info("还有 {} 轮面试轮次正在评分中", unEvaluationTurns);
            return;
        }

        // 更新面试会话状态
        int updateStatus = interviewRepository.updateStatusIfWaiting(interviewId, "REPORTING", "WAITING_REPORT");
        if(updateStatus > 0){
            log.info("已经完成所有面试轮次评价，开始生成报告");
            executorService.execute(() -> getInterviewReport(interviewId));
        } else{
            log.info("已经完成所有面试轮次评价，但是更新面试会话状态失败, {}", interviewId);
        }
    }
}
