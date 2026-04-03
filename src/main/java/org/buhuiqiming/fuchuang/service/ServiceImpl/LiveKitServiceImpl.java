package org.buhuiqiming.fuchuang.service.ServiceImpl;

import io.livekit.server.*;
import lombok.extern.slf4j.Slf4j;
import org.buhuiqiming.fuchuang.dto.InterviewMetadata;
import org.buhuiqiming.fuchuang.entity.jpa.InterviewEntity;
import org.buhuiqiming.fuchuang.service.InterviewService;
import org.buhuiqiming.fuchuang.service.LiveKitService;
import org.springframework.stereotype.Service;
import retrofit2.Response;

import java.io.IOException;
import java.util.Map;

@Slf4j
@Service
public class LiveKitServiceImpl implements LiveKitService {

    private final String host = System.getenv("LIVEKIT_URL");
    private final String apiKey = System.getenv("LIVEKIT_API_KEY");
    private final String apiSecret = System.getenv("LIVEKIT_API_SECRET");
    private final InterviewService interviewService;
    public LiveKitServiceImpl(InterviewService interviewService) {
        this.interviewService = interviewService;
    }

    // 创建 RoomServiceClient 实例
    private final RoomServiceClient client = RoomServiceClient.createClient(host, apiKey, apiSecret);

    @Override
    public Map<String, String> startAutoInterview(String interviewId) throws IOException {
        // 1. 准备业务数据
        String roomName = "room_" + interviewId ;
        InterviewEntity interview = interviewService.getInterviewOrElseThrow(interviewId);
        String agentName = "ai-interview-3";


        String livekitUrl = host;
        // 使用蛇形命名的 Metadata 对象
        InterviewMetadata metadataObj = new InterviewMetadata(interview);
        String metadataJson = metadataObj.toJson();

        RoomServiceClient roomClient =
                RoomServiceClient.createClient(
                        livekitUrl.replace("wss://", "https://"),
                        apiKey,
                        apiSecret
                );
        log.info("metadata:{}",metadataJson);
        roomClient.createRoom(
                roomName,          // name
                300,               // emptyTimeout
                5,                 // maxParticipants
                null,              // nodeId
                metadataJson,      // metadata
                null,              // minPlayoutDelay
                null,              // maxPlayoutDelay
                null,              // syncStreams
                null               // departureTimeout
        ).execute();



        AgentDispatchServiceClient dispatchClient =
                AgentDispatchServiceClient.createClient(
                        livekitUrl.replace("wss://", "https://"),
                        apiKey,
                        apiSecret
                );

        Response<?> dispatchResp =
                dispatchClient
                        .createDispatch(roomName, agentName, metadataJson)
                        .execute();

        if (!dispatchResp.isSuccessful()) {
            throw new RuntimeException("Dispatch failed: " + dispatchResp.errorBody());
        }


        AccessToken token = new AccessToken(apiKey, apiSecret);
        token.setIdentity("candidate_" + interviewId);
        token.setName("Candidate-" + interviewId);
        token.addGrants(
                new RoomJoin(true),
                new RoomName(roomName)
        );
        return Map.of(
                "token", token.toJwt(),
                "room", roomName,
                "url", host
        );
    }
}
