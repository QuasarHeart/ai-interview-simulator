<template>
  <div class="assessment-container">
    
    <!-- 1. 顶部：方向选择与核心数据概览 (整合了首页的4个数据) -->
    <div class="overview-section">
      <!-- 左侧区域：标题与筛选器 -->
      <div class="overview-header">
        <div class="title-group">
          <h2>综合能力评估</h2>
          <p class="subtitle">AI 教练基于您的历史面试数据生成</p>
        </div>
        
        <!-- 优化后的精美下拉框 -->
        <div class="custom-select-wrapper">
          <span class="select-label">评估方向：</span>
          <el-select 
            v-model="selectedDirection" 
            class="direction-filter"
            @change="handleDirectionChange"
            :teleported="false"
            popper-class="assessment-direction-dropdown"
          >
            <el-option label="Web 前端" value="web_frontend" />
            <el-option label="Java 后端" value="java_backend" />
            <el-option label="Python 后端" value="python_backend" />
            <el-option label="Golang 后端" value="golang_backend" />
            <el-option label="DevOps" value="devops" />
            <el-option label="软件测试工程师" value="software_test_engineer" />
            <el-option label="系统架构师" value="system_architect" />
            <el-option label="数据工程师" value="data_engineer" />
            <el-option label="SRE" value="site_reliability_engineer" />
            <el-option label="机器学习工程师" value="machine_learning_engineer" />
          </el-select>
        </div>
      </div>

      <!-- 右侧区域：4个核心指标数据 -->
      <div class="stats-grid">
        <div class="stat-box">
          <div class="stat-icon blue"><el-icon><Trophy /></el-icon></div>
          <div class="stat-info">
            <span class="stat-num">{{ overallScore }}</span>
            <span class="stat-desc">综合均分</span>
          </div>
        </div>
        <div class="stat-box">
          <div class="stat-icon green"><el-icon><DataLine /></el-icon></div>
          <div class="stat-info">
            <span class="stat-num">{{ interviewCount }}</span>
            <span class="stat-desc">完成面试</span>
          </div>
        </div>
        <div class="stat-box">
          <div class="stat-icon orange"><el-icon><Star /></el-icon></div>
          <div class="stat-info">
            <span class="stat-num">{{ highestScore }}</span>
            <span class="stat-desc">最高得分</span>
          </div>
        </div>
        <div class="stat-box">
          <div class="stat-icon purple"><el-icon><Timer /></el-icon></div>
          <div class="stat-info">
            <span class="stat-num">{{ practiceHours }}<small>h</small></span>
            <span class="stat-desc">练习时长</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 2. 下半部分：图表与建议 (采用 5:4 左右分栏) -->
    <div class="analysis-layout">
      
      <!-- 左列：趋势图 + 建议 (占据较大空间) -->
      <div class="layout-left">
        <div class="chart-card flex-card">
          <div class="card-title">
            <h3><el-icon><TrendCharts /></el-icon> 成长趋势</h3>
          </div>
          <div ref="lineChartRef" class="chart-box"></div>
        </div>

        <!-- 建议卡片自动填满剩余高度 -->
        <div class="suggestion-card flex-grow-card">
          <div class="card-title">
            <h3><el-icon><MagicStick /></el-icon> AI 教练诊断建议</h3>
          </div>
          <div v-if="loading" class="loading-state">
            <el-icon class="is-loading"><Loading /></el-icon> 分析中...
          </div>
          <div v-else class="suggestion-content">
            <div class="suggestion-item warning">
              <div class="item-header">
                <el-icon><Warning /></el-icon>
                <span>核心薄弱项</span>
              </div>
              <p>{{ weakPoint }}</p>
            </div>
            <div class="suggestion-item success">
              <div class="item-header">
                <el-icon><CircleCheck /></el-icon>
                <span>闪光点</span>
              </div>
              <p>{{ highLight }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- 右列：雷达模型图 -->
      <div class="layout-right">
        <div class="chart-card full-height-card">
          <div class="card-title">
            <h3><el-icon><Aim /></el-icon> 十维能力模型</h3>
          </div>
          
          <div ref="radarChartRef" class="radar-box"></div>
          
          <!-- 雷达图下方附带明细数据 - 分组显示 -->
          <div class="radar-details">
            <div v-for="group in dimensionDetailGroups" :key="group.key" class="dimension-group">
              <div class="group-header">
                <span class="group-label">{{ group.label }}</span>
                <span class="group-score">{{ group.score.toFixed(2) }}/5</span>
              </div>
              <div class="group-items">
                <div v-for="item in group.items" :key="item.key" class="detail-item">
                  <span class="label">{{ item.label }}</span>
                  <el-progress 
                    :percentage="(item.value || 0) * 20" 
                    :stroke-width="4" 
                    color="#409eff" 
                    class="progress-bar" 
                    :show-text="false" 
                  />
                  <span class="value">{{ (item.value || 0).toFixed(1) }}/5</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch, nextTick, computed } from 'vue'
