import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useThemeStore = defineStore('theme', () => {
  const savedTheme = localStorage.getItem('theme') || 'light'
  const currentTheme = ref(savedTheme)

  function setTheme(themeName) {
    const html = document.documentElement
    
    // 如果点击的是当前主题，直接返回，防止重复触发
    if (currentTheme.value === themeName && 
       (themeName === 'dark' ? !html.classList.contains('light-theme') && !html.classList.contains('blue-theme') : html.classList.contains(`${themeName}-theme`))) {
      return
    }

    // 实际替换类名的操作
    const applyTheme = () => {
      // ✅ 关键优化：禁用全局过渡，防止CSS变量切换时的卡顿
      html.classList.add('theme-switching')
      
      currentTheme.value = themeName
      localStorage.setItem('theme', themeName)
      html.classList.remove('light-theme', 'blue-theme')
      if (themeName !== 'dark') {
        html.classList.add(`${themeName}-theme`)
      }
      
      // 触发重排以确保样式更新，然后移除禁用类
      html.offsetHeight
      html.classList.remove('theme-switching')
    }

    // === 核心修改：水滴波浪特效 (View Transitions API) ===
    // 检查浏览器是否支持该现代 API，如果不支持则直接切换（兼容性处理）
    if (!document.startViewTransition) {
      applyTheme()
      return
    }

    // 开启视图过渡，浏览器会截取当前屏幕画面的快照
    const transition = document.startViewTransition(() => {
      applyTheme() // 渲染新主题
    })

    // 新主题渲染完毕后，开始执行水滴扩散遮罩动画
    transition.ready.then(() => {
      // 计算屏幕中心点
      const x = window.innerWidth / 2
      const y = window.innerHeight / 2
      // 计算中心到屏幕最远角落的半径距离，确保波浪能盖满全屏
      const maxRadius = Math.hypot(Math.max(x, window.innerWidth - x), Math.max(y, window.innerHeight - y))

      // 让新页面以圆形逐渐扩大的方式呈现
      document.documentElement.animate(
        {
          clipPath:[
            `circle(0px at ${x}px ${y}px)`,
            `circle(${maxRadius}px at ${x}px ${y}px)`
          ]
        },
        {
          duration: 600, // 优化：缩短到0.6秒，更流畅
          easing: 'ease-in-out', // 像水波一样平滑开始和结束
          pseudoElement: '::view-transition-new(root)' // 只作用于新页面的图层
        }
      )
    })
  }

  const initTheme = () => {
    const html = document.documentElement
    html.classList.remove('light-theme', 'blue-theme')
    if (currentTheme.value !== 'dark') {
      html.classList.add(`${currentTheme.value}-theme`)
    }
  }
  initTheme()

  return { currentTheme, setTheme }
})