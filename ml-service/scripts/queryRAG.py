"""
queryRAG.py
仅负责：
1. 连接 Zilliz / Milvus
2. 对问题生成本地 embedding
3. 检索相关上下文
4. 调 DashScope 生成最终回答

用法示例：

export DASHSCOPE_API_KEY="替换成你的 DashScope API Key"
export MILVUS_URI="替换成你的 Zilliz URI"
export MILVUS_TOKEN="替换成你的 Zilliz Token"
export LOCAL_EMBEDDING_PATH="/mnt/workspace/hf_cache/models--Qwen--Qwen3-Embedding-0.6B/snapshots/c54f2e6e80b2d7b7de06f51cec4959f6b3e03418"
export JOB_ROLE="java_backend"
export QUESTION="Spring Boot 自动装配原理是什么？"

python queryRAG.py
"""

import os
import json
import logging
from dataclasses import dataclass
from typing import Any, Dict, List

from openai import OpenAI
from pymilvus import MilvusClient
from sentence_transformers import SentenceTransformer


# ============================================================
# 1. 日志配置
# ============================================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger("rag-query")


# ============================================================
# 2. 配置
# ============================================================
@dataclass
class Settings:
    # -------- DashScope / 阿里云 --------
    dashscope_api_key: str = os.getenv("DASHSCOPE_API_KEY", "")
    dashscope_base_url: str = os.getenv(
        "DASHSCOPE_BASE_URL",
        "https://dashscope.aliyuncs.com/compatible-mode/v1"
    )
    chat_model: str = os.getenv("CHAT_MODEL", "qwen-turbo")
    temperature: float = float(os.getenv("TEMPERATURE", "0.1"))

    # -------- 本地 Embedding 模型 --------
    local_embedding_path: str = os.getenv(
        "LOCAL_EMBEDDING_PATH",
        "/mnt/workspace/hf_cache/models--Qwen--Qwen3-Embedding-0.6B/snapshots/c54f2e6e80b2d7b7de06f51cec4959f6b3e03418"
    )

    # -------- 任务信息 --------
    job_role: str = os.getenv("JOB_ROLE", "")
    question: str = os.getenv("QUESTION", "")

    # -------- Milvus / Zilliz --------
    milvus_uri: str = os.getenv("MILVUS_URI", "")
    milvus_token: str = os.getenv("MILVUS_TOKEN", "")
    collection_name: str = os.getenv("MILVUS_COLLECTION", "")

    # -------- 检索 --------
    top_k: int = int(os.getenv("TOP_K", "3"))


# ============================================================
# 3. 校验
# ============================================================
def ensure_dashscope_api_key(settings: Settings) -> None:
    if not settings.dashscope_api_key:
        raise ValueError("未检测到 DASHSCOPE_API_KEY，请先设置环境变量")


def ensure_milvus_config(settings: Settings) -> None:
    if not settings.milvus_uri:
        raise ValueError("未检测到 MILVUS_URI，请先设置环境变量")
    if not settings.milvus_token:
        raise ValueError("未检测到 MILVUS_TOKEN，请先设置环境变量")


def ensure_local_embedding_path(settings: Settings) -> None:
    if not settings.local_embedding_path:
        raise ValueError("未检测到 LOCAL_EMBEDDING_PATH")
    if not os.path.isdir(settings.local_embedding_path):
        raise FileNotFoundError(
            f"本地 embedding 模型目录不存在: {settings.local_embedding_path}"
        )


# ============================================================
# 4. 客户端
# ============================================================
def build_openai_client(settings: Settings) -> OpenAI:
    ensure_dashscope_api_key(settings)
    return OpenAI(
        api_key=settings.dashscope_api_key,
        base_url=settings.dashscope_base_url
    )


def build_milvus_client(settings: Settings) -> MilvusClient:
    ensure_milvus_config(settings)
    logger.info(f"连接 Milvus/Zilliz: {settings.milvus_uri}")
    return MilvusClient(
        uri=settings.milvus_uri,
        token=settings.milvus_token,
    )


