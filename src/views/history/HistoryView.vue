<template>
  <div class="history-container">
    <el-card class="history-card">
      <template #header>
        <div class="header-row">
          <h3>面试历史档案</h3>
          <el-input 
            v-model="searchKey" 
            placeholder="搜索岗位..." 
            prefix-icon="Search" 
            style="width: 250px" 
          />
        </div>
      </template>

      <!-- 核心修改 1：废弃 el-table，改用自定义卡片列表 -->
      <div class="history-list">
        <!-- 核心修改 2：给整行加上 @click="goToDetail" 实现整行跳转 -->
        <div 
          v-for="item in currentPageData" 
          :key="item.id" 
          class="history-item"
          @click="goToDetail(item.id)"
        >
          <!-- 左侧：图标 + 岗位 + 日期/时长 -->
          <div class="item-left">
            <div class="item-icon" :class="item.difficulty.toLowerCase()">
              <el-icon><component :is="getJobIcon(item.job)" /></el-icon>
            </div>
            <div class="item-info">
              <span class="item-title">{{ item.jobInfo || item.job }}</span>
              <div class="item-meta">
                <span class="meta-text">岗位 {{ item.job }}</span>
                <span class="meta-divider">|</span>
                <span class="meta-text">难度 {{ getDiffText(item.difficulty) }}</span>
                <span class="meta-divider">|</span>
                <span class="meta-text"><el-icon><Calendar /></el-icon> {{ item.date }}</span>
                <span class="meta-divider">|</span>
                <span class="meta-text"><el-icon><Timer /></el-icon> 耗时 {{ item.duration }}</span>
              </div>
            </div>
          </div>

          <!-- 右侧：难度 + 面试形式 + 面试状态 + 分数 + 删除按钮 -->
          <div class="item-right">
            <!-- 难度标签 -->
            <el-tag :type="getDiffType(item.difficulty)" class="diff-tag" effect="light" round>
              {{ getDiffText(item.difficulty) }}
            </el-tag>
            
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

        <!-- 空状态展示 -->
        <el-empty v-if="currentPageData.length === 0" description="没有找到匹配的面试记录" />
      </div>

      <!-- 分页 -->
      <div class="pagination-row">
        <el-pagination 
          background 
          layout="prev, pager, next" 
          :total="filteredData.length"
          :current-page="currentPage"
          :page-size="pageSize"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router' 
// 引入需要的图标
import { Search, Calendar, Timer, Platform, Monitor, Cpu, Management, Setting, Check, Grid, DataAnalysis, Connection, PieChart } from '@element-plus/icons-vue'
import { getInterviewHistory } from '../../api/history'

const router = useRouter() 
const searchKey = ref('')

// 核心修改 4：将每页数量从 14 改为 10
const currentPage = ref(1)
const pageSize = ref(10)

const tableData = ref([])

// 获取图标逻辑 - 与创建面试弹窗中的职位图标保持一致
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

const filteredData = computed(() => {
  return tableData.value.filter(item => {
    if (!searchKey.value) return true
    const keyword = searchKey.value.toLowerCase()
    return item.job.toLowerCase().includes(keyword) || String(item.jobInfo || '').toLowerCase().includes(keyword)
  })
})

const currentPageData = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return filteredData.value.slice(start, end)
})

