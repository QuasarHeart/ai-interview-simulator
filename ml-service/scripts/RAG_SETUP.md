# RAG 环境说明

## Python 环境
- conda env: ml-service

## 关键依赖
- pymilvus
- sentence-transformers
- llama-index
- openai
- tqdm
- torch
- transformers

## 本地 embedding 模型
- Qwen/Qwen3-Embedding-0.6B
- 本地缓存路径：
  /mnt/workspace/hf_cache/models--Qwen--Qwen3-Embedding-0.6B/snapshots/c54f2e6e80b2d7b7de06f51cec4959f6b3e03418

## 环境变量
- DASHSCOPE_API_KEY
- MILVUS_URI
- MILVUS_TOKEN
- LOCAL_EMBEDDING_PATH
- JOB_ROLE
- INGEST_MODE
- QUESTION

## 常用命令

### 重建知识库
./run_rag.sh rebuild java_backend

### 增量导入
./run_rag.sh append java_backend

### 查询
./run_rag.sh query java_backend "Spring Boot 自动装配原理是什么？"