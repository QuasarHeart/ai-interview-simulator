package org.buhuiqiming.fuchuang.mapper;

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

    @Update("update user set vita = #{vita} where id = #{id}")
    void updateVita(@Param("vita")String vita,@Param("id") Long id);

    @Select("select vita from user where id = #{id}")
    String getVita(Long id);
    void init_user();
    void init_account();

}
