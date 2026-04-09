package org.buhuiqiming.fuchuang.service.ServiceImpl;

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

import java.util.ArrayList;
import java.util.List;

@Slf4j
public class LLMCallServiceImpl implements LLMCallService {

    private  final UserMapper userMapper;
    private final RedisTemplate<String, String> redisTemplate;

    private final OpenAIClient client;

    public LLMCallServiceImpl(UserMapper userMapper,RedisTemplate redisTemplate) {
        // DeepSeek 设计哲学：兼容 OpenAI 规范，只需换地址
        this.client = OpenAIOkHttpClient.builder()
                .apiKey(System.getenv("DEEPSEEK_API_KEY"))
                .baseUrl("https://api.deepseek.com/v1")
                .build();

        this.userMapper = userMapper;
        this.redisTemplate = redisTemplate;
    }
    private static final String SYSTEM_PROMPT =
            "你是一个专业的简历解析助手。你的任务是从 OCR 提取的杂乱文本中抽取出结构化的简历信息。" +
            "### 约束：" +
            "1. 必须返回逻辑通顺的纯文本。" +
            "2. 修正 OCR 识别错误（如 'spring' 统一为 'Spring Boot'）。" +
            "3. 对项目经历进行语义合并，修复因换行导致的断句。"+
            "4. 不能擅自增加虚构内容";
    public String parseResume(String extractedText) {
        List<ChatCompletionMessageParam> messages = new ArrayList<>();

        // 1. 系统消息：定义规则 (显式转型解决报错)
        messages.add(ChatCompletionMessageParam.ofSystem(
                ChatCompletionSystemMessageParam.builder()
                        .content(SYSTEM_PROMPT)
                        .build()
        ));

        // 2. 用户消息：传入 OCR 文本
        messages.add(ChatCompletionMessageParam.ofUser(
                ChatCompletionUserMessageParam.builder()
                        .content("请解析以下简历内容：\n" + extractedText)
                        .build()
        ));

        // 3. 构造请求参数
        ChatCompletionCreateParams params = ChatCompletionCreateParams.builder()
                .model(ChatModel.of("deepseek-chat"))
                .messages(messages)
                .temperature(0.0)
                .build();

        // 4. 发送请求
        ChatCompletion chatCompletion = client.chat().completions().create(params);

        // 5. 获取结果
        return chatCompletion.choices().getFirst().message().content().orElse("");
    }
    @Override
    public void analyzeXml(String xml){
        //粗略处理xml，
        String text = ResumeParserUtils.extractTextFromXml( xml);
        log.info("用户id:{},粗略处理",UserContext.get());
        //redis缓存状态，防止重复请求
        if(redisTemplate.hasKey("userVita:"+UserContext.get()+":status")){
            log.info("用户id:{},已存在请求，请勿重复请求",UserContext.get());
            return;
        }

        log.info("开始调用大模型");
        //设置请求，请求大模型

        String result = parseResume(text);
        userMapper.updateVitaContent(result, UserContext.get());
        //保存状态,设置一分钟后删除
        redisTemplate.opsForValue().set("userVita:"+UserContext.get()+":status", "1", 60, java.util.concurrent.TimeUnit.SECONDS);
        UserContext.remove();
    }

}
