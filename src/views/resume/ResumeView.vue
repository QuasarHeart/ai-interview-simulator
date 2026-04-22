<template>
  <div :class="['resume-layout', { 'is-empty': !hasResume }]">
    <!-- 所有的注释必须放在这唯一的根 div 内部！防止 Vue 动画引擎崩溃白屏 -->

    <!-- 左侧：我的简历区 -->
    <div class="layout-left">
      <div class="resume-view-container">
        
        <!-- 未上传简历状态 -->
        <div v-if="!hasResume" class="empty-state">
          <div class="start-card">
            <el-icon :size="60" class="start-icon"><Document /></el-icon>
            <h2>上传简历</h2>
            <p>请上传您的简历，支持 PDF 格式</p>
            <el-upload
              class="upload-btn"
              :auto-upload="false"
              accept=".pdf"
              :on-change="handleFileChange"
            >
              <el-button type="primary" size="large" round class="upload-button">
                <el-icon><UploadFilled /></el-icon>
                选择文件
              </el-button>
            </el-upload>
          </div>
        </div>

        <!-- 已上传简历状态 -->
        <div v-else class="resume-display">
          <div class="resume-header">
            <h2>您的简历</h2>
            <div class="header-actions">
              <el-upload
                :auto-upload="false"
                accept=".pdf"
                :on-change="handleFileChange"
                :show-file-list="false"
              >
                <el-button type="primary" size="default">
                  <el-icon><UploadFilled /></el-icon> 重新上传
                </el-button>
              </el-upload>
              <el-button v-if="showPreview" type="info" size="default" @click="closePreview">
                <el-icon><Close /></el-icon> 关闭预览
              </el-button>
            </div>
          </div>
          
          <!-- 预览区域 -->
          <div v-if="showPreview" class="resume-preview">
            <div v-if="isPDF" class="pdf-preview">
              <embed :src="previewUrl" type="application/pdf" width="100%" height="600px" />
            </div>
            <div v-else-if="previewUrl" class="word-preview">
              <div class="word-content" v-html="previewUrl"></div>
            </div>
            <div v-else class="file-preview">
              <el-icon :size="60" class="file-icon"><Document /></el-icon>
              <p>文件类型不支持预览</p>
            </div>
          </div>
          
          <!-- 简历卡片 -->
          <div class="resume-card" @click="previewResume">
            <div class="resume-card-content">
              <el-icon :size="32" class="file-icon"><Document /></el-icon>
              <div class="file-details">
                <h3>{{ resumeFileName }}</h3>
                <p>文件大小: {{ resumeFileSize }}</p>
                <p>上传时间: {{ resumeUploadTime }}</p>
              </div>
              <div class="preview-icon">
                <el-icon><View /></el-icon>
                <span>点击预览</span>
              </div>
            </div>
          </div>
          
          <!-- AI评价 -->
          <div class="ai-evaluation">
            <div class="ai-evaluation-header">
              <el-icon :size="24" class="ai-icon"><Cpu /></el-icon>
              <h3>AI 简历评价</h3>
            </div>
            <div class="ai-evaluation-content">
              <div v-if="analysisLoading" class="evaluation-loading">正在生成简历评价...</div>
              <div v-else-if="analysisError" class="evaluation-empty">{{ analysisError }}</div>
              <template v-else>
                <div class="evaluation-section">
                <h4>优点</h4>
                  <ul v-if="resumeEvaluation.strengths.length">
                    <li v-for="(item, index) in resumeEvaluation.strengths" :key="`strength-${index}`">{{ item }}</li>
                  </ul>
                  <div v-else class="evaluation-empty">暂无优点分析</div>
                </div>
                <div class="evaluation-section">
                  <h4>缺点</h4>
                  <ul v-if="resumeEvaluation.weaknesses.length">
                    <li v-for="(item, index) in resumeEvaluation.weaknesses" :key="`weakness-${index}`">{{ item }}</li>
                  </ul>
                  <div v-else class="evaluation-empty">暂无缺点分析</div>
                </div>
                <div class="evaluation-section">
                  <h4>建议</h4>
                  <ul v-if="resumeEvaluation.suggestions.length">
                    <li v-for="(item, index) in resumeEvaluation.suggestions" :key="`suggestion-${index}`">{{ item }}</li>
                  </ul>
                  <div v-else class="evaluation-empty">暂无建议</div>
                </div>
              </template>
            </div>
          </div>
        </div>

      </div>
    </div>

    <!-- 右侧：优秀简历库 -->
    <div class="layout-right">
      <div class="excellent-library">
        
        <div class="library-header">
          <div class="header-title">
            <el-icon class="star-icon"><Star /></el-icon>
            <h2>优秀简历模板</h2>
          </div>
          <p class="lib-desc">精选可直接参考的简历模板，覆盖开发与测试岗位，重点学习版式和项目表达方式。</p>
        </div>

        <div class="library-list">
          <div 
            v-for="item in excellentResumes" 
            :key="item.id" 
            class="excellent-card"
            @click="previewExcellent(item)"
          >
            <div class="card-icon" :style="{ color: item.color, background: `rgba(255,255,255,0.05)` }">
              <el-icon :size="24"><component :is="item.icon" /></el-icon>
            </div>
            <div class="card-info">
              <h4 class="job-title">{{ item.title }}</h4>
              <p v-if="item.author" class="author">{{ item.author }}</p>
            </div>
            <div class="view-btn">
              <el-icon><View /></el-icon>
            </div>
          </div>
        </div>

      </div>
    </div>

    <!-- 优秀简历的预览弹窗 -->
    <el-dialog
      v-model="showExcellentPreview"
      width="76%"
      class="theme-adapt-dialog"
      align-center
      @closed="closeExcellentPreview"
    >
      <div class="resume-preview-area">
        <div class="pdf-preview excellent-pdf-preview">
          <embed :src="excellentPreviewUrl" type="application/pdf" width="100%" height="100%" />
        </div>
      </div>
    </el-dialog>

  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, markRaw } from 'vue';
