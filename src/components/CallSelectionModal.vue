<template>
  <el-dialog
    v-model="visible"
    :show-close="true"
    title="新的面试模拟"
    width="90%"
    style="max-width: 550px; border-radius: 12px;"
    align-center
  >
    <div class="modal-scroll-body">
      <div class="modal-content">
        <!-- 修改点：步骤 1 标题和选项 -->
        <h3 class="section-title">1. 选择面试模式</h3>
        <div class="call-type-options">
          <div 
            v-for="type in callTypes" 
            :key="type.value"
            class="call-type-chip"
            :class="{ active: selectedCallType === type.value }"
            @click="selectedCallType = type.value"
          >
            <el-icon :size="20" :color="selectedCallType === type.value ? '#ffffff' : '#409eff'">
              <component :is="type.icon" />
            </el-icon>
            <span>{{ type.label }}</span>
          </div>
        </div>

        <h3 class="section-title">2. 选择面试方向</h3>
        <div class="job-grid">
          <div 
            v-for="job in jobs" 
            :key="job.id" 
            class="job-card"
            :class="{ active: selectedJob === job.id }"
            @click="selectJob(job.id)"
          >
            <el-icon :size="28" :color="job.color"><component :is="job.icon" /></el-icon>
            <span class="job-name">{{ job.name }}</span>
          </div>
        </div>

        <h3 class="section-title">3. 选择面试难度</h3>
        <div class="difficulty-options">
          <div 
            v-for="diff in difficulties" 
            :key="diff.value"
            class="diff-chip"
            :class="{ active: selectedDifficulty === diff.value }"
            @click="selectedDifficulty = diff.value"
          >
            <el-icon size="16" style="margin-right: 6px;"><component :is="diff.icon" /></el-icon>
            <span>{{ diff.label }}</span>
          </div>
        </div>

        <h3 class="section-title">4. 岗位信息</h3>
        <el-input
          v-model="jobInfo"
          type="textarea"
          :rows="2"
          placeholder="请输入岗位相关信息（必填）"
          maxlength="500"
          show-word-limit
        />

        <h3 class="section-title">5. 面试官风格</h3>
        <div class="style-options">
          <div 
            v-for="style in interviewStyles" 
            :key="style.value"
            class="style-chip"
            :class="{ active: selectedInterviewStyle === style.value }"
            @click="selectedInterviewStyle = style.value"
          >
            {{ style.label }}
          </div>
        </div>

        <!-- 简历状态标识 -->
        <div class="resume-status-container">
          <div v-if="hasUploadedResume" class="resume-status success">
            <el-icon class="status-icon"><DocumentCopy /></el-icon>
            <div class="status-text">
              <span class="status-label">✓ 简历已上传</span>
              <span class="status-tip">系统将使用您上传的简历进行面试评估</span>
            </div>
          </div>
          <div v-else class="resume-status warning">
            <el-icon class="status-icon"><DocumentDelete /></el-icon>
            <div class="status-text">
              <span class="status-label">未上传简历</span>
              <span class="status-tip">建议先上传简历以获得更准确的面试评估</span>
            </div>
            <el-button type="primary" link class="goto-resume-btn" @click="goToResume">
              去上传
              <el-icon style="margin-left: 4px;"><ArrowRight /></el-icon>
            </el-button>
          </div>
        </div>

      </div>
    </div>
    
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="visible = false">取消</el-button>
        <el-button type="primary" :disabled="!selectedCallType || !selectedJob || !jobInfo.trim() || !hasUploadedResume" @click="confirm" round>
          确定开始
        </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getResumeDownloadUrl } from '../api/resume'
import { getUserStorage } from '../utils/storage'
// 引入图标
import { Monitor, Platform, Cpu, VideoCamera, Microphone, ChatDotRound, Sunny, Aim, Lightning, DocumentCopy, DocumentDelete, ArrowRight, Setting, Check, Grid, DataAnalysis, Connection, PieChart, Management } from '@element-plus/icons-vue'

const router = useRouter()

const visible = ref(false)
const selectedCallType = ref('')
const selectedJob = ref('')
const selectedDifficulty = ref('medium')
const jobInfo = ref('')
const selectedInterviewStyle = ref('standard')
const hasUploadedResume = ref(false)

// 修改点：添加了对话模式选项
const callTypes =[
  { value: 'text', label: '对话模式', icon: ChatDotRound },
  { value: 'audio', label: '语音模式', icon: Microphone },
  { value: 'video', label: '视频模式', icon: VideoCamera }
]

