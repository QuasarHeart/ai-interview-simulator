<template>
  <div class="dashboard-container">
    <div class="column left-col">
      
      <!-- 功能宗旨介绍 -->
      <div class="dashboard-card intro-card">
        <div class="intro-content">
          <h2>Hello, {{ username }}! 👋</h2>
          <p class="subtitle">欢迎回到 AI 模拟面试平台</p>
          <div class="mission-box">
            <p><strong>核心宗旨：</strong> 融合多模态 AI 技术，沉浸式面试环境，精准评估技术能力与表达逻辑，助你斩获心仪 Offer。</p>
          </div>
          <el-button type="primary" round class="start-btn" @click="router.push('/interview')">
            立即开始模拟
            <!-- 这里用 Element 的箭头即可，或者你也想换成实心的？暂时保持原样 -->
            <el-icon class="btn-icon"><ArrowRight /></el-icon>
          </el-button>
        </div>
        <!-- 修改点：使用动态绑定的 img src -->
        <img :src="introImage" class="intro-img" alt="illustration" />
      </div>

      <!-- 近期面试记录 -->
      <div class="dashboard-card history-card">
        <div class="card-header">
          <h3>近期面试记录</h3>
          <div class="more-btn" @click="router.push('/history')">
            更多
            <svg class="custom-arrow" viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
              <path d="M4 11H16.17L10.58 5.41L12 4L20 12L12 20L10.59 18.59L16.17 13H4V11Z"/>
            </svg>
          </div>
        </div>
        
        <div class="history-list">
          <div v-for="item in recentHistory" :key="item.id" class="history-item" @click="router.push(`/history/${item.id}`)">
            <!-- 左侧：图标 + 岗位 + 日期/时长 -->
            <div class="item-left">
              <div class="item-icon">
                <el-icon><component :is="getJobIcon(item.job)" /></el-icon>
              </div>
              <div class="item-info">
                <span class="item-title">{{ item.jobInfo || item.job }}</span>
                <div class="item-meta">
                  <span class="meta-text">岗位 {{ item.job }}</span>
                  <span class="meta-divider">|</span>
                  <span class="meta-text"><el-icon><Calendar /></el-icon> {{ item.date }}</span>
                  <span class="meta-divider">|</span>
                  <span class="meta-text"><el-icon><Timer /></el-icon> 耗时 {{ item.duration }}</span>
                </div>
              </div>
            </div>

            <!-- 右侧：面试形式 + 面试状态 + 分数 -->
            <div class="item-right">
              <!-- 面试形式 -->
              <el-tag type="info" class="mode-tag" effect="plain" round>
                {{ getModeText(item.mode) }}
              </el-tag>
              
              <!-- 面试状态 -->
              <el-tag :type="getStatusType(item.interviewStatus)" class="status-tag" effect="light" round>
                {{ getStatusText(item.interviewStatus) }}
              </el-tag>
              
              <!-- 分数 -->
              <div class="score-block">
                <span class="score-val" :class="getScoreClass(item.score)">{{ item.score }}</span>
                <span class="score-unit">分</span>
              </div>
            </div>
          </div>
          
          <!-- 空状态显示 -->
          <el-empty v-if="recentHistory.length === 0" description="没有找到面试记录" />
        </div>
      </div>
    </div>

    <div class="column right-col">
      
      <!-- 3. 用户信息 + 主题切换 -->
      <div class="dashboard-card profile-card">
        <div class="profile-header">
          <div class="profile-info">
            <el-avatar :size="50" :src="avatarUrl" class="user-avatar" />
            <div class="user-text">
              <h3 class="user-name">{{ username }}</h3>
              <p class="user-email">{{ email }}</p>
            </div>
          </div>
          <div class="profile-actions">
            <!-- 核心修改：删除了这里的简历图标，只保留设置图标 -->
            <el-tooltip content="设置" placement="top">
              <div class="action-icon" @click="router.push('/profile')"><el-icon><Setting /></el-icon></div>
            </el-tooltip>
          </div>
        </div>
        <div class="profile-theme">
          <div class="mini-header">快捷风格切换</div>
          <ThemeSwitch />
        </div>
      </div>

      <!-- === 新增：简历状态卡片 === -->
      <div class="dashboard-card resume-mini-card" @click="handleResumeClick">
        <template v-if="hasUploadedResume">
          <div class="resume-content">
            <el-icon class="resume-icon"><Document /></el-icon>
            <div class="resume-text">
              <h4>{{ uploadedResumeFileName }}</h4>
              <p>点击预览当前使用的简历</p>
            </div>
          </div>
        </template>
        <template v-else>
          <div class="resume-content empty">
            <el-icon class="resume-icon"><Warning /></el-icon>
            <div class="resume-text">
              <h4>目前还没上传简历</h4>
              <p>点击跳转至简历界面进行上传</p>
            </div>
          </div>
        </template>
      </div>

      <!-- 统计数据 -->
      <div class="stats-row">
        <!-- 卡片 1 -->
        <div class="dashboard-card stat-box">
          <div class="stat-icon-bg blue"><el-icon><DataLine /></el-icon></div>
          <div class="stat-text">
            <span class="stat-num">{{ interviewCount }}</span>
            <span class="stat-label">完成面试</span>
          </div>
        </div>
        <!-- 卡片 2 -->
        <div class="dashboard-card stat-box">
          <div class="stat-icon-bg green"><el-icon><Trophy /></el-icon></div>
          <div class="stat-text">
            <span class="stat-num">{{ overallScore }}</span>
            <span class="stat-label">综合均分</span>
          </div>
        </div>
        <!-- 卡片 3 (新增) -->
        <div class="dashboard-card stat-box">
          <div class="stat-icon-bg orange"><el-icon><Star /></el-icon></div>
          <div class="stat-text">
            <span class="stat-num">{{ highestScore }}</span>
            <span class="stat-label">最高得分</span>
          </div>
        </div>
        <!-- 卡片 4 (新增) -->
        <div class="dashboard-card stat-box">
          <div class="stat-icon-bg purple"><el-icon><Timer /></el-icon></div>
          <div class="stat-text">
            <span class="stat-num">{{ practiceHours }}</span>
            <span class="stat-label">练习时长(h)</span>
          </div>
        </div>
      </div>

      <!-- 综合能力概览 -->
      <div class="dashboard-card charts-card">
        <div class="card-header">
          <div class="header-left">
            <h3>能力概览</h3>
            <el-select 
              v-model="selectedDirection" 
              size="small" 
              class="direction-select"
              popper-class="dashboard-direction-dropdown"
              @change="handleDirectionChange"
            >
              <el-option label="Web前端" value="web_frontend" />
              <el-option label="Java后端" value="java_backend" />
              <el-option label="Python后端" value="python_backend" />
              <el-option label="Golang后端" value="golang_backend" />
              <el-option label="DevOps" value="devops" />
              <el-option label="软件测试工程师" value="software_test_engineer" />
              <el-option label="系统架构师" value="system_architect" />
              <el-option label="数据工程师" value="data_engineer" />
              <el-option label="SRE" value="site_reliability_engineer" />
              <el-option label="机器学习工程师" value="machine_learning_engineer" />
            </el-select>
          </div>
          <el-button link type="primary" @click="router.push('/assessment')">
            详情 <el-icon><DArrowRight /></el-icon>
          </el-button>
        </div>
        
        <div class="charts-wrapper">
          <div class="chart-block">
            <p class="chart-title">成长趋势</p>
            <div ref="lineChartRef" class="mini-chart"></div>
          </div>
          <div class="chart-block">
            <p class="chart-title">能力模型</p>
            <div ref="radarChartRef" class="mini-chart"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- === 新增：简历预览弹窗 === -->
    <el-dialog v-model="showResumePreview" width="70%" class="theme-adapt-dialog" align-center>
      <template #header>
        <div class="preview-header">
          <span style="font-size: 16px; font-weight: bold; color: var(--text-color);">简历预览 - {{ uploadedResumeFileName }}</span>
          <el-button type="primary" size="small" round @click="goToResumeEdit">去修改</el-button>
        </div>
      </template>
      
      <!-- 预览区域 (模拟后端请求与加载) -->
      <div class="resume-preview-area">
        
        <!-- 状态 1：正在从后端获取 (加载动画) -->
        <div v-if="isLoadingPreview" class="file-preview">
          <el-icon class="is-loading" :size="40" color="#409eff"><Loading /></el-icon>
          <p style="margin-top: 15px; color: var(--text-color);">正在从服务器安全获取简历数据...</p>
        </div>

        <!-- 状态 2：PDF 预览 (获取成功) -->
        <div v-else-if="isPDF && previewUrl" class="pdf-preview">
          <embed :src="previewUrl" type="application/pdf" width="100%" height="100%" />
        </div>

        <!-- 状态 3：Word 预览 (获取成功，显示后端解析的 HTML) -->
        <div v-else-if="!isPDF && previewUrl" class="word-preview">
          <div class="word-content" v-html="previewUrl"></div>
        </div>

        <!-- 状态 4：暂无可预览内容 -->
        <div v-else class="file-preview">
          <el-icon :size="40" color="#e6a23c"><Warning /></el-icon>
          <p style="margin-top: 12px; color: var(--text-color);">当前文件暂不支持预览，请前往简历页重新上传 PDF</p>
        </div>

      </div>
    </el-dialog>

  </div>
