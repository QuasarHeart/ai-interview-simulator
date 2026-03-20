package org.buhuiqiming.fuchuang.controller;

import lombok.extern.slf4j.Slf4j;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@Slf4j
@RestController
@RequestMapping("/cos")
public class CosController {
    @RequestMapping("/analyze")
    public void analyze_result(@RequestBody String xml){
        log.info("xml:{}", xml);
    }
}
