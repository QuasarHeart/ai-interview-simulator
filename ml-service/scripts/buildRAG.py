"""
buildRAG.py
仅负责：
1. 加载文档
2. 文本切分
3. 本地 embedding
4. 写入 Zilliz / Milvus

支持两种模式：
- INGEST_MODE=rebuild  : 删除并重建 collection
- INGEST_MODE=append   : 追加写入（使用稳定唯一 chunk_id）

用法示例：

export MILVUS_URI="替换成你的 Zilliz URI"
export MILVUS_TOKEN="替换成你的 Zilliz Token"
export LOCAL_EMBEDDING_PATH="/mnt/workspace/hf_cache/models--Qwen--Qwen3-Embedding-0.6B/snapshots/c54f2e6e80b2d7b7de06f51cec4959f6b3e03418"
export JOB_ROLE="java_backend"
export INGEST_MODE="rebuild"

python buildRAG.py

如需自定义文档目录：
export DOCS_DIR="/mnt/workspace/ai-interview-simulator/ml-service/knowledge_base/java_backend/reference_docs"
"""

import os
import json
import math
import hashlib
import logging
from dataclasses import dataclass
from typing import Any, Dict, List, Iterable

from pymilvus import MilvusClient
from tqdm import tqdm
from sentence_transformers import SentenceTransformer

from llama_index.core import SimpleDirectoryReader, Document
from llama_index.core.embeddings import BaseEmbedding
from llama_index.core.node_parser import SentenceSplitter


# ============================================================
# 1. 日志配置
# ============================================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger("rag-ingest")


# ============================================================
# 2. 配置
# ============================================================
@dataclass
class Settings:
    # -------- 本地 Embedding 模型 --------
    local_embedding_path: str = os.getenv(
        "LOCAL_EMBEDDING_PATH",
        "/mnt/workspace/hf_cache/models--Qwen--Qwen3-Embedding-0.6B/snapshots/c54f2e6e80b2d7b7de06f51cec4959f6b3e03418"
    )

    # -------- 任务信息 --------
    job_role: str = os.getenv("JOB_ROLE", "")
    ingest_mode: str = os.getenv("INGEST_MODE", "append").strip().lower()

    # -------- 文档目录 --------
    docs_dir: str = os.getenv("DOCS_DIR", "")
    docs_exts: tuple = (".md",)

    # -------- 文本处理 --------
    max_text_length: int = int(os.getenv("MAX_TEXT_LENGTH", "8000"))
    min_chunk_length: int = int(os.getenv("MIN_CHUNK_LENGTH", "20"))

    # -------- 切分参数 --------
    chunk_size: int = int(os.getenv("CHUNK_SIZE", "500"))
    chunk_overlap: int = int(os.getenv("CHUNK_OVERLAP", "50"))

    # -------- Embedding 批处理 --------
    embedding_batch_size: int = int(os.getenv("EMBEDDING_BATCH_SIZE", "16"))

    # -------- Milvus / Zilliz --------
    milvus_uri: str = os.getenv("MILVUS_URI", "")
    milvus_token: str = os.getenv("MILVUS_TOKEN", "")
    collection_name: str = os.getenv("MILVUS_COLLECTION", "")
    milvus_metric_type: str = os.getenv("MILVUS_METRIC_TYPE", "COSINE")

    # -------- 去重与控制 --------
    skip_existing_in_append: bool = os.getenv("SKIP_EXISTING_IN_APPEND", "true").lower() == "true"


# ============================================================
# 3. 基础校验
# ============================================================
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


def ensure_ingest_mode(settings: Settings) -> None:
    if settings.ingest_mode not in {"rebuild", "append"}:
        raise ValueError("INGEST_MODE 仅支持 'rebuild' 或 'append'")


def truncate_text(text: str, max_length: int) -> str:
    if not text:
        return ""
    return text[:max_length]


def batched(items: List[Any], batch_size: int) -> Iterable[List[Any]]:
    total = len(items)
    for i in range(0, total, batch_size):
        yield items[i:i + batch_size]


