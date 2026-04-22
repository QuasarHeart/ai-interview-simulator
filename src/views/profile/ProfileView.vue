<template>
  <div class="profile-layout">
    
    <!-- 左侧：核心资料卡 -->
    <div class="profile-col left">
      <el-card class="user-card">
        <div class="avatar-area">
          <div class="avatar-wrapper" @click="triggerUpload">
            <el-avatar :size="100" :src="profileAvatar" class="main-avatar" />
            <!-- 核心修改：移除黑影和文字，替换为右下角的相机徽章 -->
            <div class="camera-badge">
              <el-icon><Camera /></el-icon>
            </div>
          </div>
          <!-- 隐藏的文件上传 input -->
          <el-upload
            class="hidden-uploader"
            action="#" 
            :show-file-list="false"
            :auto-upload="false"
            :on-change="handleAvatarChange"
          >
            <button id="avatar-trigger"></button>
          </el-upload>
        </div>

        <div class="info-area">
          <!-- 昵称编辑区：原地编辑，不切换新布局 -->
          <div class="name-display-box">
            <el-input
              v-model="tempName"
              class="username-input"
              :class="{ editing: isEditingName }"
              :readonly="!isEditingName"
              placeholder="默认名字"
              maxlength="20"
              @keyup.enter="saveName"
            />
            <el-icon v-if="!isEditingName" class="edit-icon" @click="startEditName"><EditPen /></el-icon>
            <div v-else class="name-inline-actions">
              <el-icon class="save-icon" @click="saveName"><Select /></el-icon>
              <el-icon class="cancel-icon" @click="cancelEditName"><CloseBold /></el-icon>
            </div>
          </div>
          
          <p class="email">{{ userStore.userInfo.email }}</p>
          <el-tag size="small" effect="dark" class="role-tag">求职者</el-tag>
        </div>

        <div class="actions-area">
          <el-button type="primary" plain round class="action-btn" @click="dialogVisible = true">
            <el-icon><Lock /></el-icon> 修改密码
          </el-button>
        </div>
      </el-card>
    </div>

    <!-- 右侧：详情与设置 -->
    <div class="profile-col right">
      
      <!-- 1. 个人简介模块 -->
      <div class="section-card">
        <div class="section-header">
          <h3><el-icon><Postcard /></el-icon> 个人简介</h3>
          <el-button v-if="!isEditingBio" type="primary" link @click="startEditBio">编辑简介</el-button>
          <div v-else class="bio-actions">
            <el-button type="info" link @click="cancelEditBio">取消</el-button>
            <el-button type="success" link @click="saveBio">保存</el-button>
          </div>
        </div>
        
        <div class="bio-content">
          <el-input
            ref="bioInputRef"
            v-model="tempBio"
            class="bio-input"
            :class="{ editing: isEditingBio }"
            type="textarea"
            :rows="4"
            :readonly="!isEditingBio"
            resize="none"
            maxlength="200"
            placeholder="这个人很懒，什么都没写~ 点击右上角添加简介。"
          />
        </div>
      </div>

      <!-- 2. 主题设置模块 -->
      <div class="section-card">
        <div class="section-header">
          <h3><el-icon><Brush /></el-icon> 界面风格</h3>
        </div>
        <!-- 引入新写的组件 -->
        <ThemeSwitch />
      </div>

    </div>

    <!-- 弹窗：修改密码 -->
    <el-dialog v-model="dialogVisible" title="修改密码" width="400px" class="glass-dialog" @closed="resetPasswordForm">
      <el-form label-position="top">
        <el-form-item label="邮箱">
          <el-input v-model="userStore.userInfo.email" disabled />
        </el-form-item>
        <el-form-item label="验证码">
          <div style="display: flex; gap: 10px; width: 100%;">
            <el-input v-model="verificationCode" placeholder="请输入验证码" />
            <el-button type="primary" :disabled="countdown > 0 || isSendingCode" :loading="isSendingCode" @click="sendVerificationCode">
              {{ countdown > 0 ? `${countdown}s后重试` : '发送验证码' }}
            </el-button>
          </div>
        </el-form-item>
        <el-form-item label="新密码">
          <el-input v-model="newPassword" type="password" show-password placeholder="8-16位字母和数字组合" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="loading" @click="submitPasswordChange">确认修改</el-button>
      </template>
    </el-dialog>

  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick, computed } from 'vue'
