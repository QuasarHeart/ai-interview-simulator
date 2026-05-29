package org.buhuiqiming.fuchuang.service.ServiceImpl;

import tools.jackson.databind.JsonNode;
import tools.jackson.databind.ObjectMapper;
import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.models.ChatModel;
import com.openai.models.chat.completions.*;
import lombok.extern.slf4j.Slf4j;
import org.buhuiqiming.fuchuang.mapper.UserMapper;
import org.buhuiqiming.fuchuang.service.LLMCallService;
import org.buhuiqiming.fuchuang.util.ResumeParserUtils;
import org.buhuiqiming.fuchuang.util.UserContext;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

@Slf4j
@Service
public class LLMCallServiceImpl_2 implements LLMCallService {

    private final UserMapper userMapper;
    private final RedisTemplate<String, String> redisTemplate;
    private final OpenAIClient client;
    private final ObjectMapper objectMapper;

    private static final String SYSTEM_PROMPT =
            "你是一个专业的简历解析助手。你的任务是从 OCR 提取的杂乱文本中抽取出结构化的简历信息。" +
                    "### 约束：" +
                    "1. 必须返回逻辑通顺的纯文本。" +
                    "2. 修正 OCR 识别错误（如 'spring' 统一为 'Spring Boot'）。" +
                    "3. 对项目经历进行语义合并，修复因换行导致的断句。" +
                    "4. 不能擅自增加虚构内容";

    // 修改提示词，要求返回JSON数组格式
    private static final String ANALYSIS_SYSTEM_PROMPT =
            "你是一个专业的HR和职业发展顾问，擅长分析简历的优缺点并提供建设性意见。" +
                    "### 任务：" +
                    "1. 分析简历的优势和亮点（至少3条）" +
                    "2. 指出简历的不足和改进空间（至少3条）" +
                    "3. 提供具体的、可操作的改进建议（至少3条）" +
                    "4. 评估候选人的整体竞争力并给出评分（满分10分，保留1位小数）" +
                    "### 输出格式要求：" +
                    "必须严格按照以下JSON格式返回，不要包含其他说明文字：\n" +
                    "{\n" +
                    "  \"strengths\": [\"优点1的描述\", \"优点2的描述\", \"优点3的描述\"],\n" +
                    "  \"weaknesses\": [\"缺点1的描述\", \"缺点2的描述\", \"缺点3的描述\"],\n" +
                    "  \"suggestions\": [\"建议1的描述\", \"建议2的描述\", \"建议3的描述\"],\n" +
                    "  \"overall_score\": 8.5\n" +
                    "}" +
                    "### 约束：" +
                    "1. 分析要客观、专业、有建设性" +
                    "2. 每条优点、缺点、建议都要具体明确，不要空泛" +
                    "3. 避免过于主观或情绪化的评价" +
                    "4. 建议要具体可行，最好包含可执行的步骤" +
                    "5. overall_score为满分10分的评分，保留1位小数" +
                    "6. 所有字段都是数组格式，即使只有一条也要用数组表示";

    public LLMCallServiceImpl_2(UserMapper userMapper, RedisTemplate redisTemplate, ObjectMapper objectMapper) {
        this.client = OpenAIOkHttpClient.builder()
                .apiKey(System.getenv("DEEPSEEK_API_KEY"))
                .baseUrl("https://api.deepseek.com")
                .build();
        this.userMapper = userMapper;
        this.redisTemplate = redisTemplate;
        this.objectMapper = objectMapper;
    }

    /**
     * 解析简历
     */
    public String parseResume(String extractedText) {
        return callDeepSeek(SYSTEM_PROMPT, "请解析以下简历内容：\n" + extractedText, 0.0);
    }

    /**
     * 分析简历优缺点，返回列表形式的结果
     */
    public AnalysisResult analyzeResumeStrengths(String parsedResume) {
        String userPrompt = String.format(
                "请分析以下简历的优缺点：\n\n%s",
                parsedResume
        );

        String response = callDeepSeek(ANALYSIS_SYSTEM_PROMPT, userPrompt, 0.3);
        return parseAnalysisResponseToList(response);
    }

