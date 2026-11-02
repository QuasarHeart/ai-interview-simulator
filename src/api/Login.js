// src/api/login.js
import service from '../utils/request'

// 登录（调用后端真实接口）
export const login = ({ email, password }) => {
  return service({
    url: 'api/login',
    method: 'get',
    params: {
      email,
      password
    },
    headers: {
      'Cache-Control': 'no-cache',
      Pragma: 'no-cache'
    },
    skipAuth: true
  })
}

// 注册（调用后端真实接口）
export const register = ({ email, password, code, nickName, gender }) => {
  return service({
    url: 'api/users',
    method: 'post',
    skipAuth: true,
    data: {
      account: {
        email,
        password
      },
      user: {
        nickName,
        gender
      },
      code
    }
  })
}

// 发送验证码（调用后端真实接口）
export const sendCode = (email) => {
  // 使用项目统一的 axios 实例，调用后端发送验证码接口
  return service({
    url: 'api/code',
    method: 'get',
    params: { email },
    skipAuth: true
  })
}



// 重置密码（调用后端真实接口）
export const resetPassword = ({ email, code, newPassword }) => {
  return service({
    url: 'api/users/resetPassword',
    method: 'put',
    skipAuth: true,
    data: {
      account: {
        email,
        password: newPassword
      },
      code
    }
  })
}