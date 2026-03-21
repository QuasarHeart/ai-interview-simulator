package org.buhuiqiming.fuchuang.service.ServiceImpl;

import lombok.extern.slf4j.Slf4j;
import org.buhuiqiming.fuchuang.service.LLMCallService;
import org.buhuiqiming.fuchuang.util.ResumeParserUtils;
import org.buhuiqiming.fuchuang.util.UserContext;
import org.springframework.stereotype.Service;

@Slf4j
@Service
public class LLMCallServiceImpl implements LLMCallService {

    @Override
    public void analyzeXml(String xml){
        //粗略处理xml，
        String text = ResumeParserUtils.extractTextFromXml( xml);
        log.info("粗略处理，text:{}", text);
        log.info("开始调用大模型");
        //设置请求，请求大模型


        UserContext.remove();
    }
}
