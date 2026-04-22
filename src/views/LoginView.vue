<template>
  <!-- [核心修改] 动态绑定大背景 -->
  <div class="login-container" :style="containerStyle">

    <!-- === 新增：独立的顶部标题栏 === -->
    <div class="app-title-bar" v-if="isElectron">
      <!-- 这个区域负责拖拽整个窗口 -->
      <div class="title-bar-drag-area"></div>
      <!-- 窗口控制按钮组 -->
      <div class="window-controls">
        <div class="control-btn min-btn" @click="minimizeWin" title="最小化">
          <svg viewBox="0 0 10 10" class="win-icon"><path d="M1 4.5h8v1H1z" fill="currentColor"/></svg>
        </div>
        <div class="control-btn max-btn" @click="maximizeWin" :title="isMaximized ? '向下还原' : '最大化'">
          <svg v-if="isMaximized" viewBox="0 0 10 10" class="win-icon">
            <path d="M3 1h6v6h-1V3H3V1zm-2 2h6v6H1V3zm1 1v4h4V4H2z" fill="currentColor"/>
          </svg>
          <svg v-else viewBox="0 0 10 10" class="win-icon">
            <path d="M1 1h8v8H1V1zm1 1v6h6V2H2z" fill="currentColor"/>
          </svg>
        </div>
        <div class="control-btn close-btn" @click="closeWin" title="关闭">
          <svg viewBox="0 0 10 10" class="win-icon"><path d="M1.4 1l4 4-4 4 .6.6 4-4 4 4 .6-.6-4-4 4-4-.6-.6-4 4-4-4-.6.6z" fill="currentColor"/></svg>
        </div>
      </div>
    </div>

    <!-- [核心修改] 动态绑定卡片插画 -->
    <div class="auth-card" :class="{ 'flipped': isFlipped }" :style="cardStyle">
      
      <!-- === 登录表单（左侧） === -->
      <div class="auth-form login-form">
        <div class="login-theme-switch" role="group" aria-label="主题切换">
          <button
            v-for="item in themeOptions"
            :key="`login-${item.value}`"
            type="button"
            class="theme-pill"
            :class="[item.value, { active: currentTheme === item.value }]"
            @click="handleThemeChange(item.value)"
          >
            <span class="pill-dot"></span>
            <span class="pill-text">{{ item.label }}</span>
          </button>
        </div>

        <!-- 核心修改：独立放在左上角的角标 Logo -->
        <img src="@/assets/images/logo.jpg" class="corner-logo" alt="Logo" />
        
        <h1 class="app-title">AI 模拟面试平台</h1>
        <h2 class="form-title">用户登入</h2>
        
        <el-form ref="loginFormRef" :model="loginForm" :rules="rules" size="large" class="form-content">
          <div class="form-group">
            <label class="form-label">邮箱</label>
            <el-form-item prop="email">
              <el-input v-model="loginForm.email" placeholder="请输入邮箱" />
            </el-form-item>
          </div>
          <div class="form-group">
            <label class="form-label">密码</label>
            <el-form-item prop="password">
              <el-input v-model="loginForm.password" type="password" placeholder="请输入密码" show-password />
            </el-form-item>
          </div>
          <div class="remember-forgot">
            <el-checkbox v-model="loginForm.remember">记住账号密码</el-checkbox>
            <div class="forgot-password"><span @click="handleForgotPassword">忘记密码?</span></div>
          </div>

          <el-button class="submit-btn login-btn-spacing" @click="handleLogin" :loading="isLoading">登录</el-button>

          <div class="switch-text">
            <span>还没有账号？</span>
            <span class="switch-link" @click="toggleFlip">
              去注册 
              <!-- 纯 CSS SVG 箭头 -->
              <svg class="block-arrow" viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                <path d="M2 11H16V7L23 12L16 17V13H2V11Z"/>
              </svg>
            </span>
          </div>
        </el-form>
      </div>
      
      <!-- === 注册表单（右侧） === -->
      <div class="auth-form register-form">
        <!-- 核心修改：独立放在左上角的角标 Logo -->
        <img src="@/assets/images/logo.jpg" class="corner-logo" alt="Logo" />
        
        <h1 class="app-title">AI 模拟面试平台</h1>
        <h2 class="form-title">注册账号</h2>
        
        <el-form ref="registerFormRef" :model="registerForm" :rules="rules" size="large" class="form-content">
          <div class="form-group">
            <label class="form-label">邮箱</label>
            <el-form-item prop="email">
              <div class="email-row">
                <el-input v-model="registerForm.email" placeholder="请输入邮箱" />
                <el-button class="code-btn" :disabled="isCodeSent" @click="handleSendCode">
                  {{ isCodeSent ? `${countdown}s后重发` : '获取验证码' }}
                </el-button>
              </div>
            </el-form-item>
          </div>
          <div class="form-group">
            <label class="form-label">验证码</label>
            <el-form-item prop="code">
              <el-input v-model="registerForm.code" placeholder="6位数字验证码" />
            </el-form-item>
          </div>
          <div class="form-group">
            <label class="form-label">昵称</label>
            <el-form-item prop="nickName">
              <el-input v-model="registerForm.nickName" placeholder="请输入昵称" />
            </el-form-item>
          </div>
          <div class="form-group">
            <label class="form-label">性别</label>
            <el-form-item prop="gender">
              <el-select
                v-model="registerForm.gender"
                placeholder="请选择性别"
                style="width: 100%"
                popper-class="theme-adapt-select-dropdown"
              >
                <el-option label="男" :value="1" />
                <el-option label="女" :value="2" />
              </el-select>
            </el-form-item>
          </div>
          <div class="form-group">
            <label class="form-label">密码</label>
            <el-form-item prop="password">
              <el-input v-model="registerForm.password" type="password" placeholder="设置密码 (8-16位字母和数字)" show-password />
            </el-form-item>
          </div>

          <el-button class="submit-btn" @click="handleRegister" :loading="isLoading">注册</el-button>

          <div class="switch-text">
            <span class="switch-link" @click="toggleFlip">
              <svg class="block-arrow arrow-left" viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                <path d="M2 11H16V7L23 12L16 17V13H2V11Z"/>
              </svg>
              登录
            </span>
            <span>已有账号？</span>
          </div>
        </el-form>
      </div>
    </div>

    <!-- [新增] 找回密码弹窗 -->
    <el-dialog 
      v-model="forgotDialogVisible" 
      title="找回密码" 
      width="400px" 
      :append-to-body="true"
      align-center
      class="theme-adapt-dialog"
    >
      <el-form ref="forgotFormRef" :model="forgotForm" :rules="forgotRules" label-position="top" size="large">
        <el-form-item label="注册邮箱" prop="email">
          <el-input v-model="forgotForm.email" placeholder="请输入绑定的邮箱" />
        </el-form-item>
        
        <el-form-item label="验证码" prop="code">
          <div class="email-row">
            <el-input v-model="forgotForm.code" placeholder="6位数字验证码" />
            <el-button class="code-btn" :disabled="isForgotCodeSent" @click="handleSendForgotCode">
              {{ isForgotCodeSent ? `${forgotCountdown}s后重发` : '获取验证码' }}
            </el-button>
          </div>
        </el-form-item>
        
          <el-form-item label="新密码" prop="newPassword">
          <el-input v-model="forgotForm.newPassword" type="password" placeholder="请输入新密码 (8-16位字母和数字)" show-password />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="forgotDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleResetPassword" :loading="isResetting">确认修改</el-button>
        </span>
      </template>
    </el-dialog>

  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { login, register, sendCode, resetPassword } from '../api/Login'
