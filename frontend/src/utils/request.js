/* src/utils/request.js */
import axios from 'axios'
import { ElMessage } from 'element-plus'
import { clearCurrentUserCache } from './storage'

let isAuthRedirecting = false
const TOKEN_REFRESH_CODES = [401, 40105]

const isLikelyJwt = (value) => {
  if (typeof value !== 'string') return false
  const token = value.trim()
  if (!token) return false
  // JWT 常见格式：header.payload.signature（3段）
  return token.split('.').length === 3
}

const tryParseJson = (value) => {
  if (typeof value !== 'string') return value
  const text = value.trim()
  if (!text) return value
  if (!((text.startsWith('{') && text.endsWith('}')) || (text.startsWith('[') && text.endsWith(']')))) {
    return value
  }
  try {
    return JSON.parse(text)
  } catch (_) {
    return value
  }
}

const extractTokenFromPayload = (payload, allowRawToken = false) => {
  const normalized = tryParseJson(payload)
  if (!normalized || typeof normalized !== 'object') {
    if (allowRawToken && typeof normalized === 'string' && isLikelyJwt(normalized)) {
      return normalized
    }
    return ''
  }

  const data = normalized.data
  const dataObj = typeof data === 'object' && data ? data : {}

  const fromDataString =
    allowRawToken && typeof data === 'string' && isLikelyJwt(data)
      ? data
      : ''

  return (
    normalized.token ||
    normalized.accessToken ||
    normalized.access_token ||
    normalized.newToken ||
    normalized.jwt ||
    normalized['x-access-token'] ||
    normalized['new-token'] ||
    dataObj.token ||
    dataObj.accessToken ||
    dataObj.access_token ||
    dataObj.newToken ||
    dataObj.jwt ||
    dataObj['x-access-token'] ||
    dataObj['new-token'] ||
    fromDataString ||
    ''
  )
}

const clearAuthAndRedirect = () => {
  // 清空当前用户缓存（包括简历信息）
  clearCurrentUserCache()
  localStorage.removeItem('token')

  if (isAuthRedirecting) return
  isAuthRedirecting = true

  const currentPath = window.location.pathname
  if (currentPath !== '/login') {
    window.location.href = '/login'
  }

  setTimeout(() => {
    isAuthRedirecting = false
  }, 500)
}

// 从响应中提取并更新 token（兼容响应头与响应体常见字段）
const syncTokenFromResponse = (response) => {
  if (!response) return

  const authHeader = response.headers?.authorization || response.headers?.Authorization
  let tokenFromHeader = ''

  if (typeof authHeader === 'string') {
    tokenFromHeader = authHeader.replace(/^Bearer\s+/i, '').trim()
  }

  const body = tryParseJson(response.data) || {}
  const tokenFromBody = extractTokenFromPayload(body, false)

  const nextToken = tokenFromHeader || tokenFromBody
  if (nextToken) {
    localStorage.setItem('token', nextToken)
  }
}

// 1. 创建 axios 实例
const service = axios.create({
  // 这里填后端的真实地址，本地开发通常是 localhost:8080
  baseURL: 'https://nas.feixingxr.com',  
  timeout: 60000 
})

// 2. 请求拦截器：自动在 Header 里加 Token
service.interceptors.request.use(
  (config) => {
    if (config.skipAuth) {
      return config
    }

    const token = localStorage.getItem('token')
    if (token) {
      // 按照文档要求，Bearer Token 格式
      config.headers = config.headers || {}
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// 3. 响应拦截器：统一处理报错
service.interceptors.response.use(
  (response) => {
    syncTokenFromResponse(response)

    if (response.config.returnNativeResponse) {
      return response
    }

    // 假设后端返回格式是 { code: 200, data: ... }
    const rawRes = response.data
    const res = tryParseJson(rawRes)
    const contentType = String(response.headers?.['content-type'] || response.headers?.['Content-Type'] || '').toLowerCase()
    // 如果是二进制流（比如音频），直接返回
    if (response.config.responseType === 'blob' || response.config.responseType === 'arraybuffer') {
      return rawRes
    }
    // 先处理对象响应中的 code（包括 responseType: text 时返回的 JSON 字符串）。
    // 这样窗口期 401/40105 在文本接口中也能续 token 并自动重试。
    if (res && typeof res === 'object') {
      if (TOKEN_REFRESH_CODES.includes(Number(res.code))) {
      // 窗口期内的 token 续期逻辑：
      // 当 token 过期时，后端在 res.data 中返回新 token（窗口期内的特殊处理）
      // data 可能是字符串 token 直接或对象中的 token 字段
      const newToken = extractTokenFromPayload(res, true)
      
      if (newToken && !response.config.__tokenRetried) {
        // 有新 token，说明在窗口期内，自动更新并重试
        localStorage.setItem('token', newToken)
        const retryConfig = {
          ...response.config,
          __tokenRetried: true,
          headers: {
            ...(response.config.headers || {}),
            Authorization: `Bearer ${newToken}`
          }
        }
        return service(retryConfig)
      }
      
      // 没有新 token 或已经重试过，才真正流转到错误处理
      ElMessage.error(res.message || res.msg || '登录已过期，请重新登录')
      clearAuthAndRedirect()
      return Promise.reject(new Error(res.message || res.msg || 'Unauthorized'))
      }

      if (res.code === 200 || res.code === 201) { // 201 Created
        return res
      }

      // 无 code 的普通对象响应兜底透传，避免误判。
      if (typeof res.code === 'undefined') {
        return res
      }

      ElMessage.error(res.message || res.msg || '系统错误')
      return Promise.reject(new Error(res.message || res.msg || 'Error'))
    }

    // SSE/纯文本接口不走 { code, data } 包装，直接透传
    if (contentType.includes('text/event-stream') || typeof rawRes === 'string') {
      return rawRes
    }
    // 非对象响应兜底透传，避免误判为系统错误
    return rawRes
  },
  (error) => {
    const silentError = Boolean(error?.config?.silentError)

    // 处理 401 HTTP Status 错误（不同于 code: 401）
    if (error.response && error.response.status === 401) {
      const errorData = tryParseJson(error.response.data) || {}
      // 检查窗口期内是否有新 token 在错误响应体中（兼容字符串 JSON）
      const newToken = extractTokenFromPayload(errorData, true)
      
      if (newToken && error.config && !error.config.__tokenRetried) {
        // 有新 token，更新并重试
        localStorage.setItem('token', newToken)
        const retryConfig = {
          ...error.config,
          __tokenRetried: true,
          headers: {
            ...(error.config.headers || {}),
            Authorization: `Bearer ${newToken}`
          }
        }
        return service(retryConfig)
      }
      
      // 没有新 token 或已经重试过，则清除认证
      if (!silentError) {
        ElMessage.error(error.response.data?.message || error.response.data?.msg || '登录已过期，请重新登录')
      }
      clearAuthAndRedirect()
    } else {
      if (!silentError) {
        ElMessage.error(error.message || '网络请求失败')
      }
    }
    return Promise.reject(error)
  }
)

export default service