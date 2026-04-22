import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useUserStore = defineStore('user', () => {
  const normalizeAvatar = (avatar) => {
    if (typeof avatar !== 'string') return ''
    const value = avatar.trim()
    if (!value) return ''

    const lowered = value.toLowerCase()
    if (lowered === 'null' || lowered === 'undefined' || lowered === 'none') {
      return ''
    }

    return value
  }

  // 模拟用户信息
  const userInfo = ref({
    email: 'student@university.edu.cn', // 默认展示
    username: '', // 初始为空
    avatar: '',   // 初始为空
    bio: ''       // [新增] 个人简介
  })

  // 更新资料
  function updateProfile(data) {
    const nextData = { ...data }
    if (Object.prototype.hasOwnProperty.call(nextData, 'avatar')) {
      nextData.avatar = normalizeAvatar(nextData.avatar)
    }

    Object.assign(userInfo.value, nextData)
  }

  return { userInfo, updateProfile }
})