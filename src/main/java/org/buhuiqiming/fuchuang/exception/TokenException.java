package org.buhuiqiming.fuchuang.exception;

public class TokenException extends  RuntimeException{
    private String token;
    private Integer code;
    public TokenException(Integer code,String token,String message){
        super(message);
        this.token=token;
        this.code=code;
    }
    public String getToken(){
        return token;
    }
    public Integer getCode(){
        return code;
    }
}
