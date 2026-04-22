<template>
  <div class="detail-container">
    <div class="page-header">
      <div class="left">
        <el-button link @click="router.back()">
          <el-icon><ArrowLeft /></el-icon> 返回
        </el-button>
        <span class="title">面试复盘 #{{ interviewId }}</span>
      </div>
      <div class="right">
        <el-tag type="success">得分: {{ hasReportContent ? overallScoreValue : '--' }}</el-tag>
        <el-button
          v-if="activeTab === 'report'"
          type="primary"
          round
          :disabled="!hasReportContent"
          @click="exportToPDF"
          style="margin-left: 10px"
        >
          <el-icon><Document /></el-icon> 导出PDF
        </el-button>
      </div>
    </div>

    <el-tabs v-model="activeTab" class="detail-tabs">
      <el-tab-pane label="对话全纪录" name="transcript">
        <div class="chat-review-area">
          <div v-for="(turn, index) in turns" :key="index" class="turn-block">
            <div class="message-row row-left">
              <el-avatar :size="36" :src="aiAvatar" class="msg-avatar" />
              <div class="message-container">
                <div class="sender-name">面试官</div>
                <div class="message-bubble" v-html="renderMarkdown(turn.question)"></div>
              </div>
            </div>

            <div class="message-row row-right">
              <div class="message-container">
                <div class="sender-name">我</div>
                <div class="message-bubble user-bubble">{{ turn.answer }}</div>
                <div v-if="turn.comment" class="ai-comment">
                  <el-icon><Comment /></el-icon>
                  <span>点评：{{ turn.comment }}</span>
                </div>
              </div>
              <el-avatar :size="36" :src="userAvatar" class="msg-avatar" />
            </div>
          </div>
          <el-empty v-if="turns.length === 0" description="暂无历史对话" />
        </div>
      </el-tab-pane>

      <el-tab-pane label="面试报告" name="report">
        <div v-if="hasReportContent" class="result-content" :class="{ 'pdf-exporting': isExportingPdf, 'pdf-export-light': isExportingPdf }" id="report-content-export">
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

          <div class="radar-chart-container">
            <h3>核心能力评估</h3>
            <div class="radar-chart">
              <div class="radar-main">
                <div class="chart-wrapper">
                  <div ref="radarChartRef" class="chart-box"></div>
                  <div v-for="item in radarMajorBadges" :key="item.key" class="radar-major-badge" :class="`badge-${ item.key }`">
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
        </div>
        <el-empty v-else description="暂无面试报告" />
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, nextTick, watch, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ArrowLeft, Comment, Document } from '@element-plus/icons-vue'
import { useUserStore } from '../../stores/user'
import { useThemeStore } from '../../stores/theme'
import * as echarts from 'echarts'
import MarkdownIt from 'markdown-it'
import hljs from 'highlight.js'
import 'highlight.js/styles/atom-one-dark.css'
import html2pdf from 'html2pdf.js'
import { ElMessage } from 'element-plus'
import { getInterviewDialogueHistory } from '../../api/history'
import { getInterviewReport } from '../../api/interview'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()
const themeStore = useThemeStore()

const interviewId = route.params.id
const activeTab = ref('transcript')
const turns = ref([])
const radarChartRef = ref(null)
const isExportingPdf = ref(false)
let radarChart = null