    /**
     * 解析分析结果为列表形式
     */
    private AnalysisResult parseAnalysisResponseToList(String response) {
        AnalysisResult result = new AnalysisResult();

        try {
            // 提取JSON内容
            String jsonContent = extractJsonContent(response);

            JsonNode jsonNode = objectMapper.readTree(jsonContent);

            // 解析strengths数组
            if (jsonNode.has("strengths") && jsonNode.get("strengths").isArray()) {
                List<String> strengths = new ArrayList<>();
                for (JsonNode item : jsonNode.get("strengths")) {
                    strengths.add(item.asText());
                }
                result.setStrengths(strengths);
            }

            // 解析weaknesses数组
            if (jsonNode.has("weaknesses") && jsonNode.get("weaknesses").isArray()) {
                List<String> weaknesses = new ArrayList<>();
                for (JsonNode item : jsonNode.get("weaknesses")) {
                    weaknesses.add(item.asText());
                }
                result.setWeaknesses(weaknesses);
            }

            // 解析suggestions数组
            if (jsonNode.has("suggestions") && jsonNode.get("suggestions").isArray()) {
                List<String> suggestions = new ArrayList<>();
                for (JsonNode item : jsonNode.get("suggestions")) {
                    suggestions.add(item.asText());
                }
                result.setSuggestions(suggestions);
            }

            // 解析评分
            if (jsonNode.has("overall_score")) {
                result.setOverallScore(jsonNode.get("overall_score").asDouble());
            }

        } catch (Exception e) {
            log.error("解析分析结果失败: {}", e.getMessage());
            log.error("原始响应: {}", response);

            // 降级方案：使用正则表达式提取并转换为列表
            result.setStrengths(extractSectionAsList(response, "优点"));
            result.setWeaknesses(extractSectionAsList(response, "缺点|待改进"));
            result.setSuggestions(extractSectionAsList(response, "建议"));
            result.setOverallScore(extractScore(response));
        }

        return result;
    }

    /**
     * 提取JSON内容（处理可能被markdown包裹的情况）
     */
    private String extractJsonContent(String response) {
        // 尝试提取 ```json ... ``` 包裹的内容
        Pattern pattern = Pattern.compile("```json\\s*(\\{.*?\\})\\s*```", Pattern.DOTALL);
        Matcher matcher = pattern.matcher(response);
        if (matcher.find()) {
            return matcher.group(1);
        }

        // 尝试提取 ``` ... ``` 包裹的内容
        pattern = Pattern.compile("```\\s*(\\{.*?\\})\\s*```", Pattern.DOTALL);
        matcher = pattern.matcher(response);
        if (matcher.find()) {
            return matcher.group(1);
        }

        // 直接提取JSON对象
        pattern = Pattern.compile("\\{.*\\}", Pattern.DOTALL);
        matcher = pattern.matcher(response);
        if (matcher.find()) {
            return matcher.group();
        }

        return response;
    }

    /**
     * 从文本中提取章节并转换为列表
     */
    private List<String> extractSectionAsList(String text, String sectionName) {
        List<String> items = new ArrayList<>();

        // 匹配 【优点】 或 【待改进之处】 等格式
        Pattern pattern = Pattern.compile(
                String.format("【%s】\\s*\\n([\\s\\S]*?)(?=【|\\Z)", sectionName),
                Pattern.DOTALL
        );
        Matcher matcher = pattern.matcher(text);

        if (matcher.find()) {
            String content = matcher.group(1).trim();
            // 按数字序号分割（1. 2. 3. 或 1、2、3、）
            String[] lines = content.split("\\n");
            for (String line : lines) {
                line = line.trim();
                if (line.isEmpty()) continue;
                // 移除序号前缀（如 "1. " 或 "1、" 或 "1、"）
                line = line.replaceAll("^\\d+[\\.、]\\s*", "");
                if (!line.isEmpty()) {
                    items.add(line);
                }
            }
        }

        return items;
    }

    /**
     * 提取评分
     */
    private double extractScore(String text) {
        Pattern pattern = Pattern.compile("评分[：:]\\s*(\\d+(?:\\.\\d+)?)");
        Matcher matcher = pattern.matcher(text);
        if (matcher.find()) {
            try {
                return Double.parseDouble(matcher.group(1));
            } catch (NumberFormatException e) {
                return 0.0;
            }
        }
        return 0.0;
    }

