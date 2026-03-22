package org.buhuiqiming.fuchuang.service;

import lombok.extern.slf4j.Slf4j;
import org.buhuiqiming.fuchuang.VO.InterviewVO;
import org.buhuiqiming.fuchuang.VO.InterviewTurnsVO;
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

    private final int historyTurnsCount = 4;

    @Autowired
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
    public List<InterviewFollowByRequest.HistoryData.HistoryItem> getInterviewHistory(String interviewId){
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

            InterviewFollowByRequest.HistoryData.HistoryItem itemAns = InterviewFollowByRequest.HistoryData.HistoryItem.builder()
                    .role("user")
                    .content(answerText)
                    .build();

            InterviewFollowByRequest.HistoryData.HistoryItem itemQue = InterviewFollowByRequest.HistoryData.HistoryItem.builder()
                    .role("assistant")
                    .content(questionText)
                    .build();

            // 重点：使用头插法 (index: 0)，先插入回答，再插入问题。
            // 这样能保证倒序遍历出来的历史在最终 List 中是老对话在前、新对话在后，且 Q 在 A 之前。
            list.add(0, itemAns);
            list.add(0, itemQue);

            turnsNumber--;
            count--;
        }
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

        interviewTurnsRepository.save(interviewTurnsEntity);

        executorService.execute(() -> {
            try{
                getTurnsJudgement(interview, interviewTurnsEntity, resumeContent);
                interviewTurnsRepository.save(interviewTurnsEntity);
            } catch (Exception e){
                log.error("获取当前轮次评价异常, interviewId: {}, turn: {}", interviewId, currentTurn, e);
            }
        });

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
                        .resumeSummary(resumeContent)
                        .jdSummary(interview.getJobInfo())
                        .build();

                List<InterviewFollowByRequest.HistoryData.HistoryItem> historyItems = getInterviewHistory(interviewId);

                var history = InterviewFollowByRequest.HistoryData.builder()
                        .historySummary(interview.getHistorySummary())
                        .recentHistory(historyItems)
                        .build();
                var flow = InterviewFollowByRequest.FlowControl.builder()
                        .stageTransition(interviewTurnsEntity.getStageTransition())
                        .targetStage(interviewTurnsEntity.getTargetStage())
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

    // 获取单轮回答评价
    public void getTurnsJudgement(InterviewEntity interview, InterviewTurnsEntity interviewTurns, String context){
        var config = GetTurnsJudgeRequest.InterviewConfig.builder()
                .mode(interview.getMode())
                .analyzeEmotion(false)
                .companyContext("")
                .interviewerStyle(interview.getInterviewerStyle())
                .difficulty(interview.getDifficulty())
                .build();
        var analyze = GetTurnsJudgeRequest.ContentToAnalyze.builder()
                .question(interviewTurns.getQuestion())
                .userAnswer(interviewTurns.getAnswerText())
                .jobPosition(interview.getJobRole())
                .jbSummary(interview.getJobInfo())
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

    // 获取历史面试列表
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

    private GenerateReportRequest buildGenerateReportRequest(InterviewEntity interview,
                                                             List<InterviewTurnsEntity> turnsEntities,
                                                             String callbackUrl) {
        // 1. 构建 InterviewConfig
        var config = GenerateReportRequest.InterviewConfig.builder()
                .mode(interview.getMode())
                .analyzeEmotion(false)        // ToDo: 后续如果有配置可替换
                .interviewerStyle(interview.getInterviewerStyle()) // ToDo: 默认风格
                .companyContext("")           // ToDo: 公司背景
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
                        // API 要求 cognition 是 Integer，而实体里可能是 Double
                        .cognition(eval.getDimensionScores().getCognition() != null ? eval.getDimensionScores().getCognition().intValue() : null)
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

    /**
     * 通用的细项分数转换工具：将实体的 MetricDetail 转为 DTO 的 MetricDetail，处理了 Double 到 Integer 的强转
     */
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
        List<InterviewTurnsEntity> turnsEntities = interviewTurnsRepository.findByInterviewIdOrderByTurnNumberAsc(interviewId);
        String callbackUrl = "/{interviewId}/report";

        GenerateReportRequest requestBody = buildGenerateReportRequest(interview, turnsEntities, callbackUrl);
        Result result = restClient.post()
                .uri("/report")
                .body(requestBody)
                .retrieve()
                .body(Result.class);
    }
}
