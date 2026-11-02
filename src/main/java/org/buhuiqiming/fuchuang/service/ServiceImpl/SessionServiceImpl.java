package org.buhuiqiming.fuchuang.service.ServiceImpl;

import lombok.extern.slf4j.Slf4j;
import org.buhuiqiming.fuchuang.entity.MySession;
import org.buhuiqiming.fuchuang.mapper.SessionMapper;
import org.buhuiqiming.fuchuang.service.SessionService;
import org.buhuiqiming.fuchuang.util.UserContext;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;

@Service
@Slf4j
public class SessionServiceImpl implements SessionService {

    private SessionMapper sessionMapper;

    public SessionServiceImpl(SessionMapper sessionMapper) {
        this.sessionMapper = sessionMapper;
    }
    @Override
    public MySession createSession(MySession session) {
        // 创建会话
        session.setCreateTime(LocalDateTime.now());
        session.setUserId(UserContext.get());

        log.info("用户{}创建会话{}", UserContext.get(), session);
        sessionMapper.createSession(session);
        return session;
    }
}