# ============================================================
# 5. Embedding
# ============================================================
class LocalEmbedder:
    def __init__(self, model_path: str) -> None:
        logger.info(f"加载本地 embedding 模型: {model_path}")
        self.model = SentenceTransformer(model_path, device="cuda")

    def encode_query(self, text: str) -> List[float]:
        vector = self.model.encode(
            text.strip(),
            normalize_embeddings=True,
            show_progress_bar=False,
        )
        return vector.tolist()


# ============================================================
# 6. 检索
# ============================================================
def search_context(
    milvus_client: MilvusClient,
    collection_name: str,
    query_vector: List[float],
    top_k: int
) -> List[Dict[str, Any]]:
    logger.info(f"开始向量检索，top_k={top_k}")
    search_res = milvus_client.search(
        collection_name=collection_name,
        data=[query_vector],
        limit=top_k,
        output_fields=["text", "source", "metadata"],
    )

    results: List[Dict[str, Any]] = []
    for item in search_res[0]:
        entity = item.get("entity", {}) or {}
        results.append(
            {
                "text": entity.get("text", ""),
                "source": entity.get("source", ""),
                "metadata": entity.get("metadata", ""),
                "score": item.get("distance"),
            }
        )
    return results


def build_context(results: List[Dict[str, Any]]) -> str:
    context_blocks = []
    for i, item in enumerate(results, start=1):
        block = (
            f"[片段{i}]\n"
            f"来源: {item.get('source', '')}\n"
            f"相似度分数: {item.get('score')}\n"
            f"内容:\n{item.get('text', '')}"
        )
        context_blocks.append(block)
    return "\n\n".join(context_blocks)


# ============================================================
# 7. 问答
# ============================================================
def answer_question(
    client: OpenAI,
    settings: Settings,
    question: str,
    retrieved_results: List[Dict[str, Any]]
) -> str:
    context = build_context(retrieved_results)

    system_prompt = (
        "你是专业的Java后端开发助手。\n"
        "你必须严格基于 <context> 中的信息回答问题，禁止编造。\n"
        "如果 <context> 里没有足够信息，请明确回答：未找到相关信息。\n"
        "回答尽量条理清晰，优先用中文。"
    )

    user_prompt = f"""
<context>
{context}
</context>

<question>
{question}
</question>
""".strip()

    logger.info("开始调用聊天模型生成答案")
    resp = client.chat.completions.create(
        model=settings.chat_model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=settings.temperature,
    )

    if not resp.choices:
        return "未找到相关信息"

    content = resp.choices[0].message.content
    if content is None:
        return "未找到相关信息"

    return content


# ============================================================
# 8. 主流程
# ============================================================
def main() -> None:
    settings = Settings()

    if not settings.job_role:
        raise ValueError("未设置 JOB_ROLE，请先设置环境变量，例如 export JOB_ROLE='java_backend'")
    if not settings.question.strip():
        raise ValueError("未设置 QUESTION，请先设置环境变量，例如 export QUESTION='Spring Boot 自动装配原理是什么？'")

    if not settings.collection_name:
        settings.collection_name = f"job_{settings.job_role}"

    ensure_local_embedding_path(settings)

    logger.info("========== RAG Query Start ==========")
    logger.info(f"当前岗位: {settings.job_role}")
    logger.info(f"当前集合名: {settings.collection_name}")
    logger.info(f"当前问题: {settings.question}")

    client = build_openai_client(settings)
    milvus_client = build_milvus_client(settings)
    embedder = LocalEmbedder(settings.local_embedding_path)

    query_vector = embedder.encode_query(settings.question)
    retrieved_results = search_context(
        milvus_client=milvus_client,
        collection_name=settings.collection_name,
        query_vector=query_vector,
        top_k=settings.top_k,
    )

    print("\n================ 检索结果 ================\n")
    print(json.dumps(retrieved_results, ensure_ascii=False, indent=2))

    answer = answer_question(
        client=client,
        settings=settings,
        question=settings.question,
        retrieved_results=retrieved_results,
    )

    print("\n================ 最终回答 ================\n")
    print(answer)

    logger.info("========== RAG Query Done ==========")


if __name__ == "__main__":
    main()