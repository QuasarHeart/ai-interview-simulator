package org.buhuiqiming.fuchuang.service.ServiceImpl;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.Data;
import lombok.extern.slf4j.Slf4j;
import org.buhuiqiming.fuchuang.cos.URLAK;
import org.buhuiqiming.fuchuang.dto.LoginDTO;
import org.buhuiqiming.fuchuang.dto.LoginInfo;
import org.buhuiqiming.fuchuang.dto.UserDTO;
import org.buhuiqiming.fuchuang.entity.Account;
import org.buhuiqiming.fuchuang.entity.User;
import org.buhuiqiming.fuchuang.exception.ServiceException;
import org.buhuiqiming.fuchuang.mapper.UserMapper;
import org.buhuiqiming.fuchuang.service.CodeService;
import org.buhuiqiming.fuchuang.service.UserService;
import org.buhuiqiming.fuchuang.util.JwtUtils;
import org.buhuiqiming.fuchuang.util.UserContext;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Slf4j
@Service
public class UserServiceImpl implements UserService {
    private final UserMapper userMapper;
    private final CodeService codeService;
    private final JwtUtils jwtUtils;
    private final StringRedisTemplate stringRedisTemplate;
    private final URLAK urlAK;
    private final ObjectMapper objectMapper = new ObjectMapper();


    public UserServiceImpl(UserMapper userMapper, CodeService codeService, JwtUtils jwtUtils, StringRedisTemplate stringRedisTemplate, URLAK urlAK) {
        this.userMapper = userMapper;
        this.codeService = codeService;
        this.jwtUtils = jwtUtils;
        this.stringRedisTemplate = stringRedisTemplate;
        this.urlAK = urlAK;
    }

    @Override
    public String hashPassword(String password) {
        BCryptPasswordEncoder encoder = new BCryptPasswordEncoder();
        return encoder.encode(password);
    }
    @Override
    public boolean checkPassword(String password, String hashPassword) {
        BCryptPasswordEncoder encoder = new BCryptPasswordEncoder();
        return encoder.matches(password, hashPassword);
    }

    @Override
    public boolean checkPasswordFormat(String password){
        //密码校验，8-16位，数字和大小写字母构成
        return password.matches("^(?=.*[a-zA-Z])(?=.*\\d)[a-zA-Z\\d]{8,16}$");
    }

    @Override
    public User getUserBasicInfo() {
        Long id = UserContext.get();
        return userMapper.getUserBasicInfo(id);
    }
    @Override
    @Transactional(rollbackFor = Exception.class)
    public void addUser(UserDTO userDTO) {

        if(!checkPasswordFormat(userDTO.getAccount().getPassword()))
            throw new ServiceException(412,"密码格式错误,应为字母数字组合，8-16位");

        //用户注册之前，添加一下account中的时间字段
        userDTO.getAccount().setCreateTime(LocalDateTime.now());
        userDTO.getAccount().setUpdateTime(LocalDateTime.now());
        //账户状态
        userDTO.getAccount().setStatus(0);
        //密码hash
        userDTO.getAccount().setPassword(hashPassword(userDTO.getAccount().getPassword()));


        //account的email为unique
        try {

            userMapper.insertAccount(userDTO.getAccount());
            //账户字段的id
            userDTO.getUser().setUserId(userDTO.getAccount().getId());
            userMapper.insertUser(userDTO.getUser());
        } catch (Exception e) {
            log.info("用户已存在");
            throw new ServiceException(412,"用户已存在");
        }
        codeService.checkCode(userDTO.getAccount().getEmail(), userDTO.getCode());
    }
    @Transactional
    @Override
    public void updateUser(UserDTO  user){

        if(user.getAccount().getPassword()!=null&&!checkPasswordFormat(user.getAccount().getPassword()))
            throw new ServiceException(412,"密码格式错误,应为字母数字组合，8-16位");

        user.getAccount().setUpdateTime(LocalDateTime.now());
        user.getAccount().setPassword(hashPassword(user.getAccount().getPassword()));
        userMapper.updateUser(user.getUser(),UserContext.get());
        userMapper.updateAccount(user.getAccount(),UserContext.get());
    }
    @Override
    @Transactional
    public void deleteUser(){
        //先删除COS上的用户信息
        urlAK.deleteObject(userMapper.getAvatar(UserContext.get()));
        log.info("删除用户头像成功");
//todo 后续任务也需要删除

        Long id = UserContext.get();
        userMapper.deleteUser(id);
        log.info("删除用户成功");
        userMapper.deleteAccount(id);
        log.info("删除账户成功");
    }