import * as echarts from 'echarts'
// === 修复了这里的引入，把 Target 换成了 Aim ===
import { 
  Warning, CircleCheck, Trophy, DataLine, Star, Timer, 
  TrendCharts, Aim, MagicStick, Loading 
} from '@element-plus/icons-vue'
import { useThemeStore } from '../../stores/theme'
import { getGrowthCurve } from '../../api/assessment'
import { ElMessage } from 'element-plus'

const themeStore = useThemeStore()

// DOM Refs
const radarChartRef = ref(null)
const lineChartRef = ref(null)
let radarChart = null
let lineChart = null

// 状态数据
const loading = ref(true)
const selectedDirection = ref(localStorage.getItem('assessmentDirection') || 'java_backend')

// 核心指标数据
const overallScore = ref(0)
const interviewCount = ref(0)
const highestScore = ref(0)
const practiceHours = ref(0)

const weakPoint = ref('暂无数据')
const highLight = ref('暂无数据')

// 原始数据 - 用于计算雷达图值
const dimensionScores = ref({
  cognition: 0,
  expression: 0,
  professional: 0
})

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

// 图表数据
let lineValues = []
let lineDates = []

// 计算维度详情分组（参考面试报告）
const dimensionDetailGroups = computed(() => {
  const details = dimensionDetails.value || {}
  const scores = dimensionScores.value || {}
  return [
    {
      key: 'cognition',
      label: '认知',
      score: scores.cognition || 0,
      items: [
        { key: 'logicStructure', label: '逻辑结构', value: details.cognition?.logicStructure || 0 },
        { key: 'problemSolving', label: '问题拆解', value: details.cognition?.problemSolving || 0 },
        { key: 'systemThinking', label: '系统思维', value: details.cognition?.systemThinking || 0 }
      ]
    },
    {
      key: 'expression',
      label: '表达',
      score: scores.expression || 0,
      items: [
        { key: 'clarity', label: '表达清晰', value: details.expression?.clarity || 0 },
        { key: 'confidenceStability', label: '自信稳定', value: details.expression?.confidenceStability || 0 },
        { key: 'professionalMaturity', label: '职业成熟', value: details.expression?.professionalMaturity || 0 }
      ]
    },
    {
      key: 'professional',
      label: '专业',
      score: scores.professional || 0,
      items: [
        { key: 'technicalCorrectness', label: '技术准确', value: details.professional?.technicalCorrectness || 0 },
        { key: 'knowledgeMatch', label: '知识匹配', value: details.professional?.knowledgeMatch || 0 },
        { key: 'jobMatch', label: '岗位匹配', value: details.professional?.jobMatch || 0 },
        { key: 'engineeringPractice', label: '工程实践', value: details.professional?.engineeringPractice || 0 }
      ]
    }
  ]
})

// 展平的雷达图详情项（10个维度）
const radarDetailItems = computed(() =>
  dimensionDetailGroups.value.flatMap((group) =>
    group.items.map((item) => ({
      ...item,
      radarLabel: item.label
    }))
  )
)