// 引入主题
import { useThemeStore } from '../stores/theme'

const router = useRouter()
const themeStore = useThemeStore()
const currentTheme = computed(() => themeStore.currentTheme || 'dark')
const isLoading = ref(false)
const isFlipped = ref(false)

const themeOptions = [
  { label: '简约白', value: 'light' },
  { label: '科技蓝', value: 'blue' },
  { label: '深邃黑', value: 'dark' }
]

const handleThemeChange = (theme) => {
  themeStore.setTheme(theme)
}

const isElectron = navigator.userAgent.toLowerCase().includes(' electron/')
const isMaximized = ref(false)

const checkMaximizedStatus = () => {
  if (typeof window !== 'undefined') {
    isMaximized.value = window.outerWidth >= window.screen.availWidth && window.outerHeight >= window.screen.availHeight
  }
}

const minimizeWin = () => {
  if (isElectron) {
    const { ipcRenderer } = window['require']('electron')
    ipcRenderer.send('window-min')
  }
}

const maximizeWin = () => {
  if (isElectron) {
    const { ipcRenderer } = window['require']('electron')
    ipcRenderer.send('window-max')
    isMaximized.value = !isMaximized.value
  }
}

const closeWin = () => {
  if (isElectron) {
    const { ipcRenderer } = window['require']('electron')
    ipcRenderer.send('window-close')
  }
}

