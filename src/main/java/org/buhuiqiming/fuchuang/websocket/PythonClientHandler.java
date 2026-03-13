package org.buhuiqiming.fuchuang.websocket;

import lombok.extern.slf4j.Slf4j;
import org.springframework.web.socket.BinaryMessage;
import org.springframework.web.socket.CloseStatus;
import org.springframework.web.socket.TextMessage;
import org.springframework.web.socket.WebSocketSession;
import org.springframework.web.socket.handler.AbstractWebSocketHandler;

@Slf4j
public class PythonClientHandler extends AbstractWebSocketHandler {

    private final WebSocketSession frontendSession;

    public PythonClientHandler(WebSocketSession frontendSession) {
        this.frontendSession = frontendSession;
    }

    @Override
    protected void handleBinaryMessage(WebSocketSession pythonSession, BinaryMessage message) throws Exception {
        // Python传来的音频流直接转发给前端
        if(frontendSession.isOpen()){
            frontendSession.sendMessage(message);
        }

        // ToDo 异步存储到云端

    }

    @Override
    protected void handleTextMessage(WebSocketSession pythonSession, TextMessage message) throws Exception {

        // Python传来的文本内容，直接传递给前端
        if(frontendSession.isOpen()){
            frontendSession.sendMessage(message);
        }
    }

    @Override
    public void afterConnectionClosed(WebSocketSession session, CloseStatus status) throws Exception {
        /**
         * ToDo 这里的断开连接应该分两种情况：
         * 1. Python主动发出了面试结束的标志性数据之类的，这个情况下面试就应当结束，
         *    前端与后端之间的WebSocket连接也可以（或者应该）断开
         * 2. 前端用户主动结束面试，这时属于前端与后端之间的WebSocket连接先断开，
         *    Python与后端之间的WebSocket连接必须断开
         */
        log.info("与Python端连接已断开");
        if(frontendSession.isOpen()){
            frontendSession.close(status);
        }
    }
}
