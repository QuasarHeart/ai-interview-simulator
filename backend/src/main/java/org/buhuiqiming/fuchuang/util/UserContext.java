package org.buhuiqiming.fuchuang.util;

public class UserContext {

    private static final ThreadLocal<Long> THREAD_LOCAL = new ThreadLocal<>();

    // 存入当前登录用户 ID
    public static void set(Long userId) {
        THREAD_LOCAL.set(userId);
    }

    // 获取当前登录用户 ID
    public static Long get() {
        return THREAD_LOCAL.get();
    }

    public static void remove() {
        THREAD_LOCAL.remove();
    }
}