// 十维雷达图值
const radarValues = computed(() => radarDetailItems.value.map((item) => {
  const val = Number(item.value) || 0
  return Number(val.toFixed(1)) // 直接返回0-5的分值，保留一位小数
}))

// 图表颜色配置适配主题
const getChartColors = () => {
  const isLight = themeStore.currentTheme === 'light'
  return {
    axisLineColor: isLight ? 'rgba(0, 0, 0, 0.05)' : 'rgba(255, 255, 255, 0.05)',
    textColor: isLight ? '#666' : '#a0a0a0',
    splitLineColor: isLight ? 'rgba(0, 0, 0, 0.1)' : 'rgba(255, 255, 255, 0.1)',
    splitAreaColors: isLight 
      ?['rgba(245, 247, 250, 1)', 'rgba(255, 255, 255, 1)'] 
      :['rgba(255, 255, 255, 0.03)', 'rgba(255, 255, 255, 0.01)'],
    tooltipBg: isLight ? '#fff' : 'rgba(30, 41, 59, 0.9)',
    tooltipText: isLight ? '#333' : '#fff',
    lineColor: isLight ? '#409eff' : '#00d2ff',
    areaColor: isLight ? 'rgba(64, 158, 255, 0.2)' : 'rgba(0, 210, 255, 0.2)'
  }
}

// 仅在两列布局且高度较低时启用紧凑图表配置
const isLowHeightTwoColumn = () => window.innerWidth > 1200 && window.innerHeight <= 860

// 初始化折线图
const updateLineChart = () => {
  if (!lineChartRef.value) return
  if (!lineChart) lineChart = echarts.init(lineChartRef.value)
  
  const c = getChartColors()
  const compact = isLowHeightTwoColumn()
  const totalPoints = lineDates.length || 1
  const visiblePoints = 7
  const zoomWindow = totalPoints > visiblePoints ? Math.round((visiblePoints / totalPoints) * 100) : 100
  const zoomStart = totalPoints > visiblePoints ? Math.max(0, 100 - zoomWindow) : 0
  const zoomEnd = 100

  lineChart.setOption({
    backgroundColor: 'transparent',
    grid: {
      top: compact ? 12 : 20,
      right: compact ? 14 : 20,
      bottom: compact ? 18 : 52,
      left: compact ? 22 : 30,
      containLabel: true
    },
    tooltip: { trigger: 'axis', backgroundColor: c.tooltipBg, textStyle: { color: c.tooltipText } },
    xAxis: {
      type: 'category',
      data: lineDates,
      axisLine: { lineStyle: { color: c.splitLineColor } },
      axisLabel: {
        color: c.textColor,
        fontSize: compact ? 10 : 12,
        interval: compact ? 'auto' : 0,
        hideOverlap: true
      }
    },
    yAxis: {
      type: 'value',
      splitLine: { lineStyle: { color: c.splitLineColor } },
      axisLabel: { color: c.textColor, fontSize: compact ? 10 : 12 }
    },
    series:[{
      data: lineValues,
      type: 'line',
      smooth: true,
      symbol: 'circle',
      symbolSize: compact ? 4 : 6,
      itemStyle: { color: c.lineColor },
      areaStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1,[
          { offset: 0, color: c.areaColor },
          { offset: 1, color: 'rgba(0,0,0,0)' }
        ])
      }
    }],
    dataZoom: [
      {
        type: 'inside',
        xAxisIndex: 0,
        start: zoomStart,
        end: zoomEnd,
        zoomOnMouseWheel: true,
        moveOnMouseMove: true,
        moveOnMouseWheel: true
      },
      {
        type: 'slider',
        xAxisIndex: 0,
        start: zoomStart,
        end: zoomEnd,
        show: !compact,
        height: 12,
        bottom: 12,
        borderColor: 'transparent',
        backgroundColor: c.splitAreaColors[1],
        fillerColor: c.areaColor,
        showDetail: false,
        brushSelect: false,
        dataBackground: {
          lineStyle: { color: c.lineColor, opacity: 0.35 },
          areaStyle: { color: c.areaColor, opacity: 0.12 }
        },
        selectedDataBackground: {
          lineStyle: { color: c.lineColor, opacity: 0.95 },
          areaStyle: { color: c.areaColor, opacity: 0.28 }
        },
        moveHandleSize: 0,
        handleIcon: 'path://M512 64C264.6 64 64 264.6 64 512s200.6 448 448 448 448-200.6 448-448S759.4 64 512 64z',
        handleSize: 12,
        handleStyle: {
          color: c.lineColor,
          borderColor: '#ffffff',
          borderWidth: 1.5,
          shadowBlur: 6,
          shadowColor: c.areaColor
        },
        textStyle: { color: c.textColor, fontSize: 11 }
      }
    ]
  })
}

