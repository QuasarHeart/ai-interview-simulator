package org.buhuiqiming.fuchuang;

import org.buhuiqiming.fuchuang.service.InterviewService;
import org.mybatis.spring.annotation.MapperScan;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.web.server.servlet.context.ServletComponentScan;
import org.springframework.data.jpa.repository.config.EnableJpaRepositories;

@ServletComponentScan
@SpringBootApplication
@MapperScan("org.buhuiqiming.fuchuang.mapper")
@EnableJpaRepositories(basePackages = "org.buhuiqiming.fuchuang.repository")
public class FuchuangApplication {

    public static void main(String[] args) {

        SpringApplication.run(FuchuangApplication.class, args);
    }
}
