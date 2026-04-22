<template>
  <div class="chat-view-container">
    <!-- 注释必须放在唯一的根节点 div 内部，防止 Vue Transition 动画死锁崩溃 -->

    <!-- 1. 未开始状态 (合并为空状态) -->
    <div v-if="!isStarted && !showResult" class="empty-state">
      <div class="start-card">
        <el-icon :size="60" class="start-icon"><Service /></el-icon>
        <h2>AI 模拟面试</h2>
        <p>选择面试模式与岗位，开启专业的 AI 沉浸式面试之旅</p>
        <div class="start-actions">
          <el-button type="primary" size="large" round @click="openModal" class="start-btn">
            开始新面试
          </el-button>
        </div>
      </div>
    </div>

    <!-- 2. 文字对话模式 -->
    <div v-else-if="isStarted && !showResult && currentMode === 'text'" class="chat-interface">
      <!-- 顶部栏 -->
      <div class="chat-header">
        <div class="header-info">
          <span class="status-dot"></span>
          <span class="job-title">{{ currentJobName }} 面试中 (对话模式)</span>
        </div>
        <el-button circle type="danger" @click="handleExitWithoutReport" title="退出但不保存报告">
          <el-icon><SwitchButton /></el-icon>
        </el-button>
      </div>
      
      <!-- 聊天内容区 -->
      <div class="chat-scroll-area" ref="scrollRef">
        <div class="messages-list">
          <div class="system-notice"><span>面试已开始，请等待面试官提问...</span></div>

          <div v-for="msg in interviewStore.messages" :key="msg.id" class="message-row" :class="msg.role === 'user' ? 'row-right' : 'row-left'">
            <el-avatar :size="36" :src="msg.role === 'user' ? userAvatar : aiAvatar" class="msg-avatar"/>
            <div class="message-bubble">
              <!-- 微信风格的语音气泡 (新增动态 style 绑定) -->
              <div 
                v-if="msg.type === 'audio'" 
                class="wechat-voice-bubble" 
                @click="playVoice(msg)"
                :style="{ width: getVoiceBubbleWidth(msg.duration) }"
              >
                <span class="voice-text">{{ msg.duration || 1 }}"</span>
                
                <div class="voice-icon" :class="{ 'is-playing': playingAudioId === msg.id }">
                  <div class="arc arc-3"></div>
                  <div class="arc arc-2"></div>
                  <div class="arc arc-1"></div>
                </div>
              </div>
              <div v-else-if="msg.role === 'user'" class="bubble-content">{{ msg.content }}</div>
              <div v-else class="bubble-content markdown-body" v-html="renderMarkdown(msg.content)"></div>
            </div>
          </div>

          <div v-if="interviewStore.isLoading && (interviewStore.messages.length === 0 || interviewStore.messages[interviewStore.messages.length - 1]?.role === 'user')" class="message-row row-left">
            <el-avatar :size="36" :src="aiAvatar" class="msg-avatar" />
            <div class="message-bubble typing-bubble">
              <span class="dot"></span><span class="dot"></span><span class="dot"></span>
            </div>
          </div>

          <div v-if="interviewStore.isWaitingReport" class="system-notice">
            <span>面试已结束，正在生成面试报告，请稍候...</span>
          </div>
        </div>
      </div>

      <!-- 底部输入区 -->
      <div class="input-area">
        <div class="input-wrapper">
          
          <!-- 模式切换按钮 -->
          <el-tooltip :content="isVoiceMode ? '切换到键盘输入' : '切换到语音输入'" placement="top">
            <div class="mode-switch-btn" @click="toggleInputMode">
              <el-icon v-if="!isVoiceMode" :size="20"><Microphone /></el-icon>
              <el-icon v-else :size="20"><Edit /></el-icon>
            </div>
          </el-tooltip>

          <!-- A. 文字输入模式 -->
          <template v-if="!isVoiceMode">
            <el-input 
              ref="inputRef"
              v-model="inputText" 
              type="textarea" 
              :rows="1" 
              :autosize="{ minRows: 1, maxRows: 4 }" 
              placeholder="请输入您的回答..." 
              resize="none" 
              @keydown.enter.prevent="handleSendText" 
              :disabled="interviewStore.isLoading" 
              class="flex-input" 
            />
            <div class="input-actions">
              <el-button type="primary" class="send-btn" @click="handleSendText" :disabled="!inputText.trim() || interviewStore.isLoading">
                发送
              </el-button>
            </div>
          </template>

          <!-- B. 语音输入模式 -->
          <template v-else>
            <!-- 状态 B-1: 准备录音 -->
            <div v-if="!isRecording" class="voice-btn-container" @click="startRecording">
              <div class="voice-long-btn">
                <span class="record-dot"></span>点击开始录音
              </div>
            </div>
            
            <!-- 状态 B-2: 录音中 (取消/发送) -->
            <div v-else class="recording-container">
              <div class="recording-visual">
                <div class="wave-bar"></div><div class="wave-bar"></div><div class="wave-bar"></div>
                <span class="timer-text">{{ recordingTime }}s</span>
              </div>
              <div class="recording-actions">
                <el-button type="info" size="default" round @click="cancelRecording">
                  取消
                </el-button>
                <el-button type="success" size="default" round @click="stopAndSendRecording">
                  <el-icon style="margin-right: 5px"><Check /></el-icon>发送
                </el-button>
              </div>
            </div>


          </template>

        </div>
      </div>
    </div>

    <!-- 3. 语音/视频通话模式 -->
    <div v-else-if="isStarted && !showResult && (currentMode === 'audio' || currentMode === 'video')" class="call-interface">
      
      <!-- 右上角退出按钮 -->
      <div class="header-actions" style="position: absolute; top: 20px; right: 20px; z-index: 10;">
        <el-button circle type="danger" @click="handleExitWithoutReport">
           <el-icon><SwitchButton /></el-icon>
        </el-button>
      </div>

      <!-- ============================================== -->
      <!-- 场景 A：视频通话模式 (展示 3D 影棚) -->
      <!-- ============================================== -->
      <template v-if="currentMode === 'video'">
        <div class="studio-3d-wrapper" style="width: 100%; height: 100%; position: absolute; top: 0; left: 0; z-index: 1;">
          <Interviewer3D />
        </div>

        <div class="status-overlay" style="position: absolute; top: 30px; left: 50%; transform: translateX(-50%); z-index: 2; text-align: center; background: rgba(30, 41, 59, 0.6); padding: 12px 24px; border-radius: 30px; backdrop-filter: blur(8px); border: 1px solid rgba(255,255,255,0.1);">
          <h2 class="status-text" style="margin: 0; font-size: 16px; color: white;">
            {{ interviewStore.isLiveKitConnected ? `正在与 ${currentJobName} 面试官通话中...` : `正在连接 ${currentJobName} 面试官...` }}
          </h2>
          <div class="status-sub-row">
            <p class="status-sub" :class="{ 'text-active': interviewStore.aiIsSpeaking }" style="margin: 6px 0 0; font-size: 13px; color: #94a3b8; font-weight: bold;">
              {{ interviewStore.isLiveKitConnected ? (interviewStore.aiIsSpeaking ? '🔊 AI 面试官正在讲话...' : ' 正在倾听您发言...') : ' 正在建立音视频连接，请稍候...' }}
            </p>

            <div v-if="isUserTurn" class="user-speaking-widget user-speaking-widget--compact user-speaking-widget--inline" aria-live="polite">
              <div class="user-speaking-visual" :class="{ 'is-speaking': interviewStore.userIsSpeaking }">
                <span class="idle-dot"></span>
                <span class="idle-dot"></span>
                <span class="idle-dot"></span>

                <span class="active-bar"></span>
                <span class="active-bar"></span>
                <span class="active-bar"></span>
              </div>
            </div>
          </div>
        </div>

        <!-- 视频通话本地小窗 -->
        <div class="video-window" :style="{ left: videoWindowPosition.x + 'px', top: videoWindowPosition.y + 'px' }" @mousedown="startDrag" @touchstart.prevent="startDrag">
          <video ref="videoRef" autoplay playsinline muted width="200" height="150"></video>
        </div>
      </template>

      <!-- ============================================== -->
      <!-- 场景 B：语音通话模式 (展示 2D 头像与声纹波浪) -->
      <!-- ============================================== -->
      <template v-else-if="currentMode === 'audio'">
        <div class="call-center" style="width: 100%; height: 100%; display: flex; flex-direction: column; align-items: center; justify-content: center; z-index: 1;">
          <!-- 核心：动态绑定 ai-speaking 类来触发波浪动画 -->
          <div class="avatar-wrapper" :class="{ 'ai-speaking': interviewStore.aiIsSpeaking }">
            <div class="wave"></div>
            <div class="wave"></div>
            <el-avatar :size="120" :src="aiAvatar" style="border: 2px solid var(--glass-border); box-shadow: 0 10px 30px rgba(0,0,0,0.2);" />
          </div>
          <h2 class="status-text" style="margin-top: 30px; font-size: 20px; color: var(--text-color);">
            {{ interviewStore.isLiveKitConnected ? `正在与 ${currentJobName} 语音通话中...` : `正在连接 ${currentJobName} 语音通话...` }}
          </h2>
          <p class="status-sub" :class="{ 'text-active': interviewStore.aiIsSpeaking }" style="margin-top: 10px; font-size: 14px;">
            {{ interviewStore.isLiveKitConnected ? (interviewStore.aiIsSpeaking ? '🔊 对方正在讲话...' : '正在倾听您发言...') : ' 正在建立语音连接，请稍候...' }}
          </p>

          <div v-if="isUserTurn" class="user-speaking-widget" aria-live="polite">
            <div class="user-speaking-visual" :class="{ 'is-speaking': interviewStore.userIsSpeaking }">
              <span class="idle-dot"></span>
              <span class="idle-dot"></span>
              <span class="idle-dot"></span>

              <span class="active-bar"></span>
              <span class="active-bar"></span>
              <span class="active-bar"></span>
            </div>
            <p class="user-speaking-hint">你可以开始说话</p>
          </div>
        </div>
      </template>

      <!-- [共用组件] 隐藏的音频播放器，用来播放真实的 LiveKit 声音 -->
      <audio ref="remoteAudioRef" autoplay></audio>
      
    </div>

    <!-- 4. 面试结果报告状态 -->
    <div v-else-if="showResult" class="result-interface">
      <div class="result-header">
        <h2>面试结果报告</h2>
        <div class="header-actions">
          <el-button type="primary" round @click="backToStart">返回入口</el-button>
          <el-button type="primary" round @click="exportToPDF">
            <el-icon style="margin-right: 5px"><Document /></el-icon>
            导出为PDF
          </el-button>
        </div>
      </div>
      
      <div class="result-content" :class="{ 'pdf-exporting': isExportingPdf, 'pdf-export-light': isExportingPdf }" id="report-content-export">
        <div class="report-hero">
          <div class="hero-main">
            <span class="hero-kicker">录用建议</span>
            <h3>{{ reportViewData.hiringRecommendation }}</h3>
            <div class="hero-summary markdown-body" v-html="renderMarkdown(reportViewData.detailedRecommendation)"></div>
          </div>
          <div class="hero-score" :style="{ backgroundColor: stampConfig.bg, borderColor: stampConfig.border }">
            <p class="hero-score-label">综合评分</p>
            <p class="hero-score-value" :style="{ color: stampConfig.color }">{{ overallScoreValue }}</p>
            <div class="score-stamp" :style="{ color: stampConfig.color, borderColor: stampConfig.color }">
              {{ stampConfig.text }}
            </div>
          </div>
        </div>

        <!-- 雷达图部分 -->
        <div class="radar-chart-container">
          <h3>核心能力评估</h3>
          <div class="radar-chart">
            <div class="radar-main">
              <div class="chart-wrapper">
                <div ref="radarChartRef" class="chart-box"></div>
                <div v-for="item in radarMajorBadges" :key="item.key" class="radar-major-badge" :class="`badge-${item.key}`">
                  <span class="major-dot"></span>
                  <div class="major-meta">
                    <span class="major-label">{{ item.shortLabel }}</span>
                    <span class="major-value">{{ item.score.toFixed(2) }}/5</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="dimension-breakdown">
          <h3>维度细分明细</h3>
          <div class="dimension-grid">
            <div v-for="group in dimensionDetailGroups" :key="group.key" class="dimension-group">
              <h4>
                <span>{{ group.label }}</span>
                <em>{{ group.score.toFixed(2) }}/5</em>
              </h4>
              <div v-for="row in group.items" :key="row.key" class="metric-row">
                <div class="metric-head">
                  <span>{{ row.label }}</span>
                  <strong>{{ row.value }}/5</strong>
                </div>
                <div class="metric-track">
                  <div class="metric-fill" :style="{ width: `${row.value * 20}%` }"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="evaluation-section">
          <h3>执行总结</h3>
          <div class="evaluation-content markdown-body" v-html="renderMarkdown(reportViewData.executiveSummary)"></div>
        </div>

        <div class="evaluation-section">
          <h3>亮点优势</h3>
          <ul class="suggestion-list">
            <li v-for="(item, index) in reportViewData.strengths" :key="`s-${index}`">
              <div class="markdown-body" v-html="renderMarkdown(item)"></div>
            </li>
          </ul>
        </div>

        <div class="suggestion-section">
          <h3>待提升项</h3>
          <ul class="suggestion-list">
            <li v-for="(item, index) in reportViewData.weaknesses" :key="`w-${index}`">
              <div class="markdown-body" v-html="renderMarkdown(item)"></div>
            </li>
          </ul>
        </div>

        <!-- 详细建议已移除 -->
      </div>
    </div>

    <!-- 弹窗：使用统一组件 -->
    <CallSelectionModal ref="modalRef" @confirmed="handleStart" />
  </div>
