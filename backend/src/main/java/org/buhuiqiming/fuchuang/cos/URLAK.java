package org.buhuiqiming.fuchuang.cos;

import com.qcloud.cos.COSClient;
import com.qcloud.cos.ClientConfig;
import com.qcloud.cos.auth.BasicSessionCredentials;
import com.qcloud.cos.auth.COSCredentials;
import com.qcloud.cos.exception.CosClientException;
import com.qcloud.cos.exception.CosServiceException;
import com.qcloud.cos.http.HttpMethodName;
import com.qcloud.cos.http.HttpProtocol;
import com.qcloud.cos.region.Region;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

import java.net.URL;
import java.util.Date;
import java.util.Map;

@Slf4j
@Component
public class URLAK {

    private final CosConfig cosConfig;

    // STS 临时密钥有效期 30 分钟，缓存 25 分钟后重建 COSClient
    private static final long CLIENT_TTL_MS = 25 * 60 * 1000;
    private volatile COSClient cachedClient;
    private volatile long clientCreatedAt;

    public URLAK(CosConfig cosConfig) {
        this.cosConfig = cosConfig;
    }

    private COSClient getOrCreateCOSClient() {
        long now = System.currentTimeMillis();
        if (cachedClient != null && (now - clientCreatedAt) < CLIENT_TTL_MS) {
            return cachedClient;
        }
        synchronized (this) {
            now = System.currentTimeMillis();
            if (cachedClient != null && (now - clientCreatedAt) < CLIENT_TTL_MS) {
                return cachedClient;
            }
            if (cachedClient != null) {
                cachedClient.shutdown();
            }

            TmpSK tmpSK = new TmpSK();
            tmpSK.getTmpSK("*", cosConfig);
            COSCredentials cred = new BasicSessionCredentials(
                    tmpSK.getTmpSecretId(), tmpSK.getTmpSecretKey(), tmpSK.getSessionToken());

            ClientConfig clientConfig = new ClientConfig();
            clientConfig.setRegion(new Region("ap-chengdu"));
            clientConfig.setHttpProtocol(HttpProtocol.https);

            cachedClient = new COSClient(cred, clientConfig);
            clientCreatedAt = now;
            log.info("COSClient 已重建，将在 25 分钟后过期");
            return cachedClient;
        }
    }

    public URL generatePresignedUrl(String key, HttpMethodName method,
                                    Map<String, String> headers, Map<String, String> params,
                                    Boolean signPrefixMode, Boolean signHost) throws CosClientException{
        COSClient cosClient = getOrCreateCOSClient();

        Date expirationDate = new Date(System.currentTimeMillis() + 30 * 60 * 1000);

        return cosClient.generatePresignedUrl(cosConfig.getBucket(), key, expirationDate, method, headers, params);
    }

    public void deleteObject(String key){
        COSClient cosClient = getOrCreateCOSClient();

        try {
            cosClient.deleteObject(cosConfig.getBucket(), key);
        } catch (CosServiceException e) {
            e.printStackTrace();
        } catch (CosClientException e) {
            e.printStackTrace();
        }
    }
}
