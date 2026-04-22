// src/api/MainLayout.js
import service from '../utils/request'

// 用户退出（调用后端真实接口）
export const logout = () => {
  return service({
    url: 'api/logout',
    method: 'post'
  })
}


