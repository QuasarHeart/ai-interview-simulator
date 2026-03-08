package org.buhuiqiming.fuchuang.service;

import org.buhuiqiming.fuchuang.dto.MessageDTO;
import org.buhuiqiming.fuchuang.entity.MyMessage;

import java.util.List;

public interface ChatService {
    void saveMessage(MyMessage message);

    List<MessageDTO> getMessage(Long sessionId);

}