// [新增] 动态获取图片 URL 的函数
const getImageUrl = (name) => new URL(`../assets/images/${name}`, import.meta.url).href

// [新增] 动态计算背景图样式
const containerStyle = computed(() => {
  const theme = themeStore.currentTheme || 'light'
  return { backgroundImage: `url(${getImageUrl(`auth-bg-${theme}.jpg`)})` }
})

// [新增] 动态计算卡片插画样式
const cardStyle = computed(() => {
  const theme = themeStore.currentTheme || 'light'
  const illustration = getImageUrl(`auth-illustration-${theme}.jpg`)
  return { backgroundImage: `linear-gradient(to bottom, rgba(255, 255, 255, 0.15), rgba(255, 255, 255, 0.32)), url(${illustration})` }
})

const loginFormRef = ref(null)
const registerFormRef = ref(null)
const loginForm = reactive({ email: '', password: '', remember: false })
const registerForm = reactive({ email: '', code: '', nickName: '', gender: 1, password: '' })

const toggleFlip = () => isFlipped.value = !isFlipped.value

const isCodeSent = ref(false)
const countdown = ref(60)
let timer = null

const rules = reactive({
  email:[{ required: true, message: '请输入邮箱', trigger: 'blur' }, { type: 'email', message: '格式错误', trigger: ['blur', 'change'] }],
  password:[{ required: true, message: '请输入密码', trigger: 'blur' }, { pattern: /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,16}$/, message: '密码需为8-16位字母和数字组合', trigger: 'blur' }],
  code:[{ required: true, message: '请输入验证码', trigger: 'blur' }],
  nickName:[{ required: true, message: '请输入昵称', trigger: 'blur' }],
  gender:[{ required: true, message: '请选择性别', trigger: 'change' }]
})

const handleSendCode = async () => {
  // 简单校验邮箱是否填写（避免 validateField 未挂载或异常时无反应）
  if (!registerForm.email) {
    ElMessage.error('请输入邮箱')
    return
  }

  try {
    const res = await sendCode(registerForm.email)
    // 支持多种后端返回格式的友好处理
    if (res && (res.code === 200 || res.success || res.status === 200)) {
      ElMessage.success(res.message || '验证码已发送')
      isCodeSent.value = true
      countdown.value = 60
      timer = setInterval(() => {
        countdown.value--
        if (countdown.value <= 0) {
          clearInterval(timer)
          isCodeSent.value = false
        }
      }, 1000)
    } else {
      ElMessage.error((res && res.message) || '验证码发送失败')
    }
  } catch (e) {
    console.error('sendCode error', e)
    ElMessage.error('验证码发送失败，请重试')
  }
}

const handleLogin = async () => {
  if (!loginFormRef.value) return
  await loginFormRef.value.validate(async (valid) => {
    if (valid) {
      isLoading.value = true
      try {
        console.log('loginForm', loginForm)
        const data = await login({ email: loginForm.email, password: loginForm.password })
        const token = data?.data?.token || data?.token
        console.log(token)
        if (!token) {
          throw new Error(data?.msg || data?.message || '登录失败，未返回 token')
        }
        localStorage.setItem('token', token)
        if (loginForm.remember) { localStorage.setItem('rememberedEmail', loginForm.email); localStorage.setItem('rememberedPassword', loginForm.password) }
        else { localStorage.removeItem('rememberedEmail'); localStorage.removeItem('rememberedPassword') }
        ElMessage.success('登录成功'); router.push('/dashboard')
      } catch (e) {
        console.error('login error', e)
        ElMessage.error(e?.response?.data?.msg || e?.response?.data?.message || e?.message || '登录失败')
      } finally { isLoading.value = false }
    }
  })
}

