#!/usr/bin/env bash
#运行之前先要给执行权限chmod +x run_rag.sh
set -e

ENV_FILE=".env.rag"

if [ ! -f "$ENV_FILE" ]; then
  echo "未找到环境文件: $ENV_FILE"
  echo "请先创建 .env.rag"
  exit 1
fi

source "$ENV_FILE"

ACTION="$1"
JOB_ROLE_ARG="$2"
QUESTION_ARG="$3"

if [ -z "$ACTION" ]; then
  echo "用法:"
  echo "  ./run_rag.sh rebuild <job_role>"
  echo "  ./run_rag.sh append <job_role>"
  echo "  ./run_rag.sh query <job_role> \"你的问题\""
  exit 1
fi

if [ -n "$JOB_ROLE_ARG" ]; then
  export JOB_ROLE="$JOB_ROLE_ARG"
fi

case "$ACTION" in
  rebuild)
    export INGEST_MODE="rebuild"
    echo "========== 开始重建知识库 =========="
    echo "JOB_ROLE=$JOB_ROLE"
    python buildRAG.py
    ;;
  append)
    export INGEST_MODE="append"
    echo "========== 开始增量入库 =========="
    echo "JOB_ROLE=$JOB_ROLE"
    python buildRAG.py
    ;;
  query)
    if [ -z "$QUESTION_ARG" ]; then
      echo "query 模式必须传问题"
      echo "示例: ./run_rag.sh query java_backend \"Spring Boot 自动装配原理是什么？\""
      exit 1
    fi
    export QUESTION="$QUESTION_ARG"
    echo "========== 开始查询 =========="
    echo "JOB_ROLE=$JOB_ROLE"
    echo "QUESTION=$QUESTION"
    python queryRAG.py
    ;;
  *)
    echo "不支持的 ACTION: $ACTION"
    echo "仅支持: rebuild / append / query"
    exit 1
    ;;
esac