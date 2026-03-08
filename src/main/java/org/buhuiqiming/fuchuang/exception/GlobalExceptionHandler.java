package org.buhuiqiming.fuchuang.exception;

import org.buhuiqiming.fuchuang.dto.Result;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

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
    @ExceptionHandler(Exception.class)
    public ResponseEntity<Result> ExceptionHandler(Exception e) {
        Result result =Result.error(500,"服务器异常");
        return new ResponseEntity<>(result, HttpStatus.INTERNAL_SERVER_ERROR);
    }
}
