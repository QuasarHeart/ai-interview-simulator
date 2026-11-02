package org.buhuiqiming.fuchuang.service;

public interface CodeService {
    public void sendCode(String email);
    public boolean checkCode(String email, String code);
}
