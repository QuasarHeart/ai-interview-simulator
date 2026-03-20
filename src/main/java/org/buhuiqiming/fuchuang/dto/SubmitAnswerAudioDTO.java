package org.buhuiqiming.fuchuang.dto;

import lombok.Data;
import org.springframework.web.multipart.MultipartFile;

@Data
public class SubmitAnswerAudioDTO {
    private String type;
    private MultipartFile file;

}
