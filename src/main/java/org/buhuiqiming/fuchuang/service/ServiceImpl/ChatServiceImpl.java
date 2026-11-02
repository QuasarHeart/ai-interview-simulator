package org.buhuiqiming.fuchuang.service.ServiceImpl;

import org.buhuiqiming.fuchuang.dto.MessageDTO;
import org.buhuiqiming.fuchuang.entity.MyMessage;
import org.buhuiqiming.fuchuang.mapper.MessageMapper;
import org.buhuiqiming.fuchuang.service.ChatService;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class ChatServiceImpl implements ChatService {

    private MessageMapper messageMapper;

    public ChatServiceImpl(MessageMapper messageMapper) {
        this.messageMapper = messageMapper;
    }

    @Override
    public void saveMessage(MyMessage message) {
        messageMapper.saveMessage(message);
    }
    @Override
    public List<MessageDTO> getMessage(Long sessionId) {
        List<MessageDTO> messages = messageMapper.getMessageBySessionIdLimitByNum(sessionId,8);
        messages.add(messageMapper.getMessageOfSystem(sessionId));
        return messages;
    }

}
