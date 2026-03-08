package org.buhuiqiming.fuchuang.entity;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class User {
    private Integer userId;
    private String nickName;
    private Integer gender;
    private String email;
    private String description;
}
