import os
import json
import re
import logging
from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional

from openai import OpenAI


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger("score-answer")


# ============================================================
# 1. 配置
# ============================================================
@dataclass
class ScoringSettings:
    dashscope_api_key: str = os.getenv("DASHSCOPE_API_KEY", "")
    dashscope_base_url: str = os.getenv(
        "DASHSCOPE_BASE_URL",
        "https://dashscope.aliyuncs.com/compatible-mode/v1"
    )
    judge_model: str = os.getenv("JUDGE_MODEL", "qwen-turbo")
    temperature: float = float(os.getenv("SCORING_TEMPERATURE", "0.1"))

    # 一级维度权重
    professional_weight: float = 0.5
    cognition_weight: float = 0.3
    expression_weight: float = 0.2

    # 专业能力二级权重（你们的 V1）
    professional_subweights: Dict[str, float] = None

    def __post_init__(self):
        if self.professional_subweights is None:
            self.professional_subweights = {
                "technical_correctness": 0.20,
                "knowledge_match": 0.09,
                "job_match": 0.31,
                "engineering_practice": 0.40,
            }

            


# ============================================================
# 2. 输入 / 输出数据结构
# ============================================================
@dataclass
class ScoringInput:
    question: str
    answer: str
    job_role: str
    jd_summary: str = ""
    # 可选：语音/情感分析结果。若提供，将用于覆盖或辅助表达维度
#   voice_metrics: Optional[Dict[str, Any]] = None


@dataclass
class DimensionItem:
    score: float
    reason: str


# ============================================================
# 3. OpenAI Compatible Client
# ============================================================
def build_openai_client(settings: ScoringSettings) -> OpenAI:
    if not settings.dashscope_api_key:
        raise ValueError("未检测到 DASHSCOPE_API_KEY，请先设置环境变量")
    return OpenAI(
        api_key=settings.dashscope_api_key,
        base_url=settings.dashscope_base_url
    )