# ============================================================
# 4. 本地 Embedding
# ============================================================
class LocalSentenceTransformerEmbedding(BaseEmbedding):
    model_name: str = ""
    model: Any = None
    max_text_length: int = 8000
    batch_size: int = 16

    def __init__(
        self,
        model_path: str,
        max_text_length: int = 8000,
        batch_size: int = 16,
        **kwargs: Any,
    ) -> None:
        super().__init__(model_name=model_path, **kwargs)
        self.model_name = model_path
        self.max_text_length = max_text_length
        self.batch_size = batch_size

        logger.info(f"加载本地 embedding 模型: {model_path}")
        self.model = SentenceTransformer(model_path, device="cuda")

    def _sanitize(self, text: str) -> str:
        return truncate_text((text or "").strip(), self.max_text_length)

    def _get_text_embedding(self, text: str) -> List[float]:
        clean_text = self._sanitize(text)
        if not clean_text:
            raise ValueError("空文本无法生成 embedding")

        vector = self.model.encode(
            clean_text,
            normalize_embeddings=True,
            show_progress_bar=False,
        )
        return vector.tolist()

    def _get_text_embeddings(self, texts: List[str]) -> List[List[float]]:
        clean_texts = [self._sanitize(t) for t in texts]
        clean_texts = [t for t in clean_texts if t]
        if not clean_texts:
            return []

        vectors = self.model.encode(
            clean_texts,
            batch_size=self.batch_size,
            normalize_embeddings=True,
            show_progress_bar=False,
        )
        return vectors.tolist()

    def _get_query_embedding(self, query: str) -> List[float]:
        return self._get_text_embedding(query)

    async def _aget_query_embedding(self, query: str) -> List[float]:
        return self._get_query_embedding(query)

    async def _aget_text_embedding(self, text: str) -> List[float]:
        return self._get_text_embedding(text)

    async def _aget_text_embeddings(self, texts: List[str]) -> List[List[float]]:
        return self._get_text_embeddings(texts)


# ============================================================
# 5. 文档加载与切分
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


def build_text_splitter(settings: Settings) -> SentenceSplitter:
    return SentenceSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
        include_metadata=True,
        include_prev_next_rel=True,
    )


def stable_chunk_id(source_file: str, text: str) -> str:
    raw = f"{source_file}\n{text}".encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def split_documents_to_chunks(
    documents: List[Document],
    splitter: Any,
    settings: Settings
) -> List[Dict[str, Any]]:
    logger.info("开始进行文本切分")
    nodes = splitter.get_nodes_from_documents(documents)

    chunks: List[Dict[str, Any]] = []

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

        chunk_id = stable_chunk_id(source_file, text)

        chunks.append(
            {
                "id": chunk_id,
                "text": text,
                "source": source_file,
                "metadata": metadata,
            }
        )

    logger.info(f"切分完成，有效 chunk 数量: {len(chunks)}")
    if not chunks:
        raise ValueError("切分后没有有效 chunk，请检查文档内容或切分参数")

    return chunks


# ============================================================
# 6. Embedding 维度检测
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
# 7. Milvus 管理
# ============================================================
def build_milvus_client(settings: Settings) -> MilvusClient:
    ensure_milvus_config(settings)
    logger.info(f"连接 Milvus/Zilliz: {settings.milvus_uri}")
    return MilvusClient(
        uri=settings.milvus_uri,
        token=settings.milvus_token,
    )


def prepare_collection(
    milvus_client: MilvusClient,
    settings: Settings,
    embedding_dim: int
) -> None:
    exists = milvus_client.has_collection(settings.collection_name)

    if settings.ingest_mode == "rebuild":
        if exists:
            logger.info(f"INGEST_MODE=rebuild，删除已有集合: {settings.collection_name}")
            milvus_client.drop_collection(settings.collection_name)
        logger.info(f"重建集合: {settings.collection_name}")
        milvus_client.create_collection(
            collection_name=settings.collection_name,
            dimension=embedding_dim,
            metric_type=settings.milvus_metric_type,
        )
        return

    if not exists:
        logger.info(f"集合不存在，自动创建: {settings.collection_name}")
        milvus_client.create_collection(
            collection_name=settings.collection_name,
            dimension=embedding_dim,
            metric_type=settings.milvus_metric_type,
        )
    else:
        logger.info(f"INGEST_MODE=append，复用已有集合: {settings.collection_name}")


