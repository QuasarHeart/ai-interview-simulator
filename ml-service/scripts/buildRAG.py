"""
后续添加新的资料进入RAG数据库只需要按照岗位的不同直接输出如下指令：
JOB_ROLE=岗位名 python buildRAG.py
"""

import os
import json
import time
import math
import logging
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Iterable

from openai import OpenAI
from pymilvus import MilvusClient
from tqdm import tqdm

from llama_index.core import SimpleDirectoryReader, Document
from llama_index.core.embeddings import BaseEmbedding
from llama_index.core.node_parser import SemanticSplitterNodeParser
#from sentence_transformers import SentenceTransformer
from llama_index.core.node_parser import SentenceSplitter


# ============================================================
# 1. 日志配置
# ============================================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger("industrial-rag")


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

    embedding_model: str = os.getenv("EMBEDDING_MODEL", "text-embedding-v2")
    chat_model: str = os.getenv("CHAT_MODEL", "qwen-turbo")
    job_role: str = os.getenv("JOB_ROLE", "")
    # -------- 文档目录 --------
    docs_dir: str = os.getenv("DOCS_DIR","")
    docs_exts: tuple = (".md",)

    # -------- 文本处理 --------
    max_text_length: int = int(os.getenv("MAX_TEXT_LENGTH", "8000"))
    min_chunk_length: int = int(os.getenv("MIN_CHUNK_LENGTH", "20"))

    # -------- 语义切分 --------
    semantic_buffer_size: int = int(os.getenv("SEMANTIC_BUFFER_SIZE", "1"))
    semantic_breakpoint_percentile_threshold: int = int(
        os.getenv("SEMANTIC_BREAKPOINT_PERCENTILE_THRESHOLD", "90")
    )

    # -------- Embedding 批处理 --------
    embedding_batch_size: int = int(os.getenv("EMBEDDING_BATCH_SIZE", "16"))
    embedding_max_retries: int = int(os.getenv("EMBEDDING_MAX_RETRIES", "3"))
    embedding_retry_backoff: float = float(os.getenv("EMBEDDING_RETRY_BACKOFF", "1.5"))

    # -------- Milvus --------
    milvus_uri: str = os.getenv("MILVUS_URI", "http://localhost:19530")
    collection_name: str = os.getenv("MILVUS_COLLECTION", "")
    milvus_metric_type: str = os.getenv("MILVUS_METRIC_TYPE", "COSINE")
    recreate_collection: bool = os.getenv("RECREATE_COLLECTION", "false").lower() == "true"

    # -------- 检索 --------
    top_k: int = int(os.getenv("TOP_K", "3"))

    # -------- LLM --------
    temperature: float = float(os.getenv("TEMPERATURE", "0.1"))

    # -------- 演示问题 --------
    question: str = os.getenv("QUESTION", "Java语言的优点是什么？")


# ============================================================
# 3. 通用工具函数
# ============================================================
def ensure_api_key(settings: Settings) -> None:
    if not settings.dashscope_api_key:
        raise ValueError(
            "未检测到 DASHSCOPE_API_KEY。请先设置环境变量，例如：\n"
            "Linux/macOS: export DASHSCOPE_API_KEY='你的Key'\n"
            "Windows PowerShell: $env:DASHSCOPE_API_KEY='你的Key'"
        )


def truncate_text(text: str, max_length: int) -> str:
    if not text:
        return ""
    return text[:max_length]


def batched(items: List[Any], batch_size: int) -> Iterable[List[Any]]:
    total = len(items)
    for i in range(0, total, batch_size):
        yield items[i:i + batch_size]


# ============================================================
# 4. OpenAI Compatible Client（阿里云 DashScope）
# ============================================================
def build_openai_client(settings: Settings) -> OpenAI:
    ensure_api_key(settings)
    client = OpenAI(
        api_key=settings.dashscope_api_key,
        base_url=settings.dashscope_base_url
    )
    return client


