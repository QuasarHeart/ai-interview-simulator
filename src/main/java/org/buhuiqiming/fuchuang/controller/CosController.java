package org.buhuiqiming.fuchuang.controller;

import lombok.extern.slf4j.Slf4j;
import org.buhuiqiming.fuchuang.dto.Result;
import org.buhuiqiming.fuchuang.service.LLMCallService;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@Slf4j
@RestController
@RequestMapping("/api/cos")
public class CosController {

    LLMCallService llmCallService;
    public CosController(LLMCallService llmCallService) {
        this.llmCallService = llmCallService;
    }
    @RequestMapping("/analyze")
    public Result analyze_result(@RequestBody String xml){
        log.info("cos analyze result callback");
        llmCallService.analyzeXml(xml);
        return Result.success();
    }
}
