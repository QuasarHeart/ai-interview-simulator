package org.buhuiqiming.fuchuang.dto;

import lombok.Data;
import org.springframework.web.multipart.MultipartFile;

@Data
public class CreateInterviewDTO {
    // 岗位类型
    private String jobRole;

    // 难度(easy, mid , hard)
    private String difficulty;

    // 输入模式(text, voice)
    private String mode;

    // 简历文件(pdf/doc/docx) -- 可选
    private MultipartFile resumeFile;

    @Override
    public String toString() {
        if(resumeFile != null){
            return "jobRole=" + jobRole
                    + ", difficulty=" + difficulty
                    + ", mode=" + mode
                    + ", 有简历文件";
        }
        return "jobRole=" + jobRole
                + ", difficulty=" + difficulty
                + ", mode=" + mode
                + ", 无简历文件";
    }
}