# ============================================================
# 4. Prompt 构造
# ============================================================
def build_scoring_prompt(payload: ScoringInput) -> str:
    voice_metrics_text = json.dumps(payload.voice_metrics, ensure_ascii=False, indent=2) if payload.voice_metrics else "null"

    rubric = """
你是一名严谨的技术面试评分官。请根据给定的岗位、问题、候选人回答和评分标准，对候选人的回答进行结构化评分。

【一级维度】
1. 专业能力（50%）
2. 认知能力（30%）
3. 表达能力（20%）

【二级维度与评分标准】
一、专业能力
1. technical_correctness（技术正确性）
- 0：存在严重技术错误，核心概念完全错误
- 1：多处错误，关键知识理解不清
- 2：有明显错误或混淆
- 3：基本正确，但存在小错误或表达不严谨
- 4：完全正确，无明显错误
- 5：完全正确，且能主动澄清常见误区

2. knowledge_match（知识匹配度）
- 0：完全偏题
- 1：仅涉及边缘知识点
- 2：覆盖部分核心点
- 3：覆盖大部分核心点
- 4：完整覆盖核心知识点
- 5：完整覆盖且有补充延伸

3. job_match（岗位匹配度）
- 0：与岗位无关
- 1：弱相关
- 2：部分相关
- 3：基本符合岗位技能
- 4：明显贴合岗位场景
- 5：深度结合岗位实际业务或技术栈

4. engineering_practice（工程实践能力）
- 0：无任何实践描述
- 1：仅理论描述
- 2：简单提及项目经历
- 3：描述具体实践案例
- 4：描述实践 + 技术权衡
- 5：描述复杂场景 + 方案对比 + 优化思路

二、认知能力
1. logic_structure（逻辑结构能力）
- 0：杂乱无序
- 1：结构混乱
- 2：有部分结构但不清晰
- 3：基本分层清楚
- 4：清晰分点表达
- 5：明确结构（如 1-2-3 分点、总结）且逻辑严密

2. problem_solving（解决问题能力）
- 0：无解决思路
- 1：模糊表达
- 2：简单方案
- 3：可行方案
- 4：多方案对比
- 5：方案 + 风险分析 + 优化建议

3. system_thinking（系统思维能力）
- 0：完全无系统视角
- 1：仅局部考虑
- 2：提及部分系统因素
- 3：基本考虑扩展性或异常
- 4：综合考虑性能、稳定性等
- 5：全局视角 + 权衡分析

三、表达能力
1. clarity（表达清晰度）
- 0：表达混乱无法理解
- 1：多次中断或不连贯
- 2：有明显口语化混乱
- 3：基本清晰
- 4：表达流畅
- 5：语言简洁精准

2. confidence_stability（自信稳定性）
- 若提供 voice_metrics，请结合 voice_metrics 判断：
  - 0：极度紧张，频繁停顿
  - 1：明显犹豫
  - 2：有多次不自然停顿
  - 3：基本稳定
  - 4：稳定自然
  - 5：稳定且语气坚定
- 若未提供 voice_metrics，只能根据文本做保守估计，不要轻易给高分

3. professional_maturity（职业成熟度）
- 0：非正式、不专业
- 1：过度口语化
- 2：部分不规范表达
- 3：基本专业
- 4：用语专业得体
- 5：表达成熟，有职业感

【评分要求】
1. 所有分数必须是 0 到 5 之间的数字，可以保留 1 位小数。
2. 必须给出每个维度的简洁理由。
3. 不要输出总分，不要输出一级维度分，系统会自行计算。
4. 如果回答内容明显不足，请如实打低分。
5. 不要因为语气礼貌就给高分，必须严格依据内容质量评分。
6. 如果问题要求技术原理，而回答偏项目经历，则“知识匹配度”应下降。
7. 如果回答正确但过于基础、缺少岗位相关性，则“岗位匹配度”和“工程实践能力”不应高。
8. 输出必须是 JSON，且不得包含 JSON 以外的任何文字。

【输出 JSON 格式】
{
  "professional": {
    "technical_correctness": {"score": 0-5, "reason": "..."},
    "knowledge_match": {"score": 0-5, "reason": "..."},
    "job_match": {"score": 0-5, "reason": "..."},
    "engineering_practice": {"score": 0-5, "reason": "..."}
  },
  "cognition": {
    "logic_structure": {"score": 0-5, "reason": "..."},
    "problem_solving": {"score": 0-5, "reason": "..."},
    "system_thinking": {"score": 0-5, "reason": "..."}
  },
  "expression": {
    "clarity": {"score": 0-5, "reason": "..."},
    "confidence_stability": {"score": 0-5, "reason": "..."},
    "professional_maturity": {"score": 0-5, "reason": "..."}
  },
  "overall_feedback": "...",
  "improvement_suggestions": ["...", "...", "..."]
}
""".strip()

    prompt = f"""
请根据以下输入进行评分。

【岗位】
{payload.job_role}

【岗位要求摘要 JD】
{payload.jd_summary if payload.jd_summary.strip() else "未提供"}

【面试问题】
{payload.question}

【候选人回答】
{payload.answer}

【语音/情感特征（可选）】
{voice_metrics_text}

【评分标准】
{rubric}
""".strip()

    return prompt


# ============================================================
# 5. 解析与校验
# ============================================================
def extract_json(text: str) -> Dict[str, Any]:
    text = text.strip()

    # 兼容 ```json ... ``` 这种输出
    fenced_match = re.search(r"```json\s*(\{.*\})\s*```", text, re.S)
    if fenced_match:
        text = fenced_match.group(1)

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # 尝试截取最外层 JSON
        first = text.find("{")
        last = text.rfind("}")
        if first != -1 and last != -1 and last > first:
            candidate = text[first:last + 1]
            return json.loads(candidate)
        raise ValueError("LLM 返回内容无法解析为 JSON")


def clamp_score(value: Any) -> float:
    try:
        score = float(value)
    except Exception:
        raise ValueError(f"非法分数: {value}")
    if score < 0:
        score = 0.0
    if score > 5:
        score = 5.0
    return round(score, 1)


def validate_dimension_item(item: Dict[str, Any], field_name: str) -> Dict[str, Any]:
    if not isinstance(item, dict):
        raise ValueError(f"{field_name} 不是对象")
    if "score" not in item or "reason" not in item:
        raise ValueError(f"{field_name} 缺少 score 或 reason")
    return {
        "score": clamp_score(item["score"]),
        "reason": str(item["reason"]).strip()
    }