const EMPTY_REPORT_DATA = {
  abilityTrend: null,
  overallScore: 0,
  hiringRecommendation: '',
  executiveSummary: '',
  detailedRecommendation: '',
  dimensionScores: {
    cognition: 0,
    expression: 0,
    professional: 0
  },
  dimensionDetails: {
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
      engineeringPractice: 0,
      jobMatch: 0,
      knowledgeMatch: 0,
      technicalCorrectness: 0
    }
  },
  strengths: [],
  weaknesses: [],
  duration: ''
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
    abilityTrend: source.abilityTrend ?? EMPTY_REPORT_DATA.abilityTrend,
    detailedRecommendation: source.detailedRecommendation || EMPTY_REPORT_DATA.detailedRecommendation,
    dimensionDetails: {
      cognition: {
        ...EMPTY_REPORT_DATA.dimensionDetails.cognition,
        ...(details.cognition || {})
      },
      expression: {
        ...EMPTY_REPORT_DATA.dimensionDetails.expression,
        ...(details.expression || {})
      },
      professional: {
        ...EMPTY_REPORT_DATA.dimensionDetails.professional,
        ...(details.professional || {})
      }
    },
    dimensionScores: {
      ...EMPTY_REPORT_DATA.dimensionScores,
      ...(source.dimensionScores || {})
    },
    executiveSummary: source.executiveSummary || EMPTY_REPORT_DATA.executiveSummary,
    hiringRecommendation: source.hiringRecommendation || EMPTY_REPORT_DATA.hiringRecommendation,
    overallScore: toSafeNumber(source.overallScore, EMPTY_REPORT_DATA.overallScore),
    strengths: Array.isArray(source.strengths) && source.strengths.length ? source.strengths : EMPTY_REPORT_DATA.strengths,
    weaknesses: Array.isArray(source.weaknesses) && source.weaknesses.length ? source.weaknesses : EMPTY_REPORT_DATA.weaknesses,
    duration: source.duration || EMPTY_REPORT_DATA.duration
  }
}

const hasReportContent = computed(() => {
  const data = reportPayload.value
  if (!data || typeof data !== 'object') return false

  const summary = String(data.executiveSummary || '').trim()
  const recommendation = String(data.hiringRecommendation || '').trim()
  const detailed = String(data.detailedRecommendation || '').trim()
  const strengths = Array.isArray(data.strengths) ? data.strengths.length : 0
  const weaknesses = Array.isArray(data.weaknesses) ? data.weaknesses.length : 0
  const score = Number(data.overallScore)

  return Boolean(summary || recommendation || detailed || strengths > 0 || weaknesses > 0 || Number.isFinite(score))
})

const reportViewData = computed(() => normalizeReportData(reportPayload.value || EMPTY_REPORT_DATA))
const overallScoreValue = computed(() => toSafeNumber(reportViewData.value.overallScore, 0))

const reportDimensionRows = computed(() => {
  const scores = reportViewData.value.dimensionScores || {}
  return [
    { key: 'cognition', label: '认知思维', score: toSafeNumber(scores.cognition, 0) },
    { key: 'expression', label: '表达能力', score: toSafeNumber(scores.expression, 0) },
    { key: 'professional', label: '专业能力', score: toSafeNumber(scores.professional, 0) }
  ]
})

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

