package org.buhuiqiming.fuchuang.config;

import org.buhuiqiming.fuchuang.interceptor.LoginInterceptor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.InterceptorRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@Configuration
public class WebMvcConfig implements WebMvcConfigurer {

    @Autowired
    private LoginInterceptor loginInterceptor;

    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(loginInterceptor)
                .addPathPatterns("/**")             // 拦截所有请求
                .excludePathPatterns(               // 排除不需要登录的接口
                        "/login",              // 登录接口
                        "/code",// 发送验证码
                        "/users/resetPassword",// 重置密码
                        "/cos/analyze",  //COS回调
                        "/api/v1/interviews/{interviewId}/report-callback"
                );
    }
    @Override
    public void addCorsMappings(CorsRegistry registry) {
        registry.addMapping("/**") // 匹配所有路径
                .allowedOrigins("*") // 允许的域名
                .allowedMethods("GET", "POST", "PUT", "DELETE", "OPTIONS") // 允许的方法
                .allowedHeaders("*") // 允许的请求头
                .maxAge(3600); // 预检请求的有效期（秒）
    }
}