const jobs =[
  { id: 'java_backend', name: 'Java 后端', icon: Platform, color: '#e6a23c' },
  { id: 'python_backend', name: 'Python 后端', icon: Cpu, color: '#1890ff' },
  { id: 'golang_backend', name: 'Golang 后端', icon: Management, color: '#409eff' },
  { id: 'web_frontend', name: 'Web 前端', icon: Monitor, color: '#409eff' },
  { id: 'devops', name: 'DevOps', icon: Setting, color: '#67c23a' },
  { id: 'software_test_engineer', name: '软件测试工程师', icon: Check, color: '#a6e22e' },
  { id: 'system_architect', name: '系统架构师', icon: Grid, color: '#f56c6c' },
  { id: 'data_engineer', name: '数据工程师', icon: DataAnalysis, color: '#1890ff' },
  { id: 'site_reliability_engineer', name: 'SRE', icon: Connection, color: '#9c27b0' },
  { id: 'machine_learning_engineer', name: '机器学习工程师', icon: PieChart, color: '#ff7875' }
]

const difficulties =[
  { label: '简单', value: 'easy', icon: Sunny },
  { label: '一般', value: 'medium', icon: Aim },
  { label: '困难', value: 'hard', icon: Lightning }
]

const interviewStyles = [
  { label: '标准专业型', value: 'standard' },
  { label: '亲和鼓励型', value: 'friendly' },
  { label: '压力挑战型', value: 'aggressive' },
  { label: '技术专家型', value: 'expert' }
]

const getJobNameById = (id) => jobs.find((job) => job.id === id)?.name || ''

const selectJob = (id) => selectedJob.value = id
const emit = defineEmits(['confirmed'])

const confirm = async () => {
  const trimmedJobInfo = jobInfo.value.trim()
  if (!trimmedJobInfo) {
    ElMessage.warning('请填写岗位信息')
    return
  }

  visible.value = false
  emit('confirmed', { 
    callType: selectedCallType.value,
    jobRole: selectedJob.value, 
    difficulty: selectedDifficulty.value,
    jobInfo: trimmedJobInfo,
    interviewerStyle: selectedInterviewStyle.value
  })
}

const checkResumeStatus = async () => {
  try {
    // 检查 localStorage 中的缓存，这是唯一的真实来源
    const stored = JSON.parse(getUserStorage('resumeInfo') || '{}')
    if (stored?.hasResume) {
      hasUploadedResume.value = true
    } else {
      // 缓存中明确表示未上传，不再查询API
      hasUploadedResume.value = false
    }
  } catch (error) {
    console.warn('检测简历上传状态失败', error)
    // 出错时保守处理：认为未上传
    hasUploadedResume.value = false
  }
}

const goToResume = () => {
  visible.value = false
  router.push('/resume')
}

const open = () => {
  selectedCallType.value = ''
  selectedJob.value = ''
  selectedDifficulty.value = 'medium'
  jobInfo.value = ''
  selectedInterviewStyle.value = 'standard'
  visible.value = true
  checkResumeStatus() // 打开标签时检测简历状态
}

onMounted(() => {
  checkResumeStatus() // 组件加载时检测一次
})

// 监听模态框打开时重新检查简历状态（仅当从关闭变为打开时）
watch(visible, (newVal) => {
  if (newVal === true) {
    checkResumeStatus()
  }
})

// 默认将岗位信息填充为已选岗位名；若用户已手动修改内容则不强制覆盖。
watch(selectedJob, (newJobId, oldJobId) => {
  const newJobName = getJobNameById(newJobId)
  const oldJobName = getJobNameById(oldJobId)
  const currentJobInfo = jobInfo.value.trim()

  if (!newJobName) {
    if (currentJobInfo === oldJobName) {
      jobInfo.value = ''
    }
    return
  }

  if (!currentJobInfo || currentJobInfo === oldJobName) {
    jobInfo.value = newJobName
  }
})

defineExpose({ open })
</script>

<style scoped>
/* 滚动容器：关键修复 */
.modal-scroll-body {
  height: 60vh; /* 增加最大高度，避免显示滚动条 */
  overflow-y: auto; /* 超出则滚动 */
  padding: 0 5px;   /* 预留一点滚动条位置 */
}

.section-title { margin: 10px 0 8px; font-size: 14px; font-weight: bold; color: var(--modal-text); }

/* 通话方式选择 */
.call-type-options { display: flex; gap: 10px; margin-bottom: 15px; }
.call-type-chip {
  flex: 1; display: flex; align-items: center; justify-content: center; gap: 6px;
  padding: 10px; border-radius: 8px;
  background: var(--modal-hover-bg); border: 1px solid var(--glass-border); color: var(--modal-text); font-size: 13px; cursor: pointer;
  transition: all 0.2s;
}
.call-type-chip:hover { background: var(--modal-hover-bg); border-color: var(--primary-color); }
.call-type-chip.active { background: var(--primary-color); color: white; border-color: var(--primary-color); }

