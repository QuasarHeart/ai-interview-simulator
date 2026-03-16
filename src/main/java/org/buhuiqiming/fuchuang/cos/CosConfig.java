package org.buhuiqiming.fuchuang.cos;

import lombok.Data;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

import static java.lang.System.getenv;

@Data
@Component
@Slf4j
public class CosConfig {
    private final String secretId;
    private final String secretKey;
    private final String bucket;
    private final String region;
    private final String appId;

    public CosConfig() {
        log.info("初始化云存储");
        this.secretId = getenv("COS_SECRET_ID");
        this.secretKey = getenv("COS_SECRET_KEY");
        this.bucket = getenv("COS_BUCKET");
        this.region = getenv("COS_REGION");
        this.appId = getenv("COS_APP_ID");
    }
}