</template>

<script setup>
import mammoth from 'mammoth'
import ThemeSwitch from '../../components/ThemeSwitch.vue'
import { ref, onMounted, onUnmounted, watch, computed, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useUserStore } from '../../stores/user'
import { useThemeStore } from '../../stores/theme'
import { getUserProfile, getAvatarDownloadUrl } from '../../api/Profile'
import { getResumeDownloadUrl, fetchResumeBlob } from '../../api/resume'
import { getInterviewHistory } from '../../api/history'
import { getGrowthCurve } from '../../api/assessment'
import { getUserStorage, setUserStorage } from '../../utils/storage'
import { 
  ArrowRight, Platform, Monitor, Cpu, Document, Setting, 
  DataLine, Trophy, DArrowRight, Star, Timer, Warning, Loading, Calendar,
  Management, Check, Grid, DataAnalysis, Connection, PieChart
} from '@element-plus/icons-vue'
import * as echarts from 'echarts'

const router = useRouter()
const userStore = useUserStore()
const themeStore = useThemeStore()

const username = computed(() => userStore.userInfo.username || 'User')
const email = computed(() => userStore.userInfo.email)
const avatarUrl = computed(() => userStore.userInfo.avatar || 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png')

// === 简历状态逻辑 ===
const hasUploadedResume = ref(false)
const uploadedResumeFileName = ref('')
const showResumePreview = ref(false)
// 新增预览相关的状态
const isPDF = ref(false)
const previewUrl = ref('')
const resumeRemoteUrl = ref('')
const previewObjectUrl = ref('')
const isLoadingPreview = ref(false)

// === 核心修复：动态计算图片路径 ===
const introImage = computed(() => {
  const theme = themeStore.currentTheme || 'light'
  // 必须使用 import.meta.url 才能在 Vite 中动态解析路径
  // 注意：这里假设 Dashboard 文件夹在 src/views/dashboard，所以相对路径是 ../../assets/images
  return new URL(`../../assets/images/auth-illustration-${theme}.jpg`, import.meta.url).href
})

const recentHistory = ref([])

const getJobIcon = (job) => {
  if (!job) return Cpu
  const jobStr = String(job).toLowerCase()
  
  // 精确匹配每个职位对应的图标
  if (jobStr.includes('java') && jobStr.includes('backend')) {
    return Platform  // Java 后端
  }
  if (jobStr.includes('python') && (jobStr.includes('backend') || jobStr.includes('后端'))) {
    return Cpu  // Python 后端
  }
  if (jobStr.includes('golang') || jobStr.includes('go')) {
    return Management  // Golang 后端
  }
  if (jobStr.includes('web') || jobStr.includes('frontend')) {
    return Monitor  // Web 前端
  }
  if (jobStr.includes('devops')) {
    return Setting  // DevOps
  }
  if (jobStr.includes('test') || jobStr.includes('软件测试')) {
    return Check  // 软件测试工程师
  }
  if (jobStr.includes('architect') || jobStr.includes('架构')) {
    return Grid  // 系统架构师
  }
  if (jobStr.includes('data') && jobStr.includes('engineer')) {
    return DataAnalysis  // 数据工程师
  }
  if (jobStr.includes('sre') || jobStr.includes('reliability')) {
    return Connection  // SRE
  }
  if (jobStr.includes('machine') || jobStr.includes('learning') || jobStr.includes('ml')) {
    return PieChart  // 机器学习工程师
  }
  
  // 其他后端职位默认用Platform
  if (jobStr.includes('backend') || jobStr.includes('后端')) {
    return Platform
  }
  
  return Cpu
}

// 获取岗位类型的中文名
const getJobTitle = (jobRole) => {
  if (!jobRole) return '未知岗位'
  const normalizedRole = String(jobRole).toLowerCase().trim()

  const roleMap = {
    java_backend: 'Java后端',
    python_backend: 'Python后端',
    golang_backend: 'Golang后端',
    web_frontend: 'Web前端',
    go_backend: 'Go后端',
    cpp_backend: 'C++后端',
    nodejs_backend: 'Node后端',
    ui_design: 'UI设计',
    product_manager: '产品经理',
    algorithm: '算法工程',
    test_engineer: '软件测试',
    software_test_engineer: '软件测试',
    system_architect: '系统架构',
    data_engineer: '数据工程',
    data_analysis: '数据分析',
    devops: 'DevOps',
    machine_learning_engineer: '机器学习',
    site_reliability_engineer: 'SRE'
  }

  return roleMap[normalizedRole] || jobRole
}

// 规范化难度值
const normalizeDifficulty = (difficulty) => {
  if (!difficulty) return 'Normal'
  const lower = String(difficulty).toLowerCase()
  if (lower === 'hard' || lower === '困难') return 'Hard'
  if (lower === 'easy' || lower === '简单') return 'Easy'
  return 'Normal'
}

// 获取面试形式文本
const getModeText = (mode) => {
  if (!mode) return '未知'
  const normalizedMode = String(mode).toLowerCase()
  if (normalizedMode === 'text') return '对话面试'
  if (normalizedMode === 'audio' || normalizedMode === 'voice' || normalizedMode === 'live') return '语音面试'
  if (normalizedMode === 'video') return '视频面试'
  return mode
}

// 获取分数样式类
const getScoreClass = (score) => {
  if (score >= 90) return 'score-high'
  if (score >= 70) return 'score-mid'
  return 'score-low'
}

// 获取面试状态对应的Tag类型
const getStatusType = (status) => {
  if (status === 'REPORTED') return 'success'
  return 'info'
}

// 获取面试状态的显示文本
const getStatusText = (status) => {
  if (status === 'REPORTED') return '已完成'
  return '未完成'
}

// 将秒数转换成可读格式 (如 285 -> "4分45秒")
const formatDuration = (seconds) => {
  if (!seconds || seconds === 0) return '0秒'
  const totalSeconds = Number(seconds)
  const minutes = Math.floor(totalSeconds / 60)
  const secs = totalSeconds % 60
  
  if (minutes === 0) return `${secs}秒`
  if (secs === 0) return `${minutes}分`
  return `${minutes}分${secs}秒`
}

// 格式化日期 (如 "2026年03月30日03:23" -> "2026-03-30")
const formatDate = (dateStr) => {
  if (!dateStr) return '未知'
  // 如果是 ISO 格式或时间戳
  if (typeof dateStr === 'number' || /^\d{4}-\d{2}-\d{2}/.test(dateStr)) {
    const date = new Date(dateStr)
    return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`
  }
  // 如果是 "2026年03月30日03:23" 这样的格式
  const match = dateStr.match(/(\d{4})年(\d{1,2})月(\d{1,2})日/)
  if (match) {
    return `${match[1]}-${String(match[2]).padStart(2, '0')}-${String(match[3]).padStart(2, '0')}`
  }
  return dateStr
}

const fetchRecentInterviews = async () => {
  try {
    const res = await getInterviewHistory()
    console.log('获取面试记录:', res)
    const payload = res?.data ?? res

    let allRecords = []
    if (Array.isArray(payload)) {
      allRecords = payload.map((item) => ({
        id: item?.id ?? item?.interviewId ?? '',
        date: formatDate(item?.startTime ?? item?.date ?? item?.createTime ?? ''),
        job: getJobTitle(item?.jobRole ?? item?.job ?? ''),
        jobInfo: String(item?.jobInfo || '').trim(),
        duration: formatDuration(item?.duration),
        difficulty: normalizeDifficulty(item?.difficulty ?? item?.level ?? 'Normal'),
        score: Number(item?.score ?? 0),
        mode: item?.mode ?? 'text',
        interviewStatus: item?.interviewStatus ?? 'CREATED'
      }))
    } else {
      const list = payload?.records ?? payload?.list ?? payload?.rows ?? []
      if (Array.isArray(list)) {
        allRecords = list.map((item) => ({
          id: item?.id ?? item?.interviewId ?? '',
          date: formatDate(item?.startTime ?? item?.date ?? item?.createTime ?? ''),
          job: getJobTitle(item?.jobRole ?? item?.job ?? ''),
          jobInfo: String(item?.jobInfo || '').trim(),
          duration: formatDuration(item?.duration),
          difficulty: normalizeDifficulty(item?.difficulty ?? item?.level ?? 'Normal'),
          score: Number(item?.score ?? 0),
          mode: item?.mode ?? 'text',
          interviewStatus: item?.interviewStatus ?? 'CREATED'
        }))
      }
    }

    // 只保留最近6条
    recentHistory.value = allRecords.slice(0, 6)
  } catch (error) {
    console.error('获取最近面试记录失败:', error)
    // 静默失败，保持空列表
  }
}

// 获取并处理能力评估数据
const fetchAssessmentData = async () => {
  try {
    // 映射选择的方向到岗位 (后端所需的下划线格式)
    const jobRoleMap = {
      'web_frontend': 'web_frontend',
      'java_backend': 'java_backend',
      'python_backend': 'python_backend',
      'golang_backend': 'golang_backend',
      'devops': 'devops',
      'software_test_engineer': 'software_test_engineer',
      'system_architect': 'system_architect',
      'data_engineer': 'data_engineer',
      'site_reliability_engineer': 'site_reliability_engineer',
      'machine_learning_engineer': 'machine_learning_engineer'
    }
    const jobRole = jobRoleMap[selectedDirection.value] || 'java_backend'
    
    const res = await getGrowthCurve(jobRole)
    console.log('获取能力评估数据:', res)
    const data = res?.data || {}
    
    // 更新统计数据卡片
    overallScore.value = Math.round((data.overallRating || 0) * 10) / 10
    interviewCount.value = data.interviewCount || 0
    highestScore.value = data.bestScore || 0
    practiceHours.value = (data.practiceTime || 0).toFixed(1)
    
    // 处理成长曲线数据 (最后9项用于趋势展示)
    if (Array.isArray(data.growthPoints) && data.growthPoints.length > 0) {
      const firstItem = data.growthPoints[0]
      if (typeof firstItem === 'number') {
        // 直接是数值数组
        lineHistoryScores = data.growthPoints
      } else if (typeof firstItem === 'object' && firstItem.score !== undefined) {
        // 是对象数组，包含 score 属性
        lineHistoryScores = data.growthPoints.map(p => p.score || 0)
      }
    } else {
      // 没有成长数据时不回退静态值，保持空数据
      lineHistoryScores = []
    }
    
    // 处理维度数据用于10维雷达图
    if (data.dimensionDetails) {
      dimensionDetails.value = {
        cognition: {
          logicStructure: data.dimensionDetails.cognition?.logicStructure || 0,
          problemSolving: data.dimensionDetails.cognition?.problemSolving || 0,
          systemThinking: data.dimensionDetails.cognition?.systemThinking || 0
        },
        expression: {
          clarity: data.dimensionDetails.expression?.clarity || 0,
          confidenceStability: data.dimensionDetails.expression?.confidenceStability || 0,
          professionalMaturity: data.dimensionDetails.expression?.professionalMaturity || 0
        },
        professional: {
          technicalCorrectness: data.dimensionDetails.professional?.technicalCorrectness || 0,
          knowledgeMatch: data.dimensionDetails.professional?.knowledgeMatch || 0,
          jobMatch: data.dimensionDetails.professional?.jobMatch || 0,
          engineeringPractice: data.dimensionDetails.professional?.engineeringPractice || 0
        }
      }
    }
    
    // 构建10维雷达数据
    const details = dimensionDetails.value
    radarDimensionValues = [
      (details.cognition.logicStructure || 0),
      (details.cognition.problemSolving || 0),
      (details.cognition.systemThinking || 0),
      (details.expression.clarity || 0),
      (details.expression.confidenceStability || 0),
      (details.expression.professionalMaturity || 0),
      (details.professional.technicalCorrectness || 0),
      (details.professional.knowledgeMatch || 0),
      (details.professional.jobMatch || 0),
      (details.professional.engineeringPractice || 0)
    ]
    
    // 重新初始化图表
    initLineChart()
    initRadarChart()
    nextTick(() => handleResize())
  } catch (error) {
    console.error('获取能力评估数据失败:', error)
    // 失败时不展示静态 mock 数据
    lineHistoryScores = []
    radarDimensionValues = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    initLineChart()
    initRadarChart()
  }
}

const withVersion = (url) => {
  if (!url || typeof url !== 'string') return url

  try {
    const parsed = new URL(url, window.location.origin)
    parsed.searchParams.set('_v', String(Date.now()))
    return parsed.toString()
  } catch {
    return `${url}${url.includes('?') ? '&' : '?'}_v=${Date.now()}`
  }
}

const canLoadAvatar = (url) => {
  if (!url || typeof url !== 'string') return Promise.resolve(false)

  return new Promise((resolve) => {
    const img = new Image()
    const timer = window.setTimeout(() => {
      img.onload = null
      img.onerror = null
      resolve(false)
    }, 5000)

    img.onload = () => {
      window.clearTimeout(timer)
      resolve(true)
    }
    img.onerror = () => {
      window.clearTimeout(timer)
      resolve(false)
    }

    img.src = url
  })
}

const extractNameFromUrl = (url) => {
  if (!url || typeof url !== 'string') return ''

  try {
    const pathname = new URL(url, window.location.origin).pathname
    const parts = pathname.split('/').filter(Boolean)
    return decodeURIComponent(parts[parts.length - 1] || '')
  } catch {
    return ''
  }
}

const cleanupPreviewObjectUrl = () => {
  if (!previewObjectUrl.value) return
  URL.revokeObjectURL(previewObjectUrl.value)
  previewObjectUrl.value = ''
}

const loadUserSummary = async () => {
  try {
    const res = await getUserProfile()
    const payload = res?.data || res || {}
    const rawUser = payload?.user || payload
    const rawAccount = payload?.account || payload

    userStore.updateProfile({
      email: rawAccount?.email || rawUser?.email || userStore.userInfo.email,
      username: rawUser?.nickname || rawUser?.nickName || rawUser?.username || rawUser?.name || userStore.userInfo.username,
      avatar: withVersion(rawUser?.avatar || rawUser?.avatarUrl || userStore.userInfo.avatar),
      bio: rawUser?.description || rawUser?.bio || rawUser?.introduction || rawUser?.profile || userStore.userInfo.bio
    })

    try {
      const avatarAccessUrl = await getAvatarDownloadUrl()
      const safeAvatarUrl = withVersion(avatarAccessUrl)
      if (await canLoadAvatar(safeAvatarUrl)) {
        userStore.updateProfile({ avatar: safeAvatarUrl })
      }
    } catch (avatarErr) {
      console.warn('首页获取头像下载地址失败，已回退到用户资料头像字段', avatarErr)
    }
  } catch (e) {
    console.warn('首页获取用户资料失败', e)
  }
}

const loadResumeSummary = async () => {
  try {
    // 第一步：读取本地缓存，这是判断用户是否上传简历的唯一真实来源
    const stored = JSON.parse(getUserStorage('resumeInfo') || '{}')
    let hasUploadedBeforeCache = false
    
    if (stored?.hasResume) {
      hasUploadedResume.value = true
      uploadedResumeFileName.value = stored.fileName || 'resume.pdf'
      resumeRemoteUrl.value = stored.remoteUrl || ''
      hasUploadedBeforeCache = true // 缓存中明确表示已上传
    } else {
      // 缓存中明确表示未上传，就不再查询API
      hasUploadedResume.value = false
      return
    }
  } catch (e) {
    console.warn('读取简历缓存失败:', e)
    hasUploadedResume.value = false
    return
  }

  // 第二步：仅在缓存表示已上传时，才获取远程URL更新
  try {
    const remoteDownloadUrl = await getResumeDownloadUrl()
    if (!remoteDownloadUrl) {
      // 如果API没有返回URL，保持缓存中的状态
      return
    }

    resumeRemoteUrl.value = withVersion(remoteDownloadUrl)

    // 记录缓存中的文件名，用于判断是否需要从URL覆盖
    const oldInfo = JSON.parse(getUserStorage('resumeInfo') || '{}')
    const cachedFileName = oldInfo?.fileName
    
    // 仅在缓存中没有有效文件名时，才从URL中提取文件名
    if (!cachedFileName || cachedFileName === 'resume.pdf') {
      const name = extractNameFromUrl(remoteDownloadUrl)
      if (name && (!uploadedResumeFileName.value || uploadedResumeFileName.value === 'resume.pdf')) {
        uploadedResumeFileName.value = name
      }
    }

    // 更新缓存，但保留缓存中有效的文件名
    setUserStorage('resumeInfo', JSON.stringify({
      ...oldInfo,
      hasResume: true,
      fileName: uploadedResumeFileName.value || oldInfo.fileName || 'resume.pdf',
      remoteUrl: resumeRemoteUrl.value
    }))
  } catch (e) {
    console.warn('首页获取简历信息失败，使用本地缓存:', e)
    // 出错时保持缓存中的状态
  }
}

// 统计数据 - 来自后端 API
const overallScore = ref(0)
const interviewCount = ref(0)
const highestScore = ref(0)
const practiceHours = ref(0)

// 维度数据 - 用于10维雷达图
const dimensionDetails = ref({
  cognition: {
    logicStructure: 0,
    problemSolving: 0,
    systemThinking: 0
  },
  expression: {
    clarity: 0,
    confidenceStability: 0,
    professionalMaturity: 0
  },
  professional: {
    technicalCorrectness: 0,
    knowledgeMatch: 0,
    jobMatch: 0,
    engineeringPractice: 0
  }
})

// 10维雷达图标签和数据
const radarDetailLabels = [
  '逻辑结构', '问题拆解', '系统思维',
  '表达清晰', '自信稳定', '职业成熟',
  '技术准确', '知识匹配', '岗位匹配', '工程实践'
]
let radarDimensionValues = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

// 图表逻辑保持不变，为节省篇幅略去部分细节，确保复制时包含之前的 ECharts 代码
const selectedDirection = ref('java_backend')
const lineChartRef = ref(null)
const radarChartRef = ref(null)
let lineChart = null
let radarChart = null
let chartResizeObserver = null
let lineHistoryScores = []

const getRecentFiveTrend = (scores) => {
  const recent = scores.slice(-5)
  const labels = recent.map((_, i) => (i === recent.length - 1 ? '最近' : String(i + 1)))
  return { labels, recent }
}

const getChartColors = () => {
  const isLight = themeStore.currentTheme === 'light'
  return {
    lineColor: isLight ? '#409eff' : '#00d2ff',
    areaColor: isLight ? 'rgba(64, 158, 255, 0.2)' : 'rgba(0, 210, 255, 0.2)',
    textColor: isLight ? '#999' : '#888',
    splitLine: isLight ? 'rgba(0,0,0,0.05)' : 'rgba(255,255,255,0.05)',
    radarArea: isLight ? 'rgba(64, 158, 255, 0.4)' : 'rgba(0, 210, 255, 0.4)',
    tooltipBg: isLight ? '#ffffff' : 'rgba(11, 34, 64, 0.95)',
    tooltipText: isLight ? '#303133' : '#e6f7ff',
    tooltipBorder: isLight ? '#e2e8f0' : 'rgba(24, 144, 255, 0.35)'
  }
}

const initLineChart = () => {
  if (!lineChartRef.value) return
  if (lineChart) lineChart.dispose()
  lineChart = echarts.init(lineChartRef.value)
  const c = getChartColors()
  const { labels, recent } = getRecentFiveTrend(lineHistoryScores)
  lineChart.setOption({
    backgroundColor: 'transparent',
    grid: { top: 10, right: 10, bottom: 0, left: 0, containLabel: true },
    tooltip: {
      trigger: 'axis',
      backgroundColor: c.tooltipBg,
      borderColor: c.tooltipBorder,
      textStyle: { color: c.tooltipText }
    },
    xAxis: { type: 'category', data: labels, axisLine: { show: false }, axisTick: { show: false }, axisLabel: { color: c.textColor, fontSize: 10 } },
    yAxis: { type: 'value', splitLine: { lineStyle: { color: c.splitLine } }, axisLabel: { show: false } },
    series: [{ data: recent, type: 'line', smooth: true, symbol: 'none', lineStyle: { width: 2, color: c.lineColor }, areaStyle: { color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{ offset: 0, color: c.areaColor }, { offset: 1, color: 'rgba(0,0,0,0)' }]) } }]
  })
}

const initRadarChart = () => {
  if (!radarChartRef.value) return
  if (radarChart) radarChart.dispose()
  radarChart = echarts.init(radarChartRef.value)
  const c = getChartColors()
  
  // 构建10维指标
  const indicator = radarDetailLabels.map((label) => ({
    name: label,
    max: 5
  }))
  
  radarChart.setOption({
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'item',
      backgroundColor: c.tooltipBg,
      borderColor: c.tooltipBorder,
      textStyle: { color: c.tooltipText },
      z: 1000,
      confine: false,
      formatter: (params) => {
        if (!params || !params.value) return ''
        const values = params.value
        const radarName = params.name || '能力评分'
        let html = `<div style="font-weight: bold; margin-bottom: 6px;">${radarName}</div>`
        radarDetailLabels.forEach((label, idx) => {
          const val = values[idx] !== undefined ? Number(values[idx]).toFixed(1) : '0'
          html += `<div style="margin: 2px 0;">• ${label}: <strong>${val}</strong></div>`
        })
        return html
      }
    },
    radar: { 
      indicator,
      center: ['50%', '50%'],
      radius: '62%',
      splitNumber: 5, 
      splitArea: { show: false }, 
      axisLine: { lineStyle: { color: c.splitLine } }, 
      splitLine: { lineStyle: { color: c.splitLine } }, 
      axisName: { 
        color: c.textColor, 
        fontSize: 9,
        formatter: (name) => name.replace('-', '\n')
      } 
    },
    series: [{ 
      type: 'radar', 
      data: [{ 
        value: radarDimensionValues, 
        name: '能力评分',
        areaStyle: { color: c.radarArea },
        lineStyle: { color: c.lineColor, width: 2 },
        itemStyle: { color: c.lineColor },
        symbolSize: 4
      }] 
    }]
  })
}

const handleDirectionChange = () => {
  // 选择方向改变时，重新获取该岗位的能力评估数据
  fetchAssessmentData()
}

const handleResize = () => {
  lineChart?.resize()
  radarChart?.resize()

  // 容器尺寸动画/断点切换后再补一次，避免折线图偶发丢失
  setTimeout(() => {
    if (!lineChart || !lineChartRef.value) return
    const width = lineChartRef.value.clientWidth
    const height = lineChartRef.value.clientHeight
    if (width < 40 || height < 40) {
      initLineChart()
      return
    }
    lineChart.resize()
  }, 80)
}

const setupChartResizeObserver = () => {
  if (typeof ResizeObserver === 'undefined') return

  chartResizeObserver?.disconnect()
  chartResizeObserver = new ResizeObserver(() => {
    handleResize()
  })

  if (lineChartRef.value?.parentElement) {
    chartResizeObserver.observe(lineChartRef.value.parentElement)
  }
  if (radarChartRef.value?.parentElement) {
    chartResizeObserver.observe(radarChartRef.value.parentElement)
  }
}

const loadResumePreview = async () => {
  cleanupPreviewObjectUrl()
  isLoadingPreview.value = true
  previewUrl.value = ''

  try {
    let targetUrl = resumeRemoteUrl.value
    if (!targetUrl) {
      const stored = JSON.parse(localStorage.getItem('resumeInfo') || '{}')
      targetUrl = stored?.remoteUrl || ''
      if (targetUrl) {
        resumeRemoteUrl.value = withVersion(targetUrl)
        targetUrl = resumeRemoteUrl.value
      }
    }

    if (!targetUrl) {
      throw new Error('未找到可预览的简历地址，请先前往简历页上传')
    }

    const blob = await fetchResumeBlob(targetUrl)
    const fileName = (uploadedResumeFileName.value || '').toLowerCase()
    const blobType = (blob?.type || '').toLowerCase()
    const isPdfFile = fileName.endsWith('.pdf') || blobType.includes('pdf')
    const isWordFile = fileName.endsWith('.doc') || fileName.endsWith('.docx') || blobType.includes('word') || blobType.includes('officedocument')

    if (isPdfFile) {
      isPDF.value = true
      previewObjectUrl.value = URL.createObjectURL(blob)
      previewUrl.value = `${previewObjectUrl.value}#toolbar=0&navpanes=0`
      return
    }

    if (isWordFile) {
      isPDF.value = false
      const arrayBuffer = await blob.arrayBuffer()
      const result = await mammoth.convertToHtml({ arrayBuffer })
      previewUrl.value = result.value || '<p>文档内容为空</p>'
      return
    }

    isPDF.value = false
    ElMessage.warning('当前文件类型暂不支持预览')
  } catch (e) {
    isPDF.value = false
    previewUrl.value = ''
    ElMessage.error(e?.message || '简历预览失败，请稍后重试')
  } finally {
    isLoadingPreview.value = false
  }
}

