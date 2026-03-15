"""
通用接入大模型的框架，适配面试过程中的不同流程
"""
import os
import yaml
import json_repair
from dataclasses import dataclass, field
from typing import Dict, Any
from jinja2 import Template
from openai import AsyncOpenAI
from jinja2 import Environment, StrictUndefined
from app.schemas.schemas import StartRequest, FollowupRequest, AnalysisRequest, ReportRequest

# ========================================================
# 1、基础配置 (算分权重配置)
# ========================================================
@dataclass
class Settings:
    # 一级维度权重
    professional_weight: float = 0.5
    cognition_weight: float = 0.3
    expression_weight: float = 0.2

    # 每个一级权重下二级维度的权重
    professional_subweights: Dict[str, float] = field(
        default_factory=lambda: {
            "technical_correctness": 0.20,
            "knowledge_match": 0.09,
            "job_match": 0.31,
            "engineering_practice": 0.40,
        }
    )

    cognition_subweights: Dict[str, float] = field(
        default_factory=lambda: {
            "logic_structure": 1/3,
            "problem_solving": 1/3,
            "system_thinking": 1/3,
        }
    )

    expression_subweights: Dict[str, float] = field( # 修正了命名拼写
        default_factory=lambda: {
            "clarity": 1/3,
            "confidence_stability": 1/3,
            "professional_maturity": 1/3,
        }
    )

settings = Settings()

