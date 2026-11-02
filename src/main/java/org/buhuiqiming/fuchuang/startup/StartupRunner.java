package org.buhuiqiming.fuchuang.startup;

import lombok.extern.slf4j.Slf4j;
import org.buhuiqiming.fuchuang.mapper.MessageMapper;
import org.buhuiqiming.fuchuang.mapper.SessionMapper;
import org.buhuiqiming.fuchuang.mapper.UserMapper;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

@Component
@Slf4j
public class StartupRunner implements CommandLineRunner {

    private UserMapper userMapper;
    private SessionMapper sessionMapper;
    private MessageMapper messageMapper;

    public StartupRunner(UserMapper userMapper, SessionMapper sessionMapper, MessageMapper messageMapper) {
        this.userMapper = userMapper;
        this.sessionMapper = sessionMapper;
        this.messageMapper = messageMapper;
    }
    @Override
    public void run(String... args) throws Exception {
        log.info("初始化数据库");
        userMapper.init_user();
        userMapper.init_account();
        sessionMapper.init_session();
        messageMapper.init_message();
    }
}