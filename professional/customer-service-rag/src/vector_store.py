import json
import os
from typing import List, Dict, Optional

import faiss
import numpy as np

from src.config import config
from src.embeddings import EmbeddingModel


def chunk_text(text: str, chunk_size: int = None, overlap: int = None) -> List[str]:
    if chunk_size is None:
        chunk_size = config.chunk_size
    if overlap is None:
        overlap = config.chunk_overlap

    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunks.append(" ".join(words[start:end]))
        if end >= len(words):
            break
        start += chunk_size - overlap
    return chunks


class VectorStore:
    def __init__(self):
        self.embedder = EmbeddingModel()
        self.index: Optional[faiss.Index] = None
        self.metadata: List[Dict] = []
        self.dimension: int = 0

    def build_from_pages(
        self, pages: List[Dict[str, str]]
    ) -> None:
        chunks = []
        metadata = []
        for page in pages:
            page_chunks = chunk_text(page["text"])
            for c in page_chunks:
                chunks.append(c)
                metadata.append({"url": page["url"], "text": c})

        if not chunks:
            print("  No content to index.")
            return

        print(f"  Embedding {len(chunks)} chunks...")
        embeddings = self.embedder.embed(chunks)
        self.dimension = embeddings.shape[1]

        self.index = faiss.IndexFlatIP(self.dimension)
        self.index.add(embeddings)
        self.metadata = metadata
        print(f"  Index built: {self.index.ntotal} vectors")

    def search(
        self, query: str, top_k: int = None
    ) -> List[Dict]:
        if top_k is None:
            top_k = config.top_k
        if self.index is None or self.index.ntotal == 0:
            return []

        query_vec = self.embedder.embed([query])
        scores, indices = self.index.search(query_vec, min(top_k, self.index.ntotal))

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < 0:
                continue
            results.append(
                {
                    "url": self.metadata[idx]["url"],
                    "text": self.metadata[idx]["text"],
                    "score": float(score),
                }
            )
        return results

    def save(self, path: str = None) -> None:
        if path is None:
            path = config.vector_store_path
        os.makedirs(os.path.dirname(path), exist_ok=True)

        faiss.write_index(self.index, path)
        meta_path = path + ".meta.json"
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(self.metadata, f, ensure_ascii=False)
        print(f"  Saved index to {path}")

    def load(self, path: str = None) -> bool:
        if path is None:
            path = config.vector_store_path
        meta_path = path + ".meta.json"

        if not os.path.exists(path) or not os.path.exists(meta_path):
            return False

        self.index = faiss.read_index(path)
        with open(meta_path, "r", encoding="utf-8") as f:
            self.metadata = json.load(f)
        self.dimension = self.index.d
        print(f"  Loaded index: {self.index.ntotal} vectors")
        return True
