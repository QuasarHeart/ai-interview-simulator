package org.buhuiqiming.fuchuang.controller;

import lombok.extern.slf4j.Slf4j;
import org.buhuiqiming.fuchuang.dto.LoginDTO;
import org.buhuiqiming.fuchuang.dto.Result;
import org.buhuiqiming.fuchuang.service.UserService;
import org.buhuiqiming.fuchuang.util.UserContext;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api")
@Slf4j
public class LoginController {

    private final UserService userService;

    public LoginController(UserService userService) {
        this.userService = userService;
    }

    @GetMapping("/login")
    public Result login( LoginDTO loginDTO){
        return Result.success(userService.login(loginDTO));
    }
    @PostMapping("/logout")
    public Result logout(){
        try {
            log.info("用户{}退出登录", UserContext.get());
            userService.logout();
        } catch (Exception e) {
            log.error("用户退出登录失败",e);
        }
        return Result.success();
    }
}
