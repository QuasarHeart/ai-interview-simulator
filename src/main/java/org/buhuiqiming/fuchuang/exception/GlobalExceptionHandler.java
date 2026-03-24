package org.buhuiqiming.fuchuang.exception;

import lombok.extern.slf4j.Slf4j;
import org.buhuiqiming.fuchuang.dto.Result;
import org.springframework.dao.DataAccessException;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;
import org.springframework.web.client.RestClientResponseException;

@Slf4j
@RestControllerAdvice
public class GlobalExceptionHandler {
    @ExceptionHandler(ServiceException.class)
    public ResponseEntity<Result> ServiceExceptionHandler(ServiceException e) {
        Result result= Result.error(e.getCode(),e.getMessage());
        return new ResponseEntity<>(result,HttpStatus.BAD_REQUEST);
    }
    @ExceptionHandler(TokenException.class)
    public ResponseEntity<Result> TokenExceptionHandler(TokenException e) {
        Result result =Result.error(e.getCode(),e.getMessage(), e.getToken());
        return new ResponseEntity<>(result, HttpStatus.UNAUTHORIZED);
    }
    @ExceptionHandler(DataAccessException.class)
    public ResponseEntity<Result> dataAccessExceptionHandler(DataAccessException e) {
        log.error("数据库操作异常: ", e);
        Result result = Result.error(500, "系统数据处理异常，请稍后重试");
        return new ResponseEntity<>(result, HttpStatus.INTERNAL_SERVER_ERROR);
    }
    @ExceptionHandler(RestClientResponseException.class)
    public ResponseEntity<Result> restClientResponseExceptionHandler(RestClientResponseException e) {
        log.error("调用算法端服务发生 HTTP 异常! 状态码: {}", e.getStatusCode());
        String responseBody = e.getResponseBodyAsString();
        log.error("算法端详细报错内容: {}", responseBody);
        Result result = Result.error(500, "算法端处理失败，详细错误已记录在后端日志中");
        return new ResponseEntity<>(result, HttpStatus.INTERNAL_SERVER_ERROR);
    }
    @ExceptionHandler(Exception.class)
    public ResponseEntity<Result> ExceptionHandler(Exception e) {
        Result result =Result.error(500,"服务器异常");
        return new ResponseEntity<>(result, HttpStatus.INTERNAL_SERVER_ERROR);
    }
}