import { UploadFilled, Document, Cpu, View, Close, 
         Star, Platform, Monitor 
        } from '@element-plus/icons-vue';
import { ElMessage } from 'element-plus'
import { getResumeUploadUrl, uploadResumeBinary, getResumeDownloadUrl, fetchResumeBlob, getResumeAnalysis } from '../../api/resume'
import { getUserStorage, setUserStorage } from '../../utils/storage'

const resumeAssetModules = import.meta.glob('../../../resume/*.pdf', {
  eager: true,
  import: 'default'
})

// 模拟已上传简历的状态
const hasResume = ref(false);
const resumeFileName = ref('resume.pdf');
const resumeFileSize = ref('1.2 MB');
const resumeUploadTime = ref('2026-03-02 10:00');

// 预览相关变量
const showPreview = ref(false);
const isPDF = ref(false);
const previewUrl = ref('');
const resumeFile = ref(null);
const resumeRemoteUrl = ref('');
const localPreviewObjectUrl = ref('');
const analysisLoading = ref(false)
const analysisError = ref('')
const resumeEvaluation = ref({
  strengths: [],
  suggestions: [],
  weaknesses: []
})

// === 优秀简历库数据 ===
const showExcellentPreview = ref(false)
const excellentPreviewUrl = ref('')
const excellentPreviewTitle = ref('')
const excellentPreviewObjectUrl = ref('')

const iconPool = [markRaw(Platform), markRaw(Monitor), markRaw(Cpu)]
const colorPool = ['#e6a23c', '#409eff', '#f56c6c', '#67c23a', '#00bcd4', '#9c27b0', '#ff9800']

const getResumeDisplayTitle = (path) => {
  const fileName = path.split('/').pop() || '简历'
  return decodeURIComponent(fileName).replace(/\.pdf$/i, '')
}

const buildExcellentResumes = () => {
  return Object.entries(resumeAssetModules)
    .map(([path, url], index) => ({
      id: index + 1,
      title: getResumeDisplayTitle(path),
      author: '',
      icon: iconPool[index % iconPool.length],
      color: colorPool[index % colorPool.length],
      fileType: 'pdf',
      url
    }))
    .sort((a, b) => a.title.localeCompare(b.title, 'zh-CN'))
}

const excellentResumes = ref(buildExcellentResumes())

