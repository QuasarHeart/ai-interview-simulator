package org.buhuiqiming.fuchuang.controller;

import org.buhuiqiming.fuchuang.dto.Result;
import org.buhuiqiming.fuchuang.service.CodeService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;


@RestController
@RequestMapping("/api/code")
public class CodeController {
    private final CodeService codeService;

    public CodeController(CodeService codeService) {
        this.codeService = codeService;
    }
    @GetMapping
    public Result sendCode(String email){
        codeService.sendCode(email);
        return Result.success();
    }
}