const handleResumeClick = async () => {
  if (!hasUploadedResume.value) {
    router.push('/resume')
    return
  }

  showResumePreview.value = true
  await loadResumePreview()
}

const goToResumeEdit = () => {
  showResumePreview.value = false
  router.push('/resume')
}

onMounted(async () => {
  window.addEventListener('resize', handleResize)

  await loadUserSummary()
  await loadResumeSummary()
  await fetchRecentInterviews()
  // 获取能力评估数据并初始化图表
  await fetchAssessmentData()
  
  nextTick(() => {
    setupChartResizeObserver()
    handleResize()
  })
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  chartResizeObserver?.disconnect()
  chartResizeObserver = null
  lineChart?.dispose(); radarChart?.dispose()
})

watch(() => themeStore.currentTheme, () => {
  initLineChart()
  initRadarChart()
  nextTick(() => handleResize())
})
// 弹窗关闭时清理 URL
watch(showResumePreview, (newVal) => {
  if (!newVal) {
    cleanupPreviewObjectUrl()
    previewUrl.value = ''
  }
})
</script>

<style scoped>
.dashboard-container { height: 100%; padding: 30px; display: flex; gap: 25px; box-sizing: border-box; overflow: hidden; min-width: 0; }
.dashboard-container {
  scrollbar-width: thin;
  scrollbar-color: var(--page-scrollbar-thumb, var(--report-scrollbar-thumb)) var(--page-scrollbar-track, transparent);
}

