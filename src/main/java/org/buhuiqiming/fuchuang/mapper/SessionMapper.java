package org.buhuiqiming.fuchuang.mapper;

import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Options;
import org.buhuiqiming.fuchuang.entity.MySession;

@Mapper
public interface SessionMapper {
    void init_session();

    @Options(useGeneratedKeys = true, keyProperty = "sessionId")
    @Insert("insert into chat_session(user_id,create_time,title,session_type) values(#{userId},#{createTime},#{title},#{sessionType})")
    void createSession(MySession mySession);

    MySession getSessionByUserId(Long userId,Integer page,Integer pageSize);
}
