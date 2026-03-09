from sentence_transformers import SentenceTransformer
import torch

local_path = "/mnt/workspace/hf_cache/models--Qwen--Qwen3-Embedding-0.6B/snapshots/c54f2e6e80b2d7b7de06f51cec4959f6b3e03418"

print("CUDA available:", torch.cuda.is_available())
print("Loading from local path:", local_path)

model = SentenceTransformer(local_path, device="cuda")

texts = [
    "Golang 中 channel 的底层实现原理是什么？",
    "MySQL 索引为什么能够提高查询效率？",
    "Redis 为什么适合做缓存？"
]

embeddings = model.encode(
    texts,
    batch_size=8,
    show_progress_bar=True,
    normalize_embeddings=True
)

print("Embedding shape:", embeddings.shape)
print("Done.")