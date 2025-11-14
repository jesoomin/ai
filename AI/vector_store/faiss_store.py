import os
import faiss
import pickle
from typing import List, Dict, Any
from app_config import Config
from agents.embeddings_provider import get_embedding
import numpy as np


class FaissStore:
    def __init__(self, dim=384, path=None):
        self.dim = dim
        self.path = path or Config.VECTOR_STORE_DIR
        os.makedirs(self.path, exist_ok=True)
        self.index_file = os.path.join(self.path, "faiss.index")
        self.meta_file = os.path.join(self.path, "meta.pkl")

        if os.path.exists(self.index_file) and os.path.exists(self.meta_file):
            self.index = faiss.read_index(self.index_file)
            with open(self.meta_file, "rb") as f:
                self.meta = pickle.load(f)
        else:
            self.index = faiss.IndexFlatL2(self.dim)
            self.meta = []

    def add(self, id: str, text: str, metadata: Dict[str, Any] = None):
        emb = get_embedding(text)
        if len(emb) != self.dim:
            raise ValueError(f"Embedding dim {len(emb)} does not match index dim {self.dim}")
        vec = np.array([emb], dtype="float32")
        self.index.add(vec)
        self.meta.append({"id": id, "text": text, "metadata": metadata or {}})
        self._save()

    def search(self, query: str, top_k=5):
        if self.index.ntotal == 0:
            return []  # 인덱스가 비어있으면 빈 리스트 반환

        q_emb = get_embedding(query)
        if len(q_emb) != self.dim:
            raise ValueError(f"Query embedding dim {len(q_emb)} does not match index dim {self.dim}")
        q = np.array([q_emb], dtype="float32")
        D, I = self.index.search(q, top_k)
        results = []
        for score, idx in zip(D[0], I[0]):
            if idx < len(self.meta):
                m = self.meta[idx]
                results.append({
                    "id": m["id"],
                    "text": m["text"],
                    "metadata": m.get("metadata", {}),
                    "score": float(score)
                })
        return results

    def _save(self):
        faiss.write_index(self.index, self.index_file)
        with open(self.meta_file, "wb") as f:
            pickle.dump(self.meta, f)
