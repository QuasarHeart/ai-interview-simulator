<template>
  <!-- 外层布局：稍微增加顶部 padding，为独立的标题栏留出空间 -->
  <div class="layout-wrapper" :style="wrapperStyle">
    
    <!-- === 新增：独立的顶部标题栏 (占据第一行) === -->
    <div class="app-title-bar" v-if="isElectron">
      <!-- 这个区域负责拖拽整个窗口 -->
      <div class="title-bar-drag-area"></div>
      <!-- 窗口控制按钮组 -->
      <div class="window-controls">
        <div class="control-btn min-btn" @click="minimizeWin" title="最小化">
          <!-- 最小化: 一字线 -->
          <svg viewBox="0 0 10 10" class="win-icon"><path d="M1 4.5h8v1H1z" fill="currentColor"/></svg>
        </div>
        <div class="control-btn max-btn" @click="maximizeWin" :title="isMaximized ? '向下还原' : '最大化'">
          <!-- 最大化时: 两个重叠的正方形 -->
          <svg v-if="isMaximized" viewBox="0 0 10 10" class="win-icon">
            <path d="M3 1h6v6h-1V3H3V1zm-2 2h6v6H1V3zm1 1v4h4V4H2z" fill="currentColor"/>
          </svg>
          <!-- 非最大化时: 单个正方形 -->
          <svg v-else viewBox="0 0 10 10" class="win-icon">
            <path d="M1 1h8v8H1V1zm1 1v6h6V2H2z" fill="currentColor"/>
          </svg>
        </div>
        <div class="control-btn close-btn" @click="closeWin" title="关闭">
          <!-- 关闭: 细十字线 -->
          <svg viewBox="0 0 10 10" class="win-icon"><path d="M1.4 1l4 4-4 4 .6.6 4-4 4 4 .6-.6-4-4 4-4-.6-.6-4 4-4-4-.6.6z" fill="currentColor"/></svg>
        </div>
      </div>
    </div>

    <!-- 左侧：悬浮侧边栏 -->
    <aside class="floating-sidebar" :class="{ 'collapsed': isCollapse }" @mouseenter="handleSidebarMouseEnter" @mouseleave="handleSidebarMouseLeave">
      
      <!-- Logo 区域 -->
      <div class="sidebar-header">
        <img src="@/assets/images/logo.jpg" class="logo-image" alt="Logo" />
        <div class="logo-text-wrapper">
          <span class="logo-text">AI 智面</span>
        </div>
      </div>

      <!-- 导航菜单 -->
      <el-menu :default-active="activePath" class="el-menu-vertical" @select="handleMenuSelect">
        <el-menu-item index="/dashboard">
          <div class="menu-icon-wrapper"><el-icon><Odometer /></el-icon></div>
          <span class="menu-text">首页概览</span>
        </el-menu-item>
        
        <!-- 修复点 1：恢复合并后的面试入口 -->
        <el-menu-item index="/interview">
          <div class="menu-icon-wrapper"><el-icon><Service /></el-icon></div>
          <span class="menu-text">面试入口</span>
        </el-menu-item>

        <el-menu-item index="/history">
          <div class="menu-icon-wrapper"><el-icon><Clock /></el-icon></div>
          <span class="menu-text">历史记录</span>
        </el-menu-item>
        <el-menu-item index="/assessment">
          <div class="menu-icon-wrapper"><el-icon><TrendCharts /></el-icon></div>
          <span class="menu-text">能力评估</span>
        </el-menu-item>
        <el-menu-item index="/resume">
          <div class="menu-icon-wrapper"><el-icon><Document /></el-icon></div>
          <span class="menu-text">个人简历</span>
        </el-menu-item>
        <el-menu-item index="/profile">
          <div class="menu-icon-wrapper"><el-icon><User /></el-icon></div>
          <span class="menu-text">用户信息</span>
        </el-menu-item>
      </el-menu>
      
      <!-- 底部退出按钮 -->
      <div class="logout-btn-container">
        <el-button type="danger" plain class="logout-btn" @click="handleLogout">
          <el-icon><SwitchButton /></el-icon>
        </el-button>
      </div>
    </aside>

    <!-- 右侧：主内容大框 -->
    <main class="main-content-wrapper">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

  </div>
</template>

