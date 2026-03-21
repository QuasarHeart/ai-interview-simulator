from pydantic import BaseModel, Field
from typing import Optional, List, Literal

# ==========================================
# 第一部分：全局基础配置 (积木块)
# ==========================================

class InterviewConfig(BaseModel):
    mode: Literal["text", "audio", "video"]
    interviewer_style: Literal["standard", "friendly", "aggressive", "expert"]
    difficulty: Literal["easy", "medium", "hard"]
    company_context: Optional[str] = None
    analyze_emotion: Optional[bool] = False

class FlowControl(BaseModel):
    # 严格限制只能传这几个控制指令
    stage_transition: Literal["continue", "switch", "end"]
    target_stage: Literal["intro", "resume_deep_dive", "tech_general", "tech_scenario", "reverse_qa", "end"]

class Background(BaseModel):
    job_position: str
    resume_content: str
    jd_summary: str

class RecentHistoryItem(BaseModel):
    role: Literal["assistant", "user"]
    content: str

class HistoryData(BaseModel): 
    history_summary: str
    recent_history: List[RecentHistoryItem]

class ContentToAnalyze(Background): 
    # 继承 Background，自动包含 job_position, resume_summary, jd_summary
    question: str
    user_answer: str
    history_summary: str

class InterviewContext(BaseModel):
    # Report 接口的特有上下文
    job_position: str
    jd_summary: str
    resume_content: str
    total_rounds: int
    interview_duration_seconds: int

# ==========================================
# 第二部分：打分详情组件 (Analysis 和 Report 复用)
# ==========================================

class ScoreReason(BaseModel):
    reason: str
    score: int  # 若允许小数可改为 float

class ProfessionalDetails(BaseModel):
    technical_correctness: ScoreReason
    knowledge_match: ScoreReason
    job_match: ScoreReason
    engineering_practice: ScoreReason

class CognitionDetails(BaseModel):
    logic_structure: ScoreReason
    problem_solving: ScoreReason
    system_thinking: ScoreReason

class ExpressionDetails(BaseModel):
    clarity: ScoreReason
    confidence_stability: ScoreReason
    professional_maturity: ScoreReason

class DimensionDetails(BaseModel):
    professional: ProfessionalDetails
    cognition: CognitionDetails
    expression: ExpressionDetails

class DimensionScores(BaseModel):
    professional: float
    cognition: float
    expression: float

class RoundResultItem(BaseModel):
    round_id: int
    current_stage: str
    dimension_scores: DimensionScores
    dimension_details: DimensionDetails
    overall_feedback: str
    final_score: float
    improvement_suggestions: List[str]

# ==========================================
# 第三部分：4 大 API 请求模型 (Request Models)
# ==========================================

class StartRequest(BaseModel):
    """对应 /api/v1/interview/start"""
    session_id: str
    job_position: str
    resume_content: str
    interview_config: InterviewConfig
    flow_control: FlowControl

class FollowupRequest(BaseModel):
    """对应 /api/v1/interview/followup"""
    session_id: str
    round_id: int
    interview_config: InterviewConfig
    background: Background
    history_data: HistoryData
    flow_control: FlowControl

class AnalysisRequest(BaseModel):
    """对应 /api/v1/interview/analysis"""
    session_id: str
    round_id: int
    current_stage: str
    interview_config: InterviewConfig
    content_to_analyze: ContentToAnalyze

class ReportRequest(BaseModel):
    """对应 /api/v1/interview/report"""
    session_id: str
    callback_url: str
    interview_config: InterviewConfig
    interview_context: InterviewContext
    round_results: List[RoundResultItem]