package org.buhuiqiming.fuchuang.interceptor;

import io.jsonwebtoken.ExpiredJwtException;
import io.jsonwebtoken.security.SignatureException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import lombok.extern.slf4j.Slf4j;
import org.buhuiqiming.fuchuang.exception.ServiceException;
import org.buhuiqiming.fuchuang.exception.TokenException;
import org.buhuiqiming.fuchuang.util.JwtUtils;
import org.buhuiqiming.fuchuang.util.UserContext;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.stereotype.Component;
import org.springframework.web.servlet.HandlerInterceptor;

import java.util.concurrent.TimeUnit;

@Component
@Slf4j
public class LoginInterceptor implements HandlerInterceptor {

    @Autowired
    private StringRedisTemplate stringRedisTemplate;
    @Autowired
    private JwtUtils jwtUtils;
    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {


        // 所有的拦截器第一步都应该是放行 OPTIONS
        if ("OPTIONS".equalsIgnoreCase(request.getMethod()))
            return true;
        //因为采用的RESTful api，所以用户注册单独 处理
        if(request.getMethod().equals("POST")&&request.getRequestURI().contains("user"))
            return true;

        // 1. 从 Header 中获取 Token
        String authHeader = request.getHeader("Authorization");

        // 2. 校验基础格式
        if (authHeader == null || !authHeader.startsWith("Bearer ")) {
            throw new ServiceException(401, "未登录，请先登录");
        }

        // 3. 解析 Token
        String token = authHeader.substring(7);

        try{
        jwtUtils.parseToken(token);
        } catch (ExpiredJwtException e) {
            // 专门捕获：Token 已过期
            log.info("Token已过期,即将查询redis");
            // 查询redis
            String key = "token:userid:" + e.getClaims().get("id");
            String redisToken =stringRedisTemplate.opsForValue().get(key);
            // 判断redis中token是否一致
            if(redisToken == null||!redisToken.equals(token)){
                throw new ServiceException(401, "登录已失效，请重新登录");
            }
            //一致则更新token
            else {
                // 更新redis

                String lockKey = "lock:token:" + e.getClaims().get("id");
                stringRedisTemplate.delete(lockKey);
                String newToken =jwtUtils.generateJwt(e.getClaims());

                log.info("更新token: {}", newToken);
                stringRedisTemplate.delete(key);
                stringRedisTemplate.opsForValue().set(key,newToken, 75, TimeUnit.MINUTES);
                throw new TokenException(40105, newToken, "Token已过期,请更换新token");
            }
        } catch (SignatureException e) {
            // 专门捕获：签名不正确（Token 被篡改过）
            throw new ServiceException(401, "非法访问");

        } catch (Exception e) {
            // 其他异常（格式错误等）
            throw new ServiceException(401, "Token解析异常");
        }
        return true; // 放行
    }

    @Override
    public void afterCompletion(HttpServletRequest request, HttpServletResponse response, Object handler, Exception ex) {
        // 清理用户信息
        UserContext.remove();
    }
}