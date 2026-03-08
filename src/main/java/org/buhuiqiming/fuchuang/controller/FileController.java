package org.buhuiqiming.fuchuang.controller;

import jakarta.servlet.http.HttpServletRequest;
import lombok.extern.slf4j.Slf4j;
import org.buhuiqiming.fuchuang.dto.Result;
import org.buhuiqiming.fuchuang.service.FileService;
import org.buhuiqiming.fuchuang.util.UserContext;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@Slf4j
@RestController
@RequestMapping("/cos/file")
public class FileController {
    private final FileService fileService;

    public FileController(FileService fileService) {
        this.fileService = fileService;
    }

    @RequestMapping("/avatar")
    public Result avatarRequest( HttpServletRequest request){
        log.info("用户{}请求头像{},method:{}", UserContext.get(), request.getParameter("filename"), request.getMethod());
        return Result.success(fileService.generateCOSURL(request, "avatar"));
    }
    @RequestMapping("/file")
    public Result fileRequest( HttpServletRequest request){
        log.info("用户{}请求文件{},method:{}", UserContext.get(), request.getParameter("filename"), request.getMethod());
        return Result.success(fileService.generateCOSURL(request, "file"));
    }


}
