import request from '../utils/request'

const parseSseBlock = (block) => {
  const result = {
    event: '',
    id: '',
    retry: '',
    data: ''
  }
  const dataLines = []

  for (const line of block.split('\n')) {
    if (!line || line.startsWith(':')) continue
    if (line.startsWith('event:')) {
      result.event = line.slice(6).trim()
      continue
    }
    if (line.startsWith('id:')) {
      result.id = line.slice(3).trim()
      continue
    }
    if (line.startsWith('retry:')) {
      result.retry = line.slice(6).trim()
      continue
    }
    if (line.startsWith('data:')) {
      dataLines.push(line.slice(5).trimStart())
    }
  }

  result.data = dataLines.join('\n')
  return result
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

const isLikelyJwt = (value) => {
  if (typeof value !== 'string') return false
  const token = value.trim()
  return Boolean(token) && token.split('.').length === 3
}

const extractRefreshTokenFromPayload = (payload) => {
  const normalized = tryParseJson(payload)
  if (!normalized || typeof normalized !== 'object') return ''

  const code = Number(normalized.code)
  if (!(code === 401 || code === 40105)) return ''

  const data = normalized.data
  const dataObj = typeof data === 'object' && data ? data : {}
  const tokenFromDataString = typeof data === 'string' && isLikelyJwt(data) ? data : ''

  return (
    normalized.token ||
    normalized.accessToken ||
    normalized.access_token ||
    normalized.newToken ||
    dataObj.token ||
    dataObj.accessToken ||
    dataObj.access_token ||
    dataObj.newToken ||
    tokenFromDataString ||
    ''
  )
}

const extractRefreshTokenFromSseText = (sseText) => {
  // 后端在窗口期可能直接返回 JSON（不是 data: 前缀的 SSE 块）
  const tokenFromRawPayload = extractRefreshTokenFromPayload(String(sseText || '').trim())
  if (tokenFromRawPayload) {
    return tokenFromRawPayload
  }

  const blocks = String(sseText || '').split(/\r?\n\r?\n/)
  for (const rawBlock of blocks) {
    const block = rawBlock.trim()
    if (!block) continue
    const parsed = parseSseBlock(block)
    if (!parsed.data) continue
    const token = extractRefreshTokenFromPayload(parsed.data)
    if (token) {
      return token
    }
  }
  return ''
}

// 将 SSE 文本流分块处理
const processSseStream = (sseText, handlers = {}) => {
  const lines = sseText.split('\n')
  let buffer = ''

  for (const line of lines) {
    buffer += line + '\n'
    if (line === '') {
      const block = buffer.slice(0, -1).trim()
      buffer = ''
      if (block) {
        const parsed = parseSseBlock(block)
        if (parsed.data) {
          handlers.onMessage?.(parsed.data, parsed)
        }
      }
    }
  }

  if (buffer.trim()) {
    const parsed = parseSseBlock(buffer.trim())
    if (parsed.data) {
      handlers.onMessage?.(parsed.data, parsed)
    }
  }
}

const REQUIRED_ERROR_MAP = {
  jobRole: '请选择面试方向',
  difficulty: '请选择面试难度',
  mode: '请选择面试模式',
  jobInfo: '请填写岗位信息',
  interviewerStyle: '请选择面试官风格'
}

const ensureRequiredText = (value, field) => {
  const normalized = String(value || '').trim()
  if (!normalized) {
    throw new Error(REQUIRED_ERROR_MAP[field] || `${field} 为必填项`)
  }
  return normalized
}

const ensureEnumValue = (value, field, allowedValues) => {
  const normalized = String(value || '').toLowerCase().trim()
  if (!normalized) {
    throw new Error(REQUIRED_ERROR_MAP[field] || `${field} 为必填项`)
  }
  if (!allowedValues.includes(normalized)) {
    throw new Error(`${field} 仅支持: ${allowedValues.join(', ')}`)
  }
  return normalized
}

// 1. 创建面试会话
// 文档要求 multipart/form-data
export const createInterview = async (data) => {
  const formData = new FormData()
  const jobRole = ensureRequiredText(data.jobRole, 'jobRole')
  const difficulty = ensureEnumValue(data.difficulty, 'difficulty', ['easy', 'medium', 'hard'])
  const mode = ensureEnumValue(data.mode, 'mode', ['text', 'audio', 'video'])
  const jobInfo = ensureRequiredText(data.jobInfo, 'jobInfo')
  const interviewerStyle = ensureEnumValue(data.interviewerStyle, 'interviewerStyle', ['standard', 'friendly', 'aggressive', 'expert'])

  formData.append('jobRole', jobRole)
  formData.append('difficulty', difficulty)
  formData.append('mode', mode)
  formData.append('jobInfo', jobInfo)
  formData.append('interviewerStyle', interviewerStyle)

  return request({
    url: '/api/v1/interviews',
    method: 'post',
    data: formData
  })
}

// 2. 开始面试 (触发首题)
export const startInterview = (interviewId) => {
  return request({
    url: `/api/v1/interviews/${interviewId}/start`,
    method: 'post'
  })
}

// 3. 提交文本回答
export const submitAnswerText = (interviewId, content) => {
  return request({
    url: `/api/v1/interviews/${interviewId}/ans`,
    method: 'post',
    data: {
      type: 'text',
      content: content
    }
  })
}

// 3.1 提交文本回答（SSE 流式返回，使用 axios）
export const submitAnswerTextStream = async (interviewId, content, handlers = {}, _retryCount = 0) => {
  try {
    const apiResponse = await request({
      url: `/api/v1/interviews/${interviewId}/ans`,
      method: 'POST',
      headers: {
        'Accept': 'text/event-stream',
        'Content-Type': 'application/json'
      },
      data: {
        type: 'text',
        content
      },
      responseType: 'text'
    })

    // axios 的拦截器已处理 40105 token 续期
    const sseText = typeof apiResponse === 'string' ? apiResponse : apiResponse.data || ''
    const refreshedToken = extractRefreshTokenFromSseText(sseText)
    if (refreshedToken && _retryCount < 1) {
      // SSE 过程中若返回 token 续期消息，更新后立即重试一次
      localStorage.setItem('token', refreshedToken)
      return submitAnswerTextStream(interviewId, content, handlers, _retryCount + 1)
    }
    
    handlers.onOpen?.()
    processSseStream(sseText, handlers)
    handlers.onDone?.()
  } catch (error) {
    handlers.onError?.(error)
    throw error
  }
}

// 3.2 提交语音回答（SSE 流式返回，使用 axios）
export const submitAnswerVoiceStream = async (interviewId, audioFile, handlers = {}, _retryCount = 0) => {
  try {
    const formData = new FormData()
    formData.append('file', audioFile)

    const apiResponse = await request({
      url: `/api/v1/interviews/${interviewId}/ans/voice`,
      method: 'POST',
      headers: {
        'Accept': 'text/event-stream'
        // 不设置 Content-Type，让 axios 自动设置为 multipart/form-data
      },
      data: formData,
      responseType: 'text'
    })

    // axios 的拦截器已处理 40105 token 续期
    const sseText = typeof apiResponse === 'string' ? apiResponse : apiResponse.data || ''
    const refreshedToken = extractRefreshTokenFromSseText(sseText)
    if (refreshedToken && _retryCount < 1) {
      // SSE 过程中若返回 token 续期消息，更新后立即重试一次
      localStorage.setItem('token', refreshedToken)
      return submitAnswerVoiceStream(interviewId, audioFile, handlers, _retryCount + 1)
    }
    
    handlers.onOpen?.()
    processSseStream(sseText, handlers)
    handlers.onDone?.()
  } catch (error) {
    handlers.onError?.(error)
    throw error
  }
}

// 4. 结束面试
export const finishInterview = (interviewId) => {
  return request({
    url: `/api/v1/interviews/${interviewId}/finish`,
    method: 'post'
  })
}

// 4.1 强制结束面试（不生成报告）
export const forceFinishInterview = (interviewId, config = {}) => {
  return request({
    url: `/api/v1/interviews/${interviewId}/finish`,
    method: 'post',
    ...config
  })
}

// 5. 获取面试历史列表
export const getHistoryList = (params) => {
  return request({
    url: '/api/v1/interviews',
    method: 'get',
    params // { page, pageSize, status... }
  })
}

// 6. 获取面试评估报告 (雷达图数据)
export const getInterviewReport = (interviewId) => {
  return request({
    url: `/api/v1/interviews/${interviewId}/report`,
    method: 'get',
    returnNativeResponse: true
  })
}
  
// 8. 提交语音回答
export const submitAnswerVoice = (interviewId, audioFile) => {
  return submitAnswerVoiceStream(interviewId, audioFile)
}

// 9. 获取轮次回放 (历史对话详情)
export const getTurnPlayback = (interviewId) => {
  return request({
    url: `/api/v1/interviews/${interviewId}/history`,
    method: 'get'
  })
}