.dashboard-container::-webkit-scrollbar {
  width: 10px;
}

.dashboard-container::-webkit-scrollbar-track {
  background: var(--page-scrollbar-track, rgba(0, 0, 0, 0.1));
  border-radius: 999px;
}

.dashboard-container::-webkit-scrollbar-thumb {
  background: var(--page-scrollbar-thumb, var(--report-scrollbar-thumb));
  border-radius: 999px;
  border: 2px solid transparent;
  background-clip: padding-box;
}

.dashboard-container::-webkit-scrollbar-thumb:hover {
  background: color-mix(in srgb, var(--page-scrollbar-thumb, var(--report-scrollbar-thumb)) 82%, var(--primary-color) 18%);
  border: 2px solid transparent;
  background-clip: padding-box;
}
.column { display: flex; flex-direction: column; gap: 25px; }
.left-col { flex: 4; display: flex; flex-direction: column; min-width: 0; min-height: 0; } 
.right-col { flex: 3; display: flex; flex-direction: column; min-width: 0; min-height: 0; }

/* 确保双列布局下左右两列高度一致 */
.dashboard-container {
  display: flex;
  align-items: stretch;
}

/* 确保历史记录卡片和图表卡片都能填充剩余空间 */
.history-card, .charts-card {
  flex: 1;
  min-height: 0;
}