    /**
     * 调用DeepSeek API
     */
    private String callDeepSeek(String systemPrompt, String userPrompt, double temperature) {
        List<ChatCompletionMessageParam> messages = new ArrayList<>();

        messages.add(ChatCompletionMessageParam.ofSystem(
                ChatCompletionSystemMessageParam.builder()
                        .content(systemPrompt)
                        .build()
        ));

        messages.add(ChatCompletionMessageParam.ofUser(
                ChatCompletionUserMessageParam.builder()
                        .content(userPrompt)
                        .build()
        ));

        ChatCompletionCreateParams params = ChatCompletionCreateParams.builder()
                .model(ChatModel.of("deepseek-v4-flash"))
                .messages(messages)
                .temperature(temperature)
                .build();

        try {
            ChatCompletion chatCompletion = client.chat().completions().create(params);
            String content = chatCompletion.choices().getFirst().message().content().orElse("");
            log.info("DeepSeek API响应: {}", content);
            return content;
        } catch (Exception e) {
            log.error("调用DeepSeek API失败: {}", e.getMessage(), e);
            return "";
        }
    }

    @Override
    public void analyzeXml(String xml) {

        String text = ResumeParserUtils.extractTextFromXml(xml);
        Long userId = UserContext.get();
        log.info("用户id:{}, 粗略处理完成", userId);

        if (Boolean.TRUE.equals(redisTemplate.hasKey("userVita:" + userId + ":status"))) {
            log.info("用户id:{}, 已存在请求，请勿重复请求", userId);
            return;
        }

        try {
            // 1. 解析简历
            log.info("开始调用大模型解析简历，用户id:{}", userId);
            String parsedResume = parseResume(text);
            userMapper.updateVitaContent(parsedResume, userId);
            redisTemplate.delete("userVita:content:" + userId);

            // 2. 分析简历优缺点（返回列表）
            log.info("开始分析简历优缺点，用户id:{}", userId);
            AnalysisResult analysisResult = analyzeResumeStrengths(parsedResume);

            // 3. 将列表转换为JSON字符串存储
            String strengthsJson = objectMapper.writeValueAsString(analysisResult.getStrengths());
            String weaknessesJson = objectMapper.writeValueAsString(analysisResult.getWeaknesses());
            String suggestionsJson = objectMapper.writeValueAsString(analysisResult.getSuggestions());

            // 4. 保存到数据库
            userMapper.updateAnalysisResult(
                    strengthsJson,
                    weaknessesJson,
                    suggestionsJson,
                    analysisResult.getOverallScore(),
                    userId
            );

            log.info("简历分析完成，用户id:{}, 优点数:{}, 缺点数:{}, 建议数:{}, 评分:{}",
                    userId,
                    analysisResult.getStrengths().size(),
                    analysisResult.getWeaknesses().size(),
                    analysisResult.getSuggestions().size(),
                    analysisResult.getOverallScore()
            );

        } catch (Exception e) {
            log.error("处理简历失败，用户id:{}: {}", userId, e.getMessage(), e);
            try {
                userMapper.updateVitaContent("处理失败：" + e.getMessage(), userId);
            } catch (Exception ex) {
                log.error("保存错误信息失败", ex);
            }
        } finally {
            redisTemplate.opsForValue().set(
                    "userVita:" + userId + ":status",
                    "1",
                    60,
                    java.util.concurrent.TimeUnit.SECONDS
            );
            UserContext.remove();
        }
    }

    /**
     * 分析结果类（使用列表存储）
     */
    public static class AnalysisResult {
        private List<String> strengths = new ArrayList<>();
        private List<String> weaknesses = new ArrayList<>();
        private List<String> suggestions = new ArrayList<>();
        private double overallScore;

        public List<String> getStrengths() { return strengths; }
        public void setStrengths(List<String> strengths) { this.strengths = strengths; }

        public List<String> getWeaknesses() { return weaknesses; }
        public void setWeaknesses(List<String> weaknesses) { this.weaknesses = weaknesses; }

        public List<String> getSuggestions() { return suggestions; }
        public void setSuggestions(List<String> suggestions) { this.suggestions = suggestions; }

        public double getOverallScore() { return overallScore; }
        public void setOverallScore(double overallScore) { this.overallScore = overallScore; }
    }
}