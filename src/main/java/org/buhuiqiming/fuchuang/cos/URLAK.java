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

    public URLAK(CosConfig cosConfig) {
        this.cosConfig = cosConfig;
    }

    // 创建 COSClient 实例，这个实例用来后续调用请求
    public COSClient createCOSClient(String path) {
        // 这里需要已经获取到临时密钥的结果。
        // 临时密钥的生成参见 https://cloud.tencent.com/document/product/436/14048#cos-sts-sdk
        TmpSK tmpSK = new TmpSK();

        tmpSK.getTmpSK(path,cosConfig);
        log.info("tmpSK:{}",tmpSK);
        COSCredentials cred = new BasicSessionCredentials(tmpSK.getTmpSecretId(), tmpSK.getTmpSecretKey(), tmpSK.getSessionToken());

        // ClientConfig 中包含了后续请求 COS 的客户端设置：
        ClientConfig clientConfig = new ClientConfig();

        // 设置 bucket 的地域
        // COS_REGION 请参见 https://cloud.tencent.com/document/product/436/6224
        clientConfig.setRegion(new Region("ap-chengdu"));
        clientConfig.setHttpProtocol(HttpProtocol.https);
        // 以下的设置，是可选的：

        // 设置 socket 读取超时，默认 30s
        // clientConfig.setSocketTimeout(30*1000);
        // 设置建立连接超时，默认 30s
        // clientConfig.setConnectionTimeout(30*1000);

        // 如果需要的话，设置 http 代理，ip 以及 port
        // clientConfig.setHttpProxyIp("httpProxyIp");
        // clientConfig.setHttpProxyPort(80);

        // 生成 cos 客户端。
        return new COSClient(cred, clientConfig);
    }


    public URL generatePresignedUrl(String key, HttpMethodName method,
                                    Map<String, String> headers, Map<String, String> params,
                                    Boolean signPrefixMode, Boolean signHost) throws CosClientException{
        // 调用 COS 接口之前必须保证本进程存在一个 COSClient 实例，如果没有则创建
// 详细代码参见本页：创建 COSClient
        COSClient cosClient = createCOSClient(key);

// 存储桶的命名格式为 BucketName-APPID，此处填写的存储桶名称必须为此格式
//        String bucketName = "examplebucket-1250000000";
// 对象键(Key)是对象在存储桶中的唯一标识。详情请参见 [对象键](https://cloud.tencent.com/document/product/436/13324)


// 设置签名过期时间(可选), 若未进行设置则默认使用 ClientConfig 中的签名过期时间(1小时)
// 这里设置签名在半个小时后过期
        Date expirationDate = new Date(System.currentTimeMillis() + 30 * 60 * 1000);
// 填写本次请求的参数，需与实际请求相同，能够防止用户篡改此签名的 HTTP 请求的参数
//        Map<String, String> params = new HashMap<String, String>();
//        params.put("param1", "value1");

// 填写本次请求的头部，需与实际请求相同，能够防止用户篡改此签名的 HTTP 请求的头部
//        Map<String, String> headers = new HashMap<String, String>();
//        headers.put("header1", "value1");

// 请求的 HTTP 方法，上传请求用 PUT，下载请求用 GET，删除请求用 DELETE
//        HttpMethodName method = HttpMethodName.GET;

        URL url = cosClient.generatePresignedUrl(cosConfig.getBucket(), key, expirationDate, method, headers, params);
        log.info("URl:"+url.toString());

// 确认本进程不再使用 cosClient 实例之后，关闭即可
        cosClient.shutdown();
        return url;
    }

    /**
     * 删除对象
     * @param key
     */
    public void deleteObject(String key){
        // 调用 COS 接口之前必须保证本进程存在一个 COSClient 实例，如果没有则创建
// 详细代码参见本页：简单操作 -> 创建 COSClient
        COSClient cosClient = createCOSClient(key);

        try {
            cosClient.deleteObject(cosConfig.getBucket(), key);
        } catch (CosServiceException e) {
            e.printStackTrace();
        } catch (CosClientException e) {
            e.printStackTrace();
        }

// 确认本进程不再使用 cosClient 实例之后，关闭即可
        cosClient.shutdown();
    }
}