// 预览优秀简历
const previewExcellent = async (resume) => {
  if (!resume?.url) {
    ElMessage.warning('未找到可预览的简历文件')
    return
  }

  if (excellentPreviewObjectUrl.value) {
    URL.revokeObjectURL(excellentPreviewObjectUrl.value)
    excellentPreviewObjectUrl.value = ''
  }

  excellentPreviewTitle.value = `${resume.title} - ${resume.author}`

  try {
    const blob = await fetchResumeBlob(resume.url)
    excellentPreviewObjectUrl.value = URL.createObjectURL(blob)
    excellentPreviewUrl.value = `${excellentPreviewObjectUrl.value}#toolbar=0&navpanes=0`
    showExcellentPreview.value = true
  } catch (error) {
    excellentPreviewUrl.value = ''
    ElMessage.error('优秀简历预览失败，请稍后重试')
    console.error('优秀简历预览失败:', error)
  }
}

const closeExcellentPreview = () => {
  showExcellentPreview.value = false
  if (excellentPreviewObjectUrl.value) {
    URL.revokeObjectURL(excellentPreviewObjectUrl.value)
    excellentPreviewObjectUrl.value = ''
  }
  excellentPreviewUrl.value = ''
}

onBeforeUnmount(() => {
  if (excellentPreviewObjectUrl.value) {
    URL.revokeObjectURL(excellentPreviewObjectUrl.value)
    excellentPreviewObjectUrl.value = ''
  }
})

const withResumeVersion = (url) => {
  if (!url || typeof url !== 'string') return url

  try {
    const parsed = new URL(url, window.location.origin)
    parsed.searchParams.set('_v', String(Date.now()))
    return parsed.toString()
  } catch {
    return `${url}${url.includes('?') ? '&' : '?'}_v=${Date.now()}`
  }
}

const extractNameFromUrl = (url) => {
  if (!url || typeof url !== 'string') return ''
  try {
    const pathname = new URL(url, window.location.origin).pathname
    const segments = pathname.split('/').filter(Boolean)
    return decodeURIComponent(segments[segments.length - 1] || '')
  } catch {
    return ''
  }
}

const loadResumeAnalysis = async () => {
  if (!hasResume.value) {
    analysisError.value = ''
    resumeEvaluation.value = { strengths: [], suggestions: [], weaknesses: [] }
    return
  }

  analysisLoading.value = true
  analysisError.value = ''
  try {
    const data = await getResumeAnalysis()
    resumeEvaluation.value = {
      strengths: Array.isArray(data?.strengths) ? data.strengths : [],
      suggestions: Array.isArray(data?.suggestions) ? data.suggestions : [],
      weaknesses: Array.isArray(data?.weaknesses) ? data.weaknesses : []
    }

    const totalCount =
      resumeEvaluation.value.strengths.length +
      resumeEvaluation.value.suggestions.length +
      resumeEvaluation.value.weaknesses.length

    if (!totalCount) {
      analysisError.value = '暂未生成简历评价，请稍后再试'
    }
  } catch (e) {
    analysisError.value = e?.message || '简历评价获取失败，请稍后重试'
  } finally {
    analysisLoading.value = false
  }
}

// 处理文件上传
const handleFileChange = async (file) => {
  const rawFile = file?.raw
  if (!rawFile) {
    ElMessage.error('未获取到上传文件')
    return
  }

  const isPdf = rawFile.name.toLowerCase().endsWith('.pdf') || rawFile.type === 'application/pdf'
  if (!isPdf) {
    ElMessage.warning('仅支持上传 PDF 简历')
    return
  }

  try {
    const uploadUrl = await getResumeUploadUrl(rawFile.name)
    await uploadResumeBinary(uploadUrl, rawFile)

    const downloadUrl = await getResumeDownloadUrl()
    if (!downloadUrl) {
      throw new Error('上传成功，但未获取到简历访问地址')
    }

    hasResume.value = true
    resumeFile.value = rawFile
    resumeRemoteUrl.value = withResumeVersion(downloadUrl)
    resumeFileName.value = rawFile.name
    resumeFileSize.value = formatFileSize(rawFile.size)
    resumeUploadTime.value = new Date().toLocaleString()

    const resumeInfo = {
      hasResume: true,
      fileName: resumeFileName.value,
      fileSize: resumeFileSize.value,
      uploadTime: resumeUploadTime.value,
      remoteUrl: resumeRemoteUrl.value
    }
    setUserStorage('resumeInfo', JSON.stringify(resumeInfo))
    await loadResumeAnalysis()
    ElMessage.success('简历上传成功')
  } catch (e) {
    ElMessage.error(e?.response?.data?.msg || e?.message || '简历上传失败')
  }
}

