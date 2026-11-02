import service from '../utils/request'
import axios from 'axios'

const toAbsoluteUrl = (url) => {
	if (!url || typeof url !== 'string') return ''
	if (/^https?:\/\//i.test(url)) return url
	if (url.startsWith('//')) return `https:${url}`
	if (url.startsWith('/')) {
		const base = (service.defaults.baseURL || '').replace(/\/$/, '')
		return `${base}${url}`
	}
	return url
}

const pickUrl = (obj) => {
	if (!obj || typeof obj !== 'object') return ''
	for (const key of ['tmpSecretUrl', 'tempSecretUrl', 'uploadUrl', 'downloadUrl', 'url']) {
		if (obj[key]) return obj[key]
	}
	for (const value of Object.values(obj)) {
		if (typeof value === 'string') return value
	}
	return ''
}

const extractUrl = (res) => {
	const data = res?.data || res || {}
	const raw = typeof data === 'string' ? data : pickUrl(data) || pickUrl(res)
	return toAbsoluteUrl(raw)
}

// 获取简历上传临时地址
export const getResumeUploadUrl = (filename) => {
	return service({
		url: 'api/cos/file/vita',
		method: 'put',
		params: { filename }
	}).then((res) => {
		const uploadUrl = extractUrl(res)
		if (!uploadUrl) {
			throw new Error(res?.msg || res?.message || '未获取到简历上传地址')
		}
		return uploadUrl
	})
}

// 使用临时地址直传二进制文件
export const uploadResumeBinary = (uploadUrl, file) => {
	return axios.put(uploadUrl, file, {
		headers: {
			'Content-Type': file.type || 'application/pdf'
		},
		timeout: 30000
	})
}

// 获取简历访问地址
export const getResumeDownloadUrl = () => {
	return service({
		url: 'api/cos/file/vita',
		method: 'get'
	}).then((res) => extractUrl(res))
}

// 根据访问地址拉取简历二进制，用于前端内嵌预览
export const fetchResumeBlob = (downloadUrl) => {
	return axios.get(downloadUrl, {
		responseType: 'blob',
		timeout: 30000
	}).then((res) => res.data)
}

const normalizeArrayField = (value) => {
	if (!Array.isArray(value)) return []
	return value
		.map((item) => (typeof item === 'string' ? item.trim() : ''))
		.filter(Boolean)
}

// 获取简历评价
export const getResumeAnalysis = () => {
	return service({
		url: 'api/users/resumeAnalysis',
		method: 'get'
	}).then((res) => {
		const data = res?.data || {}
		return {
			strengths: normalizeArrayField(data.strengths),
			suggestions: normalizeArrayField(data.suggestions),
			weaknesses: normalizeArrayField(data.weaknesses)
		}
	})
}