const handleRegister = async () => {
  
  if (!registerFormRef.value) return
  await registerFormRef.value.validate(async (valid) => {
    if (valid) {
      isLoading.value = true
      console.log('registerForm', registerForm)
      try {
        const data = await register({
          email: registerForm.email,
          password: registerForm.password,
          code: registerForm.code,
          nickName: registerForm.nickName,
          gender: registerForm.gender
        })
        console.log('register response', data)
        const token = data?.data?.token || data?.token
        if (token) {
          localStorage.setItem('token', token)
        }
        ElMessage.success(data?.message || '注册成功'); router.push('/dashboard')
      } catch (e) {
        console.error('register error', e)
        ElMessage.error(e?.response?.data?.msg || e?.response?.data?.message || e?.message || '注册失败')
      } finally { isLoading.value = false }
    }
  })
}

// ==========================================
// === [新增] 忘记密码相关状态与逻辑 ===
// ==========================================
const forgotDialogVisible = ref(false)
const isResetting = ref(false)
const forgotFormRef = ref(null)
const forgotForm = reactive({ email: '', code: '', newPassword: '' })

// 独立的验证码倒计时（防止和注册页的倒计时冲突）
const isForgotCodeSent = ref(false)
const forgotCountdown = ref(60)
let forgotTimer = null

// 独立的表单校验规则
const forgotRules = reactive({
  email:[
    { required: true, message: '请输入邮箱地址', trigger: 'blur' },
    { type: 'email', message: '邮箱格式错误', trigger: ['blur', 'change'] }
  ],
  code:[
    { required: true, message: '请输入验证码', trigger: 'blur' }
  ],
    newPassword:[
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { pattern: /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,16}$/, message: '密码需为8-16位字母和数字组合', trigger: 'blur' }
  ]
})

// 1. 点击打开弹窗
const handleForgotPassword = () => {
  forgotDialogVisible.value = true
  // 每次打开清空上次填写的表单
  if (forgotFormRef.value) {
    forgotFormRef.value.resetFields()
  }
}

// 2. 发送找回密码的验证码
const handleSendForgotCode = async () => {
  if (!forgotForm.email) {
    ElMessage.error('请输入邮箱')
    return
  }

  try {
    const res = await sendCode(forgotForm.email)
    if (res && (res.code === 200 || res.success || res.status === 200)) {
      ElMessage.success(res.message || '验证码已发送至您的邮箱')
      isForgotCodeSent.value = true
      forgotCountdown.value = 60
      forgotTimer = setInterval(() => {
        forgotCountdown.value--
        if (forgotCountdown.value <= 0) {
          clearInterval(forgotTimer)
          isForgotCodeSent.value = false
        }
      }, 1000)
    } else {
      ElMessage.error((res && res.message) || '验证码发送失败')
    }
  } catch (e) {
    console.error('sendCode forgot error', e)
    ElMessage.error('验证码发送失败，请重试')
  }
}

// 3. 提交修改密码请求
const handleResetPassword = async () => {
  if (!forgotFormRef.value) return
  await forgotFormRef.value.validate(async (valid) => {
    if (valid) {
      isResetting.value = true
      try {
        // 调用刚才在 api/user.js 中预留的重置接口
        await resetPassword({
          email: forgotForm.email,
          code: forgotForm.code,
          newPassword: forgotForm.newPassword
        })
        ElMessage.success('密码重置成功，请使用新密码登录')
        forgotDialogVisible.value = false // 关闭弹窗
      } catch (e) { 
        console.error(e) 
      } finally { 
        isResetting.value = false 
      }
    }
  })
}
// ==========================================

onMounted(() => {
  const e = localStorage.getItem('rememberedEmail'); const p = localStorage.getItem('rememberedPassword')
  if (e && p) { loginForm.email = e; loginForm.password = p; loginForm.remember = true }

  // 新增：挂载窗口大小监听
  if (isElectron) {
    window.addEventListener('resize', checkMaximizedStatus)
    checkMaximizedStatus()
  }
})

// 新增：卸载组件时清理监听
onUnmounted(() => {
  if (isElectron) {
    window.removeEventListener('resize', checkMaximizedStatus)
  }
})
</script>

