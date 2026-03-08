package org.buhuiqiming.fuchuang;

import com.qcloud.cos.http.HttpMethodName;
import org.buhuiqiming.fuchuang.cos.URLAK;
import org.buhuiqiming.fuchuang.service.CodeService;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import java.util.HashMap;
import java.util.Map;

@SpringBootTest
class FuchuangApplicationTests {
    @Autowired
    private CodeService codeService;
    @Autowired
    private URLAK urlAK;
    @Test
    void contextLoads() {
    }
    @Test
    void URLtest(){
        Map<String, String> params = new HashMap<String, String>();
       params.put("param1", "value1");
        Map<String, String> headers = new HashMap<String, String>();
       System.out.println(urlAK.generatePresignedUrl("avatar/1.png", HttpMethodName.PUT, headers, params, false, true));
    }
}