# ============================================================
# 5. 自定义 Embedding 适配 LlamaIndex
# ============================================================
class AliyunEmbedding(BaseEmbedding):
    model_name: str = ""
    client: Any = None
    max_text_length: int = 8000
    max_retries: int = 3
    retry_backoff: float = 1.5

    def __init__(
        self,
        client: Any,
        model_name: str,
        max_text_length: int = 8000,
        max_retries: int = 3,
        retry_backoff: float = 1.5,
        **kwargs: Any,
    ) -> None:
        super().__init__(model_name=model_name, **kwargs)
        self.client = client
        self.model_name = model_name
        self.max_text_length = max_text_length
        self.max_retries = max_retries
        self.retry_backoff = retry_backoff

    def _call_embedding_api(self, input_data: Any) -> Any:
        last_error = None
        for attempt in range(1, self.max_retries + 1):
            try:
                return self.client.embeddings.create(
                    model=self.model_name,
                    input=input_data
                )
            except Exception as e:
                last_error = e
                sleep_seconds = self.retry_backoff ** (attempt - 1)
                logger.warning(
                    f"Embedding API 调用失败，第 {attempt}/{self.max_retries} 次重试，"
                    f"{sleep_seconds:.2f}s 后重试。错误: {e}"
                )
                time.sleep(sleep_seconds)
        raise RuntimeError(f"Embedding API 最终失败: {last_error}")

    def _sanitize(self, text: str) -> str:
        return truncate_text((text or "").strip(), self.max_text_length)

    def _get_text_embedding(self, text: str) -> List[float]:
        clean_text = self._sanitize(text)
        if not clean_text:
            raise ValueError("空文本无法生成 embedding")
        resp = self._call_embedding_api(clean_text)
        return resp.data[0].embedding

    def _get_text_embeddings(self, texts: List[str]) -> List[List[float]]:
        clean_texts = [self._sanitize(t) for t in texts]
        clean_texts = [t for t in clean_texts if t]
        if not clean_texts:
            return []

        resp = self._call_embedding_api(clean_texts)
        return [item.embedding for item in resp.data]

    def _get_query_embedding(self, query: str) -> List[float]:
        return self._get_text_embedding(query)

    async def _aget_query_embedding(self, query: str) -> List[float]:
        return self._get_query_embedding(query)

    async def _aget_text_embedding(self, text: str) -> List[float]:
        return self._get_text_embedding(text)

    async def _aget_text_embeddings(self, texts: List[str]) -> List[List[float]]:
        return self._get_text_embeddings(texts)
# ============================================================
# 6. 文档加载
# ============================================================
def load_documents(settings: Settings) -> List[Document]:
    if not os.path.isdir(settings.docs_dir):
        raise FileNotFoundError(f"文档目录不存在: {settings.docs_dir}")

    logger.info(f"开始加载文档目录: {settings.docs_dir}")
    documents = SimpleDirectoryReader(
        input_dir=settings.docs_dir,
        required_exts=list(settings.docs_exts),
        recursive=True,
        encoding="utf-8",
        filename_as_id=True,
    ).load_data()

    logger.info(f"已加载文档数量: {len(documents)}")
    if not documents:
        raise ValueError("未读取到任何文档，请检查 DOCS_DIR 和文件扩展名")

    return documents


# ============================================================
# 7. 语义切分
# ============================================================
def build_text_splitter(settings: Settings) -> SentenceSplitter:
    splitter = SentenceSplitter(
        chunk_size=500,
        chunk_overlap=50,
        include_metadata=True,
        include_prev_next_rel=True,
    )
    return splitter


def split_documents_to_chunks(
    documents: List[Document],
    splitter: Any,
    settings: Settings
) -> List[Dict[str, Any]]:
    logger.info("开始进行语义切分")
    nodes = splitter.get_nodes_from_documents(documents)

    chunks: List[Dict[str, Any]] = []
    next_id = 0

    for node in nodes:
        text = node.get_content().strip()
        text = truncate_text(text, settings.max_text_length)

        if len(text) < settings.min_chunk_length:
            continue

        metadata = getattr(node, "metadata", {}) or {}
        source_file = (
            metadata.get("file_path")
            or metadata.get("file_name")
            or metadata.get("filename")
            or ""
        )

        chunks.append(
            {
                "id": next_id,
                "text": text,
                "source": source_file,
                "metadata": metadata,
            }
        )
        next_id += 1

    logger.info(f"语义切分完成，有效 chunk 数量: {len(chunks)}")
    if not chunks:
        raise ValueError("语义切分后没有有效 chunk，请检查文档内容或切分参数")

    return chunks


# ============================================================
# 8. Embedding 维度检测
# ============================================================
def detect_embedding_dim(embed_model: BaseEmbedding) -> int:
    probe_text = "Go语言的优点：高性能、并发友好、语法简洁。"
    vector = embed_model._get_text_embedding(probe_text)
    if not vector:
        raise ValueError("无法获取测试 embedding，无法确定向量维度")
    dim = len(vector)
    logger.info(f"检测到 embedding 维度: {dim}")
    return dim


# ============================================================
# 9. Milvus 管理
# ============================================================
def build_milvus_client(settings: Settings) -> MilvusClient:
    logger.info(f"连接 Milvus: {settings.milvus_uri}")
    return MilvusClient(uri=settings.milvus_uri)


def recreate_collection_if_needed(
    milvus_client: MilvusClient,
    settings: Settings,
    embedding_dim: int
) -> None:
    exists = milvus_client.has_collection(settings.collection_name)

    if exists and settings.recreate_collection:
        logger.info(f"集合已存在，准备删除重建: {settings.collection_name}")
        milvus_client.drop_collection(settings.collection_name)
        exists = False

    if not exists:
        logger.info(f"创建集合: {settings.collection_name}")
        milvus_client.create_collection(
            collection_name=settings.collection_name,
            dimension=embedding_dim,
            metric_type=settings.milvus_metric_type,
        )
    else:
        logger.info(f"复用已有集合: {settings.collection_name}")