<style scoped>
/* 容器大背景 */
.login-container { 
  position: relative; 
  width: 100%; 
  height: auto;
  min-height: 100dvh;
  display: flex; 
  justify-content: center; 
  align-items: center; 
  overflow-x: hidden;
  overflow-y: visible;
  background-size: cover; 
  background-position: center; 
  transition: background-image 0.5s ease; 
}

/* === 顶部标题栏 & 胶囊控制按钮 === */
.app-title-bar { 
  position: absolute; 
  top: 0; 
  left: 0; 
  width: 100%; 
  height: 40px; 
  display: flex; 
  justify-content: space-between; 
  z-index: 9999; 
}

.title-bar-drag-area { 
  flex: 1; 
  -webkit-app-region: drag; 
}

/* 修复：登录界面的窗口控制胶囊（居中且按钮红圈不溢出） */
.window-controls { 
  position: absolute;
  top: 15px;
  right: 20px;
  display: flex; 
  align-items: center; 
  -webkit-app-region: no-drag; 
  /* 强制使用半透明深色底，确保白色图标清晰可见 */
  background: rgba(0, 0, 0, 0.25); 
  backdrop-filter: blur(10px); 
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 20px; 
  padding: 4px 6px; 
  gap: 4px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  z-index: 9999;
}

/* 按钮缩小到 24px，确保被包裹在容器内，红圈不溢出 */
.control-btn { 
  width: 24px; 
  height: 24px; 
  border-radius: 50%; 
  display: flex; 
  justify-content: center; 
  align-items: center; 
  cursor: pointer; 
  color: #ffffff; /* 强制白色图标 */
  transition: all 0.2s ease; 
}

.win-icon { 
  width: 10px; 
  height: 10px; 
}

.control-btn:hover { 
  background-color: rgba(255, 255, 255, 0.3); 
}
.close-btn:hover { 
  background-color: #e81123 !important; 
  color: white; 
}

/* === 卡片与表单 === */
.auth-card { 
  width: 95%; 
  max-width: 1000px; 
  height: 700px; 
  max-height: calc(100vh - 32px);
  display: flex; 
  border-radius: 16px; 
  overflow: hidden; 
  box-shadow: 0 18px 45px rgba(0, 0, 0, 0.15); 
  position: relative; 
  background-size: cover; 
  background-position: center; 
  backdrop-filter: blur(16px); 
  transition: background-image 0.5s ease; 
}

.auth-form { 
  flex: 1; 
  display: flex; 
  flex-direction: column; 
  justify-content: center; 
  align-items: center; 
  padding: 40px; 
  transition: all 0.6s ease-in-out; 
  box-sizing: border-box; 
}

.login-theme-switch {
  position: absolute;
  top: 28px;
  right: 24px;
  display: flex;
  gap: 8px;
  z-index: 30;
}

.theme-pill {
  border: 1px solid var(--glass-border);
  border-radius: 999px;
  padding: 5px 10px;
  background: rgba(255, 255, 255, 0.34);
  color: var(--text-secondary);
  display: inline-flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  font-size: 12px;
  font-weight: 600;
  line-height: 1;
  transition: all 0.2s ease;
  backdrop-filter: blur(8px);
}

.theme-pill:hover {
  transform: translateY(-1px);
  border-color: var(--primary-color);
}

.pill-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: currentColor;
  opacity: 0.95;
  flex-shrink: 0;
}

.theme-pill.light {
  background: rgba(255, 255, 255, 0.78);
  color: #6b7280;
  border-color: rgba(148, 163, 184, 0.45);
}

.theme-pill.light .pill-dot {
  background: #ffffff;
  border: 1px solid #cfd6e4;
  box-shadow: 0 1px 2px rgba(15, 23, 42, 0.16);
}

.theme-pill.blue {
  background: rgba(1, 37, 80, 0.75);
  color: #dbeafe;
  border-color: rgba(24, 144, 255, 0.45);
}

.theme-pill.blue .pill-dot {
  background: #3aa0ff;
}

.theme-pill.dark {
  background: rgba(15, 23, 42, 0.75);
  color: #e2e8f0;
  border-color: rgba(148, 163, 184, 0.35);
}

.theme-pill.dark .pill-dot {
  background: #00d2ff;
}

.theme-pill.active {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 2px rgba(64, 158, 255, 0.2);
  color: var(--text-color);
}

.pill-text {
  white-space: nowrap;
}