import { Camera, EditPen, Lock, Postcard, Brush, Select, CloseBold } from '@element-plus/icons-vue'
import { useUserStore } from '../../stores/user'
import { getUserProfile, updateUserInfo, resetPassword, sendVerifyCode, getAvatarUploadUrl, uploadAvatarBinary, getAvatarDownloadUrl } from '../../api/Profile'
import { ElMessage } from 'element-plus'
import ThemeSwitch from '../../components/ThemeSwitch.vue' // 引入组件


const userStore = useUserStore()
const defaultAvatar = 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png'
const profileAvatar = computed(() => {
  const avatar = userStore.userInfo.avatar
  if (typeof avatar !== 'string') return defaultAvatar
  const value = avatar.trim()
  if (!value || value.toLowerCase() === 'null' || value.toLowerCase() === 'undefined') {
    return defaultAvatar
  }
  return value
})

const withAvatarVersion = (url) => {
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

// 头像上传
const triggerUpload = () => document.getElementById('avatar-trigger').click()
const avatarUploading = ref(false)
const handleAvatarChange = async (file) => {
  const rawFile = file?.raw
  if (!rawFile) {
    ElMessage.error('未获取到上传文件')
    return
  }

  let localPreviewUrl = ''
  try {
    avatarUploading.value = true

    // 先本地预览，避免上传成功后因缓存看不到新头像
    localPreviewUrl = URL.createObjectURL(rawFile)
    userStore.updateProfile({ avatar: localPreviewUrl })

    // 1) 向后端申请临时上传地址
    const uploadUrl = await getAvatarUploadUrl(rawFile.name)

    // 2) 使用临时地址 PUT 二进制文件
    await uploadAvatarBinary(uploadUrl, rawFile)

    // 3) 调用下载接口获取可访问头像地址并回显
    const avatarAccessUrl = await getAvatarDownloadUrl()
    userStore.updateProfile({ avatar: withAvatarVersion(avatarAccessUrl) })
    ElMessage.success('头像上传成功')
  } catch (e) {
    ElMessage.error(e?.response?.data?.msg || e?.message || '头像上传失败')
  } finally {
    if (localPreviewUrl) {
      URL.revokeObjectURL(localPreviewUrl)
    }
    avatarUploading.value = false
  }
}

// 昵称修改
const isEditingName = ref(false)
const tempName = ref('')

const startEditName = () => {
  tempName.value = userStore.userInfo.username || ''
  isEditingName.value = true
}

const cancelEditName = () => {
  tempName.value = userStore.userInfo.username || ''
  isEditingName.value = false
}

const saveName = async () => {
  const nextName = tempName.value.trim()
  if(!nextName) return ElMessage.warning('昵称不能为空')
  console.log("准备更新昵称为：", nextName)
  try {
    await updateUserInfo({}, { nickName: nextName })
    userStore.updateProfile({ username: nextName })
    tempName.value = nextName
    isEditingName.value = false
    ElMessage.success('昵称已更新')
  } catch (e) {
    ElMessage.error(e?.message || '昵称更新失败')
  }
}

// 简介逻辑 (Bio)
const isEditingBio = ref(false)
const tempBio = ref('')
const bioInputRef = ref(null)

const startEditBio = async () => {
  isEditingBio.value = true
  await nextTick()
  bioInputRef.value?.focus?.()
}
const cancelEditBio = () => {
  tempBio.value = userStore.userInfo.bio || ''
  isEditingBio.value = false
}
const saveBio = async () => {
  const nextBio = tempBio.value.trim()
  try {
    await updateUserInfo({}, { description: nextBio })
    userStore.updateProfile({ bio: nextBio })
    tempBio.value = nextBio
    isEditingBio.value = false
    ElMessage.success('简介已更新')
  } catch (e) {
    ElMessage.error(e?.message || '简介更新失败')
  }
}

// 密码逻辑
const dialogVisible = ref(false)
const verificationCode = ref('')
const newPassword = ref('')
const loading = ref(false)
const countdown = ref(0)
const isSendingCode = ref(false)
const passwordRule = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,16}$/
let countdownTimer = null