</template>

<script setup>
import { ref, computed, nextTick, watch, onUnmounted, onMounted } from 'vue'
import { ChatDotRound, Microphone, Edit, Check, Document, Service, PhoneFilled, SwitchButton } from '@element-plus/icons-vue'
import CallSelectionModal from '../../components/CallSelectionModal.vue'
import { ElMessageBox, ElMessage } from 'element-plus'
import { useInterviewStore } from '../../stores/interview'
import { useUserStore } from '../../stores/user'
import { useThemeStore } from '../../stores/theme'
import { convertBlobToPcmWav16kMono } from '../../utils/audio'
import { forceFinishInterview } from '../../api/interview'
import * as echarts from 'echarts'
import html2pdf from 'html2pdf.js'
import Interviewer3D from '../../components/Interviewer3D.vue'
import { onBeforeRouteLeave, useRouter } from 'vue-router' // 补充 useRouter

import MarkdownIt from 'markdown-it'
import hljs from 'highlight.js'
import 'highlight.js/styles/atom-one-dark.css'

const router = useRouter()
const interviewStore = useInterviewStore()
const userStore = useUserStore()
const themeStore = useThemeStore()

const modalRef = ref(null)
const isStarted = ref(false)
const showResult = ref(false)
const currentMode = ref('') // 'text', 'audio', 'video'
const currentJobId = ref('')

// === 文字模式状态 (包含录音) ===
const inputText = ref('')
const inputRef = ref(null)
const scrollRef = ref(null)
// [新增] 用于绑定 AI 音频轨道的 DOM 引用
const remoteAudioRef = ref(null)

const isVoiceMode = ref(false) 
const isRecording = ref(false) 
const recordingTime = ref(0)
let mediaRecorder = null
let audioChunks =[]
let timerInterval = null

// 视频模式状态
const videoStream = ref(null)
const videoRef = ref(null)
const videoWindowPosition = ref({ x: 20, y: 100 })
const isDragging = ref(false)
const dragStart = ref({ x: 0, y: 0 })
const MOBILE_BREAKPOINT = 768

// 报告状态
const radarChartRef = ref(null)
const isExportingPdf = ref(false)
let radarChart = null

// === 核心修复：无敌版路由离开守卫 (Vue Router 4 标准写法) ===
onBeforeRouteLeave(async (to, from) => {
  // 1. 【核心修复】发放 VIP 通行证！
  // 如果状态库显示“正在生成报告(正常结束)”，或者 面试根本没开始，直接无条件放行！
  if (interviewStore.isGeneratingReport || (!isStarted.value && !interviewStore.currentInterviewId)) {
    return true; // 允许跳转，绝不拦截！
  }

  // 2. 如果还在面试中，且没有在生成报告，弹窗强退拦截
  try {
    await ElMessageBox.confirm(
      '面试还在进行中，离开将强行结束面试且不生成报告。确定要离开吗？',
      '警告',
      {
        confirmButtonText: '确定离开',
        cancelButtonText: '取消',
        type: 'warning',
        customClass: 'theme-confirm-box'
      }
    );
    
    // ---- 用户点击了【确定离开】 ----
    interviewStore.isForceQuitting = true;
    stopCurrentAudio();
    if (videoStream.value) {
      videoStream.value.getTracks().forEach(track => track.stop());
      videoStream.value = null;
    }
    if (isRecording.value) cancelRecording();

    interviewStore.disconnectLiveKit();

    try {
      if (interviewStore.currentInterviewId) {
        // 后台静默通知后端结束面试失败时不抛出异常
        forceFinishInterview(interviewStore.currentInterviewId, { silentError: true }).catch(e => {
            console.warn('后台静默通知后端结束面试失败:', e)
        });
      }
    } catch (error) {
      console.warn('后端强退接口前异常，前端放行路由。', error);
    }

    interviewStore.currentInterviewId = null;
    interviewStore.isConnected = false;
    interviewStore.isReportReady = false;
    
    //[此处使用安全中文注释：使用 splice(0, length) 安全清空消息列表]
    interviewStore.messages.splice(0, interviewStore.messages.length);
    
    isStarted.value = false;
    showResult.value = false;
    currentMode.value = '';

    return true; // 允许路由跳转！
    
  } catch (error) {
    // ---- 用户点击了【取消】 ----
    return false; // 拦截路由，留在当前页面！
  }
})

