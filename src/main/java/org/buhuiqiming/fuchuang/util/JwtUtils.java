package org.buhuiqiming.fuchuang.util;

import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.security.Keys;
import lombok.extern.slf4j.Slf4j;
import org.buhuiqiming.fuchuang.exception.ServiceException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.stereotype.Component;

import javax.crypto.SecretKey;
import java.nio.charset.StandardCharsets;
import java.util.Date;
import java.util.Map;
import java.util.concurrent.TimeUnit;

@Slf4j
@Component
public class JwtUtils {
    // 密钥长度至少要 32 个字符（256位）
    private static final String secretString = "mine-very-secure-and-long-secret-key-123456";
    private static final SecretKey key = Keys.hmacShaKeyFor(secretString.getBytes(StandardCharsets.UTF_8));
    @Autowired
    private StringRedisTemplate redisTemplate;
    /**
     * 生成token,token存入redis，1小时过期
     * 目前实现了一个用户同时登录一个地方
     * 未来可能添加一个用户同时登录多处
     * @return jwt
     */
    public  String generateJwt(Map<String,Object> claims){

        String token = Jwts.builder()
                .claims(claims)
                .issuedAt(new Date()) // 签发时间
                .expiration(new Date(System.currentTimeMillis() + 300000)) // 1小时过期
                .signWith(key) // 传入生成的 SecretKey 对象
                .compact();
        //防止重复登陆，目前仅支持一个用户同时登录，未来可能添加一个用户同时登录多处
        String lockKey = "lock:token:" + claims.get("id");

        if (redisTemplate.opsForValue().setIfAbsent(lockKey, "1", 5, TimeUnit.MINUTES)) {
            log.info("生成token成功,token:{}", token);
        } else {
            log.info("重复登录,token:{}", token);
            throw new ServiceException(401, "重复登录，当前用户已经登陆");
        }

        redisTemplate.opsForValue().set("token:userid:" + claims.get("id"), token, 6, TimeUnit.MINUTES);

        return token;

    }

    /**
     * 解析tokenx
     *
     * @param jwt
     */
    public  void parseToken(String jwt){
            Long id =Jwts.parser()
                    .verifyWith(key) // 验证密钥
                    .build()
                    .parseSignedClaims(jwt)
                    .getPayload().get("id", Long.class);
            UserContext.set(id);
    }
}
