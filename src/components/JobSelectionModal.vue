<template>
  <el-dialog
    v-model="visible"
    :show-close="true"
    title="新的面试模拟"
    width="90%"
    style="max-width: 550px; border-radius: 12px;margin-top: 13vh !important;"
    align-center
    
  >
    <!-- 包裹层：限制高度，超出滚动 -->
    <div class="modal-scroll-body">
      <div class="modal-content">
        <!-- 步骤 1: 选择岗位 -->
        <h3 class="section-title">1. 选择面试方向</h3>
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

        <!-- 步骤 2: 选择难度 -->
        <h3 class="section-title">2. 选择面试难度</h3>
        <div class="difficulty-options">
          <div 
            v-for="diff in difficulties" 
            :key="diff.value"
            class="diff-chip"
            :class="{ active: selectedDifficulty === diff.value }"
            @click="selectedDifficulty = diff.value"
          >
            {{ diff.label }}
          </div>
        </div>

        <!-- 步骤 3: 上传简历 -->
        <h3 class="section-title">3. 上传简历 (可选)</h3>
        
        <div class="upload-container">
          <!-- A. 已上传简历状态 -->
          <div v-if="hasUploadedResume && !selectedFile" class="uploaded-resume-card">
            <div class="resume-card-content">
              <el-icon :size="32" class="file-icon"><Document /></el-icon>
              <div class="file-details">
                <h3>{{ uploadedResume.fileName }}</h3>
                <p>文件大小: {{ uploadedResume.fileSize }}</p>
                <p>上传时间: {{ uploadedResume.uploadTime }}</p>
              </div>
            </div>
            <!-- 上传按钮 -->
            <div class="small-upload-btn">
              <el-upload
                class="resume-uploader-small"
                action="#"
                :auto-upload="false"
                :limit="1"
                :show-file-list="false" 
                :on-change="handleFileChange"
                accept=".pdf,.doc,.docx"
              >
                <el-button type="primary" size="small">
                  <el-icon><UploadFilled /></el-icon>
                  更换简历
                </el-button>
              </el-upload>
            </div>
          </div>

          <!-- B. 文件预览状态 -->
          <div v-else-if="selectedFile" class="file-preview-box">
            <div class="file-icon-large">
              <el-icon v-if="selectedFile.name.endsWith('.pdf')" color="#f56c6c"><Document /></el-icon>
              <el-icon v-else color="#409eff"><Document /></el-icon>
            </div>
            <div class="file-name">{{ selectedFile.name }}</div>
            <div class="file-actions">
              <el-button type="danger" link size="small" @click="handleFileRemove">删除文件</el-button>
            </div>
          </div>

          <!-- C. 上传框状态 -->
          <el-upload
            v-else
            class="resume-uploader"
            drag
            action="#"
            :auto-upload="false"
            :limit="1"
            :show-file-list="false" 
            :on-change="handleFileChange"
            accept=".pdf,.doc,.docx"
          >
            <el-icon class="el-icon--upload"><upload-filled /></el-icon>
            <div class="el-upload__text">
              点击或拖拽上传简历 <br>
              <span style="font-size: 12px; color: #999;">支持 PDF, Word</span>
            </div>
          </el-upload>
        </div>
      </div>
    </div>
    
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="visible = false">取消</el-button>
        <el-button type="primary" :disabled="!selectedJob" @click="confirm" round>
          确定开始
        </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { Monitor, Platform, Cpu, UploadFilled, Document, Setting, Check, Grid, DataAnalysis, Connection, PieChart, Management } from '@element-plus/icons-vue'
import { getUserStorage } from '../utils/storage'

const visible = ref(false)
const selectedJob = ref('')
const selectedDifficulty = ref('normal')
const selectedFile = ref(null)
const hasUploadedResume = ref(false)
const uploadedResume = ref({
  fileName: '',
  fileSize: '',
  uploadTime: ''
})

// 从本地存储中获取简历信息
const checkResumeStatus = () => {
  try {
    // 从本地存储中获取简历信息
    const storedResumeInfo = getUserStorage('resumeInfo');
    if (storedResumeInfo) {
      const resumeInfo = JSON.parse(storedResumeInfo);
      if (resumeInfo.hasResume) {
        hasUploadedResume.value = true;
        uploadedResume.value = {
          fileName: resumeInfo.fileName,
          fileSize: resumeInfo.fileSize,
          uploadTime: resumeInfo.uploadTime
        };
      } else {
        // 未上传状态
        hasUploadedResume.value = false;
      }
    } else {
      // 本地存储中没有简历信息
      hasUploadedResume.value = false;
    }
  } catch (error) {
    console.error('获取简历信息失败:', error);
    // 出错时默认未上传状态
    hasUploadedResume.value = false;
  }
}

onMounted(() => {
  checkResumeStatus() // 组件加载时检查一次
});

// 监听模态框打开时重新检查简历状态（仅当从关闭变为打开时）
watch(visible, (newVal) => {
  if (newVal === true) {
    checkResumeStatus()
  }
});

const jobs = [
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

const difficulties = [
  { label: '简单', value: 'easy' },
  { label: '一般', value: 'normal' },
  { label: '困难', value: 'hard' }
]

const selectJob = (id) => selectedJob.value = id
const handleFileChange = (uploadFile) => { selectedFile.value = uploadFile.raw }
const handleFileRemove = () => { selectedFile.value = null }
const emit = defineEmits(['confirmed'])

const confirm = () => {
  visible.value = false
  emit('confirmed', { 
    jobRole: selectedJob.value, 
    difficulty: selectedDifficulty.value,
    resumeFile: selectedFile.value 
  })
}

const open = () => {
  selectedJob.value = ''
  selectedDifficulty.value = 'normal'
  selectedFile.value = null
  visible.value = true
  checkResumeStatus() // 打开时重新检查简历状态
}

defineExpose({ open })
</script>

<style scoped>
/* 滚动容器：关键修复 */
.modal-scroll-body {
  height: 50vh; /* 限制最大高度，防止撑破屏幕 */
  overflow-y: auto; /* 超出则滚动 */
  padding: 0 5px;   /* 预留一点滚动条位置 */
}

.section-title { margin: 10px 0 8px; font-size: 14px; font-weight: bold; color: var(--modal-text); }

/* 岗位卡片 */
.job-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-bottom: 15px; }
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
  flex: 1; text-align: center; padding: 6px; border-radius: 4px;
  background: var(--modal-hover-bg); border: 1px solid var(--glass-border); color: var(--modal-text); font-size: 13px; cursor: pointer;
}
.diff-chip.active { background: var(--primary-color); color: white; border-color: var(--primary-color); }

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

.modal-scroll-body::-webkit-scrollbar-thumb:hover {
  background: var(--primary-color);
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