from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
import numpy as np


def diversity_based_selection(
        samples: list[dict],
        target_size: int = 5000,
        n_clusters: int = 500,
) -> list[dict]:
    """
    基于多样性的数据筛选：
    1. 将所有样本编码为向量
    2. 聚类后从每个簇中选择最优样本
    3. 确保最终数据集覆盖尽可能多的"语义区域"
    """
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # 提取每条样本的指令文本
    instructions = [
        next(m["content"] for m in s["conversations"] if m["role"] == "user")
        for s in samples
    ]

    # 编码为向量
    embeddings = model.encode(instructions, show_progress_bar=True)

    # K-Means 聚类
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    labels = kmeans.fit_predict(embeddings)

    # 从每个簇中选择距离簇心最近的 top-k 样本
    per_cluster = target_size // n_clusters
    selected = []

    for cluster_id in range(n_clusters):
        cluster_indices = np.where(labels == cluster_id)[0]
        center = kmeans.cluster_centers_[cluster_id]

        # 按距离簇心从近到远排序
        distances = np.linalg.norm(
            embeddings[cluster_indices] - center, axis=1
        )
        sorted_idx = cluster_indices[np.argsort(distances)]

        # 选取 top-k
        selected.extend(sorted_idx[:per_cluster].tolist())

    return [samples[i] for i in selected[:target_size]]
