package org.buhuiqiming.fuchuang.websocket;

import com.fasterxml.jackson.databind.ObjectMapper;
import io.jsonwebtoken.ExpiredJwtException;
import io.jsonwebtoken.security.SignatureException;
import lombok.extern.slf4j.Slf4j;
import org.buhuiqiming.fuchuang.dto.Result;
import org.buhuiqiming.fuchuang.exception.ServiceException;
import org.buhuiqiming.fuchuang.exception.TokenException;
import org.buhuiqiming.fuchuang.util.JwtUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.server.ServerHttpRequest;
import org.springframework.http.server.ServerHttpResponse;
import org.springframework.http.server.ServletServerHttpRequest;
import org.springframework.stereotype.Component;
import org.springframework.web.socket.WebSocketHandler;
import org.springframework.web.socket.server.HandshakeInterceptor;

import java.io.IOException;
import java.util.Map;

@Slf4j
@Component
public class WebSocketAuthInterceptor implements HandshakeInterceptor {

    @Autowired
    private JwtUtils jwtUtils;

    @Autowired
    private StringRedisTemplate stringRedisTemplate;

    // 用于将 Result 对象序列化为 JSON
    private static final ObjectMapper objectMapper = new ObjectMapper();

//    @Override
//    public boolean beforeHandshake(ServerHttpRequest request, ServerHttpResponse response,
//                                   WebSocketHandler wsHandler, Map<String, Object> attributes) throws Exception {
//
//        if (request instanceof ServletServerHttpRequest) {
//            ServletServerHttpRequest servletRequest = (ServletServerHttpRequest) request;
//            String token = servletRequest.getServletRequest().getParameter("token");
//
//            try {
//                if (token == null || token.isEmpty()) {
//                    throw new ServiceException(401, "WebSocket连接拒绝：未提供Token");
//                }
//
//                Long userId = null;
//                try {
//                    userId = jwtUtils.getUserIdFromToken(token);
//                } catch (ExpiredJwtException e) {
//                    log.info("WebSocket Token已过期,即将查询redis");
//                    Long expiredUserId = e.getClaims().get("id", Long.class);
//                    String key = "token:userid:" + expiredUserId;
//                    String redisToken = stringRedisTemplate.opsForValue().get(key);
//
//                    if (redisToken == null || !redisToken.equals(token)) {
//                        throw new ServiceException(401, "登录已失效，请重新登录");
//                    } else {
//                        // Redis 中有效，签发新 Token 并抛出 TokenException 告知前端更换
//                        String lockKey = "lock:token:" + expiredUserId;
//                        stringRedisTemplate.delete(lockKey);
//                        String newToken = jwtUtils.generateJwt(e.getClaims());
//
//                        log.info("WebSocket 更新token: {}", newToken);
//                        stringRedisTemplate.delete(key);
//                        stringRedisTemplate.opsForValue().set(key, newToken);
//
//                        // 抛出自定义的 TokenException
//                        throw new TokenException(40105, newToken, "Token已过期,请更换新token后重连");
//                    }
//                } catch (SignatureException e) {
//                    throw new ServiceException(401, "非法访问：Token签名错误");
//                } catch (Exception e) {
//                    throw new ServiceException(401, "Token解析异常");
//                }
//
//                // 鉴权通过，存入 attributes 供后续 Handler 使用
//                attributes.put("userId", userId);
//                return true;
//
//            } catch (ServiceException e) {
//                // 捕获到 ServiceException，返回给前端统一的 Result 结构
//                writeErrorResponse(response, HttpStatus.UNAUTHORIZED, Result.error(e.getCode(), e.getMessage()));
//                return false;
//            } catch (TokenException e) {
//                // 捕获到 TokenException，返回带有新 Token 的 Result
//                writeErrorResponse(response, HttpStatus.UNAUTHORIZED, Result.error(e.getCode(), e.getMessage(), e.getToken()));
//                return false;
//            } catch (Exception e) {
//                log.error("WebSocket 握手发生未知异常", e);
//                writeErrorResponse(response, HttpStatus.INTERNAL_SERVER_ERROR, Result.error(500, "服务器异常"));
//                return false;
//            }
//        }
//        return false;
//    }
    @Override
    public boolean beforeHandshake(ServerHttpRequest request, ServerHttpResponse response,
                                   WebSocketHandler wsHandler, Map<String, Object> attributes) throws Exception {

        // 【开发/测试模式】直接跳过 Token 校验，硬编码一个固定的用户 ID (例如 1L)
        Long mockUserId = 1L;

        // 将 mockUserId 存入 attributes，供后续的 AudioInterviewHandler 使用
        attributes.put("userId", mockUserId);

        log.info("【开发模式】已跳过 WebSocket 鉴权，分配测试用户 ID: {}", mockUserId);

        // 直接放行
        return true;
    }

    @Override
    public void afterHandshake(ServerHttpRequest request, ServerHttpResponse response,
                               WebSocketHandler wsHandler, Exception exception) {
    }

    /**
     * 将 Result 对象序列化并写入 HTTP 响应体
     */
    private void writeErrorResponse(ServerHttpResponse response, HttpStatus status, Result result) throws IOException {
        response.setStatusCode(status);
        response.getHeaders().setContentType(MediaType.APPLICATION_JSON);
        String jsonString = objectMapper.writeValueAsString(result);
        response.getBody().write(jsonString.getBytes());
        response.getBody().flush();
    }
}