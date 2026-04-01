package org.buhuiqiming.fuchuang.service.ServiceImpl;

import io.livekit.server.AccessToken;
import io.livekit.server.RoomJoin;
import io.livekit.server.RoomName;
import io.livekit.server.RoomServiceClient;
import livekit.LivekitModels.Room;
import org.springframework.stereotype.Service;
import retrofit2.Response;

import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

@Service
public class LiveKitManagerImpl {

    private final String host = System.getenv("LIVEKIT_URL");
    private final String apiKey = System.getenv("LIVEKIT_API_KEY");
    private final String apiSecret = System.getenv("LIVEKIT_API_SECRET");

    // 创建 RoomServiceClient 实例
    private final RoomServiceClient client = RoomServiceClient.createClient(host, apiKey, apiSecret);

    public Map<String, String> startAutoInterview(String userId, String interviewId) throws IOException {
        String roomName = "interview_" + interviewId;

        // 1. 创建房间（这是给 Python Worker 发送的信号）
        // 0.12.1 推荐直接 execute() 获取同步响应
        Response<Room> response = client.createRoom(roomName).execute();
        if (!response.isSuccessful()) {
            throw new RuntimeException("无法创建房间: " + response.errorBody().string());
        }

        // 2. 存入元数据 (关键扩展点)
        // Python Worker 加入后会自动读取这段 JSON，从而知道面试题目
        String metadata = "{\"candidate_name\":\"张三\", \"level\":\"P6\", \"questions\":[\"Java锁机制\", \"LiveKit原理\"]}";
        client.updateRoomMetadata(roomName, metadata).execute();

        // 3. 仅为前端面试者生成 Access Token
        // 0.12.1 采用了更显式的 addGrants 语法
        AccessToken token = new AccessToken(apiKey, apiSecret);
        token.setIdentity("candidate_" + userId);
        token.setName("面试者-" + userId);

        // 赋予加入权限和房间名
        token.addGrants(new RoomJoin(true), new RoomName(roomName));

        Map<String, String> data = new HashMap<>();
        data.put("token", token.toJwt());
        data.put("room", roomName);
        data.put("url", "ws://localhost:7880");
        return data;
    }
}
