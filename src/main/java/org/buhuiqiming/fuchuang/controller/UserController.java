package org.buhuiqiming.fuchuang.controller;

import lombok.extern.slf4j.Slf4j;
import org.buhuiqiming.fuchuang.dto.Result;
import org.buhuiqiming.fuchuang.dto.UserDTO;
import org.buhuiqiming.fuchuang.entity.User;
import org.buhuiqiming.fuchuang.service.UserService;
import org.buhuiqiming.fuchuang.util.UserContext;
import org.springframework.web.bind.annotation.*;

@Slf4j
@RequestMapping("/api/users")
@RestController
public class UserController {
    private final UserService userService;

    public UserController(UserService userService) {
        this.userService = userService;
    }


    @GetMapping
    public Result getUser(){
        User user = userService.getUserBasicInfo();
        return Result.success(user);
    }
    @PostMapping
    public Result addUser(@RequestBody UserDTO userDTO){
        userService.addUser(userDTO);
        return Result.success();
    }
    @PutMapping
    public Result updateUser(@RequestBody UserDTO user){
        userService.updateUser(user);
        return Result.success();
    }
    @DeleteMapping
    public Result deleteUser(){
        userService.deleteUser();
        return Result.success();
    }
    @PutMapping("/resetPassword")
    public Result resetPassword(@RequestBody UserDTO userDTO){
        userService.resetPassword(userDTO);
        return Result.success();
    }
    @GetMapping("/resumeAnalysis")
    public Result getResumeAnalysis(){
        return Result.success(userService.getResumeAnalysis(UserContext.get()));
    }

}
