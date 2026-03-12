package org.buhuiqiming.fuchuang.service.ServiceImpl;

import lombok.extern.slf4j.Slf4j;
import org.buhuiqiming.fuchuang.exception.ServiceException;
import org.buhuiqiming.fuchuang.service.CodeService;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.mail.SimpleMailMessage;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.stereotype.Service;

import java.util.concurrent.TimeUnit;


@Slf4j
@Service
public class CodeServiceImpl implements CodeService {

    private JavaMailSender mailSender;
    private StringRedisTemplate redisTemplate;
    public CodeServiceImpl(JavaMailSender mailSender, StringRedisTemplate redisTemplate) {
        this.mailSender = mailSender;
        this.redisTemplate = redisTemplate;
    }

    @Override
    public void sendCode(String email) {

        String lockKey = "lock:sendemail:" + email;

        // setIfAbsent 等同于 Redis 的 SETNX 命令：如果 Key 不存在才存入，返回 true；已存在则返回 false
        Boolean success = redisTemplate.opsForValue()
                .setIfAbsent(lockKey, "1", 60, TimeUnit.SECONDS);

        if (Boolean.FALSE.equals(success)) {
            throw new ServiceException(425,"操作太快了，请60秒后再试");
        }


        String code=String.valueOf((int)((Math.random()*9+1)*100000));
        redisTemplate.opsForValue().set("email:code:" + email, code, 5, TimeUnit.MINUTES);

        SimpleMailMessage message = new SimpleMailMessage();
        message.setFrom("2979734778@qq.com");
        message.setTo(email);
        message.setSubject("您的注册/重置验证码");
        message.setText("您的验证码为：" + code + "，有效期5分钟。");
        mailSender.send(message);
    }
    @Override
    public boolean checkCode(String email, String userInputCode) {

        String redisKey = "email:code:" + email;
        String storedCode = redisTemplate.opsForValue().get(redisKey);

        if (storedCode == null) {
            throw new ServiceException(428,"验证码已过期或未发送");
        }

        if (!storedCode.equals(userInputCode)) {
            throw new ServiceException(412,"验证码错误");
        }
        log.debug("验证码验证成功");
        // 验证成功后，立即删除 Redis 中的验证码，防止“二次使用”攻击
        redisTemplate.delete(redisKey);

        return true;
    }
}