const resetPasswordForm = () => {
  verificationCode.value = ''
  newPassword.value = ''
  countdown.value = 0
  if (countdownTimer) {
    clearInterval(countdownTimer)
    countdownTimer = null
  }
}

const startCountdown = () => {
  if (countdownTimer) {
    clearInterval(countdownTimer)
  }

  countdown.value = 60
  countdownTimer = setInterval(() => {
    countdown.value--
    if (countdown.value <= 0) {
      clearInterval(countdownTimer)
      countdownTimer = null
    }
  }, 1000)
}

const sendVerificationCode = async () => {
  if (!userStore.userInfo.email) {
    ElMessage.warning('缺少邮箱信息，请刷新页面后重试')
    return
  }

  try {
    isSendingCode.value = true
    await sendVerifyCode(userStore.userInfo.email)
    ElMessage.success('验证码已发送')
    startCountdown()
  } catch (e) {
    ElMessage.error(e?.message || '验证码发送失败')
  } finally {
    isSendingCode.value = false
  }
}

const submitPasswordChange = async () => {
  const code = verificationCode.value.trim()
  const pwd = newPassword.value.trim()

  if (!code) {
    ElMessage.warning('请输入验证码')
    return
  }

  if (!passwordRule.test(pwd)) {
    ElMessage.warning('新密码需为8-16位字母和数字组合')
    return
  }

  try {
    loading.value = true
    await resetPassword({
      email: userStore.userInfo.email,
      code,
      newPassword: pwd
    })
    dialogVisible.value = false
    ElMessage.success('密码修改成功')
    resetPasswordForm()
  } catch (e) {
    ElMessage.error(e?.message || '密码修改失败')
  } finally {
    loading.value = false
  }
}

const loadUserProfile = async () => {
  try {
    const res = await getUserProfile()
    const payload = res?.data || res || {}
    const rawUser = payload?.user || payload
    const rawAccount = payload?.account || payload

    userStore.updateProfile({
      email: rawAccount?.email || rawUser?.email || userStore.userInfo.email,
      username: rawUser?.nickname || rawUser?.nickName || rawUser?.username || rawUser?.name || userStore.userInfo.username,
      avatar: withAvatarVersion(rawUser?.avatar || rawUser?.avatarUrl || userStore.userInfo.avatar),
      bio: rawUser?.description || rawUser?.bio || rawUser?.introduction || rawUser?.profile || userStore.userInfo.bio
    })

    // 头像优先从“下载头像”接口获取，但仅在链接可正常加载图片时才覆盖。
    try {
      const avatarAccessUrl = await getAvatarDownloadUrl()
      const safeAvatarUrl = withAvatarVersion(avatarAccessUrl)
      if (await canLoadAvatar(safeAvatarUrl)) {
        userStore.updateProfile({ avatar: safeAvatarUrl })
      }
    } catch (avatarErr) {
      console.warn('获取头像访问地址失败，使用用户资料中的头像字段回退', avatarErr)
    }

    tempName.value = userStore.userInfo.username || ''
    tempBio.value = userStore.userInfo.bio || ''
  } catch (e) {
    ElMessage.error(e?.message || '获取用户信息失败')
  }
}

onMounted(() => {
  loadUserProfile()
})

onUnmounted(() => {
  if (countdownTimer) {
    clearInterval(countdownTimer)
  }
})
</script>

