// src/api/Profile.js
import service from '../utils/request'
import axios from 'axios'

const normalizeUrl = (url) => {
  if (!url || typeof url !== 'string') return ''

  if (/^https?:\/\//i.test(url)) return url
  if (url.startsWith('//')) return `https:${url}`

  const base = (service.defaults.baseURL || '').replace(/\/$/, '')
  if (url.startsWith('/')) return `${base}${url}`

  return url
}

const extractUrlFromResponse = (res) => {
  const payload = res?.data || res || {}
  const directCandidates = [
    res?.tmpSecretUrl,
    res?.tempSecretUrl,
    res?.url,
    res?.uploadUrl,
    payload?.tmpSecretUrl,
    payload?.tempSecretUrl,
    payload?.url,
    payload?.uploadUrl
  ]

  for (const item of directCandidates) {
    const normalized = normalizeUrl(item)
    if (normalized) return normalized
  }

  if (typeof payload === 'string') {
    const normalized = normalizeUrl(payload)
    if (normalized) return normalized
  }

  if (payload && typeof payload === 'object') {
    for (const value of Object.values(payload)) {
      const normalized = normalizeUrl(value)
      if (normalized) return normalized
    }
  }

  return ''
}

// 查询当前登录用户信息
export const getUserProfile = () => {
	return service({
		url: 'api/users',
		method: 'get'
	})
}

// 更新用户信息（昵称、简介等）
export const updateUserInfo = (account,user) => {
  return service({
    url: 'api/users',
    method: 'put',
    data:{
      account,
      user
    }
  })
}

// 发送验证码
export const sendVerifyCode = (email) => {
  return service({
    url: 'api/code',
    method: 'get',
    params: { email }
  })
}


// 重置密码（调用后端真实接口）
export const resetPassword = ({ email, code, newPassword }) => {
  return service({
    url: 'api/users/resetPassword',
    method: 'put',
    data: {
      account: {
        email,
        password: newPassword
      },
      code
    }
  })
}

// 获取头像上传临时地址
export const getAvatarUploadUrl = (filename) => {
  return service({
    url: 'api/cos/file/avatar',
    method: 'put',
    params: { filename }
  }).then((res) => {
    const uploadUrl = extractUrlFromResponse(res)
    if (!uploadUrl) {
      throw new Error(res?.msg || res?.message || '未获取到临时上传地址')
    }
    return uploadUrl
  })
}

// 获取头像访问地址
export const getAvatarDownloadUrl = () => {
  return service({
    url: 'api/cos/file/avatar',
    method: 'get'
  }).then((res) => {
    const accessUrl = extractUrlFromResponse(res)
    if (!accessUrl) {
      throw new Error(res?.msg || res?.message || '未获取到头像访问地址')
    }
    return accessUrl
  })
}

// 使用临时地址直传二进制文件到对象存储
export const uploadAvatarBinary = (uploadUrl, file) => {
  return axios.put(uploadUrl, file, {
    headers: {
      'Content-Type': file.type || 'application/octet-stream'
    },
    timeout: 30000
  })
}