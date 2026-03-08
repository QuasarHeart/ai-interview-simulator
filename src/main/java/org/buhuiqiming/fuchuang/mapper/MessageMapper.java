package org.buhuiqiming.fuchuang.mapper;

import org.apache.ibatis.annotations.Insert;
import org.apache.ibatis.annotations.Mapper;
import org.buhuiqiming.fuchuang.dto.MessageDTO;
import org.buhuiqiming.fuchuang.entity.MyMessage;

import java.util.List;

@Mapper
public interface MessageMapper {
    void init_message();

    @Insert("insert into chat_message(session_id,role,content,msg_type,create_time) values(#{sessionId},#{role},#{content},#{msgType},#{createTime})")
    void saveMessage(MyMessage message);

    List<MessageDTO> getMessageBySessionIdLimitByNum(Long sessionId,Integer num);
    MessageDTO getMessageOfSystem(Long sessionId);


}
