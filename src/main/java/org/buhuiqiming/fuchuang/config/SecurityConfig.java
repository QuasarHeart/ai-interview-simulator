package org.buhuiqiming.fuchuang.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.web.SecurityFilterChain;
/**
 * @author buhuiqiming
 * @description:
 * 屏蔽默认的 Spring Security 配置
 */


@Configuration
@EnableWebSecurity
public class SecurityConfig {

        @Bean
        public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
            // 1. 禁用 CSRF
        http.csrf(csrf -> csrf.disable())
                    // 2. 禁用 Session（前后端分离无状态方案）
                    .sessionManagement(session -> session.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
                    // 3. 放行所有请求
                    .authorizeHttpRequests(auth -> auth.anyRequest().permitAll())
                    // 4. 禁用默认登录逻辑
                    .formLogin(form -> form.disable())
                    .httpBasic(basic -> basic.disable())
                    // 5. 【关键】禁用默认注销逻辑，把 /logout 路径还给 Controller
                    .logout(logout -> logout.disable())
                    // 6. 禁用默认安全响应头（可选，视前端需求而定）
                    .headers(headers -> headers.disable());

            return http.build();
        }
}