const handleCurrentChange = (val) => {
  currentPage.value = val
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

// 规范化难度值
const normalizeDifficulty = (difficulty) => {
  if (!difficulty) return 'Normal'
  const lower = String(difficulty).toLowerCase()
  if (lower === 'hard' || lower === '困难') return 'Hard'
  if (lower === 'easy' || lower === '简单') return 'Easy'
  return 'Normal'
}

// 获取岗位类型的中文名
const getJobTitle = (jobRole) => {
  if (!jobRole) return '未知岗位'
  const normalizedRole = String(jobRole).toLowerCase().trim()

  // 岗位名统一短中文（SRE 保留英文）
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

const fetchInterviewHistory = async () => {
  try {
    const res = await getInterviewHistory()
    console.log('面试记录接口返回:', res)
    const payload = res?.data ?? res

    if (Array.isArray(payload)) {
      tableData.value = payload.map((item) => ({
        id: item?.interviewId ?? item?.id ?? '',
        date: formatDate(item?.startTime ?? item?.date ?? item?.createTime ?? ''),
        job: getJobTitle(item?.jobRole ?? item?.job ?? ''),
        jobInfo: String(item?.jobInfo || '').trim(),
        duration: formatDuration(item?.duration),
        difficulty: normalizeDifficulty(item?.difficulty ?? item?.level),
        score: Number(item?.score ?? 0),
        mode: item?.mode ?? 'text',
        interviewStatus: item?.interviewStatus ?? 'CREATED'
      }))
      return
    }

    const list = payload?.records ?? payload?.list ?? payload?.rows ?? []
    if (Array.isArray(list)) {
      tableData.value = list.map((item) => ({
        id: item?.interviewId ?? item?.id ?? '',
        date: formatDate(item?.startTime ?? item?.date ?? item?.createTime ?? ''),
        job: getJobTitle(item?.jobRole ?? item?.job ?? ''),
        jobInfo: String(item?.jobInfo || '').trim(),
        duration: formatDuration(item?.duration),
        difficulty: normalizeDifficulty(item?.difficulty ?? item?.level),
        score: Number(item?.score ?? 0),
        mode: item?.mode ?? 'text',
        interviewStatus: item?.interviewStatus ?? 'CREATED'
      }))
    }
  } catch (error) {
    console.error('获取面试记录失败:', error)
  }
}

onMounted(() => {
  fetchInterviewHistory()
})

const goToDetail = (id) => {
  router.push(`/history/${id}`)
}

const getDiffType = (diff) => {
  if (diff === 'Hard') return 'danger'
  if (diff === 'Normal') return 'primary'
  return 'success'
}

const getDiffText = (diff) => {
  if (diff === 'Hard') return '困难'
  if (diff === 'Normal') return '一般'
  return '简单'
}

const getModeText = (mode) => {
  if (!mode) return '未知'
  const normalizedMode = String(mode).toLowerCase()
  if (normalizedMode === 'text') return '对话面试'
  if (normalizedMode === 'audio' || normalizedMode === 'voice' || normalizedMode === 'live') return '语音面试'
  if (normalizedMode === 'video') return '视频面试'
  return mode
}

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
</script>

<style scoped>
.history-container { 
  height: 100%; 
  padding: 30px; 
  box-sizing: border-box; 
  display: flex;
  flex-direction: column;
}

.history-card { 
  flex: 1;
  display: flex;
  flex-direction: column;
  background: var(--card-bg) !important; 
  border: 1px solid var(--sidebar-border) !important; 
  color: var(--text-color) !important; 
  border-radius: 20px;
}

/* 覆盖 el-card 的 body，使其可以独立滚动 */
:deep(.el-card__body) {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  padding: 20px 30px;
}

.header-row { display: flex; justify-content: space-between; align-items: center; }
.header-row h3 { margin: 0; font-size: 20px; }

/* === 核心样式：自定义卡片列表 === */
.history-list {
  flex: 1;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 6px; 
  padding-right: 10px;
  padding-top: 10px; /* === 新增：将第一条记录往下推一丢丢，增加呼吸感 === */
}

.history-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  /* 修复 2：减小上下内边距，压缩单行高度 (从 10px 改为 6px) */
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

/* 修复 3：同步缩小左侧图标尺寸以适配矮行高 */
.item-icon {
  width: 36px; /* 从 40px 缩小到 36px */
  height: 36px; 
  border-radius: 10px; 
  display: flex; align-items: center; justify-content: center; 
  font-size: 18px; /* 从 20px 缩小到 18px */
  color: white; 
}
.item-icon.hard { background: linear-gradient(135deg, #f56c6c, #c93d3d); }
.item-icon.normal { background: linear-gradient(135deg, #409eff, #2873cc); }
.item-icon.easy { background: linear-gradient(135deg, #67c23a, #479e1e); }

.item-info {
  display: flex;
  flex-direction: column;
  gap: 2px; /* 压缩文字间距 */
}

.item-title {
  font-weight: bold;
  font-size: 15px; /* 字体微缩 */
  color: var(--text-color);
}

.item-meta {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 11px; /* 字体微缩 */
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

.diff-tag { width: 60px; text-align: center; font-weight: bold; }

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

/* 分页区 */
.pagination-row { 
  margin-top: 10px; /* 进一步压缩底部空间 */
  display: flex; 
  justify-content: center; 
  padding-top: 15px;
  border-top: 1px solid var(--sidebar-border);
}

/* 分页主题适配 */
:deep(.pagination-row .el-pagination) {
  --el-pagination-bg-color: transparent;
  --el-pagination-button-bg-color: var(--card-bg);
  --el-pagination-button-color: var(--text-color);
  --el-pagination-text-color: var(--text-secondary);
  --el-pagination-hover-color: var(--primary-color);
}

:deep(.pagination-row .el-pagination .btn-prev),
:deep(.pagination-row .el-pagination .btn-next),
:deep(.pagination-row .el-pagination .el-pager li) {
  background: var(--card-bg) !important;
  border: 1px solid var(--sidebar-border);
  color: var(--text-color);
}

:deep(.pagination-row .el-pagination .el-pager li.is-active) {
  background: var(--primary-color) !important;
  border-color: var(--primary-color);
  color: #fff;
}

/* 滚动条美化 */
.history-list::-webkit-scrollbar { width: 6px; }
.history-list::-webkit-scrollbar-track { background: transparent; }
.history-list::-webkit-scrollbar-thumb { background: var(--glass-border); border-radius: 3px; }
.history-list::-webkit-scrollbar-thumb:hover { background: var(--primary-color); }

/* 输入框自适应主题 */
:deep(.el-input__wrapper) { background-color: rgba(255,255,255,0.05) !important; box-shadow: none !important; border: 1px solid var(--glass-border); }
:deep(.el-input__inner) { color: var(--text-color); }

@media (max-width: 760px) {
  .history-container {
    padding: 12px;
  }

  .history-card {
    border-radius: 14px;
  }

  :deep(.el-card__header) {
    padding: 14px;
  }

  :deep(.el-card__body) {
    padding: 12px 14px;
  }

  .header-row {
    flex-wrap: wrap;
    gap: 10px;
    align-items: flex-start;
  }

  .header-row h3 {
    font-size: 16px;
    line-height: 1.35;
  }

  .header-row :deep(.el-input) {
    width: 100% !important;
  }

  .history-list {
    padding-right: 2px;
    gap: 10px;
  }

  .history-item {
    flex-direction: column;
    align-items: stretch;
    gap: 10px;
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
    font-size: 16px;
    line-height: 1.3;
    word-break: break-word;
  }

  .item-meta {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 4px 10px;
    font-size: 12px;
  }

  .meta-divider {
    display: none;
  }

  .item-right {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    align-items: center;
  }

  .diff-tag,
  .mode-tag,
  .status-tag,
  .score-block {
    width: auto;
  }

  .score-block {
    margin-left: auto;
    text-align: right;
  }

  .score-val {
    font-size: 20px;
  }

  .pagination-row {
    margin-top: 8px;
    padding-top: 10px;
    justify-content: flex-start;
    overflow-x: auto;
  }

  .pagination-row :deep(.el-pagination) {
    flex-wrap: nowrap;
    min-width: max-content;
  }
}

@media (max-width: 560px) {
  .history-container {
    padding: 8px;
  }

  :deep(.el-card__header) {
    padding: 12px;
  }

  :deep(.el-card__body) {
    padding: 10px 12px;
  }

  .header-row h3 {
    font-size: 14px;
  }

  .item-icon {
    width: 32px;
    height: 32px;
    font-size: 16px;
  }

  .item-title {
    font-size: 14px;
  }

  .item-meta {
    grid-template-columns: 1fr;
    font-size: 11px;
  }

  .item-right {
    display: grid;
    grid-template-columns: repeat(3, auto);
    gap: 6px;
  }

  .score-block {
    grid-column: 3;
    justify-self: end;
  }

  .score-val {
    font-size: 18px;
  }
}
</style>