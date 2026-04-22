// src/api/assessment.js
import request from '../utils/request'

/**
 * 获取成长曲线数据（综合能力评估）
 * @param {string} jobRole - 岗位角色，格式为下划线分隔，e.g. 'web_frontend', 'java_backend', 'algorithm_engineer'，或空字符串表示全部
 * @returns {Promise} 返回包含以下数据:
 *   - overallRating: 综合评分
 *   - interviewCount: 面试次数
 *   - bestScore: 最高分
 *   - practiceTime: 练习时长
 *   - dimensionScores: {cognition, expression, professional} 三大维度分值
 *   - dimensionDetails: 10个细维度的具体分值
 *   - growthPoints: 数值数组，表示历次面试的得分趋势 e.g. [96.5, 98.7, 99.5]
 *   - strengths: 优势数组
 *   - weaknesses: 弱点数组
 */
export const getGrowthCurve = (jobRole) => {
  return request({
    url: '/api/v1/interviews/growth-curve',
    method: 'get',
    params: { jobRole }
  })
}
