import { createRouter, createWebHashHistory, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import MainLayout from '../layout/MainLayout.vue'

const isElectronRuntime = () => {
  if (typeof window === 'undefined') return false
  const ua = window.navigator.userAgent.toLowerCase()
  return ua.includes(' electron/') || Boolean(window.process?.versions?.electron)
}

const createAppHistory = () => {
  return isElectronRuntime() ? createWebHashHistory(import.meta.env.BASE_URL) : createWebHistory(import.meta.env.BASE_URL)
}

const router = createRouter({
  history: createAppHistory(),
  routes: [
    {
      path: '/official',
      name: 'official',
      component: () => import('../views/official/OfficialSiteView.vue')
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/',
      component: MainLayout,
      meta: { requiresAuth: true },
      redirect: () => (isElectronRuntime() ? '/dashboard' : '/official'),
      children: [
        {
          path: 'dashboard',
          name: 'dashboard',
          component: () => import('../views/dashboard/DashboardView.vue')
        },
        {
          path: 'interview',
          name: 'interview',
          component: () => import('../views/interview/InterviewPortalView.vue')
        },
        {
          path: 'history',
          name: 'history',
          component: () => import('../views/history/HistoryView.vue')
        },
        {
          path: 'history/:id', 
          name: 'interview-detail',
          component: () => import('../views/history/InterviewDetailView.vue')
        },
        {
          path: 'assessment',
          name: 'assessment',
          component: () => import('../views/assessment/AssessmentView.vue')
        },
        {
          path: 'resume',
          name: 'resume',
          component: () => import('../views/resume/ResumeView.vue')
        },
        {
          path: 'profile',
          name: 'profile',
          component: () => import('../views/profile/ProfileView.vue')
        }
      ]
    }
  ]
})

router.beforeEach((to, from) => {
  const token = localStorage.getItem('token')
  const inElectron = isElectronRuntime()
  const redirectedFromRoot = to.redirectedFrom?.path === '/'

  // 兼容根路径先重定向到 dashboard 的场景：浏览器仍应展示官网。
  if (!inElectron && redirectedFromRoot && to.path === '/dashboard') {
    return '/official'
  }

  // Electron 版本不展示官网。
  if (inElectron && to.path === '/official') {
    return token ? '/dashboard' : '/login'
  }

  if (to.meta.requiresAuth && !token) {
    return '/login'
  }

  if (to.path === '/login' && token) {
    return '/dashboard'
  }
})

export default router