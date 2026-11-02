/**
 * 用户特定的本地存储工具
 * 确保不同用户的缓存数据分离
 */

/**
 * 获取当前登录用户的标识
 * @returns {string} 用户标识（email或空字符串）
 */
export const getCurrentUserIdentity = () => {
  // 首先尝试从token解析（如果是JWT）
  const token = localStorage.getItem('token')
  if (token) {
    try {
      const parts = token.split('.')
      if (parts.length === 3) {
        const decoded = JSON.parse(atob(parts[1]))
        // JWT中通常包含email或sub字段
        if (decoded.email) return decoded.email
        if (decoded.sub) return decoded.sub
        if (decoded.userId) return decoded.userId
        if (decoded.user_id) return decoded.user_id
      }
    } catch (e) {
      console.warn('无法解析JWT token:', e)
    }
  }
  
  // 如果token解析失败，返回空字符串
  // 这样可以向后兼容（未登录状态）
  return ''
}

/**
 * 生成用户特定的storage key
 * @param {string} key - 基础key名
 * @returns {string} 用户特定的key
 */
export const getUserStorageKey = (key) => {
  const userIdentity = getCurrentUserIdentity()
  if (!userIdentity) {
    // 未登录时返回原始key（向后兼容）
    return key
  }
  // 登录后返回带用户标识的key
  return `${key}_${userIdentity}`
}

/**
 * 获取用户特定的localStorage值
 * @param {string} key - 基础key名
 * @returns {*} 存储的值
 */
export const getUserStorage = (key) => {
  const fullKey = getUserStorageKey(key)
  return localStorage.getItem(fullKey)
}

/**
 * 设置用户特定的localStorage值
 * @param {string} key - 基础key名
 * @param {*} value - 要存储的值
 */
export const setUserStorage = (key, value) => {
  const fullKey = getUserStorageKey(key)
  if (value === null || value === undefined) {
    localStorage.removeItem(fullKey)
  } else {
    localStorage.setItem(fullKey, value)
  }
}

/**
 * 删除用户特定的localStorage值
 * @param {string} key - 基础key名
 */
export const removeUserStorage = (key) => {
  const fullKey = getUserStorageKey(key)
  localStorage.removeItem(fullKey)
}

/**
 * 清空当前用户的所有简历相关缓存
 * 注：仅在用户主动删除简历时调用，不在登出时调用
 */
export const clearUserResumeCache = () => {
  removeUserStorage('resumeInfo')
}

/**
 * 清空当前用户的所有缓存（登出时调用）
 * 注意：简历缓存（resumeInfo）不被清空，因为这是用户资源，不涉及认证信息
 * 不同用户已通过 getUserStorageKey 机制自动隔离
 */
export const clearCurrentUserCache = () => {
  const userIdentity = getCurrentUserIdentity()
  if (!userIdentity) return
  
  // 登出时仅清空需要清空的缓存
  // 简历缓存保留，这样下次登录该用户能恢复自己的简历信息
  // 可以在这里添加其他需要清空的敏感数据缓存key
}