const staticReportData = {
  abilityTrend: null,
  overallScore: 98.7,
  hiringRecommendation: 'Strong Hire',
  executiveSummary:
    '候选人在全部 9 轮技术面试中表现非常突出，**每轮专业、认知与表达均获得满分评价**，综合得分达到 98.7。对 Java 后端核心技术栈（Spring Boot、Redis、ConcurrentHashMap、分布式事务）掌握扎实，并能够结合高并发与线上治理场景给出高可落地方案。',
  detailedRecommendation:
    '候选人不仅呈现出显著的技术硬实力，更在系统思维、工程判断与职业成熟度上超出同级。其经历与实战回答高度吻合，理论表达稳健，具备独立主导高并发模块设计与线上问题治理的能力。建议优先推进至核心技术面/架构面。',
  dimensionScores: {
    cognition: 4.944444,
    expression: 5,
    professional: 4.911111
  },
  dimensionDetails: {
    cognition: {
      logicStructure: 5,
      problemSolving: 5,
      systemThinking: 5
    },
    expression: {
      clarity: 5,
      confidenceStability: 5,
      professionalMaturity: 5
    },
    professional: {
      engineeringPractice: 5,
      jobMatch: 5,
      knowledgeMatch: 5,
      technicalCorrectness: 5
    }
  },
  strengths: [
    '**技术深度扎实**：对 JDK 集合类底层机制、ConcurrentHashMap 高并发实现、Redis 与 Lua 脚本原理理解深入，关键技术细节回答准确。',
    '**系统设计能力强**：在订单模块、缓存一致性、日志分层与熔断治理等问题中，能提出可执行且具工程可行性的方案。',
    '**问题拆解结构化**：面对复杂问题可快速形成“挑战-方案-效果”链路，逻辑清晰，具备从根因到闭环治理的完整思路。',
    '**表达稳定流畅**：语言精炼、术语准确、信息密度高，沟通节奏与职业感兼具，能有效支撑高级岗位技术沟通。'
  ],
  weaknesses: [
    '**极致细节仍可深化**：在部分场景（如统计口径边界、主从切换恢复链路）可进一步补足极端条件与兜底策略。',
    '**可观测性维度可扩展**：在监控告警、容量评估、巡检治理方面已具基础框架，可继续强化指标体系与演练闭环。'
  ],
  duration: '18分40秒'
}

const reportPayload = ref(null)

const toSafeNumber = (value, fallback = 0) => {
  const num = Number(value)
  return Number.isFinite(num) ? num : fallback
}

const normalizeReportData = (payload = {}) => {
  const source = payload && typeof payload === 'object' ? payload : {}
  const details = source.dimensionDetails || {}

  return {
    abilityTrend: source.abilityTrend ?? staticReportData.abilityTrend,
    detailedRecommendation: source.detailedRecommendation || staticReportData.detailedRecommendation,
    dimensionDetails: {
      cognition: {
        ...staticReportData.dimensionDetails.cognition,
        ...(details.cognition || {})
      },
      expression: {
        ...staticReportData.dimensionDetails.expression,
        ...(details.expression || {})
      },
      professional: {
        ...staticReportData.dimensionDetails.professional,
        ...(details.professional || {})
      }
    },
    dimensionScores: {
      ...staticReportData.dimensionScores,
      ...(source.dimensionScores || {})
    },
    executiveSummary: source.executiveSummary || staticReportData.executiveSummary,
    hiringRecommendation: source.hiringRecommendation || staticReportData.hiringRecommendation,
    overallScore: toSafeNumber(source.overallScore, staticReportData.overallScore),
    strengths: Array.isArray(source.strengths) && source.strengths.length ? source.strengths : staticReportData.strengths,
    weaknesses: Array.isArray(source.weaknesses) && source.weaknesses.length ? source.weaknesses : staticReportData.weaknesses,
    duration: source.duration || staticReportData.duration
  }
}

const reportViewData = computed(() => normalizeReportData(reportPayload.value || staticReportData))

const overallScoreValue = computed(() => toSafeNumber(reportViewData.value.overallScore, 0))

const reportDimensionRows = computed(() => {
  const scores = reportViewData.value.dimensionScores || {}
  return [
    { key: 'cognition', label: '认知思维', score: toSafeNumber(scores.cognition, 0) },
    { key: 'expression', label: '表达能力', score: toSafeNumber(scores.expression, 0) },
    { key: 'professional', label: '专业能力', score: toSafeNumber(scores.professional, 0) }
  ]
})

const radarMajorBadges = computed(() =>
  reportDimensionRows.value.map((item) => ({
    ...item,
    shortLabel: item.key === 'cognition' ? '认知' : item.key === 'expression' ? '表达' : '专业'
  }))
)

const radarDetailItems = computed(() =>
  dimensionDetailGroups.value.flatMap((group) =>
    group.items.map((item) => ({
      ...item,
      radarLabel: item.label
    }))
  )
)

const radarValues = computed(() => radarDetailItems.value.map((item) => Number(item.value.toFixed(2))))

const dimensionDetailGroups = computed(() => {
  const details = reportViewData.value.dimensionDetails || {}
  const scores = reportViewData.value.dimensionScores || {}
  return [
    {
      key: 'cognition',
      label: '认知',
      score: toSafeNumber(scores.cognition, 0),
      items: [
        { key: 'logicStructure', label: '逻辑结构', value: toSafeNumber(details.cognition?.logicStructure, 0) },
        { key: 'problemSolving', label: '问题拆解', value: toSafeNumber(details.cognition?.problemSolving, 0) },
        { key: 'systemThinking', label: '系统思维', value: toSafeNumber(details.cognition?.systemThinking, 0) }
      ]
    },
    {
      key: 'expression',
      label: '表达',
      score: toSafeNumber(scores.expression, 0),
      items: [
        { key: 'clarity', label: '表达清晰', value: toSafeNumber(details.expression?.clarity, 0) },
        { key: 'confidenceStability', label: '自信稳定', value: toSafeNumber(details.expression?.confidenceStability, 0) },
        { key: 'professionalMaturity', label: '职业成熟', value: toSafeNumber(details.expression?.professionalMaturity, 0) }
      ]
    },
    {
      key: 'professional',
      label: '专业',
      score: toSafeNumber(scores.professional, 0),
      items: [
        { key: 'engineeringPractice', label: '工程实践', value: toSafeNumber(details.professional?.engineeringPractice, 0) },
        { key: 'jobMatch', label: '岗位匹配', value: toSafeNumber(details.professional?.jobMatch, 0) },
        { key: 'knowledgeMatch', label: '知识匹配', value: toSafeNumber(details.professional?.knowledgeMatch, 0) },
        { key: 'technicalCorrectness', label: '技术准确', value: toSafeNumber(details.professional?.technicalCorrectness, 0) }
      ]
    }
  ]
})

