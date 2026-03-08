package org.buhuiqiming.fuchuang.dto;

import lombok.Data;
 @Data
public class Result {
    private Integer code;
    private String msg;
    private Object data;

    public static Result success(){
        Result result = new Result();
        result.code =200;
        result.msg = "success";
        return result;
    }
    public static Result success(Object data){
        Result result = new Result();
        result.code =200;
        result.msg = "success";
        result.data = data;
        return result;
    }
    public static Result error(Integer code,String msg){
        Result result = new Result();
        result.code =code;
        result.msg = msg;
        return result;
    }
    public static Result error(Integer code,String msg, Object data){
        Result result = new Result();
        result.code =code;
        result.msg = msg;
        result.data = data;
        return result;
    }
}
