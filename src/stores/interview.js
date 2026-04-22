import { defineStore } from 'pinia'
import { ref, shallowRef } from 'vue'
import { Room, RoomEvent, Track } from 'livekit-client'// 新增 LiveKit 引入
import { createInterview, submitAnswerTextStream, finishInterview, submitAnswerVoiceStream, getInterviewReport } from '../api/interview'
import { ElMessage, ElMessageBox } from 'element-plus'
import router from '../router'

export const useInterviewStore = defineStore('interview', () => {
  // === 状态定义 ===
  const currentInterviewId = ref(null) // 当前会话 ID
  const messages = ref([])             // 聊天记录列表
  const isConnected = ref(false)       // 文本流可用状态
  const isLoading = ref(false)         // AI 是否正在思考
  const isWaitingReport = ref(false)   // 面试结束后等待报告
  const isReportReady = ref(false)     // 报告是否已生成
  const isGeneratingReport = ref(false)     // 是否正在后台生成报告
  const generatingInterviewId = ref(null)   // 正在生成报告的面试 ID
  const isForceQuitting = ref(false)        // 标记：是否是用户主动强退的

  // 新增LiveKit 音视频通话核心状态
  // 使用 shallowRef 是因为 Room 对象庞大且内部触发频繁，不需要 Vue 深度劫持它，避免性能卡顿
  const livekitRoom = shallowRef(null)         
  const isLiveKitConnected = ref(false)        // 是否已成功连接到流媒体房间
  const remoteAudioTrack = shallowRef(null)    // AI 面试官的音频轨道 (用来绑定播放)
  const remoteVideoTrack = shallowRef(null)    // AI 面试官的视频轨道 (后续用)
  const aiIsSpeaking = ref(false)              // AI 是否正在说话 (用于前端动画)  
  const userIsSpeaking = ref(false)            // 用户是否正在说话 (用于前端动画)

  const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms))

  // === [核心修复] AI 正常结束面试的触发器 ===
  async function triggerNormalEnd() {
    const id = currentInterviewId.value
    if (!id) return

    // 1. 锁定后台生成状态（这相当于一张 VIP 通行证，让路由守卫放行跳转）
    isGeneratingReport.value = true
    generatingInterviewId.value = id

    // 2. 清空当前的面试态
    isLiveKitConnected.value = false
    currentInterviewId.value = null
    messages.value.splice(0, messages.value.length)
    
    // 3. 弹出报告已生成的交互框，提供两个精准的分流选项
    ElMessageBox.confirm(
      '面试已顺利结束！AI 教练已为您生成了深度评估报告。',
      '报告已就绪',
      {
        confirmButtonText: '立即查看',
        cancelButtonText: '回到首页',
        type: 'success',
        customClass: 'theme-confirm-box',
        closeOnClickModal: false, // 强制用户二选一，点击旁边空白处不关闭
        showClose: false // 隐藏右上角的 X
      }
    ).then(() => {
      // 用户点击【立即查看】，拿着刚才存下来的 id 直接杀进详情页！
      router.push(`/history/${id}`)
    }).catch(() => {
      // 用户点击【回到首页】
      router.push('/dashboard')
    })

    // ⚠️ 核心：我们在这里彻底抛弃了那个引发 400 报错的后台轮询函数！
  }

  // === 新增：连接 LiveKit 房间的核心方法 ===
  async function connectLiveKit(wsUrl, token, mode) {
    try {
      // 1. 实例化一个 Room 对象 (开启自适应流和动态广播，优化网络)
      const room = new Room({
        adaptiveStream: true,
        dynacast: true,
      })
      livekitRoom.value = room

      // 2. 监听事件：当 AI 面试官把它的声音或视频推过来时，触发订阅
      room.on(RoomEvent.TrackSubscribed, (track, publication, participant) => {
        if (track.kind === Track.Kind.Audio) {
          console.log('✅ 已接收到 AI 面试官的音频流')
          remoteAudioTrack.value = track // 存起来，马上要在页面上播放
        } else if (track.kind === Track.Kind.Video) {
          remoteVideoTrack.value = track
        }
      })

      // 3. 监听事件：房间内正在说话的人发生变化时 (ActiveSpeaker)
      // 这个极其好用！我们不需要自己算音量，LiveKit 直接告诉我们 AI 是不是在开口说话
      room.on(RoomEvent.ActiveSpeakersChanged, (speakers) => {
        // speakers 是一个数组，找出里面不是本地用户(isLocal=false)的，那就是 AI
        const aiSpeaker = speakers.find(s => !s.isLocal)
        const localSpeaker = speakers.find(s => s.isLocal)
        aiIsSpeaking.value = !!aiSpeaker // true 说明 AI 正在出声，false 说明 AI 闭嘴了
        userIsSpeaking.value = !!localSpeaker
      })

      // 4. 监听事件：意外断开连接
      room.on(RoomEvent.Disconnected, () => {
        console.log('❌ 已从面试房间断开')
        isLiveKitConnected.value = false
        remoteAudioTrack.value = null
        
        // 如果是用户自己点红钮强退的，直接 return，不需要触发正常结束逻辑
        if (isForceQuitting.value) return 

        // 如果不是用户强退的，那一定是被 ML 踢出房间或房间销毁了！触发正常结束！
        console.log('✅ 监听到 ML 端销毁房间，触发正常结束流程！')
        triggerNormalEnd()
      })

      // 5. 正式发起 WebSocket 连接
      await room.connect(wsUrl, token)
      isLiveKitConnected.value = true
      console.log('🔗 成功连入 LiveKit 面试房间')

      // 6. 白皮书核心要求：前端无脑推送麦克风流
      await room.localParticipant.setMicrophoneEnabled(true)

      // 如果是视频模式，顺便把本地摄像头推上去
      if (mode === 'video') {
        await room.localParticipant.setCameraEnabled(true)
      }

      return true
    } catch (error) {
      console.error("LiveKit 连接失败:", error)
      return false
    }
  }

  // === 新增：彻底销毁房间和媒体流 ===
  function disconnectLiveKit() {
    if (livekitRoom.value) {
      livekitRoom.value.disconnect() // 必须调用，否则麦克风灯会一直亮着
      livekitRoom.value = null
    }
    isLiveKitConnected.value = false
    remoteAudioTrack.value = null
    remoteVideoTrack.value = null
    aiIsSpeaking.value = false
    userIsSpeaking.value = false
  }
  
  const hasReportData = (value) => {
    if (value == null) return false
    if (Array.isArray(value)) return value.length > 0
    if (typeof value === 'object') return Object.keys(value).length > 0
    return String(value).trim().length > 0
  }

  const parseMaybeJson = (value) => {
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

  const unwrapReportPayload = (response) => {
    const status = Number(response?.status || 0)
    const raw = parseMaybeJson(response?.data)

    if (raw && typeof raw === 'object' && typeof raw.code !== 'undefined') {
      const code = Number(raw.code)
      if (code === 202) {
        return { ready: false, status: 202, data: null }
      }

      if (code === 200) {
        const reportData = raw.data ?? null
        return {
          ready: hasReportData(reportData),
          status: 200,
          data: reportData
        }
      }
    }

    if (status === 202) {
      return { ready: false, status: 202, data: null }
    }

    if (status === 200) {
      const reportData = raw && typeof raw === 'object' && raw.data !== undefined ? raw.data : raw
      return {
        ready: hasReportData(reportData),
        status: 200,
        data: reportData
      }
    }

    return { ready: false, status, data: null }
  }

  const waitForInterviewReport = async (interviewId, options = {}) => {
    const initialDelayMs = options.initialDelayMs ?? 3000
    const intervalMs = options.intervalMs ?? 2500
    // 默认约 3 分钟窗口：3s + (72 - 1) * 2.5s ≈ 180.5s
    const maxAttempts = options.maxAttempts ?? 72

    await sleep(initialDelayMs)

    for (let attempt = 1; attempt <= maxAttempts; attempt++) {
      const response = await getInterviewReport(interviewId)
      const parsed = unwrapReportPayload(response)

      if (parsed.ready) {
        return parsed.data
      }

      if (attempt < maxAttempts) {
        await sleep(intervalMs)
      }
    }

    throw new Error('面试报告仍在生成中，请稍后重试')
  }

  const pickInterviewId = (res) => {
    const payload = res?.data ?? res ?? {}
    return payload.interviewId || payload.id || payload.sessionId || null
  }

  const pickInitialQuestion = (res) => {
    const payload = res?.data ?? res ?? {}
    return String(payload.question || payload.firstQuestion || payload.content || '').trim()
  }

  // === 动作定义 ===

  // 1. 初始化面试 (对应 PDF 第一步)
  async function initInterview(params) {
    try {
      isForceQuitting.value = false;

      isLoading.value = true
      const createParams = {
        jobRole: params?.jobRole,
        difficulty: params?.difficulty,
        mode: params?.mode,
        jobInfo: params?.jobInfo,
        interviewerStyle: params?.interviewerStyle,
        resumeFile: params?.resumeFile,
        resumeRemoteUrl: params?.resumeRemoteUrl,
        resumeFileName: params?.resumeFileName
      }
      // 调用 API 创建会话
      const res = await createInterview(createParams)
      const interviewId = pickInterviewId(res)
      if (!interviewId) {
        throw new Error('创建成功但未返回面试 ID')
      }

      currentInterviewId.value = interviewId
      console.log(`✅ 成功创建新面试！当前 Interview ID: [ ${interviewId} ]，模式:[ ${createParams.mode} ]`)
      
      // 清空旧消息
      messages.value = []
      isWaitingReport.value = false

      // === [新增的 LiveKit 分流逻辑] ===
      if (createParams.mode === 'audio' || createParams.mode === 'video') {
        // 注意：这里需要你后端同学配合！在创建面试的返回值 res 中，带上 token 和 wsUrl
        // 比如 res.data.livekitToken 和 res.data.livekitUrl
        const payload = res?.data ?? res
        const token = payload?.livekitToken 
        const wsUrl = payload?.url

        if (!token || !wsUrl) {
          throw new Error('后端未返回 LiveKit Token 或 WS 地址')
        }

        // 调用上面刚写的核心函数，建立真正的流媒体连接！
        const connected = await connectLiveKit(wsUrl, token, createParams.mode)
        if (!connected) throw new Error('流媒体房间连接失败')
      } else {
        // === 你原有的文本模式逻辑保留 ===
        const firstQuestion = pickInitialQuestion(res)
        if (firstQuestion) {
          messages.value.push({ id: Date.now(), role: 'assistant', content: firstQuestion, type: 'text' })
        }
        isConnected.value = true
      }
      
      return true
    } catch (error) {
      console.error(error)
      return false
    } finally {
      isLoading.value = false
    }
  }

  const pickStreamText = (payload) => {
    if (payload == null) return ''

    if (typeof payload === 'object') {
      return String(payload.content || payload.text || payload.message || payload.data || '')
    }

    const raw = String(payload)
    const trimmed = raw.trim()
    if (!trimmed) return ''

    if ((trimmed.startsWith('{') && trimmed.endsWith('}')) || (trimmed.startsWith('[') && trimmed.endsWith(']'))) {
      try {
        const parsed = JSON.parse(trimmed)
        return String(parsed.content || parsed.text || parsed.message || parsed.data || '')
      } catch (_) {
        return raw
      }
    }

    return raw
  }

  const consumeAssistantStream = async (sendStreamRequest) => {
    let assistantMessageId = null
    let streamError = ''
    let interviewEnded = false
    let pendingChunks = [] // 待展示的字符队列
    let isTyping = false   // 是否正在打字
    let typewriterTimer = null // 定时器引用

    // 打字机效果函数：逐字展示
    const typeWriter = () => {
      if (pendingChunks.length === 0) {
        isTyping = false
        typewriterTimer = null
        return
      }

      isTyping = true
      const target = messages.value.find((item) => item.id === assistantMessageId)
      
      if (target) {
        // 每次取出1-3个字符追加到消息中（根据后端chunk大小调整）
        const charsToAdd = Math.min(2, pendingChunks.length)
        for (let i = 0; i < charsToAdd; i++) {
          target.content += pendingChunks.shift()
        }
        
        // 继续处理下一批字符，延迟模拟打字效果
        typewriterTimer = setTimeout(typeWriter, 30)
      }
    }

    try {
      await sendStreamRequest({
        onOpen: () => {
          isConnected.value = true
        },
        onMessage: (payload) => {
          const chunk = pickStreamText(payload)
          const marker = chunk.trim()
          const hasEndMarker = marker.includes('[END]')
          const safeChunk = hasEndMarker ? chunk.replace('[END]', '') : chunk
          const safeMarker = safeChunk.trim()

          if (hasEndMarker) {
            interviewEnded = true
            isWaitingReport.value = true
          }

          if (!safeMarker) return
          if (safeMarker === '[DONE]') {
            // 流结束标记，等待所有字符打完
            return
          }

          if (safeMarker.includes('[ERROR]')) {
            streamError = safeMarker
            return
          }

          if (!assistantMessageId) {
            assistantMessageId = Date.now() + Math.random()
            messages.value.push({
              id: assistantMessageId,
              role: 'assistant',
              content: '',
              type: 'text'
            })
          }

          // 将chunk中的每个字符加入待展示队列
          for (const char of safeChunk) {
            pendingChunks.push(char)
          }

          // 如果没有正在打字，启动打字机
          if (!isTyping) {
            typeWriter()
          }
        },
        onDone: () => {
          // SSE完成，但可能还有字符在队列中
        }
      })

      // 等待所有字符打完（最多等待10秒）
      const startWait = Date.now()
      while ((pendingChunks.length > 0 || isTyping) && Date.now() - startWait < 10000) {
        await new Promise(resolve => setTimeout(resolve, 50))
      }

      // 清理定时器
      if (typewriterTimer) {
        clearTimeout(typewriterTimer)
        typewriterTimer = null
      }

      // 如果还有剩余字符（超时情况），直接全部追加
      if (pendingChunks.length > 0 && assistantMessageId) {
        const target = messages.value.find((item) => item.id === assistantMessageId)
        if (target) {
          target.content += pendingChunks.join('')
          pendingChunks = []
        }
      }

    } catch (error) {
      isWaitingReport.value = false
      // 清理定时器
      if (typewriterTimer) {
        clearTimeout(typewriterTimer)
      }
      throw error
    }

    if (streamError) {
      throw new Error(streamError)
    }

    if (!interviewEnded) {
      isWaitingReport.value = false
      return {
        interviewEnded: false,
        reportReady: false,
        reportData: null
      }
    }

    isWaitingReport.value = true
    try {
      const reportData = await waitForInterviewReport(currentInterviewId.value)
      return {
        interviewEnded: true,
        reportReady: true,
        reportData
      }
    } finally {
      isWaitingReport.value = false
    }
  }

  // 4. 用户发送消息
  async function sendUserMessage(text) {
    if (!currentInterviewId.value) {
      ElMessage.warning('面试会话未创建，请重新开始')
      return
    }

    // 先把用户的字显示在界面上
    messages.value.push({
      id: Date.now(),
      role: 'user',
      content: text,
      type: 'text'
    })

    isLoading.value = true // 显示“对方正在输入...”

    try {
      const streamResult = await consumeAssistantStream((handlers) => submitAnswerTextStream(currentInterviewId.value, text, handlers))
      return streamResult
    } catch (error) {
      console.error(error)
      messages.value.push({
        id: Date.now(),
        role: 'system',
        content: '消息发送失败，请重试',
        type: 'error'
      })
      return {
        interviewEnded: false,
        reportReady: false,
        reportData: null
      }
    } finally {
      isLoading.value = false
    }
  }

  // 5. 用户发送语音
  async function sendUserVoice(audioBlob, duration = 1) {
    if (!currentInterviewId.value) {
      ElMessage.warning('面试会话未创建，请重新开始')
      return
    }

    const audioUrl = URL.createObjectURL(audioBlob)
    
    messages.value.push({
      id: Date.now(),
      role: 'user',
      content: '语音消息', 
      type: 'audio',       
      audioUrl: audioUrl,
      duration: duration // 核心新增：将秒数保存到这条消息数据中
    })

    isLoading.value = true

    try {
      // 转换 Blob 为 File，并通过 SSE 增量接收 AI 回复。
      const file = new File([audioBlob], 'recording.wav', { type: 'audio/wav' })

      const streamResult = await consumeAssistantStream((handlers) => submitAnswerVoiceStream(currentInterviewId.value, file, handlers))
      return streamResult
    } catch (error) {
      console.error(error)
      messages.value.push({
        id: Date.now(),
        role: 'system',
        content: '语音发送失败，请重试',
        type: 'error'
      })
      return {
        interviewEnded: false,
        reportReady: false,
        reportData: null
      }
    } finally {
      isLoading.value = false
    }
  }

  // 6. 结束面试 (手动触发)
  async function endSession() {
    if (currentInterviewId.value) {
      try {
        await finishInterview(currentInterviewId.value)
      } catch (error) {
        console.warn("后端结束接口异常，忽略:", error)
      }
      
      // 彻底清理状态
      isConnected.value = false
      currentInterviewId.value = null
      isReportReady.value = false
      isWaitingReport.value = false
      
      // [安全清理 messages 数组]
      messages.value.splice(0, messages.value.length)
    }
  }

  return {
    currentInterviewId,
    messages,
    isLoading,
    isConnected,
    isWaitingReport,
    isReportReady,
    initInterview,
    sendUserMessage,
    sendUserVoice, 
    endSession,
    
    // 新增暴漏给 UI 层的变量
    livekitRoom,
    isLiveKitConnected,
    remoteAudioTrack,
    remoteVideoTrack,
    aiIsSpeaking,
    userIsSpeaking,
    disconnectLiveKit,

    isGeneratingReport,
    generatingInterviewId,
    isForceQuitting
  }
})