# ========================================================
# 2、LLM 引擎类 (核心大脑)
# ========================================================
class LLMEngine:
    def __init__(self):
        # 初始化大模型客户端 (适配阿里云 DashScope)
        self.api_key = os.getenv("DASHSCOPE_API_KEY", "你的通义千问API_KEY")
        self.base_url = os.getenv("DASHSCOPE_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")
        self.model = os.getenv("JUDGE_MODEL", "qwen-plus") # 建议用 qwen-plus 或 qwen-max
        self.temperature = float(os.getenv("SCORING_TEMPERATURE", "0.2"))
        
        self.client = AsyncOpenAI(api_key=self.api_key, base_url=self.base_url)
        
        # 预加载所有 YAML Prompt 模板
        self.prompts = {
            "start": self._load_yaml("prompts/start/start.yaml"),
            "followup": self._load_yaml("prompts/followup/followup.yaml"),
            "analysis": self._load_yaml("prompts/analysis/analysis.yaml"),
            "report": self._load_yaml("prompts/report/report.yaml"),
        }

    def _load_yaml(self, filepath: str) -> dict:
        """加载 YAML 文件"""
        # 注意修改为你实际的路径，如果找不到可以写绝对路径
        with open(filepath, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

# 2) 在 _invoke_llm 里替换原来的拼接逻辑
async def _invoke_llm(self, prompt_config: dict, kwargs_dict: dict) -> dict:
    """通用的大模型调用与 JSON 解析通道"""

    # 使用严格模式：模板里有变量但 kwargs 没传，会直接报错，方便排查
    env = Environment(undefined=StrictUndefined)

    # 分别渲染 4 段 prompt（关键修复点）
    system_role = env.from_string(prompt_config["system_role"]).render(**kwargs_dict)
    rules = env.from_string(prompt_config["rules"]).render(**kwargs_dict)
    format_requirements = env.from_string(prompt_config["format_requirements"]).render(**kwargs_dict)
    user_prompt = env.from_string(prompt_config["input_context"]).render(**kwargs_dict)

    # 拼接 system prompt
    system_prompt = f"{system_role}\n\n{rules}\n\n{format_requirements}"

    # （可选）调试：检查是否还有未替换占位符
    # print("SYSTEM PREVIEW:", system_prompt[:500])
    # print("USER PREVIEW:", user_prompt[:500])
    # print("HAS_UNRESOLVED:", "{{" in system_prompt or "{{" in user_prompt)

    # 3. 发起异步请求
    response = await self.client.chat.completions.create(
        model=self.model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=self.temperature
    )

    raw_text = response.choices[0].message.content

    # 4. 暴力修复并解析 JSON
    parsed_json = json_repair.loads(raw_text)
    return parsed_json
    # ========================================================
    # 3、具体的业务路由方法
    # ========================================================

    async def generate_first_question(self, req: StartRequest) -> dict:
        """生成首轮问题"""
        # 提取 Pydantic 模型的数据转为字典，传给 Jinja2 渲染
        kwargs = {
            "job_position": req.job_position,
            "resume_content": req.resume_content,
            "interviewer_style": req.interview_config.interviewer_style,
            "company_context": req.interview_config.company_context,
            "difficulty": req.interview_config.difficulty
        }
        return await self._invoke_llm(self.prompts["start"], kwargs)

    async def generate_following_question(self, req: FollowupRequest) -> dict:
        """生成追问问题与调度控制"""
        kwargs = {
            "current_stage": req.flow_control.target_stage,
            "jd_summary": req.background.jd_summary,
            "resume_summary": req.background.resume_summary,
            "interviewer_style": req.interview_config.interviewer_style,
            "difficulty": req.interview_config.difficulty,
            "history_summary": req.history_data.history_summary,
            # 将历史记录列表转换为大模型容易读懂的字符串格式
            "recent_history": "\n".join([f"[{item.role}]: {item.content}" for item in req.history_data.recent_history])
        }
        return await self._invoke_llm(self.prompts["followup"], kwargs)

    async def analyze_answer(self, req: AnalysisRequest) -> dict:
        """对回答进行综合分析 (含硬编码算分逻辑)"""
        kwargs = {
            "current_stage": req.current_stage,
            "jd_summary": req.content_to_analyze.jd_summary,
            "resume_summary": req.content_to_analyze.resume_summary,
            "question": req.content_to_analyze.question,
            "user_answer": req.content_to_analyze.user_answer,
            "history_summary": req.content_to_analyze.history_summary,
            "difficulty": req.interview_config.difficulty
        }
        
        # 1. 让 AI 打出二级维度的明细分
        ai_result = await self._invoke_llm(self.prompts["analysis"], kwargs)
        
        # 2. 拦截并使用 Python 代码精准计算一级维度分与总分！
        try:
            details = ai_result["dimension_details"]
            
            # 计算专业分
            prof_score = sum(details["professional"][k]["score"] * settings.professional_subweights[k] for k in details["professional"])
            # 计算认知分
            cog_score = sum(details["cognition"][k]["score"] * settings.cognition_subweights[k] for k in details["cognition"])
            # 计算表达分
            exp_score = sum(details["expression"][k]["score"] * settings.expression_subweights[k] for k in details["expression"])
            
            # 写入一级维度
            ai_result["dimension_scores"] = {
                "professional": round(prof_score, 1),
                "cognition": round(cog_score, 1),
                "expression": round(exp_score, 1)
            }
            
            # 计算最终百分制总分 (假设 0-5 分制，乘以 20 变为 100 分制)
            total_5_point = (prof_score * settings.professional_weight +
                             cog_score * settings.cognition_weight +
                             exp_score * settings.expression_weight)
            
            ai_result["final_score"] = round(total_5_point * 20, 1)
            
        except Exception as e:
            print(f"[警告] 计算得分失败，依赖 AI 原生输出。错误: {e}")
            
        return ai_result

    async def generate_overall_report(self, req: ReportRequest) -> dict:
        """生成综合报告"""
        kwargs = {
            "job_position": req.interview_context.job_position,
            "jd_summary": req.interview_context.jd_summary,
            "total_rounds": req.interview_context.total_rounds,
            "interview_duration_seconds": req.interview_context.interview_duration_seconds,
            # 将列表对象序列化为 JSON 字符串塞给大模型看
            "round_results": [item.model_dump() for item in req.round_results]
        }
        return await self._invoke_llm(self.prompts["report"], kwargs)