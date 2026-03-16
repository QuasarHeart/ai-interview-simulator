import json

from score_answer import score_answer, ScoringInput, HistoryTurn


def main():
    payload = ScoringInput(
    session_id="sess_demo_001",
    round_id=3,
    job_position="java_backend",
    question="请解释 Spring Boot 自动装配原理。",
    user_answer=(
        "Spring Boot 自动装配的核心思想是约定大于配置。"
        "它会在启动过程中加载自动配置类，这些配置类通过条件注解判断当前环境是否满足条件，"
        "如果满足，就会把对应的 Bean 注册到 Spring 容器中。"
        "比如如果类路径下存在某些依赖，就会启用对应的自动配置。"
        "在项目里我们也可以通过自定义 starter 封装公共能力。"
        ),
    jd_summary="熟悉 Java、Spring Boot、MySQL、Redis，具备后端项目开发经验。",
    recent_history=[
    HistoryTurn(
    round_id=1,
    question="请介绍一下你的项目经验。",
    answer="我做过电商系统，主要负责订单模块和缓存优化。"
        ),
    HistoryTurn(
            round_id=2,
            question="你们项目中 Redis 是怎么使用的？",
            answer="主要用于热点数据缓存、分布式锁和登录状态管理。"
            )
        ],
        history_summary="候选人在前两轮中项目表达较自然，Redis 使用场景回答较合理，但缺少异常场景和一致性问题分析。",
        voice_metrics={
            "pause_count": 2,
            "speech_rate": "normal",
            "confidence": 0.73
        }
    )

    result = score_answer(payload)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()