.dashboard-card { background: var(--glass-bg); border: 1px solid var(--glass-border); border-radius: 24px; padding: 25px; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.05); backdrop-filter: blur(10px); color: var(--text-color); transition: transform 0.3s; }
.dashboard-card:hover { transform: translateY(-2px); border-color: var(--primary-color); }

.intro-card { flex: 0 0 auto; display: flex; justify-content: space-between; align-items: center; background: linear-gradient(135deg, var(--glass-bg) 0%, rgba(var(--primary-color-rgb), 0.1) 100%); position: relative; overflow: hidden; }
.intro-content { z-index: 2; flex: 1; }
.intro-content h2 { margin: 0 0 5px 0; font-size: 26px; }
.subtitle { color: var(--text-secondary); margin: 0 0 15px 0; font-size: 14px; }
.mission-box { background: rgba(0,0,0,0.05); padding: 12px; border-radius: 12px; margin-bottom: 15px; font-size: 13px; line-height: 1.5; color: var(--text-color); max-width: 90%; }
.start-btn { padding: 18px 25px; font-weight: bold; }
.intro-img { width: 180px; opacity: 0.8; mask-image: linear-gradient(to left, black 60%, transparent 100%); -webkit-mask-image: linear-gradient(to left, black 60%, transparent 100%); }