/* 岗位卡片 */
.job-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; margin-bottom: 15px; }
.job-card {
  background: var(--modal-hover-bg); border: 1px solid var(--glass-border); border-radius: 8px;
  padding: 12px 5px; display: flex; flex-direction: column; align-items: center; gap: 6px;
  cursor: pointer; transition: all 0.2s;
}
.job-card:hover { background: var(--modal-hover-bg); border-color: var(--primary-color); }
.job-card.active { background: rgba(24, 144, 255, 0.1); border-color: var(--primary-color); box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
.job-name { font-size: 13px; font-weight: 600; color: var(--modal-text); }
.job-card.active .job-name { color: var(--primary-color); }

/* 难度选择 */
.difficulty-options { display: flex; gap: 10px; margin-bottom: 15px; }
.diff-chip {
  flex: 1; 
  /* 新增 flex 居中对齐，让图标和文字横向排列 */
  display: flex; align-items: center; justify-content: center; 
  padding: 8px 6px; /* 稍微加高一点以容纳图标 */
  border-radius: 6px;
  background: var(--modal-hover-bg); 
  border: 1px solid var(--glass-border); 
  color: var(--modal-text); 
  font-size: 13px; 
  cursor: pointer;
  transition: all 0.2s;
}
.diff-chip.active { background: var(--primary-color); color: white; border-color: var(--primary-color); }

/* 面试官风格样式 */
.style-options { display: flex; gap: 10px; margin-bottom: 15px; }
.style-chip {
  flex: 1;
  display: flex; align-items: center; justify-content: center;
  padding: 8px 6px;
  border-radius: 6px;
  background: var(--modal-hover-bg);
  border: 1px solid var(--glass-border);
  color: var(--modal-text);
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s;
}
.style-chip:hover { background: var(--modal-hover-bg); border-color: var(--primary-color); }
.style-chip.active { background: var(--primary-color); color: white; border-color: var(--primary-color); }

/* 上传区域 */
.upload-container {
  height: 140px; /*稍微减小高度*/
  position: relative;
  margin-bottom: 10px; /* 增加底部边距，防止贴到底部 */
}
:deep(.el-upload), :deep(.el-upload-dragger) { height: 100%; width: 100%; }
:deep(.el-upload-dragger) {
  display: flex; flex-direction: column; justify-content: center; align-items: center;
  background-color: var(--modal-hover-bg); border: 1px dashed var(--glass-border);
  color: var(--modal-text) !important;
}
:deep(.el-upload__text) {
  color: var(--modal-text) !important;
}
:deep(.el-upload__text span) {
  color: var(--text-secondary) !important;
}

/* 已上传简历卡片 */
.uploaded-resume-card {
  height: 100%; border: 1px solid var(--glass-border); background: var(--modal-hover-bg);
  border-radius: 8px; padding: 15px; display: flex; flex-direction: column; gap: 10px;
}

.resume-card-content {
  display: flex; align-items: center; gap: 12px;
}

.file-icon {
  color: var(--primary-color); flex-shrink: 0;
}

.file-details {
  flex: 1;
}

.file-details h3 {
  margin: 0 0 4px 0; font-size: 14px; font-weight: bold; color: var(--modal-text);
}

.file-details p {
  margin: 2px 0; font-size: 12px; color: var(--text-secondary);
}

.small-upload-btn {
  display: flex; justify-content: flex-start;
}

.resume-uploader-small {
  margin-top: 5px;
}

/* 文件预览 */
.file-preview-box {
  height: 100%; border: 1px dashed var(--primary-color); background: rgba(24, 144, 255, 0.1);
  border-radius: 6px; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 8px;
}
.file-icon-large { font-size: 40px; }
.file-name { font-size: 13px; color: var(--modal-text); font-weight: bold; }

/* 滚动条样式 */
.modal-scroll-body::-webkit-scrollbar {
  width: 6px;
}

.modal-scroll-body::-webkit-scrollbar-track {
  background: var(--modal-hover-bg);
  border-radius: 3px;
}

.modal-scroll-body::-webkit-scrollbar-thumb {
  background: var(--glass-border);
  border-radius: 3px;
}

/* 简历状态标识 */
.resume-status-container {
  margin-top: 15px;
  margin-bottom: 10px;
}

.resume-status {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  border-radius: 8px;
  border: 1px solid;
  transition: all 0.3s ease;
}

.resume-status.success {
  background: rgba(103, 194, 58, 0.08);
  border-color: rgba(103, 194, 58, 0.3);
}

.resume-status.warning {
  background: rgba(230, 162, 60, 0.08);
  border-color: rgba(230, 162, 60, 0.3);
  position: relative;
}

.resume-status .status-icon {
  flex-shrink: 0;
  font-size: 24px;
}

.resume-status.success .status-icon {
  color: #67c23a;
}

.resume-status.warning .status-icon {
  color: #e6a23c;
}

.status-text {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.status-label {
  font-size: 14px;
  font-weight: 600;
  color: var(--modal-text);
}

.status-text .status-label {
  display: block;
}

.status-tip {
  font-size: 12px;
  color: var(--text-secondary);
  display: block;
}

.goto-resume-btn {
  flex-shrink: 0;
  padding: 6px 12px;
  font-size: 13px;
}


.modal-scroll-body::-webkit-scrollbar-thumb:hover {
  background: var(--primary-color);
}

/* 岗位信息输入框样式 */
:deep(.el-textarea__inner) {
  background-color: var(--modal-hover-bg) !important;
  border-color: var(--glass-border) !important;
  color: var(--modal-text) !important;
}

:deep(.el-textarea__inner::placeholder),
:deep(.el-input__inner::placeholder) {
  color: var(--text-secondary) !important;
}

:deep(.el-textarea__inner:focus),
:deep(.el-input__inner:focus) {
  background-color: var(--modal-hover-bg) !important;
  border-color: var(--primary-color) !important;
}

:deep(.el-input-group__suffix) {
  background-color: var(--modal-hover-bg) !important;
}

:deep(.el-character-counter) {
  color: var(--text-secondary) !important;
}

@media (max-width: 760px) {
  .modal-scroll-body {
    height: 62vh;
    padding: 0 2px;
  }

  .section-title {
    margin: 8px 0 6px;
    font-size: 13px;
  }

  .call-type-options {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 8px;
    margin-bottom: 12px;
  }

  .call-type-chip {
    min-height: 92px;
    padding: 8px 4px;
    flex-direction: column;
    gap: 6px;
  }

  .call-type-chip span {
    font-size: 13px;
    text-align: center;
    line-height: 1.25;
    white-space: normal;
    word-break: keep-all;
  }

  .job-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 8px;
    margin-bottom: 12px;
  }

  .job-card {
    padding: 10px 6px;
    min-height: 94px;
    gap: 5px;
  }

  .job-name {
    font-size: 12px;
    text-align: center;
    line-height: 1.25;
    word-break: keep-all;
  }

  .difficulty-options,
  .style-options {
    gap: 8px;
    margin-bottom: 12px;
  }

  .diff-chip,
  .style-chip {
    min-height: 36px;
    font-size: 12px;
    padding: 7px 6px;
    line-height: 1.2;
    text-align: center;
  }

  .style-options {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .resume-status {
    padding: 10px 12px;
    gap: 10px;
    flex-wrap: wrap;
  }

  .status-label {
    font-size: 13px;
  }

  .status-tip {
    font-size: 11px;
    line-height: 1.35;
  }

  .goto-resume-btn {
    margin-left: auto;
    padding: 4px 0;
  }

  .dialog-footer {
    width: 100%;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
  }

  .dialog-footer .el-button {
    margin-left: 0 !important;
    width: 100%;
  }
}

@media (max-width: 480px) {
  .modal-scroll-body {
    height: 64vh;
  }

  .call-type-chip {
    min-height: 88px;
    padding: 7px 3px;
  }

  .call-type-chip span {
    font-size: 12px;
  }

  .job-card {
    min-height: 90px;
    padding: 9px 5px;
  }

  .job-name {
    font-size: 11px;
  }

  .diff-chip,
  .style-chip {
    font-size: 11px;
  }
}
</style>

<style>
/* 弹窗样式 */
.el-dialog {
  background: var(--modal-bg) !important;
  display: flex;
  flex-direction: column;
  margin-top: 8vh !important;
  color: var(--modal-text) !important;
}
.el-dialog__body {
  padding: 20px 20px 10px;
  color: var(--modal-text) !important;
}
.el-dialog__title {
  color: var(--modal-text) !important;
  font-weight: bold;
}
.el-dialog__headerbtn .el-dialog__close {
  color: var(--text-color) !important;
  font-size: 16px !important;
  opacity: 1 !important;
  text-shadow: 0 0 2px rgba(0, 0, 0, 0.3) !important;
  background-color: var(--modal-hover-bg) !important;
  border-radius: 50% !important;
  width: 24px !important;
  height: 24px !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  margin-right: 10px !important;
  margin-top: 5px !important;
  border: 1px solid var(--glass-border) !important;
}
</style>