// 预览简历
const previewResume = async () => {
  if (localPreviewObjectUrl.value) {
    URL.revokeObjectURL(localPreviewObjectUrl.value)
    localPreviewObjectUrl.value = ''
  }

  isPDF.value = true
  try {
    if (resumeRemoteUrl.value) {
      const blob = await fetchResumeBlob(resumeRemoteUrl.value)
      localPreviewObjectUrl.value = URL.createObjectURL(blob)
      previewUrl.value = `${localPreviewObjectUrl.value}#toolbar=0&navpanes=0`
    } else if (resumeFile.value) {
      localPreviewObjectUrl.value = URL.createObjectURL(resumeFile.value)
      previewUrl.value = `${localPreviewObjectUrl.value}#toolbar=0&navpanes=0`
    } else {
      isPDF.value = false
      previewUrl.value = ''
      ElMessage.warning('简历地址不存在，无法预览')
      return
    }
    showPreview.value = true
  } catch (error) {
    isPDF.value = false
    previewUrl.value = ''
    ElMessage.error('简历预览失败，请稍后重试')
    console.error('简历预览失败:', error)
  }
};

// 关闭预览
const closePreview = () => {
  showPreview.value = false;
  // 释放URL对象
  if (localPreviewObjectUrl.value) {
    URL.revokeObjectURL(localPreviewObjectUrl.value)
    localPreviewObjectUrl.value = ''
  }
  previewUrl.value = '';
};

// 格式化文件大小
const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 B';
  const k = 1024;
  const sizes = ['B', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
};

onMounted(async () => {
  try {
    // 第一步：读取本地缓存，这是判断用户是否上传简历的唯一真实来源
    const storedResumeInfo = getUserStorage('resumeInfo')
    let cachedFileName = ''
    let hasUploadedBeforeCache = false
    
    if (storedResumeInfo) {
      try {
        const resumeInfo = JSON.parse(storedResumeInfo)
        if (resumeInfo.hasResume) {
          hasResume.value = true
          resumeFileName.value = resumeInfo.fileName
          resumeFileSize.value = resumeInfo.fileSize
          resumeUploadTime.value = resumeInfo.uploadTime
          resumeRemoteUrl.value = resumeInfo.remoteUrl || ''
          cachedFileName = resumeInfo.fileName
          hasUploadedBeforeCache = true // 缓存中明确表示已上传
        }
      } catch (e) {
        console.warn('解析缓存的简历信息失败:', e)
      }
    }

    // 第二步：获取远程简历信息
    // 仅在缓存中已经表示有简历时才更新，避免API返回默认URL导致误判
    if (hasUploadedBeforeCache) {
      try {
        const remoteDownloadUrl = await getResumeDownloadUrl()
        if (remoteDownloadUrl) {
          resumeRemoteUrl.value = withResumeVersion(remoteDownloadUrl)
          
          // 仅在缓存中没有有效文件名时，才从URL中提取
          if (!cachedFileName || cachedFileName === 'resume.pdf') {
            const nameFromUrl = extractNameFromUrl(remoteDownloadUrl)
            if (nameFromUrl && (!resumeFileName.value || resumeFileName.value === 'resume.pdf')) {
              resumeFileName.value = nameFromUrl
            }
          }

          // 如果缓存中的时间是默认值，更新为当前时间
          if (!resumeUploadTime.value || resumeUploadTime.value === '2026-03-02 10:00') {
            resumeUploadTime.value = new Date().toLocaleString()
          }
        }
      } catch (e) {
        console.warn('获取远程简历地址失败，使用本地缓存:', e)
      }
    }
    // 如果缓存中没有标记上传，则保持未上传状态，即使API返回URL也不信任
    await loadResumeAnalysis()
    
  } catch (error) {
    console.error('获取简历信息失败:', error)
    hasResume.value = false
    analysisError.value = '暂未获取到简历评价'
  }
});
</script>

<style scoped>
/* 全局样式 - 隐藏滚动条 */
html, body { margin: 0; padding: 0; overflow: hidden !important; height: 100%; width: 100%; }
* { scrollbar-width: none !important; -ms-overflow-style: none !important; }
*::-webkit-scrollbar { display: none !important; }

