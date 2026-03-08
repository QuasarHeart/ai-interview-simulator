package org.buhuiqiming.fuchuang.service.ServiceImpl;

import com.qcloud.cos.http.HttpMethodName;
import jakarta.servlet.http.HttpServletRequest;
import lombok.extern.slf4j.Slf4j;
import org.buhuiqiming.fuchuang.cos.URLAK;
import org.buhuiqiming.fuchuang.exception.ServiceException;
import org.buhuiqiming.fuchuang.mapper.UserMapper;
import org.buhuiqiming.fuchuang.service.FileService;
import org.buhuiqiming.fuchuang.util.UserContext;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.net.URL;
import java.util.HashMap;
import java.util.Map;

@Slf4j
@Service
public class FileServiceImpl implements FileService {

    @Autowired
    private URLAK urlAK;
    @Autowired
    private UserMapper userMapper;


    public static String getExtension(String fileName) {
        if (fileName == null) return null;
        int lastDot = fileName.lastIndexOf('.');
        return (lastDot == -1 || lastDot == 0 || lastDot == fileName.length() - 1)
                ? ""
                : fileName.substring(lastDot + 1);
    }
//TODO 任务逻辑后续需要完善

    @Transactional
    @Override
    public URL generateCOSURL(HttpServletRequest  request,String dir) {

            String extension="";
            Map<String,String> params = new HashMap<>();
            Map<String,String> headers = new HashMap<>();
            String key = "";

            if(request.getMethod().equals("PUT")){

                String fileName = request.getParameter("filename");
                if(fileName==null){
                    throw new ServiceException(400, "请指定上传文件名filename");
                }
                extension = getExtension(fileName);
                key = dir + "/" + UserContext.get() + "." + extension;
                userMapper.addAvatar(UserContext.get(), key);
            }
            else if(request.getMethod().equals("GET")){
                if(dir.equals("avatar"))
                    key = userMapper.getAvatar(UserContext.get());
                else
                    key = dir + "/" + request.getParameter("filename");
            }


            log.info("URL签名，签名方法:{},header:{},param:{},key:{}", request.getMethod(), headers, params, key);
            return urlAK.generatePresignedUrl(key,HttpMethodName.valueOf(request.getMethod()), headers, params, false, true);
    }

}
