// src/main.js
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'

// 1. 引入 Element Plus 的样式
import 'element-plus/dist/index.css'
// 2. 引入 Element Plus 的图标库
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
// 3. 引入 Element Plus 本体
import ElementPlus from 'element-plus'

// 4. 引入我们写的全局样式
import './assets/styles/main.scss'

const app = createApp(App)

// 注册所有图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

app.use(createPinia())
app.use(router)
app.use(ElementPlus) // 使用 UI 库

app.mount('#app')