def validate_scoring_result(data: Dict[str, Any]) -> Dict[str, Any]:
    required = {
        "professional": [
            "technical_correctness",
            "knowledge_match",
            "job_match",
            "engineering_practice",
        ],
        "cognition": [
            "logic_structure",
            "problem_solving",
            "system_thinking",
        ],
        "expression": [
            "clarity",
            "confidence_stability",
            "professional_maturity",
        ]
    }

    result: Dict[str, Any] = {
        "professional": {},
        "cognition": {},
        "expression": {},
        "overall_feedback": str(data.get("overall_feedback", "")).strip(),
        "improvement_suggestions": data.get("improvement_suggestions", []),
    }

    for top_key, sub_keys in required.items():
        if top_key not in data or not isinstance(data[top_key], dict):
            raise ValueError(f"缺少一级字段: {top_key}")
        for sub_key in sub_keys:
            if sub_key not in data[top_key]:
                raise ValueError(f"缺少字段: {top_key}.{sub_key}")
            result[top_key][sub_key] = validate_dimension_item(
                data[top_key][sub_key],
                f"{top_key}.{sub_key}"
            )

    if not isinstance(result["improvement_suggestions"], list):
        result["improvement_suggestions"] = []

    result["improvement_suggestions"] = [
        str(x).strip() for x in result["improvement_suggestions"] if str(x).strip()
    ][:5]

    return result


# ============================================================
# 6. 分数计算
# ============================================================
def compute_scores(
    validated_result: Dict[str, Any],
    settings: ScoringSettings
) -> Dict[str, Any]:
    p = validated_result["professional"]
    c = validated_result["cognition"]
    e = validated_result["expression"]

    # 专业能力加权
    P = round(
        p["technical_correctness"]["score"] * settings.professional_subweights["technical_correctness"] +
        p["knowledge_match"]["score"] * settings.professional_subweights["knowledge_match"] +
        p["job_match"]["score"] * settings.professional_subweights["job_match"] +
        p["engineering_practice"]["score"] * settings.professional_subweights["engineering_practice"],
        2
    )

    # 认知能力均值
    C = round((
        c["logic_structure"]["score"] +
        c["problem_solving"]["score"] +
        c["system_thinking"]["score"]
    ) / 3, 2)

    # 表达能力均值
    E = round((
        e["clarity"]["score"] +
        e["confidence_stability"]["score"] +
        e["professional_maturity"]["score"]
    ) / 3, 2)

    final_score = round(
        (settings.professional_weight * P +
         settings.cognition_weight * C +
         settings.expression_weight * E) * 20,
        2
    )

    return {
        "dimension_scores": {
            "professional": P,
            "cognition": C,
            "expression": E
        },
        "final_score": final_score
    }


# ============================================================
# 7. 主评分函数
# ============================================================
def score_answer(
    payload: ScoringInput,
    settings: Optional[ScoringSettings] = None
) -> Dict[str, Any]:
    settings = settings or ScoringSettings()
    client = build_openai_client(settings)

    prompt = build_scoring_prompt(payload)

    logger.info("开始调用 LLM 进行结构化评分")
    resp = client.chat.completions.create(
        model=settings.judge_model,
        messages=[
            {
                "role": "system",
                "content": "你是严格、专业、保守的技术面试评分官。你只能输出 JSON。"
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=settings.temperature,
    )

    if not resp.choices:
        raise ValueError("LLM 未返回任何结果")

    content = resp.choices[0].message.content
    if not content:
        raise ValueError("LLM 返回内容为空")

    parsed = extract_json(content)
    validated = validate_scoring_result(parsed)
    computed = compute_scores(validated, settings)

    result = {
        "input": asdict(payload),
        "scores": validated,
        **computed
    }
    return result


# ============================================================
# 8. CLI 调试入口
# ============================================================
# if __name__ == "__main__":
#     demo_input = ScoringInput(
#         question="Spring Boot 自动装配原理是什么？",
#         answer=(
#             "Spring Boot 自动装配核心是基于约定大于配置。"
#             "启动时会通过自动配置机制加载一些配置类，"
#             "这些配置类通常会结合条件注解判断当前环境是否满足，"
#             "如果满足就把对应 Bean 注册到容器中。"
#             "在实际项目里，我们也会通过自定义 starter 来复用公共能力。"
#         ),
#         job_role="java_backend",
#         jd_summary="熟悉 Java、Spring Boot、MySQL、Redis，具备后端项目开发经验。",
#         voice_metrics={
#             "pause_count": 2,
#             "speech_rate": "normal",
#             "confidence": 0.72
#         }
#     )

#     result = score_answer(demo_input)
#     print(json.dumps(result, ensure_ascii=False, indent=2))