<script setup>
import { useThemeStore } from '../stores/theme'
import { useInterviewStore } from '../stores/interview'
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
// 引入 Service 用于面试入口
import { 
  Odometer, Service, Clock, User, TrendCharts, Document, SwitchButton 
} from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { logout } from '../api/MainLayout'
import { forceFinishInterview } from '../api/interview'
import { clearCurrentUserCache } from '../utils/storage'

const route = useRoute()
const router = useRouter()
const interviewStore = useInterviewStore()
const isCollapse = ref(true)
const isMobile = ref(false)

const themeStore = useThemeStore()
// === 新增：动态背景图逻辑 (和登录界面一致) ===
const getImageUrl = (name) => {
  return new URL(`../assets/images/${name}`, import.meta.url).href
}

const wrapperStyle = computed(() => {
  const theme = themeStore.currentTheme || 'light'
  return {
    '--sidebar-width': isCollapse.value ? '80px' : '240px',
    backgroundImage: `url(${getImageUrl(`auth-bg-${theme}.jpg`)})`
  }
})
// ===========================================

const activePath = computed(() => route.path)

let mobileMediaQuery = null
const updateIsMobile = (event) => {
  isMobile.value = event?.matches ?? mobileMediaQuery?.matches ?? false
  if (isMobile.value) {
    isCollapse.value = true
  }
}

const handleSidebarMouseEnter = () => {
  if (!isMobile.value) {
    isCollapse.value = false
  }
}

const handleSidebarMouseLeave = () => {
  isCollapse.value = true
}

// === 窗口控制逻辑 ===
const isElectron = navigator.userAgent.toLowerCase().includes(' electron/')
const isMaximized = ref(false)



// 监听窗口大小变化，动态更新最大化图标状态
const checkMaximizedStatus = () => {
  if (typeof window !== 'undefined') {
    isMaximized.value = window.outerWidth >= window.screen.availWidth && window.outerHeight >= window.screen.availHeight
  }
}

onMounted(() => {
  if (typeof window !== 'undefined') {
    mobileMediaQuery = window.matchMedia('(max-width: 760px)')
    updateIsMobile(mobileMediaQuery)
    if (typeof mobileMediaQuery.addEventListener === 'function') {
      mobileMediaQuery.addEventListener('change', updateIsMobile)
    } else if (typeof mobileMediaQuery.addListener === 'function') {
      mobileMediaQuery.addListener(updateIsMobile)
    }
  }

  if (isElectron) {
    window.addEventListener('resize', checkMaximizedStatus)
    checkMaximizedStatus()
  }
})

onUnmounted(() => {
  if (mobileMediaQuery) {
    if (typeof mobileMediaQuery.removeEventListener === 'function') {
      mobileMediaQuery.removeEventListener('change', updateIsMobile)
    } else if (typeof mobileMediaQuery.removeListener === 'function') {
      mobileMediaQuery.removeListener(updateIsMobile)
    }
  }

  if (isElectron) {
    window.removeEventListener('resize', checkMaximizedStatus)
  }
})

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
    // 乐观更新状态，提升视觉响应速度
    isMaximized.value = !isMaximized.value
  }
}

// 菜单选择处理
const handleMenuSelect = (index) => {
  handleBeforeNavOrLogout(() => {
    router.push(index)
  })
}

// 检查是否面试进行中 (进行中且报告未生成)
const isInterviewOngoing = () => {
  return interviewStore.currentInterviewId && !interviewStore.isReportReady
}

// 如果面试进行中，先强制结束面试，然后执行操作
const handleBeforeNavOrLogout = async (callback) => {
  if (!isInterviewOngoing()) {
    // 面试未进行，直接执行回调
    callback()
    return
  }

  // 面试进行中，提示用户
  ElMessageBox.confirm(
    '面试还在进行中，离开将强行结束面试。确定要离开吗？',
    '警告',
    {
      confirmButtonText: '确定离开',
      cancelButtonText: '取消',
      type: 'warning',
      customClass: 'theme-confirm-box'
    }
  ).then(async () => {
    try {
      // 调用强制结束面试接口
      await forceFinishInterview(interviewStore.currentInterviewId)
      ElMessage.success('面试已强制结束')
      // 清理状态
      interviewStore.currentInterviewId = null
      interviewStore.messages.splice(0)
      interviewStore.isConnected = false
      // 执行回调（导航或登出）
      callback()
    } catch (error) {
      console.error('强制结束面试失败:', error)
      ElMessage.error('强制结束面试失败，请重试')
    }
  }).catch(() => {
    // 用户取消
  })
}

