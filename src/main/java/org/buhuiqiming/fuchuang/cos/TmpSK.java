package org.buhuiqiming.fuchuang.cos;// 根据 github 提供的 maven 集成方法导入 java sts sdk，使用 3.1.1 及更高版本

import com.tencent.cloud.CosStsClient;
import com.tencent.cloud.Policy;
import com.tencent.cloud.Response;
import com.tencent.cloud.Statement;
import com.tencent.cloud.cos.util.Jackson;
import lombok.Data;
import lombok.extern.slf4j.Slf4j;

import java.util.TreeMap;


@Data
@Slf4j
public class TmpSK {

    String sessionToken;
    String tmpSecretId;
    String tmpSecretKey;

    public void getTmpSK(String path, CosConfig cosConfig) {

        TreeMap<String, Object> config = new TreeMap<String, Object>();
        try {
            //这里的 SecretId 和 SecretKey 代表了用于申请临时密钥的永久身份（主账号、子账号等），子账号需要具有操作存储桶的权限。

            //用户的 SecretKey，建议使用子账号密钥，授权遵循最小权限指引，降低使用风险。子账号密钥获取可参见 https://cloud.tencent.com/document/product/598/37140
            // 替换为您的云 api 密钥 SecretId
            config.put("secretId", cosConfig.getSecretId());
            // 替换为您的云 api 密钥 SecretKey
            config.put("secretKey", cosConfig.getSecretKey());

            // 初始化 policy
            Policy policy = new Policy();

            // 设置域名:
            // 如果您使用了腾讯云 cvm，可以设置内部域名
            //config.put("host", "sts.internal.tencentcloudapi.com");

            // 临时密钥有效时长，单位是秒，默认 1800 秒，目前主账号最长 2 小时（即 7200 秒），子账号最长 36 小时（即 129600）秒
            config.put("durationSeconds", 1800);
            // 换成您的 bucket
            config.put("bucket", cosConfig.getBucket());
            // 换成 bucket 所在地区
            config.put("region", cosConfig.getRegion());

            // 开始构建一条 statement
            Statement statement = new Statement();
            // 声明设置的结果是允许操作
            statement.setEffect("allow");
            /**
             * 密钥的权限列表。必须在这里指定本次临时密钥所需要的权限。
             * 权限列表请参见 https://cloud.tencent.com/document/product/436/31923
             * 规则为 {project}:{interfaceName}
             * project : 产品缩写  cos相关授权为值为cos,数据万象(数据处理)相关授权值为ci
             * 授权所有接口用*表示，例如 cos:*,ci:*
             * 添加一批操作权限 :
             */
//            statement.addActions(new String[]{
//                    "cos:PutObject",
//                    // 表单上传、小程序上传
//                    "cos:PostObject",
//                    // 分块上传
//                    "cos:InitiateMultipartUpload",
//                    "cos:ListMultipartUploads",
//                    "cos:ListParts",
//                    "cos:UploadPart",
//                    "cos:CompleteMultipartUpload",
//                    // 处理相关接口一般为数据万象产品 权限中以ci开头
//                    // 创建媒体处理任务
//                    "ci:CreateMediaJobs",
//                    // 文件压缩
//                    "ci:CreateFileProcessJobs"
//            });
            statement.addAction("cos:*");
            /**
             * 这里改成允许的路径前缀，可以根据自己网站的用户登录态判断允许上传的具体路径
             * 资源表达式规则分对象存储(cos)和数据万象(ci)两种
             * 数据处理、审核相关接口需要授予ci资源权限
             *  cos : qcs::cos:{region}:uid/{appid}:{bucket}/{path}
             *  ci  : qcs::ci:{region}:uid/{appid}:bucket/{bucket}/{path}
             * 列举几种典型的{path}授权场景：
             * 1、允许访问所有对象："*"
             * 2、允许访问指定的对象："a/a1.txt", "b/b1.txt"
             * 3、允许访问指定前缀的对象："a*", "a/*", "b/*"
             *  如果填写了“*”，将允许用户访问所有资源；除非业务需要，否则请按照最小权限原则授予用户相应的访问权限范围。
             *
             * 示例：授权examplebucket-1250000000 bucket目录下的所有资源给cos和ci 授权两条Resource
             */
//            statement.addResources(new String[]{
//                    "qcs::cos:ap-chongqing:uid/1250000000:examplebucket-1250000000/*",
//                    "qcs::ci:ap-chongqing:uid/1250000000:bucket/examplebucket-1250000000/*"});

            statement.addResource(String.format("qcs::cos:%s:uid/%s:%s/%s",cosConfig.getRegion(), cosConfig.getAppId(), cosConfig.getBucket(), path));



            // 把一条 statement 添加到 policy
            // 可以添加多条
            policy.addStatement(statement);
            // 将 Policy 示例转化成 String，可以使用任何 json 转化方式，这里是本 SDK 自带的推荐方式
            config.put("policy", Jackson.toJsonPrettyString(policy));

            Response response = CosStsClient.getCredential(config);
//            System.out.println(response.credentials.tmpSecretId);
//            System.out.println(response.credentials.tmpSecretKey);
//            System.out.println(response.credentials.sessionToken);

            this.tmpSecretId = response.credentials.tmpSecretId;
            this.tmpSecretKey = response.credentials.tmpSecretKey;
            this.sessionToken = response.credentials.sessionToken;

        } catch (Exception e) {
            e.printStackTrace();
            throw new IllegalArgumentException("no valid secret !");
        }
    }
}