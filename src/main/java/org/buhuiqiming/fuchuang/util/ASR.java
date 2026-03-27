package org.buhuiqiming.fuchuang.util;


import com.tencent.SpeechClient;
import com.tencent.asr.model.FlashRecognitionRequest;
import com.tencent.asr.model.FlashRecognitionResponse;
import com.tencent.asr.service.FlashRecognizer;
import com.tencentcloudapi.asr.v20190614.AsrClient;
import com.tencentcloudapi.asr.v20190614.models.SentenceRecognitionRequest;
import com.tencentcloudapi.asr.v20190614.models.SentenceRecognitionResponse;
import com.tencentcloudapi.common.Credential;
import com.tencentcloudapi.common.profile.ClientProfile;
import com.tencentcloudapi.common.profile.HttpProfile;
import lombok.extern.slf4j.Slf4j;
import org.buhuiqiming.fuchuang.exception.ServiceException;
import org.springframework.stereotype.Component;
import org.springframework.util.StringUtils;
import org.springframework.web.multipart.MultipartFile;

import java.util.Base64;

@Slf4j
@Component
public class ASR {
    private final Credential cred;
    public final AsrClient asrClient;

    public ASR(){
        this.cred = new Credential(System.getenv("COS_SECRET_ID"), System.getenv("COS_SECRET_KEY"));
        asrClient = initAsrClient();
    }

    private AsrClient initAsrClient() {
        HttpProfile httpProfile = new HttpProfile();
        httpProfile.setEndpoint("asr.tencentcloudapi.com");

        ClientProfile clientProfile = new ClientProfile();
        clientProfile.setHttpProfile(httpProfile);

        return new AsrClient(cred, "", clientProfile);
    }

    // 获取音频文件后缀名
    public String getExtensionBySpring(MultipartFile file) {
        String originalFilename = file.getOriginalFilename();
        // Spring 的工具类会自动处理 null 和没有后缀的情况
        // 如果是 "test.wav"，它会返回 "wav" (注意，不带点)
        String extension = StringUtils.getFilenameExtension(originalFilename);

        // 转小写，并处理空值兜底
        return extension != null ? extension.toLowerCase() : "";
    }

    // ASR简单处理前端传递到后端的音频文件，这里要求文件大小小于3MB，时长小于1分钟
    public String getAudioToTextSimpleASR(MultipartFile audio){
        if(audio == null || audio.getSize() == 0){
            throw new ServiceException(400, "上传音频文件为空，请重试");
        }
        try{
            byte[] audioBytes = audio.getBytes();
            // 具体大小限制，这里留一些冗余
            if(audioBytes.length > 3000000){
                throw new ServiceException(400, "上传音频文件过大");
            }
            String base64Audio = Base64.getEncoder().encodeToString(audioBytes);
            SentenceRecognitionRequest req = new SentenceRecognitionRequest();
            req.setEngSerViceType("16k_zh");
            req.setSourceType(1L);
            req.setVoiceFormat(getExtensionBySpring(audio));
            req.setData(base64Audio);
            req.setDataLen((long) audioBytes.length);

            SentenceRecognitionResponse resp = asrClient.SentenceRecognition(req);

            return resp.getResult();
        } catch (Exception e){
            log.info("处理音频转文字流程出现错误：{}", e.getMessage());
            throw new ServiceException(500, "服务器异常，请重试");
        }
    }

    // 录音文件快速处理
    public String getAudioToTextASRFast(MultipartFile audio){
        if(audio == null || audio.getSize() == 0){
            throw new ServiceException(400, "上传音频文件为空，请重试");
        }
        try{
            byte[] audioBytes = audio.getBytes();
            com.tencent.asr.model.Credential credential = com.tencent.asr.model.Credential.builder().secretId(System.getenv("COS_SECRET_ID")).secretKey(System.getenv("COS_SECRET_KEY")).build();
            FlashRecognizer recognizer = SpeechClient.newFlashRecognizer(System.getenv("COS_APP_ID"), credential);
            FlashRecognitionRequest req = FlashRecognitionRequest.initialize();
            req.setEngineType("16k_zh");
            req.setFirstChannelOnly(1);
            req.setVoiceFormat(getExtensionBySpring(audio));
            req.setConvertNumMode(1);
            FlashRecognitionResponse resp = recognizer.recognize(req, audioBytes);
            if (resp.getFlashResult() != null && !resp.getFlashResult().isEmpty()) {
                return resp.getFlashResult().getFirst().getText();
            }
            log.info("response: {}", resp);
            throw new ServiceException(500, "腾讯云服务异常，请稍后重试");
        } catch (Exception e){
            log.info("处理音频转文字流程出现错误：{}", e.getMessage());
            throw new ServiceException(500, "服务器异常，请重试");
        }
    }
}
