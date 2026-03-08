package org.buhuiqiming.fuchuang.cos;

import lombok.Data;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

@Data
@ConfigurationProperties(prefix = "cos")
@Component
public class CosConfig {
    private String secretId;
    private String secretKey;
    private String bucket;
    private String region;
    private String appId;
}
