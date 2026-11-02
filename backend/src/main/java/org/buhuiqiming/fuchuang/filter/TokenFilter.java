package org.buhuiqiming.fuchuang.filter;

import jakarta.servlet.*;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import lombok.extern.slf4j.Slf4j;
import org.buhuiqiming.fuchuang.exception.ServiceException;
import org.buhuiqiming.fuchuang.util.JwtUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.util.StringUtils;

import java.io.IOException;


/**
 * @author buhuiqiming
 * @date
 * 鉴权过滤器，因为异常不会被spring捕捉，并且response无法设置body，所以弃用，后续使用拦截器
 */
@Deprecated
@Slf4j
//@WebFilter(urlPatterns="/*")
public class TokenFilter implements Filter {

    @Autowired
    private JwtUtils jwtUtils;
    @Override
    public void doFilter(ServletRequest req, ServletResponse resp, FilterChain chain) throws IOException, ServletException {
        HttpServletRequest request = (HttpServletRequest) req;
        HttpServletResponse response = (HttpServletResponse) resp;

        String url = request.getRequestURL().toString();

        if(url.contains("login")||url.contains("code")){
            log.info("登录请求,放行");
            chain.doFilter(request, response);
            return;
        }
        if(url.contains("user")&&request.getMethod()=="POST"){
            log.info("用户注册请求,放行");
            chain.doFilter(request, response);
            return;
        }

        String authHeader = request.getHeader("Authorization");
        String token = null;
        if (authHeader != null && authHeader.startsWith("Bearer ")) {
            token = authHeader.substring(7); // 截取掉 "Bearer "
        }

        if(!StringUtils.hasLength( token)){
            log.info("token为空,请登录");
            throw new ServiceException(40101,"token为空，请登录");
        }

        try{
            jwtUtils.parseToken( token);
        }catch (Exception e){
            e.printStackTrace();
            log.info("token解析失败,重新登录");
            throw new ServiceException(40102,"token解析失败，请重新登录");
        }
        log.info("token解析成功");
        chain.doFilter(request,response);
    }
}