/* 修复：深色模式背景透图问题，将 background: var(--glass-bg) 改为 var(--modal-bg) 实心底色 */
.login-form { 
  background: var(--modal-bg); 
  backdrop-filter: none; 
  border-right: 1px solid var(--glass-border); 
  position: absolute; 
  top: 0; 
  left: 0; 
  width: 50%; 
  height: 100%; 
  z-index: 10; 
  transform: translateX(0); 
  transition: transform 0.6s ease-in-out; 
}

.register-form { 
  background: var(--modal-bg); 
  backdrop-filter: none; 
  border-left: 1px solid var(--glass-border); 
  position: absolute; 
  top: 0; 
  right: 0; 
  width: 50%; 
  height: 100%; 
  z-index: 10; 
  transform: translateX(100%); 
  transition: transform 0.6s ease-in-out; 
}

.auth-card.flipped .login-form { transform: translateX(-100%); }
.auth-card.flipped .register-form { transform: translateX(0); }

.corner-logo {
  position: absolute;
  top: 40px;  
  left: 40px; 
  width: 42px;
  height: 42px;
  border-radius: 12px;
  object-fit: cover;
  /* 同样调浅阴影 + 增加随主题变化的边框 */
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
  border: 1px solid var(--glass-border);
  background-color: var(--card-bg);
}
.app-title { 
  font-size: 24px; 
  font-weight: 700; 
  margin-bottom: 20px; 
  color: var(--text-color); 
  text-align: center; 
}

.form-title { 
  font-size: 24px; 
  font-weight: 700; 
  margin-bottom: 20px; 
  color: var(--text-color); 
}

.form-content { 
  width: 100%; 
  max-width: 300px; 
}

:deep(.el-form-item), :deep(.el-input) { 
  width: 100%; 
}

.form-group { 
  margin-bottom: 20px; 
}

.form-label { 
  display: block; 
  margin-bottom: 0px; 
  font-weight: 500; 
  color: var(--text-secondary); 
  font-size: 13px; 
}

.remember-forgot { 
  display: flex; 
  justify-content: space-between; 
  align-items: center; 
  margin-top: 0px; 
  margin-bottom: 0px; 
}

/* 复选框与密码找回 */
:deep(.el-checkbox__label) { color: var(--text-secondary); }
:deep(.el-checkbox__input.is-checked .el-checkbox__inner) { background-color: var(--primary-color); border-color: var(--primary-color) !important; }
/* 核心修复：加深未选中时的边框，确保白底下清晰可见 */
:deep(.el-checkbox__inner) { border: 1px solid rgba(140, 140, 140, 0.5) !important; background-color: var(--input-bg); }

.forgot-password span { color: var(--primary-color); font-size: 14px; cursor: pointer; transition: all 0.2s; }
.forgot-password span:hover { opacity: 0.8; text-decoration: underline; }

