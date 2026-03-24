import os
import sys
from fastapi.testclient import TestClient

sys.path.append('/home/yys/ai-interview-simulator/ml-service')
os.environ['DASHSCOPE_API_KEY'] = os.environ.get('DASHSCOPE_API_KEY', 'dummy-key-for-smoke-test')

import app.main as main_mod


class StubEngine:
    async def aclose(self):
        return None

    async def generate_first_question(self, req):
        return {
            'question': 'Q1',
            'flow_control': {'stage_transition': 'continue', 'target_stage': 'intro'},
        }

    async def stream_first_question(self, req):
        txt = '{"question":"请先做自我介绍","flow_control":{"stage_transition":"continue","target_stage":"intro"}}'
        for ch in txt:
            yield ch

    async def generate_following_question(self, req):
        return {
            'question': 'Q2',
            'updated_history_summary': 'ok',
            'immediate_feedback': 'ok',
            'flow_control': {'stage_transition': 'continue', 'target_stage': 'tech_general'},
        }

    async def stream_following_question(self, req):
        txt = '{"question":"你如何设计限流？","updated_history_summary":"ok","flow_control":{"stage_transition":"switch","target_stage":"tech_scenario"},"immediate_feedback":"回答有条理"}'
        for ch in txt:
            yield ch

    async def analyze_answer(self, req):
        return {
            'professional': {},
            'cognition': {},
            'expression': {},
            'dimension_scores': {'professional': 4.0, 'cognition': 4.0, 'expression': 4.0},
            'final_score': 80.0,
            'overall_feedback': 'good',
            'improvement_suggestions': ['x'],
        }

    async def generate_overall_report(self, req):
        return {
            'hiring_recommendation': 'Hire',
            'overall_score': 86.0,
            'executive_summary': 'summary',
            'strengths': ['a'],
            'weaknesses': ['b'],
            'ability_trend': 'up',
            'detailed_recommendation': 'go',
        }


captured = {}


async def fake_callback(url, payload, max_attempts=3):
    captured['url'] = url
    captured['message'] = payload.get('message')


main_mod._post_callback_with_retry = fake_callback

start_payload = {
    'session_id': 'sess-001',
    'job_position': 'Java后端',
    'jd_summary': 'jd',
    'resume_content': 'resume',
    'interview_config': {
        'mode': 'text',
        'interviewer_style': 'standard',
        'difficulty': 'medium',
        'company_context': 'ctx',
        'analyze_emotion': False,
    },
    'flow_control': {'stage_transition': 'continue', 'target_stage': 'intro'},
}

follow_payload = {
    'session_id': 'sess-001',
    'round_id': 2,
    'interview_config': start_payload['interview_config'],
    'background': {'job_position': 'Java后端', 'resume_content': 'resume', 'jd_summary': 'jd'},
    'history_data': {
        'history_summary': 'sum',
        'recent_history': [
            {
                'round_id': 1,
                'assistant_content': 'a',
                'user_content': 'u',
                'flow_control': {'stage_transition': 'continue', 'target_stage': 'intro'},
            }
        ],
    },
}

analysis_payload = {
    'session_id': 'sess-001',
    'round_id': 2,
    'current_stage': 'tech_general',
    'interview_config': start_payload['interview_config'],
    'content_to_analyze': {
        'job_position': 'Java后端',
        'resume_content': 'resume',
        'jd_summary': 'jd',
        'question': 'q',
        'user_answer': 'a',
        'history_summary': 'sum',
    },
}

report_payload = {
    'session_id': 'sess-001',
    'callback_url': 'https://unused.example/cb',
    'interview_config': start_payload['interview_config'],
    'interview_context': {
        'job_position': 'Java后端',
        'jd_summary': 'jd',
        'resume_content': 'resume',
        'total_rounds': 3,
        'interview_duration_seconds': 600,
    },
    'round_results': [
        {
            'round_id': 1,
            'current_stage': 'intro',
            'dimension_scores': {'professional': 3.0, 'cognition': 3.0, 'expression': 3.0},
            'dimension_details': {
                'professional': {
                    'technical_correctness': {'reason': 'r', 'score': 3},
                    'knowledge_match': {'reason': 'r', 'score': 3},
                    'job_match': {'reason': 'r', 'score': 3},
                    'engineering_practice': {'reason': 'r', 'score': 3},
                },
                'cognition': {
                    'logic_structure': {'reason': 'r', 'score': 3},
                    'problem_solving': {'reason': 'r', 'score': 3},
                    'system_thinking': {'reason': 'r', 'score': 3},
                },
                'expression': {
                    'clarity': {'reason': 'r', 'score': 3},
                    'confidence_stability': {'reason': 'r', 'score': 3},
                    'professional_maturity': {'reason': 'r', 'score': 3},
                },
            },
            'overall_feedback': 'ok',
            'final_score': 60.0,
            'improvement_suggestions': ['x'],
        }
    ],
}

with TestClient(main_mod.app) as client:
    client.app.state.engine = StubEngine()
    r1 = client.post('/api/v1/interview/start', json=start_payload)
    r2 = client.post('/api/v1/interview/followup', json=follow_payload)
    r3 = client.post('/api/v1/interview/analysis', json=analysis_payload)
    r4 = client.post('/api/v1/interview/report', json=report_payload)
    rs = client.post('/api/v1/interview/start/stream', json=start_payload)
    rf = client.post('/api/v1/interview/followup/stream', json=follow_payload)

print('start', r1.status_code, r1.json().get('code'))
print('followup', r2.status_code, r2.json().get('code'))
print('analysis', r3.status_code, r3.json().get('code'))
print('report', r4.status_code, r4.json().get('code'))
print('start_stream', rs.status_code, '"type": "done"' in rs.text or '"type":"done"' in rs.text)
print('follow_stream', rf.status_code, '"type": "done"' in rf.text or '"type":"done"' in rf.text)
print('callback_url', captured.get('url'))
print('callback_message', captured.get('message'))