<style scoped>
/* 核心修复：强制左右两列高度等宽 (align-items: stretch) */
.profile-layout { 
  padding: 80px 30px 30px 30px; 
  display: flex; 
  gap: 30px; 
  overflow-y: auto; 
  box-sizing: border-box; 
  align-items: stretch; 
}
.profile-col {
  display: flex;
  flex-direction: column;
}
.profile-col.left {
  flex: 1;
  max-width: 350px;
}
.profile-col.right {
  flex: 2;
  gap: 25px;
}

/* 核心修复：左侧卡片设置 height: 100%，它会刚好等于右侧卡片的总高度 */
.user-card {
  height: 100%; 
  background: var(--glass-bg);
  border: 1px solid var(--glass-border);
  border-radius: 20px;
  padding: 40px 20px;
  text-align: center;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  /* 移除原本的 justify-content: center，让内容自然靠上分布，视觉更舒服 */
}

.avatar-wrapper { 
  position: relative; 
  display: inline-block; 
  cursor: pointer; 
}
.main-avatar { border: 4px solid var(--glass-border); transition: all 0.3s; }
.avatar-overlay { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-size: 30px; opacity: 0; transition: opacity 0.3s; }
.avatar-wrapper:hover .main-avatar {
  border-color: var(--primary-color);
}

/* 核心新增：相机小徽章，带有一圈和背景同色的边框，形成漂亮的“挖孔”视觉 */
.camera-badge {
  position: absolute;
  bottom: 0;
  right: 0;
  width: 32px;
  height: 32px;
  background-color: var(--primary-color);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  border: 3px solid var(--card-bg); /* 与卡片同色边框 */
  box-shadow: 0 2px 8px rgba(0,0,0,0.15);
  transition: transform 0.2s ease;
}
.avatar-wrapper:hover .camera-badge {
  transform: scale(1.1); /* 鼠标悬停时微微放大 */
}

.hidden-uploader { display: none; }
.upload-tip { font-size: 12px; color: var(--primary-color); margin-top: 10px; cursor: pointer; }

.info-area { margin-top: 20px; flex: 1; }
.name-display-box {
  position: relative;
  width: 100%;
  min-height: 38px;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 5px;
}

:deep(.username-input) { width: 170px; }
:deep(.username-input .el-input__wrapper) {
  background: transparent !important;
  box-shadow: none !important;
  border: none !important;
  border-radius: 8px;
  min-height: 38px;
  padding: 0 8px;
  transition: all 0.2s ease;
}
:deep(.username-input:not(.editing) .el-input__wrapper),
:deep(.username-input:not(.editing) .el-input__wrapper:hover),
:deep(.username-input:not(.editing) .el-input__wrapper.is-focus) {
  background: transparent !important;
  border: none !important;
  box-shadow: none !important;
  outline: none !important;
}
:deep(.username-input .el-input__inner) {
  font-size: 24px;
  font-weight: 700;
  line-height: 1.2;
  text-align: center;
  color: var(--text-color);
  cursor: default;
}
:deep(.username-input.editing .el-input__wrapper) {
  background: rgba(255, 255, 255, 0.06) !important;
  border: 1px solid var(--primary-color) !important;
  box-shadow: none !important;
}
:deep(.username-input.editing .el-input__inner) { cursor: text; }