const aiAvatar = 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png'
const userAvatar = computed(() => userStore.userInfo.avatar || 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png')

// === 新增：微信语音气泡播放逻辑 ===
const playingAudioId = ref(null) // 记录当前正在播放的语音消息 ID
let currentAudioNode = null      // 原生 Audio 对象

// === 新增：印章与颜色配置 ===
const stampConfig = computed(() => {
  const score = overallScoreValue.value
  if (score >= 90) return { text: '优秀', color: '#67c23a', bg: 'rgba(103, 194, 58, 0.1)', border: 'rgba(103, 194, 58, 0.3)' }
  if (score >= 70) return { text: '良好', color: '#409eff', bg: 'rgba(64, 158, 255, 0.1)', border: 'rgba(64, 158, 255, 0.3)' }
  if (score >= 60) return { text: '合格', color: '#e6a23c', bg: 'rgba(230, 162, 60, 0.1)', border: 'rgba(230, 162, 60, 0.3)' }
  return { text: '不合格', color: '#f56c6c', bg: 'rgba(245, 108, 108, 0.1)', border: 'rgba(245, 108, 108, 0.3)' }
})

// 核心新增：封装一个立刻停止当前播放语音的函数
const stopCurrentAudio = () => {
  if (currentAudioNode) {
    currentAudioNode.pause()
    currentAudioNode.currentTime = 0
    currentAudioNode = null
  }
  playingAudioId.value = null
}

// 优化原有的播放逻辑
const playVoice = (msg) => {
  const isClickingSame = playingAudioId.value === msg.id
  
  stopCurrentAudio() // 无论是换语音还是停止，先停掉当前正在播放的
  
  if (isClickingSame) return // 如果点的是正在播放的这条，停掉就够了，直接返回
  
  currentAudioNode = new Audio(msg.audioUrl)
  playingAudioId.value = msg.id 
  currentAudioNode.play()
  
  currentAudioNode.onended = () => {
    playingAudioId.value = null
  }
}

// === 新增：语音气泡长度计算逻辑 ===
const getVoiceBubbleWidth = (duration) => {
  const d = duration || 1;
  const minWidth = 40;  // 内部最短宽度 (px)
  const maxWidth = 250; // 内部最长宽度 (px) - 加上外层 padding 刚好不超过两个头像中点
  const maxDuration = 60; // 阈值设定：超过 60 秒不再增加长度
  
  const safeDuration = Math.min(d, maxDuration);
  
  // 核心算法：使用平方根 (Math.sqrt) 实现非线性增长。
  // 效果：前段(1-15秒)增长极快，后段(15-60秒)趋于平缓，不会无限膨胀
  const ratio = Math.sqrt(safeDuration / maxDuration);
  const width = minWidth + (maxWidth - minWidth) * ratio;
  
  return `${width}px`;
}

const currentJobName = computed(() => {
  const map = {
    'java_backend': 'Java 后端',
    'python_backend': 'Python 后端',
    'golang_backend': 'Golang 后端',
    'web_frontend': 'Web 前端',
    'devops': 'DevOps',
    'software_test_engineer': '软件测试工程师',
    'system_architect': '系统架构师',
    'data_engineer': '数据工程师',
    'site_reliability_engineer': 'SRE',
    'machine_learning_engineer': '机器学习工程师'
  }
  return map[currentJobId.value] || 'AI'
})

const isUserTurn = computed(() => interviewStore.isLiveKitConnected && !interviewStore.aiIsSpeaking)

const md = new MarkdownIt({
  html: false, linkify: true, typographer: true,
  highlight: function (str, lang) {
    if (lang && hljs.getLanguage(lang)) {
      try { return `<pre class="hljs"><code>${hljs.highlight(str, { language: lang, ignoreIllegals: true }).value}</code></pre>` } catch (__) {}
    }
    return `<pre class="hljs"><code>${md.utils.escapeHtml(str)}</code></pre>`
  }
})
const renderMarkdown = (text) => text ? md.render(text) : ''

// === [新增] 监听 LiveKit 传来的 AI 音频流 ===
// 只要远端 AI 的音频轨道一有数据，立刻把它挂载到页面隐藏的 <audio> 标签上
  watch(() => interviewStore.remoteAudioTrack, (newTrack, oldTrack) => {
  // 如果之前有旧轨道，先解绑
  if (oldTrack) {
    oldTrack.detach() 
  }
  // 如果收到了新轨道，且页面上有 audio 标签，直接绑定播放！
  if (newTrack && remoteAudioRef.value) {
    newTrack.attach(remoteAudioRef.value)
    console.log('🔊 实战联调：真实的 LiveKit 音频已成功挂载！声音应该出来了！')
  }
  }, { immediate: true })

onMounted(() => {
  if (typeof window !== 'undefined') {
    setInitialVideoWindowPosition()
  }
  window.addEventListener('resize', handleResize)
})

const openModal = () => modalRef.value.open()


const handleStart = async (data) => {
  currentJobId.value = data.jobRole
  currentMode.value = data.callType 
  const isTextMode = data.callType === 'text'
  const isCallMode = data.callType === 'audio' || data.callType === 'video'

  // 对话模式：先进入聊天界面等待首条消息，提升体感响应。
  if (isTextMode) {
    showResult.value = false
    isStarted.value = true
    interviewStore.messages.splice(0, interviewStore.messages.length)
    nextTick(() => {
      inputRef.value?.focus()
    })
  }

  // 语音/视频模式：先进入通话界面，再在界面内等待连接完成。
  if (isCallMode) {
    showResult.value = false
    isStarted.value = true
  }

  const startPayload = {
    jobRole: data.jobRole,
    difficulty: data.difficulty,
    mode: data.callType,
    jobInfo: data.jobInfo,
    interviewerStyle: data.interviewerStyle
  }

  console.log('面试参数：', startPayload)

  const success = await interviewStore.initInterview(startPayload)

  if (!success) {
    currentJobId.value = ''
    currentMode.value = ''
    interviewStore.messages.splice(0, interviewStore.messages.length)
    isStarted.value = false
    showResult.value = false
    ElMessage.error('面试创建失败，请检查网络或参数后重试')
    return
  }

  // 开始新面试时，标记报告还未生成
  interviewStore.isReportReady = false
  
  ElMessage.success('面试创建成功！面试已开始')

  // 自动聚焦输入框
  nextTick(() => {
    inputRef.value?.focus()
  })

  if (currentMode.value === 'video') {
    setInitialVideoWindowPosition()
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true })
      videoStream.value = stream
      setTimeout(() => { if (videoRef.value) videoRef.value.srcObject = stream }, 100)
    } catch (error) {
      ElMessage.error('无法访问摄像头，请检查权限设置')
    }
  }
}

const handleEndInterview = () => {
  stopCurrentAudio()

  ElMessageBox.confirm('确定要结束当前面试吗？', '提示', {
    type: 'warning', cancelButtonText: '取消', confirmButtonText: '确定', customClass: 'theme-confirm-box'
  }).then(async () => {
    // 1. 先把硬件和 LiveKit 断开，防止后端卡顿导致麦克风关不掉
    if (videoStream.value) {
      videoStream.value.getTracks().forEach(track => track.stop())
      videoStream.value = null
    }
    if (isRecording.value) cancelRecording()
    
    interviewStore.disconnectLiveKit() // 强制退出房间

    // 2. 再去调后端的结束接口
    try {
      await interviewStore.endSession()
    } catch (error) {
      console.warn("后端结束接口异常，将直接展示空报告界面", error)
    }

    // 3. 强制流转状态到结果页
    isStarted.value = false
    showResult.value = true 
  }).catch(() => {
    // 点击取消不做处理
  })
}

// === 核心修复：更安全、更彻底的强退逻辑 ===
const handleExitWithoutReport = () => {
  stopCurrentAudio()

  ElMessageBox.confirm(
    '退出后将不产生面试记录和报告，确定要离开吗？',
    '警告',
    {
      confirmButtonText: '确定退出',
      cancelButtonText: '取消',
      type: 'warning',
      customClass: 'theme-confirm-box'
    }
  ).then(async () => {
    // 1. 【核心】打上强退标记，阻止 Store 内部的自动轮询逻辑
    interviewStore.isForceQuitting = true

    // 2. 清理本地录音和视频流硬件 (必须最先做，防止隐私泄漏)
    if (isRecording.value) cancelRecording()
    if (videoStream.value) {
      videoStream.value.getTracks().forEach(track => track.stop())
      videoStream.value = null
    }

    // 3. 彻底断开 LiveKit 流媒体房间
    // 这是一个相对较重的操作，我们确保它被调用
    interviewStore.disconnectLiveKit()

    // 4. 尝试通知后端废弃本次面试
    // 我们将这个操作放在最后，且无论它成功与否，都不影响我们清空状态和跳转
    try {
      if (interviewStore.currentInterviewId) {
         // 注意：我们不要去 await 它了！让它在后台默默去发请求。
         // 因为如果 await，一旦网络卡住，用户就会被卡在这个页面无法离开。
        forceFinishInterview(interviewStore.currentInterviewId, { silentError: true }).catch(e => {
            console.warn('后台静默通知后端结束面试失败:', e)
         })
      }
    } catch (error) {
      console.warn('处理后端强制结束请求前发生错误:', error)
    }

    // 5. 彻底清理面试状态，解除页面路由锁定
    // 我们使用 nextTick 确保 DOM 更新后再清空关键状态，防止组件渲染报错
    nextTick(() => {
      inputText.value = ''
      interviewStore.currentInterviewId = null
      interviewStore.isConnected = false
      interviewStore.isReportReady = false
      
      // [使用安全语法清空记录数组]
      interviewStore.messages.splice(0, interviewStore.messages.length)

      isStarted.value = false
      showResult.value = false
      currentMode.value = ''
      
      ElMessage.success('已强制退出当前面试')
      
      // 6. 主动跳转回控制台首页
      router.push('/dashboard')
    })
    
  }).catch(() => {
    // 点击取消不做处理
  })
}

const enterReportView = (reportData) => {
  console.log('[InterviewReport] 后端返回数据:', reportData)
  reportPayload.value = normalizeReportData(reportData)

  if (videoStream.value) {
    videoStream.value.getTracks().forEach(track => track.stop())
    videoStream.value = null
  }

  if (isRecording.value) {
    cancelRecording()
  }

  // 标记报告已生成，允许正常导航
  interviewStore.isReportReady = true
  
  isStarted.value = false
  showResult.value = true
  ElMessage.success('面试报告已生成')
}

// === 文本输入与模式切换逻辑 ===
const handleSendText = async () => {
  stopCurrentAudio() // 发送文字时，立刻停止播放正在听的语音

  const text = inputText.value.trim()
  if (!text || interviewStore.isLoading) return
  inputText.value = ''
  const result = await interviewStore.sendUserMessage(text)

  // 发送消息后自动聚焦输入框
  nextTick(() => {
    inputRef.value?.focus()
  })

  if (result?.reportReady && result?.reportData) {
    enterReportView(result.reportData)
  }
}

const toggleInputMode = () => {
  isVoiceMode.value = !isVoiceMode.value
  if (isRecording.value) cancelRecording()
}

// === 录音相关逻辑 ===
const startRecording = async () => {
  stopCurrentAudio() // 用户点击开始录音时，立刻停止播放正在听的语音

  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
    const mimeType = MediaRecorder.isTypeSupported('audio/webm;codecs=opus')
      ? 'audio/webm;codecs=opus'
      : ''
    mediaRecorder = mimeType ? new MediaRecorder(stream, { mimeType }) : new MediaRecorder(stream)
    audioChunks =[]
    mediaRecorder.ondataavailable = (event) => audioChunks.push(event.data)
    mediaRecorder.start()
    isRecording.value = true
    recordingTime.value = 0
    timerInterval = setInterval(() => recordingTime.value++, 1000)
  } catch (err) {
    ElMessage.error('无法访问麦克风')
  }
}

const stopAndSendRecording = () => {
  if (!mediaRecorder) return
  
  // 核心新增：在停止录音前，立刻捕获当前的秒数（保底为 1 秒）
  const finalDuration = recordingTime.value > 0 ? recordingTime.value : 1;
  
  mediaRecorder.onstop = async () => {
    try {
      const recordedBlob = new Blob(audioChunks, { type: mediaRecorder.mimeType || 'audio/webm' })
      const pcmWavBlob = await convertBlobToPcmWav16kMono(recordedBlob)
      const result = await interviewStore.sendUserVoice(pcmWavBlob, finalDuration)
      
      // 语音发送后自动聚焦输入框
      nextTick(() => {
        inputRef.value?.focus()
      })
      
      if (result?.reportReady && result?.reportData) {
        enterReportView(result.reportData)
      }
    } catch (error) {
      console.error('[VoiceRecord] convert or upload failed:', error)
      ElMessage.error('语音处理失败，请重试')
    }

    cleanupRecording()
  }
  mediaRecorder.stop()
  isRecording.value = false
}