const closeWin = () => {
  if (isElectron) {
    const { ipcRenderer } = window['require']('electron')
    ipcRenderer.send('window-close')
  }
}

const handleLogout = () => {
  handleBeforeNavOrLogout(() => {
    ElMessageBox.confirm('确定要退出登录吗？', '提示', {
      confirmButtonText: '退出',
      cancelButtonText: '取消',
      type: 'warning',
      customClass: 'theme-confirm-box'
    }).then(async () => {
      let logoutError = null
      try {
        await logout()
      } catch (err) {
        // 如果调用后端退出失败，仍然执行本地退出（避免用户被锁定在页面）
        logoutError = err
        console.warn('logout request failed:', err)
      } finally {
        // 清空当前用户缓存（包括简历信息）
        clearCurrentUserCache()
        localStorage.removeItem('token')
        router.push('/login')
        if (logoutError?.response?.status === 401) {
          ElMessage.info('登录态已失效，已清理本地状态')
        } else {
          ElMessage.success('已退出登录')
        }
      }
    })
  })
}
</script>

<style scoped>
/* 1. 外层布局 */
.layout-wrapper {
  height: 100vh;
  width: 100vw;
  display: flex;
  flex-direction: row;
  background-size: cover;
  background-position: center;
  transition: background-image 0.5s ease; /* 图片切换时平滑过渡 */
  /* 顶部留出 32px 给标题栏，四周保持 20px 间距 */
  padding: 65px 20px 20px 20px; 
  box-sizing: border-box;
  gap: 20px;
  overflow: hidden;
  position: relative;
  /* 移除这里的 -webkit-app-region: drag，交给专用的 title-bar */
}

/* === 修复：主界面的原生标题栏和方形按钮 === */
.app-title-bar {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 65px; /* 微软标准标题栏高度 */
  display: flex;
  justify-content: space-between;
  z-index: 9999;
}

.title-bar-drag-area {
  flex: 1;
  -webkit-app-region: drag; 
}

/* 恢复和 LoginView 完全一致的深色半透明胶囊样式 */
.window-controls { 
  position: absolute;
  top: 15px;
  right: 20px;
  display: flex; 
  align-items: center; 
  -webkit-app-region: no-drag; 
  background: rgba(0, 0, 0, 0.25); 
  backdrop-filter: blur(10px); 
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 20px; 
  padding: 4px 6px; 
  gap: 4px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  z-index: 9999;
}

.control-btn { 
  width: 24px; 
  height: 24px; 
  border-radius: 50%; 
  display: flex; justify-content: center; align-items: center; 
  cursor: pointer; 
  color: #ffffff; /* 保持白色图标 */
  transition: all 0.2s ease; 
}

.win-icon { width: 10px; height: 10px; }
.control-btn:hover { background-color: rgba(255, 255, 255, 0.3); }
.close-btn:hover { background-color: #e81123 !important; color: white; }

/* 2. 侧边栏样式 (保持不变) */
.floating-sidebar { width: var(--sidebar-width); height: 100%; background: var(--sidebar-bg); backdrop-filter: blur(20px); border-radius: 30px; border: 1px solid var(--sidebar-border); display: flex; flex-direction: column; transition: width 0.4s cubic-bezier(0.25, 0.8, 0.25, 1); box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1); overflow: hidden; z-index: 10; padding: 25px 0; flex-shrink: 0; box-sizing: border-box; }
.sidebar-header { display: flex; align-items: center; padding-left: 20px; margin-bottom: 30px; height: 50px; overflow: hidden; flex-shrink: 0; }
.logo-image {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  object-fit: cover; 
  /* 阴影大幅调浅，只保留微弱的立体感 */
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06); 
  /* 新增：使用跟随主题的玻璃边框，在白底下是极浅的灰线，黑底下是极浅的白线 */
  border: 1px solid var(--glass-border); 
  background-color: var(--card-bg); /* 防止某些半透明图片透出杂色 */
  flex-shrink: 0;
}
.logo-text-wrapper { 
  margin-left: 18px; 
  opacity: v-bind("isCollapse ? 0 : 1"); 
  transform: translateX(v-bind("isCollapse ? '-10px' : '0'")); 
  transition: all 0.3s ease; 
  white-space: nowrap; 
}
.logo-text { font-weight: bold; font-size: 18px; color: var(--text-color); }

