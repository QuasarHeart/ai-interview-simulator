package org.buhuiqiming.fuchuang.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.buhuiqiming.fuchuang.entity.Account;
import org.buhuiqiming.fuchuang.entity.User;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class UserDTO {
    private Account account;
    private User user;
    private String code;

}
