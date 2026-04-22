<template>
  <div class="theme-switch-container">
    <div v-for="theme in themes" :key="theme.value" class="theme-card" :class="[theme.value, { active: currentTheme === theme.value }]" @click="handleThemeChange(theme.value)">
      <div class="deco-circle"></div>
      <span class="theme-name">{{ theme.label }}</span>
      <div class="active-indicator" v-if="currentTheme === theme.value">
        <svg viewBox="0 0 1024 1024" width="10" height="10"><path d="M912 190h-69.9c-9.8 0-19.1 4.5-25.1 12.2L404.7 724.5 207 474a32 32 0 0 0-25.1-12.2H112c-6.7 0-10.4 7.7-6.3 12.9l273.9 347c12.8 16.2 37.4 16.2 50.3 0l488.4-618.9c4.1-5.1 0.4-12.8-6.3-12.8z" fill="currentColor"></path></svg>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useThemeStore } from '../stores/theme'

const themeStore = useThemeStore()
const currentTheme = computed(() => themeStore.currentTheme)

const themes =[
  { label: '简约白', value: 'light' },
  { label: '科技蓝', value: 'blue' },
  { label: '深邃黑', value: 'dark' }
]

const handleThemeChange = (val) => themeStore.setTheme(val)
</script>

<style scoped>
.theme-switch-container {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
  width: 100%;
}

/* 改为小巧的横向布局 */
.theme-card {
  height: 36px; /* 变矮 */
  border-radius: 8px;
  cursor: pointer;
  border: 2px solid transparent;
  display: flex;
  align-items: center; /* 横向排列居中 */
  padding: 0 8px;
  gap: 6px;
  transition: all 0.2s;
  position: relative;
  overflow: hidden;
}

.theme-card:hover { transform: translateY(-1px); box-shadow: 0 2px 8px rgba(0,0,0,0.1); }

/* 主题颜色 */
.theme-card.light { background: linear-gradient(135deg, #ffffff 0%, #f0f2f5 100%); color: #333; border-color: #dcdfe6; }
.theme-card.light .deco-circle {
  background: #ffffff;
  border: 1px solid #cfd6e4;
  box-shadow: 0 1px 2px rgba(15, 23, 42, 0.14);
}
.theme-card.blue { background: linear-gradient(135deg, #001529 0%, #003a8c 100%); color: #fff; border-color: #1890ff; }
.theme-card.blue .deco-circle { background: #1890ff; }
.theme-card.dark { background: linear-gradient(135deg, #141414 0%, #2c3e50 100%); color: #fff; border-color: #444; }
.theme-card.dark .deco-circle { background: #00d2ff; }
.theme-card.active { border-color: var(--primary-color); box-shadow: 0 0 0 2px rgba(64, 158, 255, 0.2); }

.deco-circle { width: 12px; height: 12px; border-radius: 50%; opacity: 0.6; flex-shrink: 0; }
.theme-name { font-size: 12px; font-weight: bold; flex: 1; text-align: left; }
.active-indicator { width: 14px; height: 14px; border-radius: 50%; background: var(--primary-color); color: white; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }

@media (max-width: 760px) {
  .theme-switch-container {
    display: flex;
    gap: 8px;
    overflow-x: auto;
    overflow-y: hidden;
    padding: 2px 1px;
    scrollbar-width: none;
    -webkit-overflow-scrolling: touch;
  }

  .theme-switch-container::-webkit-scrollbar {
    display: none;
  }

  .theme-card {
    flex: 0 0 auto;
    min-width: 86px;
    height: 34px;
    padding: 0 9px;
    border-radius: 10px;
  }

  .theme-name {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    font-size: 13px;
  }
}

@media (max-width: 560px) {
  .theme-card {
    min-width: 82px;
    height: 32px;
    padding: 0 8px;
    gap: 5px;
  }

  .deco-circle {
    width: 11px;
    height: 11px;
  }

  .theme-name {
    font-size: 12px;
  }

  .active-indicator {
    width: 13px;
    height: 13px;
  }
}
</style>