// 初始化雷达图
const updateRadarChart = () => {
  if (!radarChartRef.value) return
  if (!radarChart) radarChart = echarts.init(radarChartRef.value)
  
  const c = getChartColors()
  const compact = isLowHeightTwoColumn()
  
  // 构建十维雷达图指标
  const indicator = radarDetailItems.value.map((item) => ({
    name: item.radarLabel,
    max: 5
  }))

  radarChart.setOption({
    backgroundColor: 'transparent',
    tooltip: { backgroundColor: c.tooltipBg, textStyle: { color: c.tooltipText }, z: 1000, confine: false },
    radar: {
      indicator,
      radius: compact ? '58%' : '65%',
      center: compact ? ['50%', '46%'] : ['50%', '45%'],
      splitArea: { areaStyle: { color: c.splitAreaColors } },
      axisLine: { lineStyle: { color: c.axisLineColor } },
      splitLine: { lineStyle: { color: c.splitLineColor } },
      axisName: { 
        color: c.textColor, 
        fontSize: compact ? 10 : 11,
        formatter: (name) => name.replace('-', '\n')
      }
    },
    series:[{
      type: 'radar',
      data:[{
        value: radarValues.value,
        name: '能力分值',
        areaStyle: { color: 'rgba(0, 210, 255, 0.4)' },
        lineStyle: { color: '#00d2ff', width: 2 },
        itemStyle: { color: '#00d2ff' }
      }]
    }]
  })
}

// 获取真实数据
const fetchData = async () => {
  loading.value = true
  
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
    const jobRole = jobRoleMap[selectedDirection.value] || ''
    
    const res = await getGrowthCurve(jobRole)
    console.log('获取评估数据成功:', res)
    const data = res?.data || {}
    
    // 更新核心指标
    overallScore.value = Math.round(data.overallRating * 10) / 10 || 0
    interviewCount.value = data.interviewCount || 0
    highestScore.value = data.bestScore || 0
    practiceHours.value = (data.practiceTime || 0).toFixed(1)
    
    // 更新维度数据
    if (data.dimensionScores) {
      dimensionScores.value = {
        cognition: data.dimensionScores.cognition || 0,
        expression: data.dimensionScores.expression || 0,
        professional: data.dimensionScores.professional || 0
      }
    }
    
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
    
    // 更新建议
    if (Array.isArray(data.weaknesses) && data.weaknesses.length > 0) {
      weakPoint.value = data.weaknesses[0]
    } else {
      weakPoint.value = '暂无弱点数据'
    }
    
    if (Array.isArray(data.strengths) && data.strengths.length > 0) {
      highLight.value = data.strengths[0]
    } else {
      highLight.value = '暂无优势数据'
    }
    
    // 处理成长曲线数据
    if (Array.isArray(data.growthPoints) && data.growthPoints.length > 0) {
      // 检查是否为数值数组或对象数组
      const firstItem = data.growthPoints[0]
      if (typeof firstItem === 'number') {
        // 直接是数值数组
        lineValues = data.growthPoints
        lineDates = data.growthPoints.map((_, i) =>
          i === data.growthPoints.length - 1 ? '最近' : String(i + 1)
        )
      } else if (typeof firstItem === 'object' && firstItem.score !== undefined) {
        // 是对象数组，包含 score 属性
        lineValues = data.growthPoints.map(p => p.score || 0)
        lineDates = data.growthPoints.map((p, i) => p.date || `第${i + 1}次`)
      }
    } else {
      // 获取不到成长曲线数据时，使用虚拟数据
      const totalInterviews = Math.max(interviewCount.value, 10)
      lineValues = Array.from({ length: totalInterviews }, (_, i) => 
        Math.round(60 + (overallScore.value - 60) * (i / (totalInterviews - 1)))
      )
      lineDates = Array.from({ length: lineValues.length }, (_, i) =>
        i === lineValues.length - 1 ? '最近' : String(i + 1)
      )
    }
    
    loading.value = false
  } catch (error) {
    console.error('获取评估数据失败:', error)
    ElMessage.error('获取评估数据失败，请稍后重试')
    
    // 设置默认值避免UI异常
    overallScore.value = 0
    interviewCount.value = 0
    highestScore.value = 0
    practiceHours.value = 0
    weakPoint.value = '无法加载数据'
    highLight.value = '无法加载数据'
    lineValues = []
    lineDates = []
    
    loading.value = false
  }
  
  nextTick(() => {
    updateLineChart()
    updateRadarChart()
  })
}

