package org.buhuiqiming.fuchuang;

import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.web.server.servlet.context.ServletComponentScan;
import org.springframework.data.jpa.repository.config.EnableJpaRepositories;
import org.springframework.scheduling.annotation.EnableScheduling;

@ServletComponentScan
@SpringBootApplication
@MapperScan("org.buhuiqiming.fuchuang.mapper")
@EnableJpaRepositories(basePackages = "org.buhuiqiming.fuchuang.repository")
@EnableScheduling
public class FuchuangApplication {

    public static void main(String[] args) {

        SpringApplication.run(FuchuangApplication.class, args);
    }
}
