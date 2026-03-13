package org.buhuiqiming.fuchuang.websocket;

import jakarta.websocket.ContainerProvider;
import jakarta.websocket.WebSocketContainer;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;
import org.springframework.web.socket.BinaryMessage;
import org.springframework.web.socket.CloseStatus;
import org.springframework.web.socket.WebSocketSession;
import org.springframework.web.socket.client.standard.StandardWebSocketClient;
import org.springframework.web.socket.handler.BinaryWebSocketHandler;

import java.nio.ByteBuffer;
import java.util.concurrent.ExecutionException;

@Slf4j
@Component
public class AudioInterviewHandler extends BinaryWebSocketHandler {

    private static final String PYTHON_WS_URL = "ws://localhost:8000/ws/interview/audio/python/";

    @Override
    public void afterConnectionEstablished(WebSocketSession session) throws Exception {
        // 从 attributes 中获取用户 ID
        Long userId = (Long) session.getAttributes().get("userId");
        log.info("WebSocket 连接建立完成，用户 ID: {}, Session ID: {}", userId, session.getId());

        // 当Python回传的时候，设置容器
        WebSocketContainer container = ContainerProvider.getWebSocketContainer();
        container.setDefaultMaxBinaryMessageBufferSize(10 * 1024 * 1024);
        container.setDefaultMaxTextMessageBufferSize(1024 * 1024);

        StandardWebSocketClient client = new StandardWebSocketClient(container);
        PythonClientHandler pythonClientHandler = new PythonClientHandler(session);

        try{
            String targetURL = PYTHON_WS_URL + userId;
            WebSocketSession pythonSession = client.execute(pythonClientHandler, targetURL).get();

            session.getAttributes().put("pythonSession", pythonSession);
            log.info("成功建立和Python端的连接");

        } catch(InterruptedException | ExecutionException e){
            log.info("建立连接失败");
            session.close(CloseStatus.SERVER_ERROR);
        }
    }

    @Override
    protected void handleBinaryMessage(WebSocketSession session, BinaryMessage message) throws Exception {
        WebSocketSession pythonSession = (WebSocketSession) session.getAttributes().get("pythonSession");

        if(pythonSession != null && pythonSession.isOpen()){
            pythonSession.sendMessage(message);
        } else{
            log.warn("音频转发失败，Python端连接未开启");
        }

        // ToDo 异步处理对于前端传送音频流的存储操作
//        Long userId = (Long) session.getAttributes().get("userId");
//        // 获取前端传来的音频二进制流
//        ByteBuffer payload = message.getPayload();
//        byte[] audioBytes = payload.array();

        // 测试打印：
        // log.debug("收到用户 {} 发来的音频数据，大小: {} bytes", userId, audioBytes.length);
    }

    @Override
    public void afterConnectionClosed(WebSocketSession session, CloseStatus status) throws Exception {
        Long userId = (Long) session.getAttributes().get("userId");
        log.info("WebSocket 连接断开，用户 ID: {}, 状态: {}", userId, status.getReason());

        WebSocketSession pythonSession = (WebSocketSession) session.getAttributes().get("pythonSession");
        if(pythonSession != null && pythonSession.isOpen()){
            pythonSession.close(status);
        }

        // TODO: 在这里可以做一些清理工作，比如通知 Python 端结束本次面试，生成最终报告
    }
}