.edit-icon {
  position: absolute;
  left: calc(50% + 96px);
  top: 50%;
  transform: translateY(-50%);
  cursor: pointer;
  color: var(--text-secondary);
  transition: color 0.2s;
}
.edit-icon:hover { color: var(--primary-color); }
.name-inline-actions {
  position: absolute;
  left: calc(50% + 90px);
  top: 50%;
  transform: translateY(-50%);
  display: flex;
  align-items: center;
  gap: 8px;
}
.save-icon, .cancel-icon { cursor: pointer; color: var(--text-secondary); transition: color 0.2s; }
.save-icon:hover { color: #67c23a; }
.cancel-icon:hover { color: #f56c6c; }
.email { margin: 0 0 15px 0; color: var(--text-secondary); font-size: 14px; }
.actions-area { margin-top: 30px; display: flex; flex-direction: column; gap: 15px; }
.action-btn {
  width: 100%;
  margin: 0 !important;
  --el-button-bg-color: transparent;
  --el-button-text-color: var(--primary-color);
  --el-button-border-color: var(--primary-color);
  --el-button-hover-bg-color: var(--input-bg);
  --el-button-hover-text-color: var(--primary-color);
  --el-button-hover-border-color: var(--primary-color);
  --el-button-active-bg-color: var(--input-bg);
  --el-button-active-border-color: var(--primary-color);
}

/* 右侧板块样式 */
.section-card { background: var(--glass-bg); border: 1px solid var(--glass-border); border-radius: 20px; padding: 25px; color: var(--text-color); }
.section-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; padding-bottom: 15px; border-bottom: 1px solid var(--glass-border); }
.section-header h3 { margin: 0; font-size: 18px; display: flex; align-items: center; gap: 8px; }
.bio-actions { min-width: 110px; text-align: right; }

:deep(.bio-input .el-textarea__inner) {
  min-height: 100px !important;
  line-height: 1.6;
  font-size: 15px;
  padding: 15px;
  background: var(--input-bg) !important;
  border-radius: 8px;
  border: 1px solid var(--input-border-color, var(--glass-border)) !important;
  color: var(--text-color);
  box-shadow: none;
  transition: all 0.2s ease;
}

:deep(.bio-input.editing .el-textarea__inner) {
  border-color: var(--primary-color);
  border-style: dashed !important;
}

/* 双列小屏修复：避免左侧名称头像卡片出现横向滚动条 */
@media (min-width: 901px) and (max-width: 1200px) {
  :deep(.user-card .el-card__body) {
    overflow-x: hidden;
  }
}

@media (max-width: 900px) {
  .profile-layout {
    padding: 16px 10px;
    flex-direction: column;
    height: 100%;
    min-height: 0;
    overflow-y: auto;
    overflow-x: hidden;
    -webkit-overflow-scrolling: touch;
    scrollbar-width: thin;
    scrollbar-color: var(--page-scrollbar-thumb, var(--glass-border)) var(--page-scrollbar-track, transparent);
  }

  .profile-layout::-webkit-scrollbar {
    width: 8px;
  }

  .profile-layout::-webkit-scrollbar-track {
    background: var(--page-scrollbar-track, transparent);
    border-radius: 999px;
  }

  .profile-layout::-webkit-scrollbar-thumb {
    background: var(--page-scrollbar-thumb, var(--glass-border));
    border-radius: 999px;
    border: 2px solid transparent;
    background-clip: content-box;
  }

  .profile-layout::-webkit-scrollbar-thumb:hover {
    background: var(--primary-color);
    background-clip: content-box;
  }

  .profile-col {
    width: 100%;
    max-width: 100%;
    flex: none;
  }

  .profile-col.left {
    max-width: 100%;
  }

  .profile-col.right {
    width: 100%;
    gap: 14px;
  }

  .user-card,
  .section-card {
    width: 100%;
    box-sizing: border-box;
  }

  .user-card {
    padding: 28px 14px;
  }

  .section-card {
    padding: 16px 14px;
  }
}
</style>

<style>
/* el-dialog 默认会 Teleport 到 body，这里使用非 scoped 样式确保弹窗输入框边框可见 */
.glass-dialog {
  background: var(--card-bg) !important;
  border: 1px solid var(--sidebar-border) !important;
}

.glass-dialog .el-dialog__title,
.glass-dialog .el-form-item__label {
  color: var(--text-color) !important;
}

.glass-dialog .el-input__wrapper {
  background: var(--input-bg) !important;
  border: 1px solid var(--input-border-color, var(--sidebar-border)) !important;
  box-shadow: none !important;
}

.glass-dialog .el-input__wrapper:hover,
.glass-dialog .el-input__wrapper.is-focus {
  border-color: var(--primary-color) !important;
}

.glass-dialog .el-input__inner {
  color: var(--text-color) !important;
}


/* 压缩自带播放器的体积 */
.audio-control audio {
  width: 100%;
  height: 36px;
  outline: none;
}
</style>