    @Override
    public LoginInfo login(LoginDTO loginDTO)
    {
        Account account= userMapper.searchAccountByEmail(loginDTO.getEmail());
        if(account==null){
            log.info("用户不存在");
            throw new ServiceException(412,"用户不存在");
        }
        if(!checkPassword(loginDTO.getPassword(),account.getPassword())){
            log.info("密码错误");
            throw new ServiceException(412,"密码错误");
        }
        Map<String,Object> claims= new HashMap<>();
        claims.put("id",account.getId());
        claims.put("email",account.getEmail());

        String token= jwtUtils.generateJwt(claims);
        log.info("生成token成功,token:{}", token);
        return new LoginInfo(account.getId(),account.getEmail(),token);
    }
    @Override
    public void logout(){
        Long id = UserContext.get();
        Account account = new Account();
        //更新账户最近登录时间
        account.setLatestLoginTime(LocalDateTime.now());
        userMapper.updateAccount(account,id);

        //删除token锁
        stringRedisTemplate.delete("lock:token:"+id);
        log.info("用户{}退出登录成功",id);

    }

    @Override
    public void resetPassword(UserDTO userDTO){

        //用户查询
        Account account= userMapper.searchAccountByEmail(userDTO.getAccount().getEmail());
        if(account==null){
            log.info("用户不存在");
            throw new ServiceException(412,"用户不存在");
        }
        //验证码
        if(!checkPasswordFormat(userDTO.getAccount().getPassword()))
            throw new ServiceException(412,"密码格式错误,应为字母数字组合，8-16位");
        codeService.checkCode(userDTO.getAccount().getEmail(), userDTO.getCode());

        userDTO.getAccount().setUpdateTime(LocalDateTime.now());
        //密码hash
        userDTO.getAccount().setPassword(hashPassword(userDTO.getAccount().getPassword()));
        userMapper.updateAccount(userDTO.getAccount(),account.getId().longValue());
    }
    /**
     * 获取用户的简历分析结果（返回解析后的列表）
     */
    @Override
    public ResumeAnalysisVO getResumeAnalysis(Long userId) {
        UserMapper.ResumeAnalysisDTO dto = userMapper.selectResumeAnalysis(userId);
        if (dto == null) {
            return null;
        }

        ResumeAnalysisVO vo = new ResumeAnalysisVO();
        vo.setOverallScore(dto.getOverall_score());

        // 解析JSON字符串为列表
        try {
            if (dto.getStrengths() != null && !dto.getStrengths().isEmpty()) {
                List<String> strengths = objectMapper.readValue(dto.getStrengths(), new TypeReference<List<String>>() {});
                vo.setStrengths(strengths);
            }

            if (dto.getWeaknesses() != null && !dto.getWeaknesses().isEmpty()) {
                List<String> weaknesses = objectMapper.readValue(dto.getWeaknesses(), new TypeReference<List<String>>() {});
                vo.setWeaknesses(weaknesses);
            }

            if (dto.getSuggestions() != null && !dto.getSuggestions().isEmpty()) {
                List<String> suggestions = objectMapper.readValue(dto.getSuggestions(), new TypeReference<List<String>>() {});
                vo.setSuggestions(suggestions);
            }
        } catch (Exception e) {
            log.error("解析JSON失败", e);
            vo.setStrengths(new ArrayList<>());
            vo.setWeaknesses(new ArrayList<>());
            vo.setSuggestions(new ArrayList<>());
        }

        return vo;
    }
    /**
     * 简历分析结果VO
     */
    @Data
    public static class ResumeAnalysisVO {
        private List<String> strengths;
        private List<String> weaknesses;
        private List<String> suggestions;
        private Double overallScore;
    }

}