# ============================================================
# 10. 批量向量化与入库
# ============================================================
def embed_chunks(
    chunks: List[Dict[str, Any]],
    embed_model: BaseEmbedding,
    settings: Settings
) -> List[Dict[str, Any]]:
    logger.info("开始批量生成 embeddings")

    rows: List[Dict[str, Any]] = []
    total_batches = math.ceil(len(chunks) / settings.embedding_batch_size)

    for batch_idx, batch in enumerate(
        tqdm(
            list(batched(chunks, settings.embedding_batch_size)),
            desc="Embedding",
            total=total_batches
        ),
        start=1
    ):
        texts = [item["text"] for item in batch]

        try:
            vectors = embed_model._get_text_embeddings(texts)
            if len(vectors) != len(texts):
                raise RuntimeError(
                    f"批量 embedding 返回数量不一致: 输入 {len(texts)} 条, 输出 {len(vectors)} 条"
                )
        except Exception as e:
            logger.warning(f"第 {batch_idx} 批批量 embedding 失败，回退到单条处理。错误: {e}")
            vectors = []
            for item in batch:
                try:
                    vec = embed_model._get_text_embedding(item["text"])
                    vectors.append(vec)
                except Exception as single_e:
                    logger.error(
                        f"单条 embedding 失败，chunk_id={item['id']} source={item.get('source', '')} 错误: {single_e}"
                    )
                    vectors.append(None)

        for item, vector in zip(batch, vectors):
            if vector is None:
                continue

            rows.append(
                {
                    "id": item["id"],
                    "vector": vector,
                    "text": item["text"],
                    "source": item.get("source", ""),
                    "metadata": json.dumps(item.get("metadata", {}), ensure_ascii=False),
                }
            )

    logger.info(f"成功生成并保留的向量记录数: {len(rows)}")
    if not rows:
        raise ValueError("没有任何有效向量可入库")

    return rows


def insert_into_milvus(
    milvus_client: MilvusClient,
    collection_name: str,
    rows: List[Dict[str, Any]]
) -> Any:
    logger.info(f"开始写入 Milvus，记录数: {len(rows)}")
    result = milvus_client.insert(
        collection_name=collection_name,
        data=rows,
    )
    logger.info(f"Milvus 插入完成: {result}")
    return result


# ============================================================
# 11. 检索
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

    logger.info(f"检索返回结果数: {len(results)}")
    return results


# ============================================================
# 12. 问答
# ============================================================
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
# 13. 主流程
# ============================================================
def main() -> None:
    settings = Settings()
    if not settings.docs_dir:
        settings.docs_dir = f"../knowledge_base/{settings.job_role}/reference_docs/"

    if not settings.collection_name:
        settings.collection_name = f"job_{settings.job_role}"
    logger.info("========== Industrial RAG Pipeline Start ==========")
    logger.info(f"当前岗位: {settings.job_role}")
    logger.info(f"当前文档目录: {settings.docs_dir}")
    logger.info(f"当前集合名: {settings.collection_name}")
    logger.info(f"当前 embedding 模型: {settings.embedding_model}")

    # 1) 构建客户端
    client = build_openai_client(settings)

    # 2) 构建 embedding 模型
    embed_model = AliyunEmbedding(
        client=client,
        model_name=settings.embedding_model,
        max_text_length=settings.max_text_length,
        max_retries=settings.embedding_max_retries,
        retry_backoff=settings.embedding_retry_backoff,
    )

    # 3) 加载文档
    documents = load_documents(settings)

    # 4) 语义切分
    splitter = build_text_splitter(settings)
    chunks = split_documents_to_chunks(documents, splitter, settings)

    # 5) embedding 维度检测
    embedding_dim = detect_embedding_dim(embed_model)

    # 6) Milvus
    milvus_client = build_milvus_client(settings)
    recreate_collection_if_needed(milvus_client, settings, embedding_dim)

    # 7) 向量化并入库
    rows = embed_chunks(chunks, embed_model, settings)
    insert_into_milvus(milvus_client, settings.collection_name, rows)

    # 8) 检索
    logger.info(f"问题: {settings.question}")
    query_vector = embed_model._get_query_embedding(settings.question)
    retrieved_results = search_context(
        milvus_client=milvus_client,
        collection_name=settings.collection_name,
        query_vector=query_vector,
        top_k=settings.top_k,
    )

    print("\n================ 检索结果 ================\n")
    print(json.dumps(retrieved_results, ensure_ascii=False, indent=2))

    # 9) 回答
    answer = answer_question(
        client=client,
        settings=settings,
        question=settings.question,
        retrieved_results=retrieved_results,
    )

    print("\n================ 最终回答 ================\n")
    print(answer)

    logger.info("========== Industrial RAG Pipeline Done ==========")


if __name__ == "__main__":
    main()