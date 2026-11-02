package org.buhuiqiming.fuchuang.entity;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class Task {
    private Integer id;
    private Integer userId;
    private String taskURL;
}