const cancelRecording = () => {
  if (mediaRecorder && mediaRecorder.state !== 'inactive') mediaRecorder.stop()
  isRecording.value = false
  cleanupRecording()
}

const cleanupRecording = () => {
  if (mediaRecorder) mediaRecorder.stream.getTracks().forEach(track => track.stop())
  clearInterval(timerInterval)
  audioChunks =[]
}

// === 视频拖拽逻辑 ===
const isMobileViewport = () => typeof window !== 'undefined' && window.innerWidth <= MOBILE_BREAKPOINT

const getVideoWindowSize = () => (isMobileViewport() ? { width: 160, height: 120 } : { width: 200, height: 150 })

const clampVideoWindowPosition = (x, y) => {
  if (typeof window === 'undefined') return { x, y }
  const { width: videoWidth, height: videoHeight } = getVideoWindowSize()
  const edgePadding = isMobileViewport() ? 12 : 0
  const minX = edgePadding
  const maxX = Math.max(minX, window.innerWidth - videoWidth - edgePadding)
  const minY = isMobileViewport() ? 96 : 0
  const maxY = Math.max(minY, window.innerHeight - videoHeight - edgePadding)

  return {
    x: Math.max(minX, Math.min(x, maxX)),
    y: Math.max(minY, Math.min(y, maxY))
  }
}

const setInitialVideoWindowPosition = () => {
  if (typeof window === 'undefined') return

  const { width: videoWidth, height: videoHeight } = getVideoWindowSize()
  if (isMobileViewport()) {
    const preferredX = 12
    const preferredY = window.innerHeight - videoHeight - 18
    videoWindowPosition.value = clampVideoWindowPosition(preferredX, preferredY)
    return
  }

  // 保持桌面端既有布局，只做边界保护
  videoWindowPosition.value = clampVideoWindowPosition(window.innerWidth - 400, 100)
}

const getPointerPosition = (event) => {
  if (event?.touches?.length) {
    return { x: event.touches[0].clientX, y: event.touches[0].clientY }
  }
  if (event?.changedTouches?.length) {
    return { x: event.changedTouches[0].clientX, y: event.changedTouches[0].clientY }
  }
  if (typeof event?.clientX === 'number' && typeof event?.clientY === 'number') {
    return { x: event.clientX, y: event.clientY }
  }
  return null
}

const startDrag = (event) => {
  const pointer = getPointerPosition(event)
  if (!pointer) return

  isDragging.value = true
  dragStart.value = { x: pointer.x - videoWindowPosition.value.x, y: pointer.y - videoWindowPosition.value.y }
  document.addEventListener('mousemove', onDrag)
  document.addEventListener('touchmove', onDrag, { passive: false })
  document.addEventListener('mouseup', stopDrag)
  document.addEventListener('touchend', stopDrag)
}

const onDrag = (event) => {
  if (isDragging.value) {
    const pointer = getPointerPosition(event)
    if (!pointer) return
    if (event.type === 'touchmove' && event.cancelable) {
      event.preventDefault()
    }

    const newX = pointer.x - dragStart.value.x
    const newY = pointer.y - dragStart.value.y
    videoWindowPosition.value = clampVideoWindowPosition(newX, newY)
  }
}

const stopDrag = () => {
  isDragging.value = false
  document.removeEventListener('mousemove', onDrag)
  document.removeEventListener('touchmove', onDrag)
  document.removeEventListener('mouseup', stopDrag)
  document.removeEventListener('touchend', stopDrag)
}

// === 报告逻辑 ===
const backToStart = () => {
  showResult.value = false
  isStarted.value = false
  currentMode.value = ''
}
const exportToPDF = async () => {
  ElMessage.success('正在生成 PDF...')
  const element = document.getElementById('report-content-export')
  if (!element) return
  const originalScrollTop = element.scrollTop
  
  try {
    isExportingPdf.value = true
    element.scrollTop = 0
    await nextTick()
    updateRadarChart()
    radarChart?.resize()
    
    await html2pdf().set({
      margin: 10,
      filename: `面试报告_${new Date().toISOString().slice(0, 10)}.pdf`,
      image: { type: 'jpeg', quality: 0.98 },
      html2canvas: { scale: 2, useCORS: true, scrollX: 0, scrollY: 0, windowWidth: element.scrollWidth, windowHeight: element.scrollHeight },
      jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' }
    }).from(element).save()
    ElMessage.success('PDF导出成功')
  } catch (error) {
    console.error('导出失败:', error)
    ElMessage.error('导出失败')
  } finally {
    isExportingPdf.value = false
    await nextTick()
    element.scrollTop = originalScrollTop
    updateRadarChart()
    radarChart?.resize()
  }
}

const getChartColors = () => {
  const isLight = themeStore.currentTheme === 'light' || isExportingPdf.value
  return {
    axisLineColor: isLight ? 'rgba(0,0,0,0.1)' : 'rgba(255,255,255,0.05)',
    textColor: isLight ? '#666' : '#a0a0a0',
    splitLineColor: isLight ? 'rgba(0,0,0,0.15)' : 'rgba(255,255,255,0.1)',
    splitAreaColors: isLight ?['rgba(245,247,250,1)', 'rgba(255,255,255,1)'] :['rgba(255,255,255,0.05)', 'rgba(255,255,255,0.02)'],
    tooltipBg: isLight ? '#fff' : 'rgba(50,50,50,0.7)',
    tooltipText: isLight ? '#333' : '#fff',
    radarColor: isLight ? '#409eff' : '#00d2ff',
    radarAreaColor: isLight ? 'rgba(64,158,255,0.4)' : 'rgba(0,210,255,0.4)'
  }
}

const initRadarChart = () => {
  if (radarChartRef.value) {
    nextTick(() => {
      radarChart = echarts.init(radarChartRef.value)
      updateRadarChart()
      radarChart.resize()
    })
  }
}

const updateRadarChart = () => {
  if (!radarChart) return
  const colors = getChartColors()
  const exportMode = isExportingPdf.value
  const indicator = radarDetailItems.value.map((item) => ({
    name: item.radarLabel,
    max: 5
  }))

  radarChart.setOption({
    backgroundColor: 'transparent',
    tooltip: { backgroundColor: colors.tooltipBg, textStyle: { color: colors.tooltipText } },
    radar: {
      indicator,
      splitArea: { areaStyle: { color: colors.splitAreaColors } },
      axisLine: { lineStyle: { color: colors.axisLineColor } },
      splitLine: { lineStyle: { color: colors.splitLineColor } },
      axisName: {
        color: colors.textColor,
        fontSize: exportMode ? 11 : 12,
        formatter: (name) => name.replace('-', '\n')
      },
      center: exportMode ? ['22%', '50%'] : ['50%', '50%'],
      radius: exportMode ? '54%' : '68%'
    },
    series:[{ type: 'radar', animation: !exportMode, data:[{ value: radarValues.value, name: '能力评估', areaStyle: { color: colors.radarAreaColor }, lineStyle: { color: colors.radarColor }, itemStyle: { color: colors.radarColor } }] }]
  })
}

const handleResize = () => {
  radarChart?.resize()
  if (currentMode.value === 'video' && isStarted.value && !showResult.value) {
    videoWindowPosition.value = clampVideoWindowPosition(videoWindowPosition.value.x, videoWindowPosition.value.y)
  }
}

watch(() => interviewStore.messages.length, () => {
  nextTick(() => { if (scrollRef.value) scrollRef.value.scrollTop = scrollRef.value.scrollHeight })
})

watch(() => showResult.value, (newValue) => { if (newValue) { nextTick(() => { initRadarChart() }) } })
watch(() => themeStore.currentTheme, () => { updateRadarChart() })

onUnmounted(() => {
  stopCurrentAudio()

  cleanupRecording()
  if (videoStream.value) videoStream.value.getTracks().forEach(track => track.stop())
  document.removeEventListener('mousemove', onDrag)
  document.removeEventListener('touchmove', onDrag)
  document.removeEventListener('mouseup', stopDrag)
  document.removeEventListener('touchend', stopDrag)
  window.removeEventListener('resize', handleResize)
  radarChart?.dispose()
})
</script>

<style scoped>
.chat-view-container { 
  width: 100%; 
  height: 100%; 
  position: relative; 
  margin: 0; 
  padding: 0; 
  box-sizing: border-box;
}

.empty-state { height: 100%; display: flex; justify-content: center; align-items: center; }
.start-card { background: var(--glass-bg); backdrop-filter: blur(10px); padding: 40px; border-radius: 16px; text-align: center; border: 1px solid var(--glass-border); color: var(--text-color); max-width: 400px; }
.start-icon { color: var(--primary-color); margin-bottom: 20px; }
.start-actions { display: flex; flex-direction: column; gap: 10px; margin-top: 18px; }