/* 菜单项居中修复 */
.el-menu-vertical {
  border: none !important;
  background: transparent !important;
  flex: 1;
  width: 100%;
  overflow-x: hidden;
  overflow-y: auto;
  scrollbar-width: thin;
  scrollbar-color: var(--sidebar-scrollbar-thumb) var(--sidebar-scrollbar-track);
}

.el-menu-vertical::-webkit-scrollbar {
  width: 10px;
}

.el-menu-vertical::-webkit-scrollbar-track {
  background: var(--sidebar-scrollbar-track);
  border-radius: 999px;
}

.el-menu-vertical::-webkit-scrollbar-thumb {
  background: var(--sidebar-scrollbar-thumb);
  border-radius: 999px;
  border: 2px solid transparent;
  background-clip: padding-box;
}

.el-menu-vertical::-webkit-scrollbar-thumb:hover {
  background: color-mix(in srgb, var(--sidebar-scrollbar-thumb) 78%, var(--primary-color) 22%);
  border: 2px solid transparent;
  background-clip: padding-box;
}
:deep(.el-menu-item) { height: 50px; line-height: 50px; margin: 8px 12px; border-radius: 12px; color: var(--text-secondary); transition: all 0.3s; display: flex; align-items: center; padding: 0 !important; }
.menu-icon-wrapper { width: 56px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
:deep(.el-icon) { font-size: 22px; margin: 0; }
.menu-text { white-space: nowrap; opacity: v-bind("isCollapse ? 0 : 1"); transform: translateX(v-bind("isCollapse ? '10px' : '0'")); transition: all 0.3s ease; padding-left: 5px; }
:deep(.el-menu-item:hover) { background-color: var(--sidebar-active-bg); color: var(--primary-color); }
:deep(.el-menu-item.is-active) { background-color: var(--primary-color); color: white; box-shadow: 0 4px 12px rgba(0,0,0,0.2); }
:deep(.el-menu-item.is-active .el-icon) { color: white; }

/* 退出按钮样式 */
.logout-btn-container { display: flex; justify-content: flex-start; padding-left: 18px; padding-top: 10px; height: 60px; flex-shrink: 0; }
.logout-btn { width: 44px !important; height: 44px !important; border-radius: 50% !important; padding: 0 !important; display: flex; align-items: center; justify-content: center; border: 1px solid var(--glass-border); background: transparent; transition: all 0.3s; flex-shrink: 0; }
.logout-btn:hover { background-color: #f56c6c !important; color: white !important; border-color: #f56c6c !important; transform: rotate(90deg); }

/* === 3. 右侧内容大卡片全透明化 === */
.main-content-wrapper {
  flex: 1; 
  height: 100%; 
  
  /* 核心修改 1：完全透明，移除原本的 var(--glass-bg) */
  background: transparent !important; 
  
  /* 核心修改 2：去除磨砂模糊效果，实现彻底看穿背景 */
  backdrop-filter: none !important; 
  -webkit-backdrop-filter: none !important;
  
  border-radius: 30px;
  border: 1px solid var(--glass-border); /* 保留边缘发光的细线 */
  position: relative;
  overflow: hidden;
  box-sizing: border-box;
}
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

@media (max-width: 760px) {
  .layout-wrapper {
    --sidebar-width: 66px !important;
    padding: 12px 8px 8px;
    gap: 8px;
  }

  .floating-sidebar {
    border-radius: 20px;
    padding: 14px 0;
  }

  .sidebar-header {
    padding-left: 13px;
    margin-bottom: 16px;
    height: 38px;
  }

  .logo-image {
    width: 30px;
    height: 30px;
    border-radius: 9px;
  }

  .menu-icon-wrapper {
    width: 44px;
  }

  :deep(.el-menu-item) {
    height: 42px;
    line-height: 42px;
    margin: 6px 8px;
    border-radius: 10px;
  }

  :deep(.el-icon) {
    font-size: 18px;
  }

  .logout-btn-container {
    padding-left: 10px;
    height: 50px;
  }

  .logout-btn {
    width: 40px !important;
    height: 40px !important;
  }

  .main-content-wrapper {
    border-radius: 20px;
  }
}
</style>