:deep(.el-form-item__error) { color: #f56c6c !important; }

/* ========================================= */
/* === 最新修复：输入框样式优化 (边框与提示词) === */
/* ========================================= */
:deep(.el-input__wrapper) { 
  /* 核心修复1：加深边框，使其在简约白风格的白底上清晰可见 */
  border: 1px solid rgba(140, 140, 140, 0.4); 
  border-radius: 8px; 
  box-shadow: none; 
  background: var(--input-bg) !important; 
  transition: all 0.2s ease;
}

:deep(.el-input__inner) { 
  color: var(--text-color); 
  background: transparent !important; 
}

/* 性别下拉框输入框本体：Element Plus 使用 el-select__wrapper */
:deep(.el-select__wrapper) {
  background: var(--input-bg) !important;
  box-shadow: 0 0 0 1px rgba(140, 140, 140, 0.4) inset !important;
  border-radius: 8px !important;
}

:deep(.el-select__wrapper.is-hovering) {
  box-shadow: 0 0 0 1px var(--primary-color) inset !important;
}

:deep(.el-select__wrapper.is-focused) {
  box-shadow: 0 0 0 1px var(--primary-color) inset, 0 0 0 2px rgba(64, 158, 255, 0.2) !important;
}

:deep(.el-select__placeholder) {
  color: rgba(150, 150, 150, 0.8) !important;
}

/* 性别下拉框：选中项和箭头颜色跟随主题 */
:deep(.el-select__selected-item) {
  color: var(--text-color) !important;
}

:deep(.el-select .el-input__suffix-inner .el-icon) {
  color: var(--text-secondary) !important;
}

/* 核心修复2：将提示词改为柔和的半透明灰，降低视觉权重，不要太黑或太亮 */
:deep(.el-input__inner::placeholder) { 
  color: rgba(150, 150, 150, 0.8) !important; 
}
:deep(.el-input__inner::-webkit-input-placeholder) { 
  color: rgba(150, 150, 150, 0.8) !important; 
}
:deep(.el-input__inner::-moz-placeholder) { 
  color: rgba(150, 150, 150, 0.8) !important; 
  opacity: 1; 
}
:deep(.el-input__inner:-ms-input-placeholder) { 
  color: rgba(150, 150, 150, 0.8) !important; 
}

/* 聚焦发光状态保持不变 */
:deep(.el-input__wrapper.is-focus) { 
  border-color: var(--primary-color); 
  box-shadow: 0 0 0 2px rgba(64, 158, 255, 0.2); 
}
/* ========================================= */

/* 提交按钮 */
.submit-btn { 
  width: 100%; 
  font-weight: bold; 
  height: 48px; 
  font-size: 16px; 
  border-radius: 8px; 
  margin-top: 20px; 
  transition: all 0.2s; 
}

.login-btn-spacing { 
  margin-top: 50px; 
}

:deep(.el-button.submit-btn) { 
  background: var(--primary-color) !important; 
  border: none !important; 
  color: white !important; 
}

:deep(.el-button.submit-btn:hover) { 
  opacity: 0.9; 
  transform: translateY(-1px); 
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.3); 
}

:deep(.el-button.submit-btn:active) { 
  transform: scale(0.98) !important; 
}

/* 验证码框 */
.email-row { 
  display: flex; 
  gap: 10px; 
  width: 100%; 
}

.code-btn { 
  width: 120px; 
  border-radius: 8px; 
}

:deep(.el-button.code-btn) { 
  background: var(--glass-bg) !important; 
  border: 1px solid var(--primary-color) !important; 
  color: var(--primary-color) !important; 
}

:deep(.el-button.code-btn:hover) { 
  background: var(--primary-color) !important; 
  color: white !important; 
}

/* 底部切换逻辑 */
.switch-text { 
  margin-top: 16px; 
  font-size: 14px; 
  color: var(--text-secondary); 
  text-align: center; 
  display: flex; 
  align-items: center; 
  justify-content: center; 
  gap: 5px; 
}

.switch-link { 
  color: var(--primary-color); 
  cursor: pointer; 
  font-weight: 600; 
  display: flex; 
  align-items: center; 
  gap: 6px; 
  transition: all 0.2s; 
}

.switch-link:hover { 
  text-decoration: underline; 
  transform: scale(1.05); 
}

.block-arrow { 
  width: 20px; 
  height: 20px; 
  display: block; 
  fill: currentColor; 
}

.arrow-left { 
  transform: rotate(180deg); 
}

@media (max-width: 1024px) {
  .login-container {
    align-items: flex-start;
    overflow-y: visible;
    padding: 16px 0;
  }

  .auth-card {
    height: auto;
    min-height: 680px;
    max-height: none;
    margin: 0 auto;
  }

  .auth-form {
    padding: 30px 24px;
  }

  .app-title,
  .form-title {
    font-size: 34px;
  }

  .form-content {
    max-width: 340px;
  }
}

/* 响应式 */
@media (max-width: 768px) {
  .login-container {
    align-items: center;
    padding: 16px 0;
    overflow-y: visible;
  }

  .login-theme-switch {
    position: static;
    width: 100%;
    justify-content: center;
    margin-bottom: 14px;
  }

  .theme-pill {
    padding: 6px 10px;
  }

  .auth-card { 
    width: min(94vw, 430px);
    max-width: 430px;
    height: auto; 
    min-height: 0;
    max-height: none;
    border-radius: 14px;
    overflow: hidden;
  }

  .auth-form {
    position: relative;
    width: 100%;
    height: auto;
    padding: 20px 18px 22px;
    border: none;
    transform: none;
  }

  .login-form,
  .register-form {
    top: auto;
    right: auto;
    left: auto;
    display: none;
  }

  .auth-card .login-form {
    display: flex;
  }

  .auth-card.flipped .login-form {
    display: none;
  }

  .auth-card .register-form,
  .auth-card.flipped .register-form {
    transform: none;
  }

  .auth-card.flipped .register-form {
    display: flex;
  }

  .corner-logo {
    top: 16px;
    left: 16px;
    width: 30px;
    height: 30px;
    border-radius: 8px;
  }

  .app-title,
  .form-title {
    font-size: 20px;
    margin-bottom: 12px;
  }

  .form-content {
    max-width: 100%;
  }

  .login-btn-spacing {
    margin-top: 24px;
  }

  .remember-forgot {
    flex-wrap: wrap;
    gap: 8px 12px;
    align-items: center;
  }

  .window-controls {
    top: 8px;
    right: 10px;
  }
}