/* 聊天模式样式 */
.chat-interface {
  height: calc(100% - 24px);
  margin: 12px;
  display: flex;
  flex-direction: column;
  position: relative;
  overflow: hidden;
  border-radius: 22px;
  border: 1px solid var(--chat-panel-border);
  background:
    var(--chat-panel-overlay),
    var(--glass-bg);
  backdrop-filter: blur(14px) saturate(130%);
  box-shadow: 0 14px 34px rgba(15, 28, 63, 0.22);
}
.chat-header {
  height: 54px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  border-bottom: 1px solid var(--chat-header-divider);
  background: var(--chat-header-bg);
  backdrop-filter: blur(8px);
}
.header-info { display: flex; align-items: center; gap: 8px; color: var(--text-color); font-weight: bold; }
.status-dot { width: 8px; height: 8px; background: #67c23a; border-radius: 50%; }

/* 聊天滚动区，留出底部输入框的高度 */
.chat-scroll-area {
  flex: 1;
  overflow-y: auto;
  padding: 16px 16px 120px 16px;
  scroll-behavior: smooth;
  background: var(--chat-scroll-bg);
}
.chat-scroll-area::-webkit-scrollbar { width: 8px; }
.chat-scroll-area::-webkit-scrollbar-track { background: var(--glass-border); border-radius: 4px; }
.chat-scroll-area::-webkit-scrollbar-thumb { background: var(--text-secondary); border-radius: 4px; }

.messages-list {
  display: flex;
  flex-direction: column;
  gap: 18px;
  max-width: 860px;
  margin: 0 auto;
  padding: 14px;
  border-radius: 18px;
  border: none;
  background: transparent;
  backdrop-filter: none;
}
.system-notice { text-align: center; margin-bottom: 4px; font-size: 12px; color: var(--text-secondary); }
.system-notice span {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 999px;
  background: var(--chat-system-notice-bg);
  border: 1px solid var(--chat-system-notice-border);
}
.message-row { display: flex; gap: 12px; align-items: flex-start; }
.row-right { flex-direction: row-reverse; }
.msg-avatar { flex-shrink: 0; border: 1px solid var(--glass-border); }

.message-bubble { padding: 12px 16px; border-radius: 12px; max-width: 85%; line-height: 1.6; font-size: 14px; position: relative; word-wrap: break-word; overflow: hidden; }
.row-left .message-bubble {
  background: var(--chat-ai-bubble-bg);
  color: var(--chat-ai-bubble-text);
  border-top-left-radius: 2px;
  border: 1px solid var(--chat-ai-bubble-border);
}
.row-right .message-bubble {
  background: linear-gradient(135deg, var(--primary-color), rgba(64, 158, 255, 0.8));
  color: #ffffff;
  border-top-right-radius: 2px;
  box-shadow: 0 8px 20px rgba(40, 96, 170, 0.3);
}

:deep(.markdown-body p) { margin: 0 0 8px 0; }
:deep(.markdown-body p:last-child) { margin: 0; }
:deep(.markdown-body strong) { font-weight: bold; color: var(--chat-ai-strong-color); }
:deep(.markdown-body code) { background: var(--chat-ai-inline-code-bg); padding: 2px 4px; border-radius: 4px; font-family: monospace; font-size: 0.9em; }
:deep(.markdown-body pre) { margin: 10px 0; padding: 12px; border-radius: 8px; background: #282c34; overflow-x: auto; }
:deep(.markdown-body pre code) { background: transparent; padding: 0; color: #abb2bf; }

/* === 底部输入区及语音样式 === */
/* 核心修复：把 fixed 改为 absolute，让它完美贴合在右侧大卡片内部 */
.input-area { 
  padding: 15px; 
  border-top: 1px solid var(--chat-input-border); 
  background: var(--chat-input-bg); 
  backdrop-filter: blur(12px); 
  /* 以下为修改部分 */
  position: absolute; 
  bottom: 0; 
  left: 0; 
  width: 100%; 
  z-index: 100; 
  box-sizing: border-box; /* 保证 padding 不会撑破宽度 */
  border-bottom-left-radius: 0;
  border-bottom-right-radius: 0;
}
.input-wrapper { max-width: 800px; margin: 0 auto; display: flex; gap: 12px; align-items: center; min-height: 42px; }

.mode-switch-btn { width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; background: rgba(255,255,255,0.1); cursor: pointer; color: var(--text-color); transition: all 0.2s; }
.mode-switch-btn:hover { background: var(--primary-color); color: white; }

.flex-input { flex: 1; }
.input-actions { display: flex; align-items: center; gap: 10px; }
.send-btn { height: 36px; }

/* 语音按钮状态 */
.voice-btn-container { flex: 1; height: 38px; cursor: pointer; }
.voice-long-btn { width: 100%; height: 100%; background: var(--glass-bg); border: 1px solid var(--border-color); border-radius: 6px; display: flex; align-items: center; justify-content: center; color: var(--text-color); font-weight: bold; transition: all 0.2s; }
.voice-long-btn:hover { border-color: var(--primary-color); background: rgba(var(--primary-color-rgb), 0.1); }
.record-dot { width: 8px; height: 8px; background: #f56c6c; border-radius: 50%; margin-right: 8px; }

.recording-container { flex: 1; display: flex; justify-content: space-between; align-items: center; padding: 0 10px; }
.recording-visual { display: flex; align-items: center; gap: 5px; color: #f56c6c; font-weight: bold; }
.wave-bar { width: 4px; height: 10px; background: #f56c6c; animation: wave 1s infinite; }
.wave-bar:nth-child(2) { animation-delay: 0.2s; }
.wave-bar:nth-child(3) { animation-delay: 0.4s; }
.recording-actions { display: flex; gap: 10px; }
@keyframes wave { 0%, 100% { height: 10px; } 50% { height: 20px; } }

.typing-bubble { display: flex; gap: 4px; padding: 16px; }
.dot { width: 6px; height: 6px; background: #909399; border-radius: 50%; animation: bounce 1.4s infinite; }
@keyframes bounce { 0%, 100% { transform: scale(0); } 50% { transform: scale(1); } }

/* 通话模式样式 */
.call-interface {
  height: calc(100% - 24px);
  margin: 12px;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  overflow: hidden;
  border-radius: 22px;
  border: 1px solid rgba(255, 255, 255, 0.35);
  background:
    linear-gradient(170deg, rgba(255, 255, 255, 0.26), rgba(255, 255, 255, 0.08)),
    var(--glass-bg);
  backdrop-filter: blur(14px) saturate(130%);
  box-shadow: 0 14px 34px rgba(15, 28, 63, 0.22);
}
.header-actions { position: absolute; top: 16px; right: 16px; z-index: 10; }
.call-center {
  text-align: center;
  padding: 28px 36px;
  border-radius: 20px;
  background: transparent;
  border: none;
  backdrop-filter: none;
  box-shadow: none;
}
.status-text { color: var(--text-color); margin-top: 20px; }
.status-sub { 
  color: var(--text-secondary); 
  transition: color 0.3s; 
}

.status-sub-row {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}
/* [新增] 当大模型说话时，状态文字变成主题色加粗 */
.status-sub.text-active { 
  color: var(--primary-color); 
  font-weight: bold; 
}

.user-speaking-widget {
  margin-top: 12px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.user-speaking-visual {
  width: 56px;
  height: 34px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.idle-dot {
  width: 12px;
  height: 12px;
  border-radius: 999px;
  background: rgba(90, 93, 108, 0.68);
  opacity: 1;
  transition: opacity 0.2s ease;
}

.active-bar {
  display: none;
  width: 12px;
  height: 12px;
  border-radius: 10px;
  background: rgba(90, 93, 108, 0.9);
  transform-origin: center bottom;
}

.user-speaking-visual.is-speaking .idle-dot {
  display: none;
}

.user-speaking-visual.is-speaking .active-bar {
  display: block;
  animation: user-speaking-bars 0.9s infinite ease-in-out;
}

.user-speaking-visual.is-speaking .active-bar:nth-child(4) {
  animation-delay: 0s;
}

.user-speaking-visual.is-speaking .active-bar:nth-child(5) {
  animation-delay: 0.12s;
}

.user-speaking-visual.is-speaking .active-bar:nth-child(6) {
  animation-delay: 0.24s;
}

.user-speaking-hint {
  margin: 2px 0 0;
  font-size: 14px;
  color: rgba(94, 94, 104, 0.88);
  font-weight: 600;
  letter-spacing: 0.02em;
}

.user-speaking-widget--compact {
  margin-top: 6px;
}

.user-speaking-widget--compact .user-speaking-visual {
  width: 44px;
  height: 22px;
  gap: 6px;
}

.user-speaking-widget--compact .idle-dot {
  width: 10px;
  height: 10px;
  opacity: 0.78;
}

.user-speaking-widget--compact .active-bar {
  width: 8px;
}

.user-speaking-widget--inline {
  margin-top: 0;
}

.user-speaking-widget--inline .user-speaking-visual {
  width: 32px;
  height: 16px;
  gap: 4px;
}

.user-speaking-widget--inline .idle-dot {
  width: 7px;
  height: 7px;
  opacity: 0.72;
}

.user-speaking-widget--inline .active-bar {
  width: 4px;
  border-radius: 6px;
  animation: user-speaking-bars-compact 0.85s infinite ease-in-out;
}

.user-speaking-widget--inline .active-bar:nth-child(4) {
  animation-delay: 0s;
}

.user-speaking-widget--inline .active-bar:nth-child(5) {
  animation-delay: 0.1s;
}

.user-speaking-widget--inline .active-bar:nth-child(6) {
  animation-delay: 0.2s;
}

@keyframes user-speaking-bars {
  0%,
  100% {
    height: 12px;
    opacity: 0.85;
  }
  45% {
    height: 28px;
    opacity: 1;
  }
}

@keyframes user-speaking-bars-compact {
  0%,
  100% {
    height: 6px;
    opacity: 0.75;
  }
  45% {
    height: 14px;
    opacity: 1;
  }
}

.avatar-wrapper { position: relative; display: inline-block; }
.wave { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 120px; height: 120px; border-radius: 50%; border: 2px solid var(--primary-color); opacity: 0; }
.wave:nth-child(2) { animation-delay: 0.5s; }
/* 波浪荡漾的动画关键帧 (略微放大了最终尺寸到 280px，效果更明显) */
@keyframes wave-ring { 
  0% { width: 120px; height: 120px; opacity: 0.8; border-width: 3px; } 
  100% { width: 280px; height: 280px; opacity: 0; border-width: 1px; } 
}
.video-window { position: absolute; width: 200px; height: 150px; background: rgba(255, 255, 255, 0.22); border: 1px solid rgba(255, 255, 255, 0.45); border-radius: 10px; overflow: hidden; z-index: 1000; box-shadow: 0 10px 22px rgba(0,0,0,0.22); cursor: move; backdrop-filter: blur(8px); touch-action: none; }
.video-window video { width: 100%; height: 100%; object-fit: cover; }
/* [新增] 当外层有 .ai-speaking 类时（即大模型正在说话），激活波浪动画 */
.ai-speaking .wave {
  animation: wave-ring 1.5s infinite ease-out; 
}
/* 第二个波纹延迟半秒，形成水波荡漾的层次感 */
.ai-speaking .wave:nth-child(2) { 
  animation-delay: 0.5s; 
}

/* 面试结果样式 */
.result-interface {
  height: calc(100% - 24px);
  margin: 12px;
  display: flex;
  flex-direction: column;
  padding: 18px;
  box-sizing: border-box;
  min-height: 0;
  overflow: hidden;
  border-radius: 22px;
  border: 1px solid var(--report-panel-border);
  background:
    var(--report-panel-overlay),
    var(--glass-bg);
  backdrop-filter: blur(14px) saturate(130%);
  box-shadow: 0 14px 34px rgba(15, 28, 63, 0.2);
}
.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 14px;
  padding: 4px 4px 14px 4px;
  border-bottom: 1px solid var(--report-header-divider);
}
.result-header h2 { color: var(--text-color); margin: 0; }
.result-content { 
  flex: 1; 
  min-height: 0;
  display: flex; 
  flex-direction: column; 
  gap: 14px; 
  overflow-y: auto; 
  overflow-x: hidden;
  padding-bottom: 40px !important; /* 核心修复：留出足够的底部空间，不再遮挡 */
  padding-right: 18px;
}.result-content::-webkit-scrollbar { width: 6px; }
.result-content::-webkit-scrollbar-thumb { background: var(--report-scrollbar-thumb); border-radius: 3px; }

/* 仅导出 PDF 时隐藏雷达图周围三项总分卡片，不影响页面正常展示 */
.result-content.pdf-exporting .radar-major-badge {
  display: none;
}

.result-content.pdf-exporting {
  overflow: visible !important;
  padding-right: 0 !important;
  padding-bottom: 0 !important;
}

/* 导出统一白色主题，并使用浅灰卡片提升与纸张背景层次 */
.result-content.pdf-exporting.pdf-export-light {
  color: #2f3742;
}

.result-content.pdf-exporting.pdf-export-light .hero-main,
.result-content.pdf-exporting.pdf-export-light .hero-score,
.result-content.pdf-exporting.pdf-export-light .radar-chart-container,
.result-content.pdf-exporting.pdf-export-light .dimension-breakdown,
.result-content.pdf-exporting.pdf-export-light .evaluation-section,
.result-content.pdf-exporting.pdf-export-light .suggestion-section,
.result-content.pdf-exporting.pdf-export-light .dimension-group {
  background: #f7f7f6 !important;
  border-color: #d4d7dc !important;
  box-shadow: none !important;
}

.result-content.pdf-exporting.pdf-export-light .suggestion-list li {
  background: #f1f2f4 !important;
  border-color: #d4d7dc !important;
}

.result-content.pdf-exporting.pdf-export-light .hero-kicker,
.result-content.pdf-exporting.pdf-export-light .major-label,
.result-content.pdf-exporting.pdf-export-light .metric-head,
.result-content.pdf-exporting.pdf-export-light .evaluation-content p,
.result-content.pdf-exporting.pdf-export-light .suggestion-list {
  color: #616a76 !important;
}

.result-content.pdf-exporting.pdf-export-light :deep(.markdown-body),
.result-content.pdf-exporting.pdf-export-light :deep(.markdown-body p) {
  color: #2f3742 !important;
}

.report-hero {
  display: grid;
  grid-template-columns: 1.5fr 0.8fr;
  gap: 14px;
}

.hero-main,
.hero-score {
  background: var(--report-card-bg);
  border: 1px solid var(--report-card-border);
  border-radius: 16px;
  box-shadow: 0 8px 22px rgba(16, 28, 57, 0.14);
}

.hero-main {
  padding: 20px 22px;
}

.hero-kicker {
  display: inline-flex;
  align-items: center;
  padding: 4px 10px;
  border-radius: 999px;
  font-size: 12px;
  letter-spacing: 0.06em;
  color: #2f6db4;
  background: linear-gradient(135deg, rgba(118, 179, 246, 0.22), rgba(148, 217, 181, 0.22));
  border: 1px solid rgba(80, 145, 228, 0.35);
}

.hero-main h3 {
  margin: 12px 0 10px;
  font-size: 28px;
  line-height: 1;
  color: var(--text-color);
}

.hero-summary {
  color: var(--text-secondary);
  line-height: 1.7;
}

.hero-score {
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 18px;
  text-align: center;
  overflow: hidden;
}

.hero-score::before {
  content: '';
  position: absolute;
  inset: -70% auto auto -20%;
  width: 220px;
  height: 220px;
  background: radial-gradient(circle, rgba(62, 146, 219, 0.2), transparent 70%);
  pointer-events: none;
}

.hero-score-label {
  margin: 0;
  font-size: 22px;
  font-weight: 700;
  color: var(--text-secondary);
}

.hero-score-value {
  margin: 10px 0 4px;
  font-size: 68px;
  font-weight: 800;
  line-height: 1;
}

.hero-score-sub {
  margin: 0;
  font-size: 13px;
  color: var(--text-secondary);
}

.radar-chart-container {
  background: var(--report-card-bg);
  border-radius: 16px;
  padding: 20px;
  border: 1px solid var(--report-card-border);
  box-shadow: 0 8px 22px rgba(16, 28, 57, 0.14);
}
.radar-chart-container h3 { color: var(--text-color); margin: 0 0 20px 0; text-align: center; }
.radar-chart { display: flex; flex-direction: column; align-items: center; gap: 12px; }
.radar-main { width: 100%; padding: 0 24px 44px; box-sizing: border-box; }
.chart-wrapper { position: relative; width: 100%; height: 360px; }
.chart-box { width: 100%; height: 100%; }

.radar-major-badge {
  position: absolute;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 7px 12px;
  border-radius: 12px;
  background: var(--radar-badge-bg);
  border: 1px solid var(--radar-badge-border);
  box-shadow: 0 10px 24px rgba(22, 52, 98, 0.12);
  backdrop-filter: blur(6px);
  min-width: 108px;
  z-index: 2;
}

.radar-major-badge::after {
  content: '';
  position: absolute;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: rgba(64, 158, 255, 0.18);
}

.badge-cognition { left: 18%; top: 18%; }
.badge-cognition::after { right: -18px; top: 50%; transform: translateY(-50%); }

.badge-expression { right: 18%; top: 20%; }
.badge-expression::after { left: -18px; top: 50%; transform: translateY(-50%); }

.badge-professional { left: 50%; transform: translateX(-50%); bottom: -24px; }
.badge-professional::after { left: 50%; top: -18px; transform: translateX(-50%); }

.major-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: linear-gradient(135deg, #5bb3ff, #2d87ec);
  flex: 0 0 auto;
}

.major-meta {
  display: flex;
  align-items: baseline;
  gap: 6px;
}

.major-label { color: var(--text-secondary); font-size: 13px; }
.major-value { color: var(--radar-badge-text); font-size: 17px; font-weight: 800; letter-spacing: 0.01em; }

.interview-duration { display: flex; align-items: center; gap: 8px; color: var(--text-secondary); font-size: 14px; padding: 8px 16px; background: var(--report-duration-bg); border-radius: 10px; border: 1px solid var(--report-duration-border); }

.dimension-breakdown {
  background: var(--report-card-bg);
  border-radius: 16px;
  padding: 20px;
  border: 1px solid var(--report-card-border);
  box-shadow: 0 8px 22px rgba(16, 28, 57, 0.12);
}

.dimension-breakdown h3 {
  color: var(--text-color);
  margin: 0 0 14px;
}

.dimension-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12px;
}

.dimension-group {
  border: 1px solid var(--report-card-border);
  border-radius: 12px;
  padding: 12px;
  background: linear-gradient(145deg, rgba(255, 255, 255, 0.16), rgba(255, 255, 255, 0.06));
}

.dimension-group h4 {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin: 0 0 10px;
  color: var(--text-color);
  font-size: 15px;
}

.dimension-group h4 em {
  font-style: normal;
  color: var(--primary-color);
  font-size: 13px;
  font-weight: 700;
}

.metric-row {
  margin-bottom: 10px;
}

.metric-row:last-child {
  margin-bottom: 0;
}

.metric-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 6px;
  color: var(--text-secondary);
  font-size: 13px;
}

.metric-head strong {
  color: var(--text-color);
}

.metric-track {
  height: 6px;
  background: rgba(90, 122, 173, 0.15);
  border-radius: 999px;
  overflow: hidden;
}

.metric-fill {
  height: 100%;
  border-radius: inherit;
  background: linear-gradient(90deg, #4b89dc, #2fc6a8);
}

/* === 新增：盖章动画 === */
.score-stamp {
  position: absolute;
  top: -15px;
  right: -10px;
  font-size: 18px;
  font-weight: 900;
  border: 3px solid;
  border-radius: 6px;
  padding: 4px 10px;
  letter-spacing: 2px;
  user-select: none;
  pointer-events: none;
  opacity: 0;
  animation: stamp-drop 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
  animation-delay: 0.8s;
}

@keyframes stamp-drop {
  0% { opacity: 0; transform: scale(3) rotate(25deg); }
  50% { opacity: 1; transform: scale(0.9) rotate(25deg); }
  100% { opacity: 1; transform: scale(1) rotate(25deg); }
}

.evaluation-section, .suggestion-section {
  background: var(--report-card-bg);
  border-radius: 16px;
  padding: 20px;
  border: 1px solid var(--report-card-border);
  box-shadow: 0 8px 22px rgba(16, 28, 57, 0.12);
}
.evaluation-section h3, .suggestion-section h3 { color: var(--text-color); margin: 0 0 15px 0; font-size: 18px; }
.evaluation-content p { color: var(--text-secondary); line-height: 1.6; margin: 0 0 10px 0; }
.suggestion-list { color: var(--text-secondary); padding-left: 0; margin: 0; list-style: none; display: grid; gap: 10px; }
.suggestion-list li { line-height: 1.6; border: 1px solid var(--report-card-border); border-radius: 12px; padding: 10px 12px; background: rgba(255, 255, 255, 0.08); }

@media (max-width: 1024px) {
  .report-hero {
    grid-template-columns: 1fr;
  }

  .dimension-grid {
    grid-template-columns: 1fr;
  }

  .chart-wrapper {
    height: 280px;
  }

  .radar-major-badge {
    min-width: 96px;
    padding: 6px 10px;
  }

  .major-value {
    font-size: 15px;
  }

  .radar-main {
    padding: 0 10px 40px;
  }

  .badge-cognition { left: 10%; top: 11%; }
  .badge-expression { right: 10%; top: 11%; }
  .badge-professional { bottom: -18px; }
}

/* === 微信风格语音气泡 === */
.wechat-voice-bubble {
  display: flex;
  align-items: center;
  gap: 4px; /* 核心修复：把原本的 8px 改成 4px，让数字紧贴波纹 */
  cursor: pointer;
  user-select: none;
  min-width: 50px; /* 稍微缩小一点底宽 */
  justify-content: flex-end; 
}

.voice-text {
  font-size: 15px;
  font-weight: bold; /* 加粗一点，视觉效果更好 */
  margin-right: 2px; /* 和波纹保持最完美的距离 */
}

/* 纯 CSS 绘制类似微信的语音播放图标 ( ((• ) */
.voice-icon {
  position: relative;
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
}

.arc {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  border-radius: 50%;
  border: 2px solid transparent;
  /* 边框朝左，因为用户气泡在右边 */
  border-left-color: currentColor; 
}

/* 中心的实心圆点 */
.arc-1 {
  width: 4px; height: 4px; 
  right: 2px; 
  background-color: currentColor; 
  border: none;
}
/* 中间波纹 */
.arc-2 { width: 12px; height: 12px; right: -2px; }
/* 外层波纹 */
.arc-3 { width: 20px; height: 20px; right: -6px; }

/* === 播放时的闪烁动画 === */
.is-playing .arc-3 { animation: voice-play 1.2s infinite; }
.is-playing .arc-2 { animation: voice-play 1.2s infinite 0.2s; }
.is-playing .arc-1 { animation: voice-play 1.2s infinite 0.4s; }

@keyframes voice-play {
  0% { opacity: 0; }
  50% { opacity: 1; }
  100% { opacity: 0; }
}

@media (max-width: 768px) {
  .chat-interface {
    height: 100%;
    margin: 0;
    border-radius: 0;
    border-left: none;
    border-right: none;
    box-shadow: none;
  }

  .chat-scroll-area {
    padding: 12px 10px 116px 10px;
  }

  .messages-list {
    padding: 10px;
    border-radius: 14px;
  }

  .input-area {
    padding: 10px;
  }

  .call-interface {
    height: 100%;
    margin: 0;
    border-radius: 0;
    border-left: none;
    border-right: none;
    box-shadow: none;
  }

  .call-center {
    width: calc(100% - 28px);
    padding: 24px 16px;
  }

  .video-window {
    width: 160px;
    height: 120px;
  }

  .call-interface .status-overlay {
    top: max(12px, env(safe-area-inset-top)) !important;
    left: 12px !important;
    right: 66px !important;
    transform: none !important;
    text-align: left !important;
    padding: 10px 12px !important;
    border-radius: 14px !important;
    border: 1px solid rgba(255, 255, 255, 0.18) !important;
    background: linear-gradient(145deg, rgba(16, 26, 42, 0.74), rgba(23, 37, 58, 0.54)) !important;
    backdrop-filter: blur(10px) saturate(120%) !important;
    box-shadow: 0 10px 22px rgba(0, 0, 0, 0.2);
  }

  .call-interface .status-overlay .status-text {
    margin: 0 !important;
    font-size: 15px !important;
    line-height: 1.35 !important;
    color: rgba(255, 255, 255, 0.95) !important;
  }

  .call-interface .status-overlay .status-sub {
    margin: 6px 0 0 !important;
    font-size: 12px !important;
    line-height: 1.35 !important;
    color: rgba(210, 222, 238, 0.92) !important;
    font-weight: 600 !important;
  }

  .call-interface .status-overlay .status-sub-row {
    gap: 6px;
  }

  .result-interface {
    height: 100%;
    margin: 0;
    border-radius: 0;
    border-left: none;
    border-right: none;
    box-shadow: none;
  }

  .result-header {
    flex-direction: column;
    align-items: stretch;
    gap: 10px;
    margin-bottom: 10px;
    padding: 2px 0 10px;
  }

  .result-header h2 {
    font-size: 24px;
    line-height: 1.2;
  }

  .result-header .header-actions {
    position: static;
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 8px;
    width: 100%;
  }

  .result-header .header-actions :deep(.el-button) {
    width: 100%;
    margin: 0;
    padding: 10px 8px;
    font-size: 15px;
  }

  .result-header .header-actions :deep(.el-button .el-icon) {
    margin-right: 4px !important;
  }

  .call-interface .header-actions {
    position: absolute;
    top: max(12px, env(safe-area-inset-top));
    right: 12px;
    z-index: 20;
    width: auto;
    display: block;
  }

  .call-interface .header-actions :deep(.el-button.is-circle) {
    width: 44px;
    height: 44px;
    margin: 0;
    border: 1px solid rgba(255, 255, 255, 0.55);
    background: linear-gradient(160deg, rgba(244, 98, 116, 0.96), rgba(228, 60, 80, 0.96));
    box-shadow: 0 10px 24px rgba(214, 52, 76, 0.35), 0 2px 6px rgba(0, 0, 0, 0.2);
    color: #fff;
  }

  .call-interface .header-actions :deep(.el-button .el-icon) {
    margin-right: 0 !important;
    font-size: 18px;
  }

  .user-speaking-widget {
    margin-top: 10px;
  }

  .user-speaking-widget--compact {
    margin-top: 6px;
  }

  .user-speaking-widget--inline {
    margin-top: 0;
  }

  .user-speaking-widget--compact .user-speaking-visual {
    width: 40px;
    height: 20px;
    gap: 5px;
  }

  .user-speaking-widget--compact .idle-dot {
    width: 8px;
    height: 8px;
  }

  .user-speaking-widget--compact .active-bar {
    width: 6px;
  }

  .user-speaking-widget--inline .user-speaking-visual {
    width: 28px;
    height: 14px;
    gap: 3px;
  }

  .user-speaking-widget--inline .idle-dot {
    width: 6px;
    height: 6px;
  }

  .user-speaking-widget--inline .active-bar {
    width: 3px;
  }

  .user-speaking-visual {
    width: 50px;
    height: 30px;
    gap: 7px;
  }

  .idle-dot,
  .active-bar {
    width: 10px;
  }

  .user-speaking-hint {
    font-size: 13px;
  }

  .radar-chart-container {
    padding: 14px 10px;
  }

  .radar-main {
    padding: 0 0 4px;
  }

  .chart-wrapper {
    width: 100%;
    max-width: 100%;
    height: 280px;
  }

  .radar-major-badge {
    display: none;
  }

  .radar-data-list {
    position: static;
    margin-top: 8px;
  }
}
</style>