def get_existing_ids(
    milvus_client: MilvusClient,
    collection_name: str,
    chunk_ids: List[str],
    batch_size: int = 200
) -> set:
    existing_ids = set()
    for batch in batched(chunk_ids, batch_size):
        expr_ids = ",".join([f'"{cid}"' for cid in batch])
        expr = f"id in [{expr_ids}]"
        try:
            res = milvus_client.query(
                collection_name=collection_name,
                filter=expr,
                output_fields=["id"],
            )
            for item in res:
                if "id" in item:
                    existing_ids.add(item["id"])
        except Exception as e:
            logger.warning(f"查询已存在 chunk id 失败，将继续尝试插入。错误: {e}")
            return set()
    return existing_ids


# ============================================================
# 8. 向量化与入库
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
        batched(chunks, settings.embedding_batch_size),
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

        if batch_idx % 10 == 0 or batch_idx == total_batches:
            logger.info(f"Embedding 进度: {batch_idx}/{total_batches} 批")

    logger.info(f"成功生成并保留的向量记录数: {len(rows)}")
    if not rows:
        raise ValueError("没有任何有效向量可入库")

    return rows


def filter_existing_rows_for_append(
    milvus_client: MilvusClient,
    collection_name: str,
    rows: List[Dict[str, Any]],
    settings: Settings
) -> List[Dict[str, Any]]:
    if settings.ingest_mode != "append" or not settings.skip_existing_in_append:
        return rows

    ids = [row["id"] for row in rows]
    existing_ids = get_existing_ids(milvus_client, collection_name, ids)

    if not existing_ids:
        logger.info("未检测到已存在 chunk，全部准备写入")
        return rows

    filtered = [row for row in rows if row["id"] not in existing_ids]
    logger.info(
        f"append 模式去重完成：原始 {len(rows)} 条，已存在 {len(existing_ids)} 条，待写入 {len(filtered)} 条"
    )
    return filtered


def insert_into_milvus(
    milvus_client: MilvusClient,
    collection_name: str,
    rows: List[Dict[str, Any]]
) -> Any:
    if not rows:
        logger.info("没有需要写入的新记录，跳过插入")
        return {"insert_count": 0}

    logger.info(f"开始写入 Milvus，记录数: {len(rows)}")
    result = milvus_client.insert(
        collection_name=collection_name,
        data=rows,
    )
    logger.info(f"Milvus 插入完成: {result}")
    return result


# ============================================================
# 9. 主流程
# ============================================================
def main() -> None:
    settings = Settings()

    if not settings.job_role:
        raise ValueError("未设置 JOB_ROLE，请先设置环境变量，例如 export JOB_ROLE='java_backend'")

    if not settings.docs_dir:
        settings.docs_dir = f"../knowledge_base/{settings.job_role}/reference_docs/"

    if not settings.collection_name:
        settings.collection_name = f"job_{settings.job_role}"

    ensure_ingest_mode(settings)
    ensure_local_embedding_path(settings)

    logger.info("========== RAG Ingest Start ==========")
    logger.info(f"当前岗位: {settings.job_role}")
    logger.info(f"当前文档目录: {settings.docs_dir}")
    logger.info(f"当前集合名: {settings.collection_name}")
    logger.info(f"当前 ingest 模式: {settings.ingest_mode}")
    logger.info(f"当前本地 embedding 路径: {settings.local_embedding_path}")

    embed_model = LocalSentenceTransformerEmbedding(
        model_path=settings.local_embedding_path,
        max_text_length=settings.max_text_length,
        batch_size=settings.embedding_batch_size,
    )

    documents = load_documents(settings)
    splitter = build_text_splitter(settings)
    chunks = split_documents_to_chunks(documents, splitter, settings)

    embedding_dim = detect_embedding_dim(embed_model)
    milvus_client = build_milvus_client(settings)
    prepare_collection(milvus_client, settings, embedding_dim)

    rows = embed_chunks(chunks, embed_model, settings)
    rows = filter_existing_rows_for_append(
        milvus_client=milvus_client,
        collection_name=settings.collection_name,
        rows=rows,
        settings=settings,
    )

    insert_result = insert_into_milvus(milvus_client, settings.collection_name, rows)

    print("\n================ 入库完成 ================\n")
    print(json.dumps({
        "collection_name": settings.collection_name,
        "ingest_mode": settings.ingest_mode,
        "input_docs_dir": settings.docs_dir,
        "chunk_count": len(chunks),
        "insert_count": insert_result.get("insert_count", 0) if isinstance(insert_result, dict) else str(insert_result),
    }, ensure_ascii=False, indent=2))

    logger.info("========== RAG Ingest Done ==========")


if __name__ == "__main__":
    main()