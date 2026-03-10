package org.buhuiqiming.fuchuang.service;

import org.buhuiqiming.fuchuang.dto.LoginDTO;
import org.buhuiqiming.fuchuang.dto.LoginInfo;
import org.buhuiqiming.fuchuang.dto.UserDTO;
import org.buhuiqiming.fuchuang.entity.User;

public interface UserService {
    User getUserBasicInfo();
    void addUser(UserDTO userDTO);
    void updateUser(UserDTO userDTO);
    void deleteUser();

    String hashPassword(String password);
    boolean checkPassword(String password, String hashPassword);
    boolean checkPasswordFormat(String password);

    void resetPassword(UserDTO userDTO);

    LoginInfo login(LoginDTO loginDTO);
    void logout();
}