/* 1. 核心新增：左右分栏布局，禁止滚动并把底部往上拉 */
.resume-layout {
  display: flex;
  height: 100%;
  width: 100%;
  gap: 20px;
  padding: 20px 20px 35px 20px; /* 核心修改：底部 padding 改为 35px 往上拉 */
  box-sizing: border-box;
  overflow: hidden; /* 核心修改：禁止滚动 */
  transition: all 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

.layout-left {
  flex: 2; 
  display: flex;
  flex-direction: column;
  min-height: 0;
  overflow: hidden;
  transition: all 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

/* 2. 右侧容器：设为 Flex 并允许收缩 */
.layout-right {
  flex: 1; 
  min-width: 300px;
  display: flex;
  flex-direction: column;
  min-height: 0;
  overflow: hidden;
  transition: all 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

.resume-view-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  position: relative;
  overflow: hidden !important;
  width: 100%;
  box-sizing: border-box;
  min-height: 0; /* 关键：允许收缩 */
  transition: all 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}
.empty-state {
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden !important;
  transition: all 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}
.start-card { background: var(--card-bg); padding: 40px; border-radius: 16px; text-align: center; border: 1px solid var(--sidebar-border); color: var(--text-color); max-width: 500px; width: 100%; transition: all 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94); }
.start-icon { color: var(--primary-color); margin-bottom: 20px; }

.upload-btn {
  margin-top: 30px;
  display: flex;
  justify-content: center;
}

.upload-button {
  min-width: 180px;
}

/* 已上传简历状态样式 */
.resume-display { 
  flex: 1; 
  display: flex; 
  flex-direction: column; 
  gap: 20px; 
  overflow: hidden !important; 
  width: 100%; 
  box-sizing: border-box; 
  min-height: 0;
  transition: all 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

.resume-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0;
}

/* 核心修复：重塑“您的简历”标题，打造高级胶囊标签 */
.resume-header h2 {
  display: inline-flex;
  align-items: center;
  gap: 12px; /* 给前面的呼吸灯留出间距 */
  white-space: nowrap;
  flex-shrink: 0;
  margin: 0;
  font-size: 20px;
  font-weight: 800;
  color: var(--text-color);
  
  /* 使用与下方卡片一致的实心背景和边框，完美适配三种主题 */
  background: var(--card-bg); 
  border: 1px solid var(--sidebar-border); 
  padding: 12px 28px; 
  border-radius: 16px; /* 更圆润的标签感 */
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
  letter-spacing: 1px;
}

/* 新增：利用伪元素画一个随主题色变化的“呼吸发光点” */
.resume-header h2::before {
  content: '';
  display: block;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background-color: var(--primary-color);
  box-shadow: 0 0 8px var(--primary-color);
  animation: title-breathe 2.5s ease-in-out infinite;
}

/* 呼吸灯动画 */
@keyframes title-breathe {
  0%, 100% { transform: scale(1); opacity: 0.8; }
  50% { transform: scale(1.3); opacity: 1; box-shadow: 0 0 12px var(--primary-color); }
}

.header-actions {
  display: flex;
  gap: 10px;
  align-items: center;
}

/* 简历卡片样式 */
.resume-card { background: var(--card-bg); border-radius: 16px; border: 1px solid var(--sidebar-border); padding: 20px; transition: all 0.3s ease; max-height: 150px; cursor: pointer; }

.resume-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border-color: var(--primary-color);
}

.resume-card-content {
  display: flex;
  align-items: center;
  gap: 15px;
  justify-content: space-between;
}

.file-icon {
  color: var(--primary-color);
  flex-shrink: 0;
}

.file-details {
  flex: 1;
}

.preview-icon {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
  color: var(--text-secondary);
  font-size: 12px;
  transition: all 0.3s ease;
}

.resume-card:hover .preview-icon {
  color: var(--primary-color);
}

/* 预览区域样式 */
.resume-preview { background: var(--card-bg); border-radius: 16px; border: 1px solid var(--sidebar-border); padding: 20px; margin-bottom: 20px; box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1); }

.pdf-preview {
  width: 100%;
  height: 800px;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  position: relative;
}

.pdf-preview embed {
  width: 100%;
  height: 100%;
  border: none;
  outline: none;
}

/* 确保 PDF 只显示主要内容 */
.pdf-preview {
  overflow: hidden;
}

.file-preview {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
  color: var(--text-secondary);
  font-size: 16px;
}