.history-card { flex: 1; display: flex; flex-direction: column; overflow: hidden; }
.card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; }
.card-header h3 { margin: 0; font-size: 18px; }
.more-btn { display: flex; align-items: center; gap: 5px; cursor: pointer; color: var(--text-secondary); font-size: 13px; font-weight: bold; transition: color 0.2s; }
.more-btn:hover { color: var(--primary-color); }
.custom-arrow { width: 14px; height: 14px; }

.history-list {
  flex: 1;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding-right: 10px;
  padding-top: 10px;
}

.history-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 6px 20px;
  background: rgba(128, 128, 128, 0.05);
  border: 1px solid rgba(140, 140, 140, 0.3);
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.history-item:hover {
  background: rgba(128, 128, 128, 0.1);
  border-color: var(--primary-color);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

/* 左侧内容 */
.item-left {
  display: flex;
  align-items: center;
  gap: 15px;
}

.item-icon {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  color: white;
  background: linear-gradient(135deg, #409eff, #2873cc);
}

.item-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.item-title {
  font-weight: bold;
  font-size: 15px;
  color: var(--text-color);
}

.item-meta {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 11px;
  color: var(--text-secondary);
}

.meta-text { display: flex; align-items: center; gap: 4px; }
.meta-divider { color: rgba(140, 140, 140, 0.3); }

/* 右侧内容 */
.item-right {
  display: flex;
  align-items: center;
  gap: 15px;
}

.mode-tag { width: 70px; text-align: center; font-weight: normal; font-size: 12px; }

.status-tag { width: 80px; text-align: center; font-weight: normal; font-size: 12px; }

.score-block { text-align: right; width: 70px; }

.score-val {
  font-size: 22px;
  font-weight: 900;
  margin-right: 4px;
}
.score-high { color: #67c23a; }
.score-mid { color: #e6a23c; }
.score-low { color: #f56c6c; }
.score-unit { font-size: 13px; color: var(--text-secondary); }

/* 滚动条美化 */
.history-list::-webkit-scrollbar { width: 6px; }
.history-list::-webkit-scrollbar-track { background: transparent; }
.history-list::-webkit-scrollbar-thumb { background: var(--glass-border); border-radius: 3px; }
.history-list::-webkit-scrollbar-thumb:hover { background: var(--primary-color); }
.score-unit { font-size: 12px; color: var(--text-secondary); }

/* 修改 .profile-card 及其内部样式 */
.profile-card { 
  flex: 0 0 auto; 
  display: flex; 
  flex-direction: column; /* 改为纵向排列 */
  gap: 20px; /* 头像区和主题区的间距 */
  padding: 20px; 
}
.profile-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}
.profile-info { display: flex; align-items: center; gap: 15px; }
.user-avatar { border: 2px solid var(--glass-border); }
.user-name { margin: 0; font-size: 18px; }
.user-email { margin: 2px 0 0 0; color: var(--text-secondary); font-size: 12px; }
.profile-actions { display: flex; gap: 8px; }
.action-icon { width: 36px; height: 36px; border-radius: 50%; background: rgba(0,0,0,0.05); display: flex; align-items: center; justify-content: center; cursor: pointer; transition: all 0.2s; color: var(--text-color); }
.action-icon:hover { background: var(--primary-color); color: white; }
/* 内部主题区 */
.profile-theme { width: 100%; }
.mini-header { font-size: 12px; color: var(--text-secondary); margin-bottom: 10px; font-weight: bold; }

/* 统计数据 2x2 网格布局 */
.stats-row { 
  flex: 0 0 auto; 
  display: grid; 
  grid-template-columns: 1fr 1fr; 
  grid-template-rows: 1fr 1fr; /* 强制两行 */
  gap: 15px; /* 稍微缩小间距让排版更紧凑 */
}
.stat-box { display: flex; align-items: center; gap: 15px; padding: 15px 20px; }
.stat-icon-bg { width: 44px; height: 44px; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 20px; color: white; }
.stat-icon-bg.blue { background: linear-gradient(135deg, #409eff, #3a8ee6); }
.stat-icon-bg.green { background: linear-gradient(135deg, #67c23a, #529b2e); }
/* 新增的两个颜色 */
.stat-icon-bg.orange { background: linear-gradient(135deg, #e6a23c, #d38c2a); }
.stat-icon-bg.purple { background: linear-gradient(135deg, #9c27b0, #7b1fa2); }

.stat-text { display: flex; flex-direction: column; }
.stat-num { font-size: 24px; font-weight: 900; line-height: 1; margin-bottom: 4px; }
.stat-label { font-size: 12px; color: var(--text-secondary); }

.charts-card { flex: 1; display: flex; flex-direction: column; min-height: 0; }
.header-left { display: flex; align-items: center; gap: 10px; }
.charts-wrapper { flex: 1; display: flex; gap: 10px; margin-top: 10px; min-height: 0; }
.chart-block { flex: 1; display: flex; flex-direction: column; background: rgba(0,0,0,0.03); border-radius: 12px; padding: 10px; min-height: 0; min-width: 0; }
.chart-title { margin: 0 0 5px 0; font-size: 12px; color: var(--text-secondary); text-align: center; }
.mini-chart {
  flex: 1;
  width: 100%;
  min-height: 0;
  height: clamp(160px, 22vh, 220px);
}

.direction-select { width: 100px; }
:deep(.direction-select .el-select__wrapper) {
  background: var(--input-bg) !important;
  box-shadow: none !important;
  border: 1px solid var(--input-border-color, var(--glass-border)) !important;
}
:deep(.direction-select .el-select__selected-item) {
  color: var(--text-color) !important;
  font-size: 12px;
}
:deep(.direction-select .el-select__placeholder) {
  color: var(--text-secondary) !important;
  font-size: 12px;
}
:deep(.direction-select .el-select__caret) {
  color: var(--text-secondary) !important;
}
:deep(.theme-adapt-dialog) {
  background: var(--card-bg) !important;
  border: 1px solid var(--sidebar-border);
}
:deep(.theme-adapt-dialog .el-dialog__title) {
  color: var(--text-color);
}

@media (max-width: 1000px) {
  .dashboard-container { flex-direction: column; overflow-y: auto; overflow-x: hidden; padding: 20px; gap: 18px; }
  .left-col, .right-col { flex: none; height: auto; }
  .left-col { display: contents; }
  .intro-card { order: 1; }
  .right-col { order: 2; }
  .history-card { order: 3; }
  .history-card { flex: none; }
  .history-list { max-height: 320px; }
  .dashboard-card { padding: 18px; border-radius: 18px; }
  .intro-card { align-items: flex-start; gap: 12px; }
  .intro-content h2 { font-size: 22px; }
  .mission-box { max-width: 100%; }
  .intro-img { width: 140px; align-self: flex-end; }
  .stats-row { grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px; }
  .stat-box { padding: 12px 14px; }
  .stat-num { font-size: 20px; }
  .charts-wrapper { flex-direction: column; gap: 12px; }
  .chart-block { min-height: 250px; }
  .mini-chart { min-height: 220px; }
  
  /* 确保近期面试记录与右列整体高度一致 */
  .right-col {
    min-height: 420px;
  }
  .history-card {
    min-height: 420px;
  }
}

@media (max-width: 760px) {
  .dashboard-container { padding: 14px; gap: 14px; }
  .column { gap: 14px; }
  .dashboard-card { padding: 14px; border-radius: 14px; }
  .profile-header { align-items: flex-start; gap: 10px; }
  .profile-info { min-width: 0; }
  .user-avatar {
    flex: 0 0 50px;
    width: 50px !important;
    height: 50px !important;
    min-width: 50px;
    min-height: 50px;
    border-radius: 50%;
    overflow: hidden;
  }
  .user-avatar :deep(img) {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
  .user-text { min-width: 0; }
  .user-name, .user-email {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  .resume-mini-card { padding: 12px 14px; }
  .resume-icon { font-size: 28px; }
  .resume-text h4 { font-size: 14px; }
  .stats-row { grid-template-columns: 1fr; }
  .header-left { width: 100%; justify-content: space-between; }
  .card-header {
    flex-wrap: wrap;
    gap: 8px;
    align-items: flex-start;
  }
  .direction-select { width: 96px; }
  .chart-block { min-height: 240px; }
  .mini-chart { min-height: 200px; }
}

@media (max-width: 560px) {
  .dashboard-container {
    padding: 10px;
    gap: 10px;
  }

  .column {
    gap: 10px;
  }

  .dashboard-card {
    padding: 12px;
    border-radius: 12px;
  }

  .intro-card {
    align-items: flex-start;
    gap: 8px;
  }

  .intro-content h2 {
    font-size: 16px;
    margin-bottom: 2px;
  }

  .subtitle {
    font-size: 12px;
    margin-bottom: 10px;
  }

  .mission-box {
    font-size: 12px;
    line-height: 1.45;
    padding: 10px;
    margin-bottom: 10px;
  }

  .start-btn {
    width: 100%;
    padding: 12px 14px;
  }

  .intro-img {
    display: none;
  }

  .card-header h3 {
    font-size: 16px;
  }

  .history-list {
    max-height: none;
    padding-right: 2px;
  }

  .history-item {
    flex-direction: column;
    align-items: stretch;
    gap: 8px;
    padding: 10px 12px;
  }

  .item-left {
    align-items: flex-start;
    gap: 10px;
  }

  .item-info {
    min-width: 0;
  }

  .item-title {
    font-size: 14px;
    line-height: 1.3;
    word-break: break-word;
  }

  .item-meta {
    display: grid;
    grid-template-columns: 1fr;
    gap: 4px;
    font-size: 11px;
  }

  .meta-divider {
    display: none;
  }

  .item-right {
    width: 100%;
    display: grid;
    grid-template-columns: auto auto 1fr;
    gap: 8px;
    align-items: center;
  }

  .mode-tag,
  .status-tag {
    width: auto;
  }

  .score-block {
    width: auto;
    text-align: right;
  }

  .score-val {
    font-size: 18px;
  }

  .profile-card {
    gap: 12px;
    padding: 12px;
  }

  .profile-info {
    gap: 10px;
  }

  .user-avatar {
    flex: 0 0 44px;
    width: 44px !important;
    height: 44px !important;
    min-width: 44px;
    min-height: 44px;
  }

  .user-name {
    font-size: 16px;
  }

  .user-email {
    max-width: 120px;
  }

  .resume-mini-card {
    padding: 10px 12px;
  }

  .resume-content {
    gap: 10px;
  }

  .resume-icon {
    font-size: 28px;
  }

  .resume-text h4 {
    font-size: 13px;
  }

  .resume-text p {
    font-size: 11px;
  }

  .stat-box {
    padding: 10px 12px;
    gap: 10px;
  }

  .stat-icon-bg {
    width: 36px;
    height: 36px;
    font-size: 16px;
  }

  .stat-num {
    font-size: 18px;
  }

  .stat-label {
    font-size: 11px;
  }

  .header-left {
    gap: 8px;
    align-items: center;
  }

  .direction-select {
    width: 84px;
  }

  .chart-block {
    min-height: 190px;
    padding: 8px;
  }

  .mini-chart {
    min-height: 160px;
    height: 170px;
  }
}

@media (max-height: 860px) {
  .dashboard-container {
    overflow-y: auto;
    overflow-x: hidden;
    padding: 20px;
    gap: 18px;
  }
  .column { gap: 18px; }
  .dashboard-card { padding: 18px; }
  .history-list { max-height: 260px; }
  .history-card, .charts-card { min-height: 0; }
  .chart-block { min-height: 220px; }
  .mini-chart { min-height: 190px; }
}

/* 强制所有仪表盘内部卡片使用不透明实心背景 */
.dashboard-card { 
  background: var(--card-bg); /* 改为实心 */
  border: 1px solid var(--sidebar-border); /* 使用专属边框 */
  border-radius: 24px; padding: 25px; 
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05); 
  color: var(--text-color); transition: transform 0.3s; 
}

/* === 简历小卡片 === */
.resume-mini-card {
  padding: 15px 25px;
  cursor: pointer;
  display: flex;
  align-items: center;
}
.resume-content {
  display: flex;
  align-items: center;
  gap: 15px;
  width: 100%;
}
.resume-icon {
  font-size: 36px;
  color: var(--primary-color);
}
.resume-content.empty .resume-icon {
  color: #e6a23c; /* 未上传时显示警告黄 */
}
.resume-text h4 {
  margin: 0 0 4px 0;
  font-size: 15px;
}
.resume-text p {
  margin: 0;
  font-size: 12px;
  color: var(--text-secondary);
}
.resume-preview-area {
  height: 60vh; /* 固定高度 */
  background: var(--input-bg);
  border-radius: 8px;
  overflow: hidden;
  border: 1px dashed var(--glass-border);
  display: flex;
  flex-direction: column;
}
/* === 弹窗预览区 === */
.preview-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-right: 25px; 
}
.mock-preview-area {
  height: 350px;
  background: var(--input-bg);
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  border: 1px dashed var(--glass-border);
}
.mock-tip {
  font-size: 12px;
  color: var(--text-secondary);
  margin-top: 8px;
}

.pdf-preview { width: 100%; height: 100%; }
.word-preview { width: 100%; height: 100%; overflow-y: auto; background: #fff; color: #333; padding: 20px; }
.file-preview { flex: 1; display: flex; flex-direction: column; justify-content: center; align-items: center; gap: 15px; color: var(--text-secondary); }

/* 放在样式尾部，确保覆盖后续统一卡片规则 */
@media (max-width: 1000px) {
  .dashboard-card { padding: 18px; border-radius: 18px; }
}

@media (max-width: 760px) {
  .dashboard-card { padding: 14px; border-radius: 14px; }
}

@media (max-height: 860px) {
  .dashboard-card { padding: 18px; }
}

/* 双列时，高度高于 1000px - 保持原始尺寸 */
@media (min-width: 1001px) and (max-height: 1000px) {
  /* 轻微过渡，仅调整间距 */
  .dashboard-container .stats-row { gap: 12px; }
  .dashboard-container .profile-card { padding: 14px 20px; }
  .dashboard-container .resume-mini-card { padding: 12px 20px; }
}

/* 双列时，高度在 920-1000px 之间 - 中等压缩 */
@media (min-width: 1001px) and (max-height: 920px) {
  .dashboard-container .profile-card { padding: 12px 18px; }
  .dashboard-container .resume-mini-card { padding: 10px 18px; }
  .dashboard-container .resume-icon { font-size: 32px; }
  .dashboard-container .resume-text h4 { font-size: 14px; }
  .dashboard-container .stats-row { gap: 10px; }
  .dashboard-container .stat-box { 
    padding: 10px 12px;
    gap: 10px;
  }
  .dashboard-container .stat-num { font-size: 20px; }
  .dashboard-container .stat-icon-bg { 
    width: 40px; 
    height: 40px; 
    font-size: 18px; 
  }
}

/* 双列时，高度小于 860px - 大幅压缩 */
@media (min-width: 1001px) and (max-height: 860px) {
  .dashboard-container {
    padding: 16px 20px;
    gap: 16px;
  }
  .column { gap: 16px; }

  .dashboard-container .intro-card {
    padding: 14px;
    min-height: 170px;
  }
  .dashboard-container .intro-content h2 { font-size: 22px; }
  .dashboard-container .mission-box {
    padding: 10px;
    margin-bottom: 10px;
    font-size: 12px;
  }
  .dashboard-container .start-btn { padding: 12px 18px; }
  .dashboard-container .intro-img { width: 145px; }

  .dashboard-container .profile-card {
    padding: 10px 12px;
    gap: 8px;
  }
  .dashboard-container .resume-mini-card {
    padding: 8px 12px;
  }
  .dashboard-container .resume-icon { font-size: 28px; }
  .dashboard-container .resume-text h4 { font-size: 12px; }
  .dashboard-container .stats-row { gap: 10px; }
  .dashboard-container .stat-box {
    padding: 8px 10px;
    gap: 8px;
  }
  .dashboard-container .stat-icon-bg {
    width: 38px;
    height: 38px;
    font-size: 17px;
  }
  .dashboard-container .stat-num { font-size: 18px; }
  .dashboard-container .stat-label { font-size: 11px; }

  .dashboard-container .left-col > .history-card,
  .dashboard-container .right-col > .charts-card {
    margin-top: auto;
  }

  /* 防止两个图在低高度双列时溢出卡片 */
  .dashboard-container .right-col > .charts-card {
    overflow: hidden;
  }
  .dashboard-container .right-col > .charts-card .charts-wrapper {
    margin-top: 6px;
    min-height: 0;
    overflow: hidden;
  }
  .dashboard-container .right-col > .charts-card .chart-block {
    min-height: 0;
    overflow: hidden;
  }
  .dashboard-container .right-col > .charts-card .mini-chart {
    min-height: 120px;
    height: clamp(120px, 14vh, 165px);
  }
}
</style>

<style>
/* 注意：下拉弹层默认挂载到 body，必须使用非 scoped 样式才能命中 */
.dashboard-direction-dropdown {
  --el-bg-color-overlay: var(--modal-bg);
  --el-fill-color-light: var(--modal-hover-bg);
  --el-text-color-regular: var(--text-color);
  --el-border-color-light: var(--input-border-color, var(--glass-border));
  --el-color-primary: var(--primary-color);
  background: var(--modal-bg) !important;
  border: 1px solid var(--input-border-color, var(--glass-border)) !important;
}

.dashboard-direction-dropdown,
.dashboard-direction-dropdown .el-select-dropdown,
.dashboard-direction-dropdown .el-select-dropdown__wrap,
.dashboard-direction-dropdown .el-scrollbar__view {
  background: var(--modal-bg) !important;
}

.dashboard-direction-dropdown .el-select-dropdown__item {
  color: var(--text-color) !important;
}

.dashboard-direction-dropdown .el-select-dropdown__item:hover,
.dashboard-direction-dropdown .el-select-dropdown__item.is-hovering {
  background: var(--modal-hover-bg) !important;
}

.dashboard-direction-dropdown .el-select-dropdown__item.is-selected {
  background: rgba(24, 144, 255, 0.16) !important;
  color: var(--primary-color) !important;
  font-weight: 600;
}

.dashboard-direction-dropdown .el-popper__arrow::before {
  background: var(--modal-bg) !important;
  border-color: var(--input-border-color, var(--glass-border)) !important;
}
</style>