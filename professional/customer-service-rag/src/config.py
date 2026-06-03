import os
from dotenv import load_dotenv

load_dotenv(".env.local")


class Config:
    # LLM
    llm_provider: str = os.getenv("LLM_PROVIDER", "openai")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_base_url: str = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    deepseek_api_key: str = os.getenv("DEEPSEEK_API_KEY", "")
    deepseek_base_url: str = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
    deepseek_model: str = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")

    # Embedding
    hf_endpoint: str = os.getenv("HF_ENDPOINT", "")
    embedding_model_name: str = os.getenv(
        "EMBEDDING_MODEL_NAME", "BAAI/bge-small-zh-v1.5"
    )

    # Crawler
    crawler_max_depth: int = int(os.getenv("CRAWLER_MAX_DEPTH", "2"))
    crawler_max_pages: int = int(os.getenv("CRAWLER_MAX_PAGES", "50"))
    crawler_delay: float = float(os.getenv("CRAWLER_DELAY", "1.0"))

    # Vector store
    vector_store_path: str = os.getenv(
        "VECTOR_STORE_PATH", "./data/vector_store.faiss"
    )
    chunk_size: int = int(os.getenv("CHUNK_SIZE", "500"))
    chunk_overlap: int = int(os.getenv("CHUNK_OVERLAP", "50"))

    # RAG
    top_k: int = int(os.getenv("TOP_K", "5"))

    @property
    def llm_api_key(self) -> str:
        if self.llm_provider == "deepseek":
            return self.deepseek_api_key
        return self.openai_api_key

    @property
    def llm_base_url(self) -> str:
        if self.llm_provider == "deepseek":
            return self.deepseek_base_url
        return self.openai_base_url

    @property
    def llm_model(self) -> str:
        if self.llm_provider == "deepseek":
            return self.deepseek_model
        return self.openai_model


config = Config()