@media (max-width: 560px) {
  .auth-card {
    width: min(96vw, 420px);
  }

  .auth-form {
    padding: 18px 14px 20px;
  }

  .email-row {
    flex-direction: column;
    gap: 8px;
  }

  .code-btn,
  :deep(.el-button.code-btn) {
    width: 100%;
  }

  .submit-btn {
    height: 44px;
    margin-top: 16px;
  }

  .switch-text {
    margin-top: 12px;
    font-size: 13px;
  }

}
</style>

<style>
/* === 找回密码弹窗主题适配 (不加 scoped 才能影响到挂载在 body 上的弹窗) === */
.theme-adapt-dialog {
  background: var(--modal-bg) !important; /* 背景色跟随主题 */
  border: 1px solid var(--glass-border) !important;
  border-radius: 16px !important;
}

/* 标题颜色 */
.theme-adapt-dialog .el-dialog__title {
  color: var(--text-color) !important;
  font-weight: bold;
}

/* 表单 Label 颜色 */
.theme-adapt-dialog .el-form-item__label {
  color: var(--text-secondary) !important;
}

/* 输入框颜色适配 (同登录框一致) */
.theme-adapt-dialog .el-input__wrapper {
  background: var(--input-bg) !important;
  border: 1px solid rgba(140, 140, 140, 0.4) !important;
  box-shadow: none !important;
  border-radius: 8px;
}

.theme-adapt-dialog .el-input__inner {
  color: var(--text-color) !important;
}

/* 提示词颜色 */
.theme-adapt-dialog .el-input__inner::placeholder {
  color: rgba(150, 150, 150, 0.8) !important;
}

/* 聚焦发光 */
.theme-adapt-dialog .el-input__wrapper.is-focus {
  border-color: var(--primary-color) !important;
  box-shadow: 0 0 0 2px rgba(64, 158, 255, 0.2) !important;
}

/* 右上角关闭按钮 (X) */
.theme-adapt-dialog .el-dialog__headerbtn .el-dialog__close {
  color: var(--text-secondary) !important;
}
.theme-adapt-dialog .el-dialog__headerbtn:hover .el-dialog__close {
  color: var(--primary-color) !important;
}

/* === 性别下拉面板主题适配 === */
.theme-adapt-select-dropdown {
  background: var(--modal-bg) !important;
  border: 1px solid var(--glass-border) !important;
}

.theme-adapt-select-dropdown .el-select-dropdown__item {
  color: var(--text-color) !important;
}

.theme-adapt-select-dropdown .el-select-dropdown__item:hover {
  background: var(--modal-hover-bg) !important;
}

/* Element Plus 实际悬停态类，覆盖默认白底 */
.theme-adapt-select-dropdown .el-select-dropdown__item.is-hovering {
  background: var(--modal-hover-bg) !important;
  color: var(--text-color) !important;
}

/* 选中项在 hover 时仍保持主题色，不回退为白底 */
.theme-adapt-select-dropdown .el-select-dropdown__item.is-selected,
.theme-adapt-select-dropdown .el-select-dropdown__item.is-selected.is-hovering {
  background: rgba(64, 158, 255, 0.16) !important;
  color: var(--primary-color) !important;
  font-weight: 600;
}

/* 弹层小三角也跟随面板颜色，避免出现白色尖角 */
.theme-adapt-select-dropdown .el-popper__arrow::before {
  background: var(--modal-bg) !important;
  border-color: var(--glass-border) !important;
}
</style>