const handleDirectionChange = (val) => {
  localStorage.setItem('assessmentDirection', val)
  fetchData()
}

const handleResize = () => {
  lineChart?.resize()
  radarChart?.resize()
}

let resizeObserver = null
let resizeTimeout = null

onMounted(() => {
  fetchData()
  window.addEventListener('resize', handleResize)
  
  // 添加 ResizeObserver 来监听容器宽度变化（侧边栏展开/收缩时）
  if (typeof ResizeObserver !== 'undefined') {
    resizeObserver = new ResizeObserver(() => {
      // 清除之前的定时器
      if (resizeTimeout) clearTimeout(resizeTimeout)
      
      // 使用 requestAnimationFrame 确保在下一帧同步调用 resize
      requestAnimationFrame(() => {
        handleResize()
      })
      
      // 在展开/收缩动画期间（0.4s）多次调用 resize 确保平滑
      resizeTimeout = setTimeout(() => {
        handleResize()
      }, 200)
    })
    
    // 监听 analysis-layout 容器的宽度变化
    const analysisLayout = document.querySelector('.analysis-layout')
    if (analysisLayout) {
      resizeObserver.observe(analysisLayout)
    }
  }
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  if (resizeObserver) {
    resizeObserver.disconnect()
  }
  if (resizeTimeout) {
    clearTimeout(resizeTimeout)
  }
  lineChart?.dispose()
  radarChart?.dispose()
})

watch(() => themeStore.currentTheme, () => {
  if (!loading.value) {
    updateLineChart()
    updateRadarChart()
  }
})
</script>

<style scoped>
/* 1. 全局容器：禁止滚动，并稍微增大底部内边距(从30px改为40px)，把整体往上提 */
.assessment-container { 
  padding: 25px 30px 40px 30px; /* 核心修改：底部 padding 改为 40px 往上提 */
  color: var(--text-color); 
  display: flex; 
  flex-direction: column; 
  height: 100%; 
  box-sizing: border-box;
  gap: 20px;
  overflow: hidden; /* 核心修改：禁止整个页面滚动 */
}

/* === 1. 顶部数据看板 === */
.overview-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: var(--card-bg);
  border: 1px solid var(--sidebar-border);
  border-radius: 20px;
  padding: 25px 30px;
}

.overview-header {
  display: flex;
  flex-direction: column;
  gap: 15px;
}
.title-group h2 { margin: 0; font-size: 24px; color: var(--text-color); }
.title-group .subtitle { margin: 5px 0 0; font-size: 13px; color: var(--text-secondary); }

/* 优化的下拉框 */
.custom-select-wrapper {
  display: flex;
  align-items: center;
  background: rgba(128,128,128,0.1);
  padding: 4px 12px;
  border-radius: 20px;
  width: fit-content;
}
.select-label { font-size: 13px; color: var(--text-secondary); font-weight: bold; }
.direction-filter { width: 130px; }

