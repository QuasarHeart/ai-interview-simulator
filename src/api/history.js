// src/api/history.js
import service from '../utils/request'

// 获取全部面试记录
export const getInterviewHistory = () => {
	return service({
		url: '/api/v1/interviews/all',
		method: 'get'
	})
}

// 获取某个面试的历史对话
export const getInterviewDialogueHistory = (interviewId) => {
	return service({
		url: `/api/v1/interviews/${interviewId}/history`,
		method: 'get'
	})
}
