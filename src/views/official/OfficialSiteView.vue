<template>
  <div class="official-redesign">
    <header class="site-nav">
      <button class="brand" @click="scrollToBlock('hero')">
        <img :src="imageUrl('logo.jpg')" alt="AI模拟面试平台" />
        <span>AI模拟面试平台</span>
      </button>

      <nav class="nav-links">
        <button v-for="item in navItems" :key="item.id" @click="scrollToBlock(item.id)">{{ item.label }}</button>
      </nav>

      <div class="nav-actions">
        <button class="btn solid" @click="goLogin">立即体验</button>
        <button class="btn ghost nav-download" type="button" @click="downloadSoftware">下载软件</button>
      </div>
    </header>

    <section id="hero" class="hero-block">
      <div class="hero-inner">
        <div class="hero-copy">
          <p class="eyebrow">AI Interview System</p>
          <h1>
            让面试准备
            <span class="hero-line-two"><em>更像</em>真实作战</span>
          </h1>
          <p>
            从岗位定制、实时追问到报告复盘，完整还原求职面试链路。语音面试、视频面试、文本陪练三种模式自由切换，
            训练效率和临场表现一起提升。
          </p>

          <div class="hero-actions">
            <button class="btn solid" @click="goLogin">开始一场模拟面试</button>
            <button class="btn ghost" @click="scrollToBlock('workflow')">查看流程</button>
          </div>

          <div class="hero-metrics">
            <div v-for="metric in metrics" :key="metric.label">
              <strong>{{ metric.value }}</strong>
              <span>{{ metric.label }}</span>
            </div>
          </div>
        </div>

        <div class="hero-preview">
          <div class="screen-stage">
            <div
              v-for="(slide, idx) in slides"
              :key="slide.title"
              class="screen-card"
              :class="slideState(idx)"
            >
              <img :src="slide.src" :alt="slide.title" />
              <div class="screen-meta">
                <p>{{ slide.tag }}</p>
                <h3>{{ slide.title }}</h3>
              </div>
            </div>
          </div>

          <div class="screen-dots">
            <button
              v-for="(slide, idx) in slides"
              :key="`dot-${slide.title}`"
              :class="{ active: activeSlide === idx }"
              @click="selectSlide(idx)"
              :aria-label="`切换到${slide.title}`"
            ></button>
          </div>

          <p class="screen-hint">界面图轮播中，自动展示不同功能场景</p>
        </div>
      </div>
    </section>

    <section id="capability" class="segment segment-a">
      <div class="segment-inner split">
        <div class="capability-copy">
          <p class="segment-kicker">核心能力</p>
          <h2>不是堆功能，而是把求职训练串成闭环</h2>
          <p>
            AI模拟面试平台围绕“准备 - 对练 - 复盘 - 迭代”设计产品路径，避免只给结论不讲策略。你可以直接看到每次问答背后的能力维度变化。
          </p>
        </div>

        <ul class="check-list">
          <li v-for="(item, idx) in capabilityBullets" :key="item">
            <span class="check-index">0{{ idx + 1 }}</span>
            <p>{{ item }}</p>
          </li>
        </ul>
      </div>
    </section>

    <section id="scenes" class="segment segment-b">
      <div class="segment-inner">
        <p class="segment-kicker">适配岗位</p>
        <h2>同一套系统，覆盖技术岗位全链路面试习惯</h2>

        <div class="scene-grid">
          <article v-for="scene in scenes" :key="scene.role">
            <h3>{{ scene.role }}</h3>
            <p>{{ scene.desc }}</p>
          </article>
        </div>

        <div class="role-tags">
          <span v-for="track in technicalTracks" :key="track">{{ track }}</span>
        </div>
      </div>
    </section>

    <section id="workflow" class="segment segment-c">
      <div class="segment-inner">
        <p class="segment-kicker">使用路径</p>
        <h2>四步进入高质量面试训练</h2>

        <div class="timeline">
          <article v-for="(step, idx) in flowSteps" :key="step.step" class="flow-step" :class="`step-${idx + 1}`">
            <span class="flow-index">{{ step.step }}</span>
            <h3>{{ step.title }}</h3>
            <p>{{ step.desc }}</p>
          </article>

          <div class="orbit-arrows" aria-hidden="true">
            <span class="orbit-arrow top">→</span>
            <span class="orbit-arrow right">↓</span>
            <span class="orbit-arrow bottom">←</span>
            <span class="orbit-arrow left">↑</span>
          </div>

          <div class="flow-core" aria-hidden="true">
            <strong>闭环训练</strong>
            <span>持续迭代</span>
          </div>
        </div>
      </div>
    </section>

    <section id="assessment" class="segment segment-h">
      <div class="segment-inner">
        <p class="segment-kicker">Assessment</p>
        <h2>能力评估中心：雷达图 + 趋势折线 + AI 建议</h2>
        <p>
          每次面试结束后自动生成综合评估结果：雷达图看维度短板，折线图看成长趋势，AI 建议告诉你下次怎么答得更好。
        </p>

        <div class="assessment-grid">
          <article
            v-for="item in assessmentHighlights"
            :key="item.title"
            class="assessment-card"
            :class="`layout-${item.chartLayout || 'text'}`"
          >
            <div class="assessment-main">
              <div class="assessment-copy">
                <h3>{{ item.title }}</h3>
                <p>{{ item.desc }}</p>
              </div>

              <figure v-if="item.chartSrc && item.chartLayout === 'right'" class="assessment-inline-chart chart-right">
                <img :src="item.chartSrc" :alt="`${item.title}图表`" loading="lazy" />
              </figure>
            </div>

            <figure v-if="item.chartSrc && item.chartLayout === 'bottom'" class="assessment-inline-chart chart-bottom">
              <img :src="item.chartSrc" :alt="`${item.title}图表`" loading="lazy" />
            </figure>

            <div class="assessment-tags">
              <span v-for="tag in item.tags" :key="tag">{{ tag }}</span>
            </div>
          </article>
        </div>
      </div>
    </section>

    <section id="resume-ai" class="segment segment-i">
      <div class="segment-inner resume-ai-layout">
        <div class="resume-copy">
          <p class="segment-kicker">Resume AI</p>
          <h2>AI 简历分析：优点、缺点与优化建议一屏呈现</h2>
          <p>
            支持上传 PDF 简历后自动分析，输出结构化结论，并配合优秀模板库辅助你快速重写关键经历，提升投递命中率。
          </p>
          <ul class="resume-bullets">
            <li v-for="item in resumeBullets" :key="item">{{ item }}</li>
          </ul>
        </div>

        <div class="resume-panels">
          <article v-for="(panel, idx) in resumePanels" :key="panel.title" class="resume-panel">
            <div>
              <h3>{{ panel.title }}</h3>
              <p>{{ panel.desc }}</p>
            </div>
          </article>
        </div>
      </div>
    </section>

    <section id="architecture" class="segment segment-d">
      <div class="segment-inner">
        <p class="segment-kicker">Engineering</p>
        <h2>基于现有代码实现的产品与工程能力</h2>

        <div class="architecture-grid">
          <article v-for="block in architectureBlocks" :key="block.title" class="architecture-card">
            <h3>{{ block.title }}</h3>
            <ul>
              <li v-for="item in block.points" :key="item">{{ item }}</li>
            </ul>
          </article>
        </div>
      </div>
    </section>

    <section id="faq" class="segment segment-g">
      <div class="segment-inner">
        <p class="segment-kicker">FAQ</p>
        <h2>常见问题</h2>

        <div class="faq-wrap">
          <details v-for="item in faqs" :key="item.q" class="faq-item">
            <summary>{{ item.q }}</summary>
            <p>{{ item.a }}</p>
          </details>
        </div>
      </div>
    </section>

    <section class="final-cta" aria-label="官网底部行动引导">
      <div class="final-cta-inner">
        <p class="final-cta-kicker">Ready to Start</p>
        <h2>用AI模拟面试平台，把每次面试都变成进步曲线</h2>
        <p class="final-cta-desc">
          从模拟问答到报告复盘，一套流程覆盖你的求职训练周期。现在开始，下一场面试会更稳。
        </p>

        <button class="final-cta-button" @click="goLogin">立即开始体验 <span>→</span></button>

        <div class="final-cta-points">
          <span v-for="point in closingHighlights" :key="point">{{ point }}</span>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { onMounted, onUnmounted, ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const localDownloadUrl = '/downloads/AI模拟面试平台-Setup.exe'
const downloadUrl = import.meta.env.VITE_APP_DOWNLOAD_URL || (import.meta.env.DEV ? localDownloadUrl : '')
const downloadFileName = 'AI模拟面试平台-Setup.exe'

const imageUrl = (name) => new URL(`../../assets/images/${name}`, import.meta.url).href

const navItems = [
  { id: 'capability', label: '核心能力' },
  { id: 'scenes', label: '适配岗位' },
  { id: 'workflow', label: '使用路径' },
  { id: 'assessment', label: '能力评估' },
  { id: 'resume-ai', label: 'AI简历分析' },
  { id: 'architecture', label: '工程架构' },
  { id: 'faq', label: '常见问题' }
]

const metrics = [
  { value: '3 种', label: '面试模式' },
  { value: '10+', label: '岗位方向' },
  { value: '4 步', label: '完整闭环' }
]

const slides = [
  { src: imageUrl('image-1.png'), title: '官网展示 01', tag: '场景 01' },
  { src: imageUrl('image-2.png'), title: '官网展示 02', tag: '场景 02' },
  { src: imageUrl('image0.png'), title: '官网展示 03', tag: '场景 03' },
  { src: imageUrl('image1.png'), title: '官网展示 04', tag: '场景 04' },
  { src: imageUrl('image2.png'), title: '官网展示 05', tag: '场景 05' },
  { src: imageUrl('image3.png'), title: '官网展示 06', tag: '场景 06' },
  { src: imageUrl('image4.png'), title: '官网展示 07', tag: '场景 07' },
  { src: imageUrl('image5.png'), title: '官网展示 08', tag: '场景 08' }
]

const capabilityBullets = [
  '面试过程实时追问，训练临场应对与结构化表达',
  '支持语音和视频模式，贴近真实沟通压强',
  '每场结束自动生成报告，定位优势与短板',
  '历史记录可回看，持续追踪你的能力变化'
]

const scenes = [
  { role: '后端开发', desc: '覆盖 Java、Python、Golang 技术问答与系统设计追问。' },
  { role: '前端开发', desc: '聚焦工程化、性能优化、框架机制与项目落地表达。' },
  { role: '测试工程师', desc: '围绕测试策略、自动化体系、质量保障与缺陷分析。' },
  { role: '数据与算法', desc: '强调建模思路、实验设计、特征工程与评估闭环。' }
]

const technicalTracks = [
  'Java 后端',
  'Python 后端',
  'Golang 后端',
  'Web 前端',
  '软件测试工程师',
  'DevOps',
  '系统架构师',
  '数据工程师',
  'SRE',
  '机器学习工程师'
]

const flowSteps = [
  { step: '01', title: '选择岗位与难度', desc: '根据目标公司和职级快速选择面试风格。' },
  { step: '02', title: '进入模拟对练', desc: '通过连续追问逼近真实面试节奏，不再只做单题练习。' },
  { step: '03', title: '查看结构化报告', desc: '系统按维度给出评分、解释与可执行建议。' },
  { step: '04', title: '复盘并迭代', desc: '回看历史表现，对症训练，持续稳定提升。' }
]

const assessmentHighlights = [
  {
    title: '雷达图能力画像',
    desc: '从表达、逻辑、专业匹配等维度直观看到当前能力分布。',
    chartSrc: imageUrl('image6.png'),
    chartLayout: 'right',
    tags: ['维度对比', '短板定位', '目标拆解']
  },
  {
    title: '折线趋势追踪',
    desc: '按场次查看核心指标变化曲线，判断训练是否真正有效。',
    chartSrc: imageUrl('image7.png'),
    chartLayout: 'bottom',
    tags: ['历史趋势', '阶段复盘', '成长轨迹']
  },
  {
    title: 'AI 个性化建议',
    desc: '结合具体回答内容输出可执行建议，不只告诉你分数。',
    tags: ['问题拆解', '表达优化', '下一次如何作答']
  },
  {
    title: '报告与历史联动',
    desc: '报告结论可回看、可对比，形成长期训练闭环。',
    tags: ['报告沉淀', '历史对比', '持续迭代']
  }
]

const resumeBullets = [
  '自动提取简历优点、缺点与优化建议',
  '支持 PDF 简历上传与预览，分析结果可复用',
  '结合优秀简历模板库快速改写项目经历',
  '与岗位方向联动，突出技术栈与业务价值表达'
]

const resumePanels = [
  {
    title: '优点亮点提取',
    desc: '识别技术深度、项目价值、结果导向表达，保留你最有竞争力的信息。'
  },
  {
    title: '问题项诊断',
    desc: '指出冗余叙述、缺失量化指标、技术关键词不完整等影响投递的问题。'
  },
  {
    title: '改写建议与模板参考',
    desc: '给出可直接落地的改写方向，并搭配优秀简历模板进行风格对照。'
  }
]

const architectureBlocks = [
  {
    title: '产品模块矩阵',
    points: ['Dashboard 数据总览', 'Interview 对练场景', 'History 历史档案', 'Assessment 能力评估', 'Resume 简历分析', 'Profile 个人设置']
  },
  {
    title: '实时与流式能力',
    points: ['LiveKit+VAD 音视频房间连接', '实时语音/视频通话模式', 'SSE 流式问答返回', '报告异步轮询与就绪跳转', '路由守卫与会话状态管理']
  },
  {
    title: '技术栈实现',
    points: ['Vue 3 + Pinia + axios', 'Element Plus 组件体系', 'Vite 构建与开发调试', 'Electron 桌面端兼容', '主题体系与多页面视觉统一']
  }
]

const faqs = [
  {
    q: 'AI模拟面试平台适用于什么岗位？',
    a: '覆盖大量技术岗位方向，包括后端、前端、测试、DevOps、数据与算法等，具体岗位可参考上方“适配岗位”模块。'
  },
  {
    q: '面试过程会被记录吗？',
    a: '会记录你的问答内容和面试评分，用于历史复盘与能力趋势分析；你也可以在个人中心管理历史数据。'
  },
  {
    q: '支持哪些面试平台与设备？',
    a: '当前支持桌面软件和 Web 网站，并已适配手机端网站访问；不同设备下核心流程和主要功能保持一致。'
  },
  {
    q: '评分依据是什么？',
    a: '系统结合表达清晰度、逻辑结构、问题拆解、专业匹配等维度给出结构化反馈，并提供可执行的改进建议。'
  },
  {
    q: '如何开始第一场模拟面试？',
    a: '登录后选择岗位方向和难度即可开始，建议先完成一场基线面试，再根据评估报告做针对性迭代。'
  }
]

const closingHighlights = [
  ' AI 面试助手',
  '支持文本/语音/视频三种模式',
  '覆盖主流技术面试场景',
  '实时反馈 + 报告复盘闭环'
]

const activeSlide = ref(0)
let timer = null

const selectSlide = (index) => {
  activeSlide.value = index
}

const slideState = (index) => {
  const total = slides.length
  const prev = (activeSlide.value - 1 + total) % total
  const next = (activeSlide.value + 1) % total

  if (index === activeSlide.value) return 'is-active'
  if (index === prev) return 'is-prev'
  if (index === next) return 'is-next'
  return 'is-hidden'
}

const goLogin = () => {
  router.push('/login')
}

const downloadSoftware = () => {
  if (typeof window === 'undefined') return
  if (!downloadUrl) {
    console.warn('未配置下载地址')
    return
  }

  const link = document.createElement('a')
  link.href = downloadUrl
  link.download = downloadFileName
  link.rel = 'noopener'
  document.body.appendChild(link)
  link.click()
  link.remove()
}

const scrollToBlock = (id) => {
  if (typeof window === 'undefined') return
  const target = document.getElementById(id)
  if (!target) return
  target.scrollIntoView({ behavior: 'smooth', block: 'start' })
}

onMounted(() => {
  timer = setInterval(() => {
    activeSlide.value = (activeSlide.value + 1) % slides.length
  }, 4200)
})

onUnmounted(() => {
  if (timer) {
    clearInterval(timer)
    timer = null
  }
})
</script>

<style scoped>
.official-redesign {
  --ink: #0f223b;
  --ink-soft: #35557a;
  --brand: #45b9ff;
  --brand-deep: #2d93ff;
  --line: rgba(15, 34, 59, 0.12);

  width: 100%;
  min-height: 100vh;
  position: relative;
  overflow-x: clip;
  color: var(--ink);
  background: linear-gradient(140deg, #edf8ff, #dff2ff);
  font-family: 'Outfit', 'Noto Sans SC', 'Microsoft YaHei', sans-serif;
}

section[id] {
  scroll-margin-top: 96px;
}

.site-nav {
  position: sticky;
  top: 0;
  z-index: 30;
  height: 78px;
  padding: 0 48px;
  display: grid;
  grid-template-columns: auto 1fr auto;
  align-items: center;
  gap: 22px;
  background: rgba(237, 248, 255, 0.84);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(15, 34, 59, 0.08);
  box-shadow: 0 8px 18px rgba(23, 79, 131, 0.08);
}

.brand {
  border: none;
  background: transparent;
  display: inline-flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  padding: 0;
}

.brand img {
  width: 38px;
  height: 38px;
  border-radius: 9px;
}

.brand span {
  font-size: 33px;
  font-weight: 700;
  letter-spacing: 0.02em;
  white-space: nowrap;
  line-height: 1;
}

.nav-links {
  justify-self: center;
  display: inline-flex;
  align-items: center;
  gap: 10px;
  min-width: 0;
}

.nav-links button {
  border: none;
  background: transparent;
  color: rgba(15, 34, 59, 0.76);
  padding: 8px 10px;
  border-radius: 10px;
  white-space: nowrap;
  flex: 0 0 auto;
  cursor: pointer;
  font-weight: 500;
  transition: background 0.2s ease;
}

.nav-links button:hover {
  background: rgba(15, 34, 59, 0.08);
}

.nav-actions {
  display: flex;
  gap: 10px;
}

.btn {
  border: 1px solid transparent;
  border-radius: 999px;
  padding: 0 18px;
  height: 40px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.25s ease, box-shadow 0.25s ease;
}

.btn:focus-visible,
.nav-links button:focus-visible,
.screen-dots button:focus-visible,
.brand:focus-visible,
.final-cta-button:focus-visible {
  outline: 2px solid rgba(35, 134, 219, 0.55);
  outline-offset: 2px;
}

.btn:hover {
  transform: translateY(-2px);
}

.btn.solid {
  color: #ffffff;
  background: linear-gradient(135deg, var(--brand), var(--brand-deep));
  box-shadow: 0 10px 20px rgba(69, 185, 255, 0.3);
}

.btn.ghost {
  color: var(--ink);
  background: rgba(255, 255, 255, 0.6);
  border-color: rgba(15, 34, 59, 0.16);
}

.nav-download {
  color: #1f5f99;
  background: rgba(255, 255, 255, 0.82);
  border-color: rgba(39, 122, 197, 0.28);
}

.hero-block {
  padding: 36px 24px 62px;
  position: relative;
  background:
    radial-gradient(circle at 84% 22%, rgba(135, 203, 255, 0.28), rgba(135, 203, 255, 0) 35%),
    linear-gradient(140deg, #eef9ff, #e5f5ff);
  border-bottom: 1px solid rgba(43, 120, 196, 0.14);
  isolation: isolate;
}

.hero-block::before,
.hero-block::after {
  content: '';
  position: absolute;
  border-radius: 50%;
  pointer-events: none;
  z-index: -1;
}

.hero-block::before {
  width: 420px;
  height: 420px;
  right: -140px;
  top: -120px;
  background: radial-gradient(circle, rgba(111, 194, 255, 0.24), rgba(111, 194, 255, 0));
  animation: floatDrift 13s ease-in-out infinite;
}

.hero-block::after {
  width: 320px;
  height: 320px;
  left: -80px;
  bottom: -180px;
  background: radial-gradient(circle, rgba(124, 204, 255, 0.2), rgba(124, 204, 255, 0));
  animation: floatDrift 16s ease-in-out infinite reverse;
}

.hero-inner {
  max-width: 1220px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 0.98fr 1.02fr;
  gap: 30px;
  min-height: calc(100vh - 78px);
  align-items: start;
}

.hero-copy {
  padding-top: 28px;
  animation: heroRise 0.7s ease both;
}

.eyebrow {
  margin: 0;
  font-size: 12px;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: rgba(15, 34, 59, 0.56);
}

.hero-copy h1 {
  margin: 12px 0 14px;
  font-size: clamp(42px, 5.2vw, 78px);
  line-height: 1.02;
}

.hero-copy h1 span {
  color: #1780e8;
}

.hero-line-two {
  display: block;
}

.hero-line-two em {
  font-style: normal;
  color: #1578da;
}

.hero-copy p {
  margin: 0;
  max-width: 58ch;
  color: var(--ink-soft);
  line-height: 1.72;
  font-size: 16px;
}

.hero-actions {
  margin-top: 34px;
  display: flex;
  gap: 18px;
  align-items: center;
}

.hero-actions .btn {
  min-width: 172px;
  height: 56px;
  padding: 0 28px;
  font-size: 18px;
  font-weight: 700;
  border-radius: 999px;
}

.hero-actions .btn.solid {
  color: #123a61;
  background: linear-gradient(135deg, #a9e2ff, #66c4ff);
  box-shadow: 0 12px 26px rgba(85, 176, 235, 0.34);
}

.hero-actions .btn.ghost {
  color: #34465d;
  background: rgba(255, 255, 255, 0.78);
  border: 1px solid rgba(70, 100, 136, 0.2);
}

.hero-metrics {
  margin-top: 30px;
  display: flex;
  gap: 26px;
}

.hero-metrics div {
  display: grid;
  gap: 4px;
}

.hero-metrics strong {
  font-size: 30px;
  line-height: 1;
}

.hero-metrics span {
  color: rgba(15, 34, 59, 0.62);
  font-size: 14px;
}

.hero-preview {
  margin-top: 10px;
  display: grid;
  grid-template-rows: auto auto;
  gap: 16px;
  animation: heroRise 0.8s ease 0.08s both;
}

.screen-stage {
  min-height: 620px;
  border-radius: 0;
  position: relative;
  background: transparent;
  border: none;
  overflow: visible;
  box-shadow: none;
}

.screen-stage::before {
  content: none;
}

.screen-stage::after {
  content: none;
}

.screen-card {
  position: absolute;
  left: 50%;
  top: 50%;
  width: min(620px, 92%);
  border-radius: 20px;
  overflow: hidden;
  background: #ffffff;
  box-shadow: 0 20px 38px rgba(13, 23, 37, 0.2);
  transform-origin: center;
  transition: transform 0.75s ease, opacity 0.65s ease;
}

.screen-card img {
  width: 100%;
  display: block;
}

.screen-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 14px;
  background: linear-gradient(120deg, rgba(249, 254, 255, 0.95), rgba(225, 243, 255, 0.9));
}

.screen-meta p {
  margin: 0;
  font-size: 12px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: rgba(15, 34, 59, 0.56);
}

.screen-meta h3 {
  margin: 0;
  font-size: 15px;
}

.screen-card.is-active {
  z-index: 4;
  opacity: 1;
  transform: translate(-50%, -50%) scale(1) rotate(0deg);
}

.screen-card.is-prev {
  z-index: 2;
  opacity: 0.62;
  transform: translate(-56%, -47%) scale(0.91) rotate(-4deg);
}

.screen-card.is-next {
  z-index: 3;
  opacity: 0.75;
  transform: translate(-43%, -52%) scale(0.93) rotate(4deg);
}

.screen-card.is-hidden {
  z-index: 1;
  opacity: 0;
  transform: translate(-50%, -50%) scale(0.82);
}

.screen-dots {
  display: flex;
  gap: 8px;
  justify-content: center;
  margin-top: 6px;
}

.screen-dots button {
  width: 28px;
  height: 6px;
  border-radius: 999px;
  border: none;
  background: rgba(15, 34, 59, 0.2);
  cursor: pointer;
  transition: width 0.25s ease, background 0.25s ease;
}

.screen-dots button.active {
  width: 44px;
  background: linear-gradient(120deg, #54beff, #2e97ff);
}

.screen-hint {
  margin: 0;
  text-align: center;
  color: rgba(15, 34, 59, 0.58);
  font-size: 13px;
}

.segment {
  padding: 90px 48px;
  min-height: 620px;
  display: flex;
  align-items: center;
}

.segment-inner {
  max-width: 1220px;
  margin: 0 auto;
  width: 100%;
}

.segment-kicker {
  margin: 0;
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.12em;
}

.segment h2 {
  margin: 12px 0 14px;
  font-size: clamp(30px, 3.5vw, 52px);
  line-height: 1.08;
}

.segment p {
  margin: 0;
  font-size: 16px;
  line-height: 1.8;
}

.segment-a {
  background:
    radial-gradient(circle at 87% 12%, rgba(123, 203, 255, 0.2), rgba(123, 203, 255, 0) 34%),
    linear-gradient(125deg, #fbfdff, #ecf6ff);
  border-top: 1px solid rgba(43, 120, 196, 0.12);
}

.split {
  display: grid;
  grid-template-columns: 1.1fr 0.9fr;
  gap: 44px;
  align-items: center;
}

.capability-copy h2 {
  max-width: 12ch;
}

.capability-copy > p {
  max-width: 56ch;
}

.check-list {
  margin: 0;
  padding: 12px 0 12px 20px;
  list-style: none;
  display: grid;
  gap: 12px;
  position: relative;
}

.check-list::before {
  content: '';
  position: absolute;
  left: 7px;
  top: 14px;
  bottom: 14px;
  width: 1px;
  background: linear-gradient(180deg, rgba(41, 131, 206, 0.34), rgba(41, 131, 206, 0.12));
}

.check-list li {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 14px;
  align-items: start;
  padding: 8px 0;
  color: rgba(15, 34, 59, 0.82);
  background: transparent;
  transition: transform 0.2s ease, color 0.2s ease;
}

.check-list li:hover {
  transform: translateX(3px);
  color: rgba(15, 34, 59, 0.92);
}

.check-index {
  width: 28px;
  height: 28px;
  border-radius: 999px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.04em;
  color: #1e7fd2;
  background: linear-gradient(150deg, rgba(173, 222, 255, 0.8), rgba(133, 203, 255, 0.48));
  box-shadow: 0 6px 12px rgba(65, 149, 216, 0.22);
}

.check-list li p {
  margin: 0;
  line-height: 1.65;
}

.segment-b {
  color: #f9fbff;
  background:
    radial-gradient(circle at 90% 12%, rgba(75, 183, 255, 0.25), rgba(75, 183, 255, 0) 30%),
    linear-gradient(140deg, #0f2740, #132f50);
}

.segment-b,
.segment-c,
.segment-h,
.segment-i,
.segment-d,
.segment-g {
  border-top: 1px solid rgba(15, 34, 59, 0.08);
}

.role-tags {
  margin-top: 24px;
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.role-tags span {
  display: inline-flex;
  padding: 7px 12px;
  border-radius: 999px;
  color: #eaf6ff;
  border: 1px solid rgba(255, 255, 255, 0.24);
  background: rgba(255, 255, 255, 0.08);
  font-size: 13px;
}

.segment-b h2,
.segment-b p {
  color: rgba(249, 251, 255, 0.94);
}

.scene-grid {
  margin-top: 28px;
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px 26px;
}

.scene-grid article {
  padding: 12px 0 14px;
  border-radius: 0;
  background: transparent;
  border: none;
  border-bottom: 1px solid rgba(255, 255, 255, 0.16);
  transition: border-color 0.25s ease, transform 0.25s ease;
}

.scene-grid article:hover {
  border-bottom-color: rgba(136, 215, 255, 0.68);
  transform: translateY(-2px);
}

.scene-grid h3 {
  margin: 0 0 10px;
  font-size: 24px;
}

.scene-grid p {
  margin: 0;
  color: rgba(242, 246, 255, 0.78);
}

.segment-c {
  background:
    radial-gradient(circle at 12% 12%, rgba(147, 220, 255, 0.16), rgba(147, 220, 255, 0) 35%),
    linear-gradient(140deg, #edf7ff, #e2f2ff);
  min-height: auto;
  padding-top: 76px;
  padding-bottom: 82px;
}

.segment-h {
  background:
    radial-gradient(circle at 90% 10%, rgba(113, 191, 255, 0.2), rgba(113, 191, 255, 0) 35%),
    radial-gradient(circle at 8% 88%, rgba(102, 182, 248, 0.14), rgba(102, 182, 248, 0) 34%),
    linear-gradient(140deg, #f6fbff, #e8f4ff);
}

.segment-h .segment-inner > p {
  max-width: 74ch;
}

.assessment-grid {
  margin-top: 30px;
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16px;
}

.assessment-card {
  border-radius: 14px;
  padding: 16px 18px;
  background: rgba(255, 255, 255, 0.58);
  border: 1px solid rgba(56, 145, 214, 0.2);
  display: flex;
  flex-direction: column;
  transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
}

.assessment-card:hover {
  transform: translateY(-3px);
  border-color: rgba(56, 145, 214, 0.34);
  box-shadow: 0 12px 24px rgba(43, 127, 195, 0.12);
}

.assessment-main {
  display: flex;
  gap: 16px;
  align-items: flex-start;
}

.assessment-copy {
  min-width: 0;
  flex: 1;
}

.assessment-card h3 {
  margin: 0 0 7px;
  font-size: 22px;
}

.assessment-card p {
  margin: 0;
  color: rgba(15, 34, 59, 0.76);
}

.assessment-inline-chart {
  margin: 0;
  border-radius: 14px;
  overflow: hidden;
  background: linear-gradient(160deg, rgba(245, 252, 255, 0.92), rgba(224, 242, 255, 0.88));
  border: 1px solid rgba(64, 150, 221, 0.2);
  padding: 8px;
}

.assessment-inline-chart img {
  display: block;
  width: 100%;
  border-radius: 9px;
}

.assessment-card.layout-right .chart-right {
  width: min(46%, 255px);
  flex-shrink: 0;
}

.assessment-card.layout-bottom .chart-bottom {
  margin-top: 12px;
}

.assessment-tags {
  margin-top: 10px;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.assessment-tags span {
  padding: 4px 10px;
  border-radius: 999px;
  font-size: 12px;
  color: #2b7ec9;
  border: 1px solid rgba(49, 137, 211, 0.2);
  background: rgba(97, 177, 240, 0.12);
}

.segment-i {
  background:
    radial-gradient(circle at 15% 10%, rgba(132, 206, 255, 0.18), rgba(132, 206, 255, 0) 34%),
    linear-gradient(142deg, #e8f4ff, #ddedff);
}

.resume-ai-layout {
  display: grid;
  grid-template-columns: 1.05fr 0.95fr;
  gap: 44px;
  align-items: start;
}

.resume-copy h2 {
  max-width: 14ch;
}

.resume-copy > p {
  max-width: 54ch;
}

.resume-bullets {
  margin: 26px 0 0;
  padding: 0;
  list-style: none;
  display: grid;
  gap: 12px;
}

.resume-bullets li {
  position: relative;
  padding-left: 28px;
  color: rgba(15, 34, 59, 0.8);
  line-height: 1.65;
}

.resume-bullets li::before {
  content: '✓';
  position: absolute;
  left: 0;
  top: 2px;
  width: 18px;
  height: 18px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 999px;
  color: #177cda;
  font-size: 12px;
  font-weight: 700;
  background: rgba(103, 189, 255, 0.2);
}

.resume-panels {
  position: relative;
  display: grid;
  gap: 14px;
  padding-left: 10px;
}

.resume-panels::before {
  content: '';
  position: absolute;
  left: 0;
  top: 8px;
  bottom: 8px;
  width: 2px;
  background: linear-gradient(180deg, rgba(42, 138, 220, 0.5), rgba(42, 138, 220, 0.16));
}

.resume-panel {
  display: grid;
  grid-template-columns: 1fr;
  gap: 10px;
  border-radius: 16px;
  padding: 16px 18px;
  background: linear-gradient(145deg, rgba(255, 255, 255, 0.74), rgba(241, 250, 255, 0.86));
  border: 1px solid rgba(50, 140, 215, 0.16);
  box-shadow: 0 10px 20px rgba(53, 128, 199, 0.08);
  transition: transform 0.25s ease, box-shadow 0.25s ease;
}

.resume-panel:hover {
  transform: translateY(-3px);
  box-shadow: 0 14px 24px rgba(53, 128, 199, 0.14);
}

.resume-panel h3 {
  margin: 0 0 6px;
  font-size: 30px;
}

.resume-panel p {
  margin: 0;
  color: rgba(15, 34, 59, 0.76);
}

.timeline {
  margin-top: 34px;
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 54px 98px;
  position: relative;
  padding: 18px 20px 22px;
}

.timeline::before {
  content: '';
  position: absolute;
  left: 50%;
  top: 50%;
  width: min(390px, 44%);
  aspect-ratio: 1 / 1;
  transform: translate(-50%, -50%);
  border: 2px dashed rgba(41, 133, 212, 0.24);
  border-radius: 50%;
  pointer-events: none;
}

.timeline::after {
  content: '';
  position: absolute;
  left: 50%;
  top: 50%;
  width: 250px;
  height: 250px;
  transform: translate(-50%, -50%);
  border-radius: 50%;
  background: radial-gradient(circle, rgba(129, 200, 255, 0.14), rgba(129, 200, 255, 0));
  pointer-events: none;
}

.flow-step {
  position: relative;
  z-index: 2;
  padding: 18px 20px 20px;
  min-height: 156px;
  border-radius: 16px;
  background: linear-gradient(148deg, rgba(255, 255, 255, 0.86), rgba(244, 251, 255, 0.94));
  border: 1px solid rgba(54, 142, 217, 0.2);
  box-shadow: 0 10px 24px rgba(56, 131, 205, 0.12);
  transition: transform 0.25s ease, box-shadow 0.25s ease;
}

.flow-step:hover {
  transform: translateY(-3px);
  box-shadow: 0 14px 28px rgba(56, 131, 205, 0.18);
}

.step-1 {
  grid-area: 1 / 1;
}

.step-2 {
  grid-area: 1 / 2;
}

.step-3 {
  grid-area: 2 / 2;
}

.step-4 {
  grid-area: 2 / 1;
}

.orbit-arrows {
  position: absolute;
  left: 50%;
  top: 50%;
  width: min(390px, 44%);
  aspect-ratio: 1 / 1;
  transform: translate(-50%, -50%);
  pointer-events: none;
  z-index: 1;
}

.orbit-arrow {
  position: absolute;
  width: 30px;
  height: 30px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid rgba(56, 140, 214, 0.34);
  color: #1e80de;
  font-size: 16px;
  font-weight: 700;
  box-shadow: 0 6px 12px rgba(28, 120, 202, 0.2);
}

.orbit-arrow.top {
  left: 50%;
  top: -15px;
  transform: translateX(-50%);
}

.orbit-arrow.right {
  right: -15px;
  top: 50%;
  transform: translateY(-50%);
}

.orbit-arrow.bottom {
  left: 50%;
  bottom: -15px;
  transform: translateX(-50%);
}

.orbit-arrow.left {
  left: -15px;
  top: 50%;
  transform: translateY(-50%);
}

.flow-index {
  display: inline-flex;
  width: 34px;
  height: 34px;
  align-items: center;
  justify-content: center;
  border-radius: 999px;
  font-weight: 700;
  color: #177fdf;
  background: rgba(72, 170, 246, 0.16);
  margin-bottom: 10px;
}

.flow-step h3 {
  margin: 8px 0;
  font-size: 20px;
}

.flow-step p {
  margin: 0;
  color: rgba(15, 34, 59, 0.72);
}

.flow-core {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  width: 132px;
  height: 132px;
  border-radius: 50%;
  background: radial-gradient(circle at 30% 30%, rgba(255, 255, 255, 0.95), rgba(214, 237, 255, 0.95));
  border: 1px solid rgba(44, 126, 199, 0.26);
  box-shadow: 0 10px 24px rgba(45, 126, 198, 0.18);
  display: grid;
  place-content: center;
  gap: 4px;
  text-align: center;
  z-index: 1;
}

.flow-core strong {
  font-size: 16px;
  color: #1d5f99;
}

.flow-core span {
  font-size: 12px;
  color: rgba(20, 76, 128, 0.74);
}

.segment-d {
  background:
    radial-gradient(circle at 84% 14%, rgba(97, 176, 238, 0.26), rgba(97, 176, 238, 0) 36%),
    linear-gradient(146deg, #d8ebff, #cfe5fb 46%, #d9ecff);
}

.architecture-grid {
  margin-top: 30px;
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 0;
  border-top: 1px solid rgba(43, 127, 203, 0.16);
  border-bottom: 1px solid rgba(43, 127, 203, 0.16);
}

.architecture-card {
  border-radius: 0;
  padding: 22px 18px;
  background: transparent;
  border: none;
  border-right: 1px solid rgba(43, 127, 203, 0.16);
  transition: background 0.25s ease;
}

.architecture-card:hover {
  background: rgba(255, 255, 255, 0.34);
}

.architecture-card:last-child {
  border-right: none;
}

.architecture-card h3 {
  margin: 0 0 12px;
  font-size: 24px;
}

.architecture-card ul {
  margin: 0;
  padding-left: 18px;
  display: grid;
  gap: 8px;
}

.architecture-card li {
  color: rgba(15, 34, 59, 0.78);
}

.segment-g {
  position: relative;
  overflow: hidden;
  background:
    radial-gradient(circle at 12% 8%, rgba(173, 225, 255, 0.3), rgba(173, 225, 255, 0) 34%),
    linear-gradient(138deg, #f8fcff, #eef6ff);
  border-top: 2px solid rgba(45, 123, 198, 0.2);
}

.segment-g::before {
  content: '';
  position: absolute;
  left: 0;
  right: 0;
  top: 0;
  height: 34px;
  background: linear-gradient(180deg, rgba(49, 127, 201, 0.16), rgba(49, 127, 201, 0));
  pointer-events: none;
}

.faq-wrap {
  margin-top: 30px;
  max-width: 980px;
  display: grid;
  gap: 14px;
}

.faq-item {
  border: 1px solid rgba(26, 109, 196, 0.18);
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.8);
  overflow: hidden;
  transition: border-color 0.25s ease, box-shadow 0.25s ease, background 0.25s ease;
}

.faq-item:hover {
  border-color: rgba(31, 117, 199, 0.34);
  box-shadow: 0 10px 20px rgba(38, 111, 186, 0.1);
}

.faq-item summary {
  list-style: none;
  cursor: pointer;
  padding: 22px 24px;
  font-size: 20px;
  font-weight: 600;
  color: var(--ink);
  position: relative;
}

.faq-item summary::-webkit-details-marker {
  display: none;
}

.faq-item summary::after {
  content: '+';
  position: absolute;
  right: 24px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 22px;
  color: rgba(26, 109, 196, 0.66);
  transition: transform 0.25s ease;
}

.faq-item[open] summary::after {
  transform: translateY(-50%) rotate(45deg);
}

.faq-item[open] {
  background: rgba(255, 255, 255, 0.9);
}

.faq-item p {
  margin: 0;
  padding: 0 24px 20px;
  color: rgba(15, 34, 59, 0.74);
}

.final-cta {
  position: relative;
  padding: 96px 24px 88px;
  border-top: 1px solid rgba(24, 93, 163, 0.16);
  background:
    radial-gradient(circle at 20% -10%, rgba(82, 176, 244, 0.24), rgba(82, 176, 244, 0) 40%),
    radial-gradient(circle at 88% 112%, rgba(146, 220, 255, 0.28), rgba(146, 220, 255, 0) 40%),
    linear-gradient(145deg, #dff0ff, #cae5ff 44%, #e8f4ff);
}

.final-cta-inner {
  max-width: 1220px;
  margin: 0 auto;
  text-align: center;
}

.final-cta-kicker {
  margin: 0;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: rgba(18, 58, 97, 0.56);
  font-size: 12px;
}

.final-cta h2 {
  margin: 14px auto 16px;
  max-width: 880px;
  font-size: clamp(38px, 4.8vw, 72px);
  line-height: 1.12;
}

.final-cta-desc {
  margin: 0 auto;
  max-width: 760px;
  font-size: 18px;
  line-height: 1.75;
  color: rgba(15, 34, 59, 0.8);
}

.final-cta-button {
  margin-top: 34px;
  height: 76px;
  padding: 0 42px;
  border: none;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.9);
  color: #1e6cb1;
  font-size: 34px;
  font-weight: 700;
  letter-spacing: 0.01em;
  cursor: pointer;
  box-shadow: 0 16px 30px rgba(41, 118, 194, 0.24);
  transition: transform 0.22s ease, box-shadow 0.22s ease;
}

.final-cta-button span {
  margin-left: 10px;
}

.final-cta-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 20px 34px rgba(41, 118, 194, 0.3);
}

@keyframes heroRise {
  from {
    opacity: 0;
    transform: translateY(14px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes floatDrift {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-12px);
  }
}

@media (prefers-reduced-motion: reduce) {
  .hero-copy,
  .hero-preview,
  .hero-block::before,
  .hero-block::after {
    animation: none;
  }
}

.final-cta-points {
  margin-top: 56px;
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 16px 24px;
}

.final-cta-points span {
  font-size: 30px;
  color: rgba(20, 58, 97, 0.86);
  line-height: 1.4;
}

.final-cta-points span::before {
  content: '✓';
  margin-right: 8px;
  color: #2786d8;
}

@media (max-width: 1180px) {
  .site-nav {
    grid-template-columns: auto minmax(0, 1fr) auto;
    gap: 12px;
  }

  .site-nav,
  .segment {
    padding-left: 24px;
    padding-right: 24px;
  }

  .brand span {
    font-size: 24px;
  }

  .nav-links {
    justify-self: stretch;
    overflow-x: auto;
    padding-bottom: 2px;
    scrollbar-width: none;
  }

  .nav-links::-webkit-scrollbar {
    display: none;
  }

  .nav-links button {
    padding: 7px 8px;
    font-size: 15px;
  }

  .nav-actions {
    gap: 8px;
  }

  .nav-actions .btn {
    height: 36px;
    padding: 0 12px;
    font-size: 13px;
  }

  .hero-inner,
  .split {
    grid-template-columns: 1fr;
    min-height: auto;
  }

  .hero-copy {
    padding-top: 20px;
  }

  .hero-preview {
    margin-top: 6px;
  }

  .hero-block::before,
  .hero-block::after {
    opacity: 0.7;
  }

  .segment {
    min-height: auto;
    padding-top: 70px;
    padding-bottom: 70px;
  }

  .timeline {
    gap: 44px 72px;
    padding-left: 14px;
    padding-right: 14px;
  }

  .timeline::before {
    width: min(330px, 46%);
  }

  .timeline::after {
    width: 210px;
    height: 210px;
  }

  .orbit-arrows {
    width: min(330px, 46%);
  }

  .orbit-arrow {
    width: 26px;
    height: 26px;
    font-size: 14px;
  }

  .orbit-arrow.top {
    top: -13px;
  }

  .orbit-arrow.right {
    right: -13px;
  }

  .orbit-arrow.bottom {
    bottom: -13px;
  }

  .orbit-arrow.left {
    left: -13px;
  }

  .flow-core {
    width: 114px;
    height: 114px;
  }

}

@media (max-width: 880px) {
  .site-nav {
    height: auto;
    padding-top: 14px;
    padding-bottom: 14px;
    grid-template-columns: minmax(0, 1fr) auto;
    grid-template-areas:
      'brand actions'
      'links links';
    row-gap: 10px;
  }

  .brand {
    grid-area: brand;
    justify-self: start;
  }

  .brand span {
    font-size: 28px;
  }

  .nav-links {
    grid-area: links;
    justify-self: stretch;
    display: flex;
    overflow-x: auto;
    width: 100%;
    padding: 2px 0 8px;
    gap: 8px;
    scrollbar-width: none;
    -webkit-overflow-scrolling: touch;
  }

  .nav-links::-webkit-scrollbar {
    display: none;
  }

  .nav-links button {
    padding: 7px 14px;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.62);
    border: 1px solid rgba(44, 120, 192, 0.16);
    font-size: 14px;
  }

  .nav-actions {
    grid-area: actions;
    justify-self: end;
    width: auto;
  }

  .hero-copy h1 {
    font-size: clamp(36px, 11vw, 56px);
  }

  .hero-metrics {
    flex-wrap: wrap;
    gap: 14px;
  }

  .scene-grid,
  .timeline,
  .architecture-grid,
  .assessment-grid,
  .resume-ai-layout {
    grid-template-columns: 1fr;
  }

  .resume-ai-layout {
    gap: 24px;
  }

  .capability-copy h2,
  .capability-copy > p {
    max-width: none;
  }

  .resume-copy h2 {
    max-width: none;
  }

  .resume-panels {
    padding-left: 0;
  }

  .resume-panels::before {
    display: none;
  }

  .timeline {
    gap: 12px;
    padding: 0;
  }

  .timeline::before,
  .flow-core,
  .orbit-arrows {
    display: none;
  }

  .step-1,
  .step-2,
  .step-3,
  .step-4 {
    grid-area: auto;
  }

  .architecture-grid {
    gap: 8px;
    border-top: none;
    border-bottom: none;
  }

  .architecture-card {
    border-right: none;
    border-bottom: 1px solid rgba(43, 127, 203, 0.16);
    padding-left: 0;
    padding-right: 0;
  }

  .architecture-card:last-child {
    border-bottom: none;
  }

  .final-cta {
    padding-top: 74px;
    padding-bottom: 72px;
  }

  .final-cta h2 {
    font-size: clamp(30px, 8.8vw, 52px);
  }

  .final-cta-desc {
    font-size: 16px;
  }

  .final-cta-button {
    height: 64px;
    padding: 0 30px;
    font-size: 28px;
  }

  .final-cta-points span {
    font-size: 24px;
  }

  .screen-stage {
    min-height: 400px;
    border-radius: 0;
  }

  .assessment-card.layout-right .assessment-main {
    flex-direction: column;
  }

  .assessment-card.layout-right .chart-right {
    width: 100%;
  }

}

@media (max-width: 560px) {
  .hero-actions {
    width: 100%;
  }

  .hero-actions .btn {
    flex: 1;
  }

  .site-nav {
    padding-top: 12px;
    padding-bottom: 10px;
    row-gap: 8px;
  }

  .brand {
    gap: 8px;
  }

  .brand img {
    width: 30px;
    height: 30px;
    border-radius: 7px;
  }

  .brand span {
    font-size: 17px;
  }

  .nav-links {
    padding-bottom: 6px;
  }

  .nav-links button {
    font-size: 13px;
    padding: 6px 12px;
  }

  .nav-actions {
    width: auto;
    gap: 8px;
  }

  .nav-actions .btn {
    flex: 0 0 auto;
    height: 34px;
    padding: 0 14px;
    font-size: 13px;
  }

  .hero-actions .btn {
    height: 52px;
    min-width: 0;
    padding: 0 18px;
    font-size: 18px;
  }

  .hero-actions {
    display: grid;
    grid-template-columns: 1fr;
  }

  .segment,
  .hero-block {
    padding-top: 42px;
    padding-bottom: 42px;
    min-height: auto;
  }

  .hero-block::before,
  .hero-block::after {
    display: none;
  }

  .faq-item summary {
    font-size: 16px;
    padding: 16px 18px;
  }

  .faq-item summary::after {
    right: 18px;
  }

  .faq-item p {
    padding: 0 18px 16px;
  }

  .final-cta {
    padding-top: 54px;
    padding-bottom: 52px;
  }

  .final-cta h2 {
    margin-top: 10px;
    margin-bottom: 12px;
    font-size: clamp(28px, 9.6vw, 42px);
  }

  .final-cta-desc {
    font-size: 15px;
    line-height: 1.7;
  }

  .final-cta-button {
    width: 100%;
    max-width: 360px;
    height: 58px;
    padding: 0 20px;
    font-size: 24px;
  }

  .final-cta-points {
    margin-top: 34px;
    gap: 10px;
  }

  .final-cta-points span {
    font-size: 18px;
  }

  .resume-panel {
    grid-template-columns: 1fr;
    gap: 10px;
    padding: 14px;
  }

  .check-list {
    padding-left: 14px;
  }

  .check-list::before {
    left: 5px;
  }

  .assessment-card {
    padding: 14px;
  }

  .panel-index {
    width: 30px;
    height: 30px;
    font-size: 13px;
  }

}
</style>