const aiAvatar = 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png'
const userAvatar = computed(() => userStore.userInfo.avatar || 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png')

const stampConfig = computed(() => {
  const score = overallScoreValue.value
  if (score >= 90) return { text: '优秀', color: '#67c23a', bg: 'rgba(103, 194, 58, 0.1)', border: 'rgba(103, 194, 58, 0.3)' }
  if (score >= 70) return { text: '良好', color: '#409eff', bg: 'rgba(64, 158, 255, 0.1)', border: 'rgba(64, 158, 255, 0.3)' }
  if (score >= 60) return { text: '合格', color: '#e6a23c', bg: 'rgba(230, 162, 60, 0.1)', border: 'rgba(230, 162, 60, 0.3)' }
  return { text: '不合格', color: '#f56c6c', bg: 'rgba(245, 108, 108, 0.1)', border: 'rgba(245, 108, 108, 0.3)' }
})

const md = new MarkdownIt({
  html: false,
  highlight: (str, lang) => {
    if (lang && hljs.getLanguage(lang)) {
      try {
        return `<pre class="hljs"><code>${hljs.highlight(str, { language: lang }).value}</code></pre>`
      } catch (_) {
        return ''
      }
    }
    return ''
  }
})

const renderMarkdown = (text) => (text ? md.render(text) : '')

const toPlainText = (value) => {
  if (value === null || value === undefined) return ''
  return typeof value === 'string' ? value : String(value)
}

const normalizeTurnRecord = (item) => {
  // 支持后端返回的字段名：assistantContent, userAnswer, turnNumber 等
  let question = toPlainText(item?.question ?? item?.ask ?? item?.prompt ?? item?.interviewer ?? item?.aiQuestion ?? item?.assistantContent).trim()
  const answer = toPlainText(item?.answer ?? item?.reply ?? item?.response ?? item?.userAnswer ?? item?.a ?? item?.userContent ?? item?.candidateAnswer).trim()
  const comment = toPlainText(item?.comment ?? item?.feedback ?? item?.evaluation ?? item?.review ?? item?.aiComment).trim()

  if (!question && answer) question = '（无题目记录）'
  if (!question && !answer && !comment) return null
  return { question, answer, comment }
}

const normalizeMessageRecords = (messages) => {
  const result = []
  let pendingQuestion = ''

  messages.forEach((raw) => {
    const role = toPlainText(raw?.role ?? raw?.speaker ?? raw?.type).toLowerCase().trim()
    const content = toPlainText(raw?.content ?? raw?.text ?? raw?.message ?? raw?.value).trim()
    const comment = toPlainText(raw?.comment ?? raw?.feedback).trim()

    if (!content) return

    if (role === 'assistant' || role === 'ai' || role === 'interviewer' || role === 'system') {
      if (pendingQuestion) result.push({ question: pendingQuestion, answer: '', comment: '' })
      pendingQuestion = content
      return
    }

    if (role === 'user' || role === 'candidate' || role === 'human') {
      result.push({ question: pendingQuestion || '（无题目记录）', answer: content, comment })
      pendingQuestion = ''
    }
  })

  if (pendingQuestion) result.push({ question: pendingQuestion, answer: '', comment: '' })
  return result
}

const parseInterviewTurns = (raw) => {
  const payload = raw?.data ?? raw
  const list = Array.isArray(payload)
    ? payload
    : payload?.records ?? payload?.list ?? payload?.rows ?? payload?.history ?? payload?.turns ?? payload?.messages ?? []

  if (!Array.isArray(list) || !list.length) return []

  const first = list[0]
  // 检查是否为 turn/question-answer 格式（包括后端的 assistantContent/turnNumber 格式）
  const hasTurnShape = first && typeof first === 'object' && (
    'question' in first || 
    'answer' in first || 
    'aiQuestion' in first || 
    'userAnswer' in first ||
    'assistantContent' in first ||
    'userContent' in first ||
    'candidateAnswer' in first
  )
  if (hasTurnShape) return list.map(normalizeTurnRecord).filter(Boolean)
  return normalizeMessageRecords(list)
}

const parseReportPayload = (raw) => {
  if (!raw) return null
  if (raw.data?.data) return raw.data.data
  if (raw.data && typeof raw.data === 'object') return raw.data
  if (raw?.report && typeof raw.report === 'object') return raw.report
  if (typeof raw === 'object') return raw
  return null
}

const fetchData = async () => {
  if (!interviewId) {
    ElMessage.error('缺少面试ID，无法加载复盘内容')
    turns.value = []
    reportPayload.value = null
    return
  }

  try {
    const [dialogRes, reportRes] = await Promise.all([
      getInterviewDialogueHistory(interviewId),
      getInterviewReport(interviewId)
    ])
    turns.value = parseInterviewTurns(dialogRes)
    reportPayload.value = parseReportPayload(reportRes)
  } catch (error) {
    console.error('加载复盘数据失败:', error)
    ElMessage.error('加载复盘数据失败，请稍后重试')
    turns.value = []
    reportPayload.value = null
  }
}

const getChartColors = () => {
  const isLight = themeStore.currentTheme === 'light' || isExportingPdf.value
  return {
    axisLineColor: isLight ? 'rgba(0,0,0,0.1)' : 'rgba(255,255,255,0.05)',
    textColor: isLight ? '#666' : '#a0a0a0',
    splitLineColor: isLight ? 'rgba(0,0,0,0.15)' : 'rgba(255,255,255,0.1)',
    splitAreaColors: isLight ? ['rgba(245,247,250,1)', 'rgba(255,255,255,1)'] : ['rgba(255,255,255,0.05)', 'rgba(255,255,255,0.02)'],
    tooltipBg: isLight ? '#fff' : 'rgba(50,50,50,0.7)',
    tooltipText: isLight ? '#333' : '#fff',
    radarColor: isLight ? '#409eff' : '#00d2ff',
    radarAreaColor: isLight ? 'rgba(64,158,255,0.4)' : 'rgba(0,210,255,0.4)'
  }
}

const initRadarChart = () => {
  if (radarChartRef.value) {
    nextTick(() => {
      if (radarChart) radarChart.dispose()
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
      radius: exportMode ? '60%' : '68%'
    },
    series:[{ type: 'radar', animation: !exportMode, data:[{ value: radarValues.value, name: '能力评估', areaStyle: { color: colors.radarAreaColor }, lineStyle: { color: colors.radarColor }, itemStyle: { color: colors.radarColor } }] }]
  })
}

const handleResize = () => { radarChart?.resize() }

const exportToPDF = async () => {
  if (!hasReportContent.value) {
    ElMessage.warning('暂无可导出的面试报告')
    return
  }

  const element = document.getElementById('report-content-export')
  if (!element) {
    ElMessage.error('报告内容不存在，无法导出')
    return
  }

  try {
    isExportingPdf.value = true
    await nextTick()
    updateRadarChart()
    radarChart?.resize()

    await html2pdf().set({
      margin: 10,
      filename: `面试复盘报告_${ interviewId }_${ new Date().toISOString().slice(0, 10) }.pdf`,
      image: { type: 'jpeg', quality: 0.98 },
      html2canvas: { scale: 2, useCORS: true, scrollX: 0, scrollY: 0, windowWidth: element.scrollWidth },
      jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' }
    }).from(element).save()
    ElMessage.success('PDF导出成功')
  } catch (error) {
    console.error('导出PDF失败:', error)
    ElMessage.error('导出PDF失败')
  } finally {
    isExportingPdf.value = false
    await nextTick()
    updateRadarChart()
    radarChart?.resize()
  }
}

watch(activeTab, (newTab) => {
  if (newTab === 'report') {
    nextTick(() => {
      initRadarChart()
    })
  }
})
watch(() => themeStore.currentTheme, () => { updateRadarChart() })

onMounted(() => {
  fetchData()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  radarChart?.dispose()
})
</script>

<style scoped>
.detail-container {
  height: calc(100vh - 24px);
  margin: 12px;
  display: flex;
  flex-direction: column;
  background: var(--history-detail-bg);
  color: var(--text-color);
  border: 1px solid rgba(255, 255, 255, 0.35);
  border-radius: 22px;
  overflow: hidden;
  box-shadow: 0 14px 34px rgba(15, 28, 63, 0.2);
}

.page-header {
  height: 50px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  background: var(--history-detail-header-bg, rgba(0, 0, 0, 0.2));
  border-bottom: 1px solid var(--history-detail-header-border, var(--glass-border));
}

.left {
  display: flex;
  align-items: center;
  gap: 15px;
}

.title {
  font-weight: bold;
  font-size: 16px;
}

.detail-tabs {
  flex: 1;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

:deep(.el-tabs__content) {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  /* 滚动条主题适配（Firefox + WebKit） */
  scrollbar-width: thin;
  scrollbar-color: var(--report-scrollbar-thumb, var(--page-scrollbar-thumb, rgba(0,0,0,0.12))) var(--report-scrollbar-track, var(--page-scrollbar-track, transparent));
}

/* WebKit 自定义滚动条，优先应用于选项卡内容区域 */
:deep(.el-tabs__content)::-webkit-scrollbar { width: 10px; }
:deep(.el-tabs__content)::-webkit-scrollbar-track { background: var(--report-scrollbar-track, var(--page-scrollbar-track, transparent)); border-radius: 999px; }
:deep(.el-tabs__content)::-webkit-scrollbar-thumb { background: var(--report-scrollbar-thumb, var(--page-scrollbar-thumb, rgba(0,0,0,0.12))); border-radius: 999px; border: 2px solid transparent; background-clip: padding-box; }
:deep(.el-tabs__content)::-webkit-scrollbar-thumb:hover { background: color-mix(in srgb, var(--report-scrollbar-thumb, var(--page-scrollbar-thumb, rgba(0,0,0,0.12))) 82%, var(--primary-color) 18%); }

:deep(.el-tabs__header) {
  margin: 0;
  background: var(--history-detail-tabs-header-bg, rgba(0, 0, 0, 0.1));
  padding: 0 20px;
}

:deep(.el-tabs__nav-wrap::after) {
  background-color: var(--history-detail-tabs-divider, var(--glass-border));
}

.chart-wrapper {
  position: relative;
  width: 100%;
  height: 360px;
}

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

.badge-cognition { left: 18%; top: 18%; }
.badge-expression { right: 18%; top: 20%; }
.badge-professional { left: 50%; transform: translateX(-50%); bottom: -24px; }

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

.metric-row { margin-bottom: 10px; }
.metric-row:last-child { margin-bottom: 0; }

.metric-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 6px;
  color: var(--text-secondary);
  font-size: 13px;
}

.metric-head strong { color: var(--text-color); }

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

.radar-chart-container, .dimension-breakdown, .evaluation-section, .suggestion-section {
  background: var(--glass-bg);
  border-radius: 12px;
  padding: 20px;
  border: 1px solid var(--glass-border);
  margin-top: 20px;
}

.radar-chart-container h3, .dimension-breakdown h3, .evaluation-section h3, .suggestion-section h3 {
  margin: 0 0 16px;
  font-size: 18px;
}

.radar-chart { display: flex; justify-content: center; }
.radar-main { width: 100%; padding: 0 24px 44px; box-sizing: border-box; }
.chart-box { width: 100%; height: 100%; }

.report-hero {
  display: grid;
  grid-template-columns: 1fr 230px;
  gap: 18px;
  margin-bottom: 20px;
}

.hero-main {
  background: var(--glass-bg);
  border-radius: 12px;
  border: 1px solid var(--glass-border);
  padding: 20px;
}

.hero-kicker { font-size: 12px; letter-spacing: 1px; color: var(--text-secondary); }
.hero-main h3 { margin: 8px 0 12px; font-size: 24px; }

.hero-score {
  position: relative;
  padding: 14px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  background: var(--glass-bg);
  border-radius: 12px;
  border: 1px solid var(--glass-border);
}

.hero-score-label { margin: 0; font-size: 22px; font-weight: 700; }
.hero-score-value { margin: 4px 0 0; font-size: 68px; line-height: 1; font-weight: 800; }

.score-stamp {
  position: absolute;
  top: -12px;
  right: -8px;
  font-size: 18px;
  font-weight: 900;
  border: 3px solid;
  border-radius: 6px;
  padding: 2px 10px;
  letter-spacing: 2px;
  transform: rotate(25deg);
}

.suggestion-list { color: var(--text-secondary); padding-left: 0; margin: 0; list-style: none; display: grid; gap: 10px; }
.suggestion-list li { line-height: 1.6; border: 1px solid var(--report-card-border); border-radius: 12px; padding: 10px 12px; background: rgba(255, 255, 255, 0.08); }

.evaluation-content p { color: var(--text-secondary); line-height: 1.6; margin: 0 0 10px 0; }

.chat-review-area {
  max-width: 800px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding-bottom: 90px !important;
}

.turn-block {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.message-row {
  display: flex;
  gap: 12px;
  align-items: flex-start;
}

.row-left { justify-content: flex-start; }
.row-right { justify-content: flex-end; }

.message-container {
  display: flex;
  flex-direction: column;
  max-width: 80%;
}

.row-left .message-container { align-items: flex-start; }
.row-right .message-container { align-items: flex-end; }

.sender-name { font-size: 12px; color: var(--text-secondary); margin-bottom: 4px; }
.message-bubble { padding: 12px 16px; border-radius: 8px; font-size: 14px; line-height: 1.6; background: #ffffff; color: #303133; }
.user-bubble { background: var(--primary-color); color: #fff; }

.ai-comment {
  margin-top: 5px;
  font-size: 12px;
  color: #e6a23c;
  display: flex;
  align-items: center;
  gap: 5px;
  background: rgba(230, 162, 60, 0.1);
  padding: 4px 8px;
  border-radius: 4px;
}

.result-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 20px;
  overflow-y: auto;
  padding-right: 10px;
  padding-bottom: 90px !important;
  /* 主题自适配的滚动条：Firefox 支持 + WebKit 自定义 */
  scrollbar-width: thin;
  scrollbar-color: var(--report-scrollbar-thumb, var(--page-scrollbar-thumb, rgba(0,0,0,0.12))) var(--report-scrollbar-track, var(--page-scrollbar-track, transparent));
}

/* WebKit 浏览器自定义滚动条样式 */
.result-content::-webkit-scrollbar { width: 8px; }
.result-content::-webkit-scrollbar-track { background: var(--report-scrollbar-track, var(--page-scrollbar-track, transparent)); border-radius: 6px; }
.result-content::-webkit-scrollbar-thumb { background: var(--report-scrollbar-thumb, var(--page-scrollbar-thumb, rgba(0,0,0,0.12))); border-radius: 6px; border: 2px solid transparent; background-clip: padding-box; }
.result-content::-webkit-scrollbar-thumb:hover { background: color-mix(in srgb, var(--report-scrollbar-thumb, var(--page-scrollbar-thumb, rgba(0,0,0,0.12))) 82%, var(--primary-color) 18%); }

/* 仅导出 PDF 时隐藏雷达图周围三项总分卡片，不影响页面正常展示 */
.result-content.pdf-exporting .radar-major-badge {
  display: none;
}

/* 仅白色主题导出时增强层次，避免与 PDF 白底混在一起 */
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

:deep(.message-bubble p), :deep(.markdown-body p) { margin: 0; }
:deep(.message-bubble code), :deep(.markdown-body code) { background: rgba(0, 0, 0, 0.12); padding: 2px 6px; border-radius: 4px; }

@media (max-width: 1024px) {
  .report-hero { grid-template-columns: 1fr; }
  .dimension-grid { grid-template-columns: 1fr; }
  .badge-cognition, .badge-expression, .badge-professional { position: static; margin-top: 10px; }
  .chart-wrapper { height: 280px; }
  .radar-main { padding: 0 10px 40px; }
}

@media (max-width: 760px) {
  .detail-container {
    height: 100dvh;
    margin: 0;
    border-radius: 0;
    border: none;
  }

  .page-header {
    height: auto;
    padding: 12px 12px 10px;
    gap: 8px;
    align-items: flex-start;
    flex-direction: column;
  }

  .left,
  .right {
    width: 100%;
  }

  .left {
    gap: 10px;
    flex-wrap: wrap;
  }

  .title {
    font-size: 14px;
    line-height: 1.35;
    word-break: break-all;
  }

  .right {
    display: flex;
    align-items: center;
    gap: 8px;
    flex-wrap: wrap;
    justify-content: flex-start;
  }

  .right :deep(.el-tag),
  .right :deep(.el-button) {
    display: none;
  }

  .right :deep(.el-tag) {
    margin-right: 0;
  }

  .right :deep(.el-button) {
    margin-left: 0 !important;
    width: 100%;
    justify-content: center;
  }

  :deep(.el-tabs__header) {
    padding: 0 12px;
  }

  :deep(.el-tabs__content) {
    padding: 12px;
  }

  .chat-review-area {
    max-width: none;
    gap: 14px;
    padding-bottom: 50px !important;
  }

  .message-row {
    gap: 8px;
  }

  .msg-avatar {
    flex: 0 0 auto;
    width: 32px !important;
    height: 32px !important;
    min-width: 32px;
    min-height: 32px;
    border-radius: 50%;
    overflow: hidden;
  }

  .msg-avatar :deep(img) {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }

  .message-container {
    max-width: 88%;
  }

  .message-bubble {
    padding: 10px 12px;
    font-size: 13px;
  }

  .ai-comment {
    font-size: 11px;
    padding: 4px 6px;
  }

  .result-content {
    gap: 14px;
    padding-right: 0;
    padding-bottom: 60px !important;
  }

  .report-hero {
    gap: 12px;
    margin-bottom: 10px;
  }

  .hero-main,
  .hero-score,
  .radar-chart-container,
  .dimension-breakdown,
  .evaluation-section,
  .suggestion-section {
    padding: 14px;
    border-radius: 14px;
  }

  .hero-main h3 {
    font-size: 20px;
    margin: 6px 0 10px;
    word-break: break-word;
  }

  .hero-summary :deep(p) {
    font-size: 13px;
    line-height: 1.7;
  }

  .hero-score {
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    text-align: left;
    gap: 10px;
  }

  .hero-score-label {
    display: block;
    font-size: 14px;
    margin: 0;
  }

  .hero-score-value {
    font-size: 42px;
    margin: 0;
  }

  .score-stamp {
    display: none;
  }

  .radar-chart-container h3,
  .dimension-breakdown h3,
  .evaluation-section h3,
  .suggestion-section h3 {
    font-size: 16px;
    margin-bottom: 12px;
  }

  .chart-wrapper {
    height: 230px;
  }

  .radar-main {
    padding: 0 0 30px;
  }

  .radar-major-badge {
    display: none;
  }

  .major-label {
    font-size: 11px;
  }

  .major-value {
    font-size: 13px;
  }

  .dimension-grid {
    gap: 10px;
  }

  .dimension-group {
    padding: 10px;
  }

  .dimension-group h4 {
    font-size: 14px;
  }

  .dimension-group h4 em {
    font-size: 12px;
  }

  .metric-head {
    font-size: 12px;
  }

  .metric-track {
    height: 5px;
  }

  .evaluation-content p,
  .suggestion-list li,
  .message-bubble {
    line-height: 1.65;
  }
}

@media (max-width: 560px) {
  :deep(.el-tabs__header) {
    padding: 0 10px;
  }

  :deep(.el-tabs__item) {
    font-size: 12px;
    padding: 0 10px;
  }

  :deep(.el-tabs__content) {
    padding: 10px;
  }

  .page-header {
    padding: 10px 10px 8px;
  }

  .title {
    font-size: 13px;
  }

  .left .el-button {
    padding: 0;
  }

  .message-container {
    max-width: 92%;
  }

  .msg-avatar {
    width: 28px !important;
    height: 28px !important;
    min-width: 28px;
    min-height: 28px;
  }

  .message-bubble {
    font-size: 12px;
    padding: 9px 10px;
  }

  .hero-main h3 {
    font-size: 18px;
  }

  .hero-score-value {
    font-size: 36px;
  }

  .chart-wrapper {
    height: 200px;
  }

  .dimension-grid {
    grid-template-columns: 1fr;
  }

  .metric-head {
    flex-wrap: wrap;
    gap: 4px;
  }
}
</style>
