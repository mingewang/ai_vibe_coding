from typing import List

import numpy as np
from sentence_transformers import SentenceTransformer

from src.config import config


class EmbeddingModel:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._model = None
        return cls._instance

    @property
    def model(self):
        if self._model is None:
            if config.hf_endpoint:
                import os as _os
                _os.environ["HF_ENDPOINT"] = config.hf_endpoint
            self._model = SentenceTransformer(
                config.embedding_model_name, trust_remote_code=True
            )
        return self._model

    def embed(self, texts: List[str]) -> np.ndarray:
        return self.model.encode(texts, show_progress_bar=False, normalize_embeddings=True)