/* 覆盖 Element Select 样式，让它完美融入背景 */
:deep(.el-select__wrapper) { background-color: transparent !important; box-shadow: none !important; padding: 0 !important; }
:deep(.el-select__input) { color: var(--primary-color) !important; font-weight: bold; font-size: 14px; }
:deep(.el-select__caret) { color: var(--primary-color) !important; }
:deep(.assessment-direction-dropdown) {
  background: var(--card-bg) !important;
  border: 1px solid var(--sidebar-border) !important;
}
:deep(.assessment-direction-dropdown .el-popper__arrow::before) {
  background: var(--card-bg) !important;
  border: 1px solid var(--sidebar-border) !important;
}
:deep(.assessment-direction-dropdown .el-select-dropdown__item) {
  color: var(--text-color);
}
:deep(.assessment-direction-dropdown .el-select-dropdown__item:hover) {
  background: var(--sidebar-active-bg);
}
:deep(.assessment-direction-dropdown .el-select-dropdown__item.is-selected) {
  color: var(--primary-color);
  background: var(--sidebar-active-bg);
}

/* 4个统计格子 */
.stats-grid {
  display: flex;
  gap: 30px;
}
.stat-box { display: flex; align-items: center; gap: 15px; }
.stat-icon { width: 48px; height: 48px; border-radius: 14px; display: flex; justify-content: center; align-items: center; font-size: 22px; color: white; }
.stat-icon.blue { background: linear-gradient(135deg, #409eff, #3a8ee6); }
.stat-icon.green { background: linear-gradient(135deg, #67c23a, #529b2e); }
.stat-icon.orange { background: linear-gradient(135deg, #e6a23c, #d38c2a); }
.stat-icon.purple { background: linear-gradient(135deg, #9c27b0, #7b1fa2); }

.stat-info { display: flex; flex-direction: column; gap: 4px; }
.stat-num { font-size: 26px; font-weight: 900; line-height: 1; color: var(--text-color); }
.stat-num small { font-size: 14px; font-weight: normal; margin-left: 2px; }
.stat-desc { font-size: 12px; color: var(--text-secondary); font-weight: bold; }

/* 2. 下半部分分析区域：确保它能被压缩 */
.analysis-layout {
  flex: 1;
  display: flex;
  gap: 20px;
  min-height: 0; /* 核心修改：允许 Flex 子元素收缩 */
  overflow: visible; /* 允许 tooltip 超出显示 */
}

/* 左列保持不变 */
.layout-left {
  flex: 5;
  display: flex;
  flex-direction: column;
  gap: 20px;
  min-height: 0;
}

/* 3. 右列：设为 Flex 容器 */
.layout-right {
  flex: 4;
  display: flex;
  flex-direction: column;
  min-height: 0; /* 核心修改：允许收缩 */
}

/* 卡片通用样式 */
.chart-card, .suggestion-card {
  background: var(--card-bg);
  border: 1px solid var(--sidebar-border);
  border-radius: 20px;
  padding: 20px 25px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.card-title {
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 1px solid rgba(128,128,128,0.1);
}
.card-title h3 {
  margin: 0; font-size: 16px; color: var(--text-color); display: flex; align-items: center; gap: 8px;
}
.card-title .el-icon { color: var(--primary-color); }

/* 图表容器 */
.flex-card { height: 50%; } 
.chart-box { flex: 1; width: 100%; min-height: 0; }

/* 建议卡片 */
.flex-grow-card {
  flex: 1;
  overflow-y: auto;
  scrollbar-width: thin;
  scrollbar-color: var(--glass-border) transparent;
}
.flex-grow-card::-webkit-scrollbar { width: 6px; }
.flex-grow-card::-webkit-scrollbar-track { background: transparent; }
.flex-grow-card::-webkit-scrollbar-thumb {
  background: var(--glass-border);
  border-radius: 999px;
}
.flex-grow-card::-webkit-scrollbar-thumb:hover { background: var(--primary-color); }
.loading-state { height: 100%; display: flex; flex-direction: column; justify-content: center; align-items: center; color: var(--text-secondary); gap: 10px; }
.suggestion-content { display: flex; flex-direction: column; gap: 15px; }

.suggestion-item { padding: 15px; border-radius: 12px; background: rgba(128,128,128,0.05); }
.suggestion-item.warning { border-left: 4px solid #e6a23c; }
.suggestion-item.success { border-left: 4px solid #67c23a; }

.item-header { display: flex; align-items: center; gap: 8px; font-weight: bold; margin-bottom: 8px; }
.warning .item-header { color: #e6a23c; }
.success .item-header { color: #67c23a; }
.suggestion-item p { margin: 0; font-size: 14px; line-height: 1.6; color: var(--text-color); }

/* 4. 右侧雷达图卡片：废弃 height:100%，改用 flex:1 完美贴合 */
.full-height-card { 
  flex: 1; /* 替代 height: 100% */
  min-height: 0; /* 防止内容撑破卡片 */
  min-width: 0; /* 防止 flex 容器内容溢出 */
  overflow: visible; /* 允许 tooltip 超出显示 */
}

/* 5. 确保内部的雷达图和详情也能自适应缩放 */
.radar-box { 
  flex: 1; 
  width: 100%; 
  min-height: 0;
  position: relative;
  z-index: 0;
}

.radar-details {
  margin-top: 10px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  max-height: 200px;
  overflow-y: auto;
  scrollbar-width: thin;
  scrollbar-color: var(--glass-border) transparent;
}
.radar-details::-webkit-scrollbar { width: 4px; }
.radar-details::-webkit-scrollbar-track { background: transparent; }
.radar-details::-webkit-scrollbar-thumb {
  background: var(--glass-border);
  border-radius: 999px;
}
.radar-details::-webkit-scrollbar-thumb:hover { background: var(--primary-color); }

.dimension-group {
  padding: 10px;
  background: rgba(128, 128, 128, 0.05);
  border-radius: 8px;
  border-left: 3px solid var(--primary-color);
}
.group-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}
.group-label {
  font-size: 12px;
  font-weight: bold;
  color: var(--text-color);
}
.group-score {
  font-size: 11px;
  color: var(--text-secondary);
  font-weight: bold;
}
.group-items {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.detail-item {
  display: flex;
  align-items: center;
  gap: 6px;
}
.detail-item .label { width: 50px; font-size: 11px; color: var(--text-secondary); text-align: right; }
.detail-item .progress-bar { flex: 1; }
.detail-item .value { width: auto; min-width: 32px; font-size: 11px; font-weight: bold; color: var(--text-color); text-align: left; }

/* 两列布局 + 低高度：仅做紧凑优化，不影响其他场景 */
@media (min-width: 1201px) and (max-height: 860px) {
  .assessment-container { padding: 14px 20px 18px; gap: 12px; }
  .overview-section { padding: 14px 18px; }
  .stats-grid { gap: 18px; }
  .stat-icon { width: 42px; height: 42px; font-size: 18px; }
  .stat-num { font-size: 22px; }

  .analysis-layout { gap: 12px; overflow: visible; overscroll-behavior: contain; }
  .analysis-layout {
    scrollbar-width: thin;
    scrollbar-color: var(--page-scrollbar-thumb, var(--glass-border)) var(--page-scrollbar-track, transparent);
  }
  .analysis-layout::-webkit-scrollbar { width: 8px; }
  .analysis-layout::-webkit-scrollbar-track {
    background: var(--page-scrollbar-track, transparent);
    border-radius: 999px;
  }
  .analysis-layout::-webkit-scrollbar-thumb {
    background: var(--page-scrollbar-thumb, var(--glass-border));
    border-radius: 999px;
    border: 2px solid transparent;
    background-clip: content-box;
  }
  .analysis-layout::-webkit-scrollbar-thumb:hover {
    background: var(--primary-color);
    background-clip: content-box;
  }
  .chart-card, .suggestion-card { padding: 12px 14px; }

  .flex-card { height: 42%; min-height: 240px; }
  .chart-box { min-height: 180px; }
  .full-height-card { min-height: 420px; }
  .radar-box { min-height: 210px; }
  .radar-details { margin-top: 8px; gap: 8px; max-height: 180px; }
  .detail-item .label { width: 48px; font-size: 10px; }
  .detail-item .value { font-size: 10px; min-width: 28px; }
  .group-label { font-size: 11px; }
  .group-score { font-size: 10px; }
  .flex-grow-card { min-height: 170px; }
}

/* 响应式兼容：仅影响小屏，不改变全屏布局 */
@media (max-width: 1200px) {
  .assessment-container { padding: 18px 18px 24px; overflow-y: auto; overflow-x: hidden; }
  .assessment-container {
    scrollbar-width: thin;
    scrollbar-color: var(--page-scrollbar-thumb, var(--glass-border)) var(--page-scrollbar-track, transparent);
  }
  .assessment-container::-webkit-scrollbar { width: 8px; }
  .assessment-container::-webkit-scrollbar-track {
    background: var(--page-scrollbar-track, transparent);
    border-radius: 999px;
  }
  .assessment-container::-webkit-scrollbar-thumb {
    background: var(--page-scrollbar-thumb, var(--glass-border));
    border-radius: 999px;
    border: 2px solid transparent;
    background-clip: content-box;
  }
  .assessment-container::-webkit-scrollbar-thumb:hover {
    background: var(--primary-color);
    background-clip: content-box;
  }
  .overview-section { flex-direction: column; align-items: stretch; gap: 16px; padding: 20px; }
  .overview-header { width: 100%; gap: 12px; }
  .stats-grid { width: 100%; display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 14px 16px; }
  .stat-box { min-width: 0; }
  .analysis-layout { flex-direction: column; overflow: visible; gap: 16px; }
  .layout-left, .layout-right { flex: none; min-height: 0; }
  .layout-left { display: contents; }
  .flex-card { order: 1; }
  .layout-right { order: 2; }
  .flex-grow-card { order: 3; }
  .chart-card, .suggestion-card { padding: 16px 18px; }
  .flex-card, .full-height-card { height: auto; min-height: 320px; }
  .radar-box, .chart-box { min-height: 240px; }
  .flex-grow-card { max-height: none; overflow: visible; }
}

@media (max-width: 992px) {
  .assessment-container { padding: 14px 14px 20px; gap: 14px; }
  .title-group h2 { font-size: 22px; }
  .custom-select-wrapper { width: 100%; justify-content: space-between; box-sizing: border-box; }
  .direction-filter { width: 170px; max-width: 62%; }
  .stat-icon { width: 42px; height: 42px; font-size: 19px; border-radius: 12px; }
  .stat-num { font-size: 22px; }
  .card-title h3 { font-size: 15px; }
  .radar-details { gap: 8px; max-height: 160px; }
  .detail-item .label { width: 46px; font-size: 10px; }
  .detail-item .value { font-size: 10px; min-width: 26px; }
  .group-header { margin-bottom: 6px; }
  .group-items { gap: 4px; }
}

@media (max-width: 768px) {
  .overview-section { padding: 16px; border-radius: 16px; }
  .title-group h2 { font-size: 20px; }
  .title-group .subtitle { font-size: 12px; }
  .stats-grid { grid-template-columns: 1fr; gap: 12px; }
  .chart-card, .suggestion-card { border-radius: 16px; padding: 14px; }
  .flex-card, .full-height-card { min-height: 280px; }
  .radar-box, .chart-box { min-height: 210px; }
  .detail-item .label { width: 54px; font-size: 12px; }
  .detail-item .value { font-size: 13px; min-width: 22px; }
}

@media (max-width: 576px) {
  .assessment-container { padding: 12px; }
  .custom-select-wrapper { padding: 4px 10px; border-radius: 14px; }
  .select-label { font-size: 12px; }
  .direction-filter { width: 150px; }
  .stat-box { gap: 10px; }
  .stat-num { font-size: 20px; }
  .stat-desc { font-size: 11px; }
  .card-title { margin-bottom: 10px; padding-bottom: 8px; }
}
</style>