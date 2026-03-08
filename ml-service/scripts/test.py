from sentence_transformers import SentenceTransformer

model_name = "jinaai/jina-embeddings-v5-text-small"
model = SentenceTransformer(model_name,trust_remote_code=True)

texts = [
    "Java语言的优点是什么？",
    "Go语言的并发模型有什么特点？"
]

embeddings = model.encode(texts, normalize_embeddings=True,task='retrieval')

print("模型加载成功:", model_name)
print("向量数量:", len(embeddings))
print("向量维度:", len(embeddings[0]))