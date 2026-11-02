# 🎭 伯乐智面 · Bole AI Interview

> **AI 多模态模拟面试系统** — Web 与 Electron 双端同构的前端交互与采集展现层

[![Vue](https://img.shields.io/badge/Vue-3.5-4FC08D?style=flat&logo=vue.js)](https://vuejs.org/)
[![Vite](https://img.shields.io/badge/Vite-7.x-646CFF?style=flat&logo=vite)](https://vitejs.dev/)
[![Electron](https://img.shields.io/badge/Electron-40-47848F?style=flat&logo=electron)](https://www.electronjs.org/)
[![LiveKit](https://img.shields.io/badge/LiveKit-WebRTC-0EA5E9?style=flat)](https://livekit.io/)
[![Node](https://img.shields.io/badge/Node-%E2%89%A520.19-339933?style=flat&logo=node.js)](https://nodejs.org/)

**伯乐智面**覆盖 **「准备 → 对练 → 复盘 → 迭代」** 的完整面试训练路径：支持文本、语音、视频三种面试形态，实时推送麦克风与摄像头，订阅云端数字人音视频流，并在面试结束后生成结构化评估报告。

---

## ✨ 核心能力

| | 能力 | 说明 |
|---|---|---|
| 🎙️ | **实时全双工通话** | 基于 `livekit-client`（WebRTC），前端直接推送底层麦克风/摄像头轨道，远端 AI 面试官的音频与视频通过 `Track.attach()` 挂载，取代传统 HTTP 轮询，支持自然打断。 |
| 🦸 | **端云解耦的数字人** | 数字人画面由云端渲染为音视频流下发，前端只做轻量「播放容器」，不在本地重建 3D 场景。（仓库保留了实验组件 `Interviewer3D.vue`，当前未挂载。） |
| 🛡️ | **会话状态与路由守卫** | Pinia 管理面试状态，`onBeforeRouteLeave` 拦截中途强退并释放麦克风、摄像头、录制器；正常结束时以「报告生成中」状态放行跳转，避免死锁。 |
| 📊 | **结构化报告闭环** | ECharts 渲染 **10 维**能力雷达图与维度拆解，`html2pdf.js` 在前端直接把报告 DOM 导出为 PDF。 |
| 📄 | **简历与附件** | 简历中心支持 PDF 上传与预览；创建面试时可附带 PDF / Word 简历，Word 由 `mammoth` 转为 HTML 渲染；本地缓存按用户身份隔离，避免多账号串号。 |
| 🎨 | **多主题与转场** | 原生 CSS Variables 驱动浅色 / 深色 / 蓝色主题，配合 `View Transitions API` 实现水滴扩散切换。 |
| 💻 | **双端统一** | 同一套页面同时服务浏览器与 Electron，仅在路由模式与窗口控制上按运行时做少量适配。 |

---

## 🛠 技术栈

| 分类 | 选型 | 说明 |
|---|---|---|
| 核心框架 | Vue 3.5（Composition API） | 全部视图使用 `<script setup>` |
| 构建工具 | Vite 7 + `vite-plugin-electron` | 一套配置同时产出 Web 资源与 Electron 主进程 |
| 桌面端 | Electron 40 + `electron-builder` | NSIS 安装包，ASAR 归档 |
| 状态与路由 | Pinia 3 + Vue Router 5 | 登录态与面试状态分离 |
| 流媒体 | `livekit-client` 2.18 | WebRTC 房间、推流与订阅 |
| UI | Element Plus 2.13 + 图标库 | 配合原生 CSS Variables 做主题 |
| 图表 | Apache ECharts 6 | 雷达图、折线图 |
| 文档处理 | `html2pdf.js`、`mammoth`、`markdown-it`、`highlight.js` | PDF 导出、docx 预览、复盘文本渲染 |
| 样式 | Sass | 全局变量与主题文件 |

---

## 🚀 快速开始

### 1. 环境要求

- **Node.js ≥ 20.19**（Vite 7 的最低要求，推荐 22 LTS）
- npm 10+
- 能访问后端接口与 LiveKit 服务端的网络

### 2. 安装依赖

```bash
npm install
```

### 3. 配置后端地址

接口基地址目前直接写在 **[`src/utils/request.js`](src/utils/request.js)** 的 `baseURL` 中（默认 `https://nas.feixingxr.com`），切换环境时修改此处即可。

官网「下载客户端」按钮还支持用环境变量指向外链，避免把安装包放进仓库：

```bash
# .env.local
VITE_APP_DOWNLOAD_URL=https://your-cdn.com/伯乐智面-Setup.exe
```

> 未配置时回退到 `/downloads/伯乐智面-Setup.exe`（即 `public/downloads/` 下的文件）。

### 4. 本地开发

```bash
npm run dev
```

> `npm run dev` 会同时启动 Vite 和 Electron 窗口（vite-plugin-electron 默认行为）。只想在浏览器里调试时，直接打开终端输出的 Vite 本地地址即可。

### 5. 构建

```bash
# Web 静态资源 → dist/
npm run build

# 当前平台安装包 → release/
npm run dist

# Windows NSIS 安装包 → release/
npm run dist:win
```

---

## 📜 可用脚本

| 命令 | 作用 |
|---|---|
| `npm run dev` | 启动 Vite 开发服务器并拉起 Electron（HMR） |
| `npm run build` | 生成应用图标并构建 Web 资源到 `dist/`，同时构建主进程到 `dist-electron/` |
| `npm run dist` | 构建后打包当前平台安装包到 `release/` |
| `npm run dist:win` | 构建后打包 Windows（NSIS x64）安装包 |
| `npm run preview` | 本地预览 `dist/` 产物 |
| `npm run prepare:icon` | 由源图生成 `build/icon.ico` |
| `npm run prune:downloads` | 删除 `dist/downloads/` 下的安装包副本，防止其被打进 `app.asar` |

---

## 📂 目录结构

```text
ai-interview/
├── electron/                 # Electron 主进程与预加载脚本
│   ├── main.js               # 窗口创建、无边框标题栏、窗口控制 IPC
│   └── preload.js
├── scripts/                  # 构建辅助脚本（图标生成、安装包裁剪、DOCX 导出）
├── public/                   # 原样复制到 dist 的静态资源（3D 模型、场景、下载文件）
├── src/
│   ├── api/                  # 后端接口契约，按业务域拆分
│   ├── assets/               # 主题样式与静态图片
│   ├── components/           # 复用组件（创会弹窗、主题切换、3D 面试官实验组件）
│   ├── layout/               # MainLayout：侧边栏骨架 + Electron 原生窗口控制
│   ├── router/               # 路由表与登录 / 强退守卫
│   ├── stores/               # Pinia：interview（LiveKit 调度）、theme、user
│   ├── utils/                # axios 封装、音频重采样、用户级存储、Token 续期
│   ├── views/
│   │   ├── official/         # 官网首页（Web 端默认入口）
│   │   ├── dashboard/        # 数据大盘与简历速览
│   │   ├── interview/        # 面试工作台（文本 / 语音 / 视频）
│   │   ├── history/          # 历史记录与复盘报告
│   │   ├── assessment/       # 能力评估
│   │   ├── resume/           # 简历中心
│   │   ├── profile/          # 个人中心
│   │   └── LoginView.vue     # 登录 / 注册
│   ├── App.vue
│   └── main.js
├── docs/                     # 详细设计方案（md / docx）
├── vite.config.js
└── package.json
```

---

## 🗺 页面与路由

| 路由 | 页面 | 说明 |
|---|---|---|
| `/offical` | `OfficialSiteView` | 官网首页，Web 端默认入口 |
| `/login` | `LoginView` | 登录 / 注册 / 找回密码 |
| `/dashboard` | `DashboardView` | 数据大盘、近期表现、简历速览 |
| `/interview` | `InterviewPortalView` | 面试工作台，三种面试形态 |
| `/history` | `HistoryView` | 历史面试列表 |
| `/history/:id` | `InterviewDetailView` | 复盘报告与 PDF 导出 |
| `/assessment` | `AssessmentView` | 能力评估与趋势 |
| `/resume` | `ResumeView` | 简历上传与管理 |
| `/profile` | `ProfileView` | 个人资料 |

> 除 `/offical` 与 `/login` 外，其余路由均要求登录态。

---

## 🌐 双端运行差异

| 维度 | 浏览器端 | Electron 端 |
|---|---|---|
| 路由模式 | `history` | `hash` |
| 默认入口 | `/offical` 官网 | `/dashboard`（不展示官网） |
| 窗口控制 | 无 | 自绘标题栏 + IPC（`window-min` / `window-max` / `window-close`） |
| 构建命令 | `npm run build` | `npm run dist:win` |

---

## 🔄 关键链路

1. **创建面试**：提交岗位、难度、风格与面试形态，拿到 `interviewId`。
2. **建立通话**（语音 / 视频模式）：响应中携带 `livekitToken` 与 `url`，前端 `Room.connect()` 后开启麦克风（视频模式再加摄像头）。
3. **订阅数字人**：`RoomEvent.TrackSubscribed` 拿到远端轨道，音频 `attach` 到隐藏 `<audio>`，视频 `attach` 到数字人 `<video>`。
4. **文本模式**：回答通过 `text/event-stream` 流式返回，逐字渲染。
5. **结束与复盘**：正常结束 → 报告就绪 → 跳转 `/history/:id`，渲染雷达图、维度明细与改进建议，可一键导出 PDF。

---

## 🧰 排障指南

### 麦克风 / 摄像头无法采集

浏览器安全策略要求非 `localhost` 环境必须使用 **HTTPS**，否则 `getUserMedia` 会被直接拦截。

### Web 端刷新出现 404

浏览器端使用 history 路由。部署到 Nginx 时需添加伪静态规则：

```nginx
location / {
  try_files $uri $uri/ /index.html;
}
```

### 通话延迟升高 / 画面卡顿

检查 LiveKit Server 的网络与防火墙：若 UDP 端口 `50000-60000` 被封锁，WebRTC 会降级为 TURN over TCP，延迟明显上升。

### 安装包体积异常增大

`public/` 下的文件会被原样复制进 `dist/`，而 `electron-builder` 的 `files` 包含 `dist/**/*`，因此放在 `public/downloads/` 的安装包会被打包进新的 `app.asar`。建议：

1. 安装包不要放进 `public/`，官网下载改用 `VITE_APP_DOWNLOAD_URL` 指向 CDN；
2. 构建后执行 `npm run prune:downloads` 清理 `dist/downloads/`；
3. 主进程已由 Vite 打包，可在打包配置中排除 `node_modules` 进一步瘦身。

---

## 📄 设计文档

更完整的模块设计、数据流与异常处理说明见 [`docs/前端详细设计方案.docx`](docs/前端详细设计方案.docx)。
