package org.buhuiqiming.fuchuang.mapper;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.apache.ibatis.annotations.*;
import org.buhuiqiming.fuchuang.entity.Account;
import org.buhuiqiming.fuchuang.entity.User;

@Mapper
public interface UserMapper {


    User getUserBasicInfo(Long id);


    //用户注册
    @Options(useGeneratedKeys = true, keyProperty = "id")
    @Insert("insert into account(email,password,status,create_time,update_time) values(#{email},#{password},#{status},#{createTime},#{updateTime})")
    void insertAccount(Account account);

    @Insert("insert into user(user_id,nick_name,gender) values(#{userId},#{nickName},#{gender})")
    void insertUser(User user);

    //用户信息修改,所有信息均是可选项
    void updateUser(@Param("u")User user, @Param("id")Long id);
    void updateAccount(@Param("a")Account account,@Param("id") Long uid);



    @Select("select * from account where email = #{email}")
    Account searchAccountByEmail(String email);

    @Delete("delete from user where user_id = #{id}")
    void deleteUser(Long id);
    @Delete("delete from account where id = #{id}")
    void deleteAccount(Long id);

    @Update("update user set avatar = #{avatar} where user_id = #{id}")
    void updateAvatar(@Param("avatar")String avatar,@Param("id") Long id);

    @Select("select avatar from user where user_id = #{id}")
    String getAvatar(Long id);

    @Update("update user set vita_url = #{vita} where user_id = #{id}")
    void updateVita(@Param("vita")String vita,@Param("id") Long id);

    @Select("select vita_url from user where user_id = #{id}")
    String getVita(Long id);

    @Update("update user set vita_content = #{vita_content} where user_id = #{id}")
    void updateVitaContent(@Param("vita_content")String vita_content,@Param("id") Long id);

    @Select("select vita_content from user where user_id = #{id}")
    String getVitaContent(Long id);

    @Update("UPDATE user SET strengths = #{strengths}, weaknesses = #{weaknesses}, " +
            "suggestions = #{suggestions}, overall_score = #{overallScore}" +
            "WHERE user_id = #{userId}")
    void updateAnalysisResult(@Param("strengths") String strengths,
                              @Param("weaknesses") String weaknesses,
                              @Param("suggestions") String suggestions,
                              @Param("overallScore") Double overallScore,
                              @Param("userId") Long userId);

    void init_user();
    void init_account();


    // 查询用户的简历分析结果
    @Select("SELECT strengths, weaknesses, suggestions, overall_score" +
            "FROM user WHERE user_id = #{userId}")
    ResumeAnalysisDTO selectResumeAnalysis(@Param("userId") Long userId);

    // 内部类用于查询结果
    @Data
    @AllArgsConstructor
    @NoArgsConstructor
    class ResumeAnalysisDTO {
        private String strengths;  // JSON字符串
        private String weaknesses; // JSON字符串
        private String suggestions; // JSON字符串
        private Double overallScore;
    }
}