/* Word文档预览样式 */
.word-preview {
  width: 100%;
  height: 800px;
  border-radius: 8px;
  overflow-y: auto;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  position: relative;
  background: #f5f5f5;
  color: black;
}

.word-content {
  padding: 80px 60px;
  line-height: 1.8;
  max-width: 750px;
  margin: 20px auto;
  font-family: 'Microsoft YaHei', 'SimSun', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: white;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.05);
  min-height: 100%;
  border-radius: 4px;
}

/* 标题样式 */
.word-content h1 {
  font-size: 28px;
  font-weight: bold;
  text-align: center;
  margin: 40px 0 30px;
  color: #333;
}

.word-content h2 {
  font-size: 22px;
  font-weight: bold;
  margin: 30px 0 15px;
  color: #333;
  border-bottom: 2px solid #e0e0e0;
  padding-bottom: 8px;
}

.word-content h3 {
  font-size: 18px;
  font-weight: bold;
  margin: 25px 0 12px;
  color: #333;
}

.word-content h4 {
  font-size: 16px;
  font-weight: bold;
  margin: 20px 0 10px;
  color: #333;
}

/* 段落样式 */
.word-content p {
  margin: 12px 0;
  text-align: justify;
  color: #333;
  font-size: 14px;
  line-height: 1.8;
}

/* 列表样式 */
.word-content ul,
.word-content ol {
  margin: 12px 0;
  padding-left: 30px;
}

.word-content li {
  margin: 8px 0;
  color: #333;
  font-size: 14px;
  line-height: 1.6;
}

.word-content ul li {
  list-style-type: disc;
}

.word-content ol li {
  list-style-type: decimal;
}

/* 表格样式 */
.word-content table {
  border-collapse: collapse;
  width: 100%;
  margin: 16px 0;
  font-size: 13px;
}

.word-content th,
.word-content td {
  border: 1px solid #ddd;
  padding: 10px;
  text-align: left;
  vertical-align: top;
}

.word-content th {
  background-color: #f5f5f5;
  font-weight: bold;
  color: #333;
}

.word-content tr:nth-child(even) {
  background-color: #f9f9f9;
}

/* 图片样式 */
.word-content img {
  max-width: 100%;
  height: auto;
  display: block;
  margin: 20px auto;
  border: 1px solid #e0e0e0;
  padding: 5px;
  background: #f9f9f9;
}

/* 链接样式 */
.word-content a {
  color: #1a73e8;
  text-decoration: none;
}

.word-content a:hover {
  text-decoration: underline;
}

/* 引用样式 */
.word-content blockquote {
  border-left: 4px solid #1a73e8;
  padding: 12px 16px;
  margin: 16px 0;
  background-color: #f8f9fa;
  color: #5f6368;
  font-style: italic;
}

/* 代码样式 */
.word-content code {
  background-color: #f6f8fa;
  padding: 2px 4px;
  border-radius: 3px;
  font-family: 'Courier New', Courier, monospace;
  font-size: 13px;
  color: #d73a49;
}

.word-content pre {
  background-color: #f6f8fa;
  padding: 16px;
  border-radius: 4px;
  overflow-x: auto;
  margin: 16px 0;
  border: 1px solid #e1e4e8;
}

.word-content pre code {
  background-color: transparent;
  padding: 0;
  color: #333;
}

.file-details h3 {
  margin: 0 0 5px 0;
  color: var(--text-color);
  font-size: 16px;
}

.file-details p {
  margin: 2px 0;
  color: var(--text-secondary);
  font-size: 12px;
}

/* AI评价样式 */
.ai-evaluation { 
  flex: 1; 
  min-height: 0; /* 防止内容过多时撑破卡片 */
  background: var(--card-bg); 
  border-radius: 16px; 
  border: 1px solid var(--sidebar-border); 
  padding: 25px; 
  overflow: hidden;
  box-shadow: 0 4px 15px rgba(0,0,0,0.05); 
  display: flex;
  flex-direction: column;
}

.ai-evaluation-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid var(--glass-border);
  flex-shrink: 0;
}

.ai-icon {
  color: var(--primary-color);
}

.ai-evaluation-header h3 {
  margin: 0;
  color: var(--text-color);
  font-size: 18px;
}

.ai-evaluation-content {
  flex: 1;
  min-height: 0;
  display: flex;
  flex-direction: column;
  gap: 14px;
  overflow-y: auto;
  padding-right: 4px;
}

.evaluation-loading,
.evaluation-empty {
  color: var(--text-secondary);
  font-size: 13px;
  line-height: 1.6;
  padding: 8px 4px;
}

.evaluation-loading {
  color: var(--primary-color);
}

.evaluation-section {
  background: var(--input-bg);
  border: 1px solid var(--input-border-color, var(--sidebar-border));
  border-radius: 12px;
  padding: 14px 16px;
  box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.02);
}

.evaluation-section h4 {
  margin: 0 0 10px 0;
  padding-bottom: 8px;
  border-bottom: 1px dashed var(--glass-border);
  color: var(--text-color);
  font-size: 14px;
  font-weight: 600;
}

.evaluation-section ul {
  margin: 0;
  padding-left: 18px;
  color: var(--text-secondary);
  font-size: 13px;
}

.evaluation-section li {
  margin-bottom: 8px;
  line-height: 1.6;
}

.evaluation-section li:last-child {
  margin-bottom: 0;
}

/* 3. 优秀简历库卡片：废弃 height:100%，改用 flex:1 完美贴合 */
.excellent-library {
  flex: 1; /* 替代 height: 100% */
  min-height: 0; /* 防止撑破容器 */
  background: var(--card-bg);
  border: 1px solid var(--sidebar-border);
  border-radius: 20px;
  padding: 25px 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
  display: flex;
  flex-direction: column;
  overflow: hidden; /* 保证底部圆角完美展现 */
  transition: all 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

.library-header {
  margin-bottom: 25px;
  padding-bottom: 15px;
  border-bottom: 1px dashed var(--glass-border);
}

.header-title {
  display: flex;
  align-items: center;
  gap: 10px;
}
.header-title h2 { margin: 0; font-size: 18px; color: var(--text-color); }
.star-icon { color: #e6a23c; font-size: 22px; }
.lib-desc { margin: 8px 0 0 0; font-size: 12px; color: var(--text-secondary); line-height: 1.5; }

.library-list {
  flex: 1;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 15px;
  transition: all 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

.excellent-card {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 15px;
  background: rgba(128, 128, 128, 0.05);
  border: 1px solid rgba(140, 140, 140, 0.2);
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s;
}

.excellent-card:hover {
  background: rgba(128, 128, 128, 0.1);
  border-color: var(--primary-color);
  transform: translateX(5px);
}

.card-icon {
  width: 44px; height: 44px;
  border-radius: 10px;
  display: flex; justify-content: center; align-items: center;
  flex-shrink: 0;
}

.card-info { flex: 1; }
.job-title { margin: 0 0 4px 0; font-size: 15px; color: var(--text-color); font-weight: bold; }
.author { margin: 0; font-size: 12px; color: var(--text-secondary); }

.view-btn {
  color: var(--text-secondary);
  font-size: 16px;
  transition: color 0.3s;
}
.excellent-card:hover .view-btn { color: var(--primary-color); }

/* 未上传状态下的布局优化 */
.resume-layout.is-empty {
  gap: 8px !important; /* 收紧间距 */
  align-items: center !important;
  justify-content: center !important;
}

.resume-layout.is-empty .empty-state {
  height: auto !important;
  justify-content: center;
  align-items: center;
  padding-top: 0;
}

.resume-layout.is-empty .start-card {
  height: 332px !important;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  margin: 0;
}

.resume-layout.is-empty .layout-left {
  flex: 0 0 auto !important;
  min-height: 380px !important;
}

.resume-layout.is-empty .layout-right {
  flex: 0 0 auto !important;
  min-height: 380px !important;
  align-items: center;
}

.resume-layout.is-empty .excellent-library {
  flex: 0 0 auto !important;
  height: 380px !important;
  min-height: 380px !important;
  padding: 16px;
  display: flex;
  flex-direction: column;
}

.resume-layout.is-empty .library-list {
  max-height: 280px !important;
  padding-right: 6px;
}

.resume-layout.is-empty .library-list::-webkit-scrollbar {
  width: 8px !important;
}

.resume-layout.is-empty .library-list::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.12) !important;
  border-radius: 6px;
}

.resume-layout.is-empty .excellent-card {
  min-height: 84px !important;
  padding: 12px;
  margin-bottom: 10px;
}

/* 弹窗专用适配 */
:deep(.theme-adapt-dialog) { background: var(--card-bg) !important; border: 1px solid var(--sidebar-border); }
:deep(.theme-adapt-dialog .el-dialog__title) { color: var(--text-color); }
.resume-preview-area {
  background: transparent;
  border-radius: 0;
  overflow: hidden;
  border: none;
}

.excellent-pdf-preview {
  height: 76vh;
  border-radius: 10px;
  overflow: hidden;
}

.excellent-pdf-preview embed {
  width: calc(100% + 56px);
  height: 100%;
  margin-left: -28px;
  border: none;
  outline: none;
}

:deep(.theme-adapt-dialog .el-dialog) {
  border-radius: 14px;
}

:deep(.theme-adapt-dialog .el-dialog__header) {
  padding: 0;
  margin: 0;
  min-height: 0;
}

:deep(.theme-adapt-dialog .el-dialog__headerbtn) {
  top: 12px;
  right: 12px;
}

:deep(.theme-adapt-dialog .el-dialog__body) {
  padding: 12px;
}

/* 响应式适配：只作用于非全屏场景，不改动大屏基线布局 */
@media (max-width: 1400px) {
  .resume-layout { gap: 14px; padding: 16px 16px 24px; }
  .layout-right { min-width: 260px; }

  .resume-header {
    align-items: flex-start;
    gap: 10px;
  }

  .header-actions {
    display: flex;
    flex-wrap: wrap;
    justify-content: flex-end;
    gap: 8px;
  }

  .resume-card { padding: 16px; }
  .resume-card-content { gap: 12px; }
}

@media (max-width: 1200px) {
  .resume-layout {
    flex-direction: column;
    overflow-y: auto;
    overflow-x: hidden;
    padding: 14px 14px 20px;
  }

  .layout-left,
  .layout-right {
    flex: none;
    min-width: 0;
    width: 100%;
  }

  .resume-display,
  .resume-view-container {
    overflow: visible !important;
  }

  .excellent-library {
    max-height: 420px;
    padding: 18px 16px;
  }

  .resume-layout.is-empty {
    align-items: stretch !important;
    justify-content: flex-start !important;
    gap: 14px !important;
  }

  .resume-layout.is-empty .layout-left,
  .resume-layout.is-empty .layout-right {
    flex: none !important;
    min-height: 0 !important;
    width: min(100%, 860px) !important;
    margin: 0 auto;
    align-items: stretch !important;
  }

  .resume-layout.is-empty .start-card {
    height: auto !important;
    min-height: 300px;
    max-width: 100%;
  }

  .resume-layout.is-empty .excellent-library {
    width: 100% !important;
    height: auto !important;
    min-height: 320px !important;
  }

  .resume-layout.is-empty .library-list {
    max-height: 240px !important;
  }
}

@media (max-width: 992px) {
  .resume-header {
    flex-direction: column;
    align-items: stretch;
  }

  .resume-header h2 {
    width: fit-content;
    font-size: 18px;
    padding: 10px 18px;
  }

  .header-actions {
    width: 100%;
    justify-content: flex-start;
  }

  .resume-card-content {
    align-items: flex-start;
    flex-wrap: wrap;
  }

  .preview-icon {
    width: 100%;
    flex-direction: row;
    justify-content: flex-end;
  }

  .ai-evaluation { padding: 18px; }
}

@media (max-width: 768px) {
  .start-card {
    padding: 24px 18px;
    border-radius: 14px;
  }

  .start-card h2 { font-size: 32px; margin: 8px 0; }
  .start-card p { font-size: 14px; line-height: 1.6; }

  .upload-btn,
  .upload-button {
    width: 100%;
  }

  .resume-card,
  .ai-evaluation,
  .excellent-library {
    border-radius: 14px;
  }

  .pdf-preview,
  .word-preview {
    height: 520px;
  }

  .word-content {
    padding: 36px 18px;
    margin: 10px;
  }
}

@media (max-width: 576px) {
  .resume-layout { padding: 12px 10px 16px; gap: 10px; }

  .header-actions {
    display: grid;
    grid-template-columns: 1fr;
    gap: 8px;
  }

  .header-actions :deep(.el-button) {
    width: 100%;
  }

  .file-details h3 { font-size: 15px; word-break: break-word; }
  .file-details p { font-size: 12px; }

  .pdf-preview,
  .word-preview {
    height: 420px;
  }
}

</style>