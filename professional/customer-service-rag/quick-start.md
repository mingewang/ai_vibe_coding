# Customer Service RAG Chatbot — Quick Start

## Project Structure

```
professional/customer-service-rag/
├── app.py                  # Streamlit chatbot UI (main entry)
├── requirements.txt        # Python dependencies
├── setup.bat               # One-click setup script (Windows)
├── .env.example            # API key config template
├── .gitignore
└── src/
    ├── config.py           # Central configuration from .env
    ├── crawler.py          # Web crawler (requests + BeautifulSoup)
    ├── embeddings.py       # Sentence-transformers embedding (local)
    ├── vector_store.py     # FAISS vector index + chunking + persist
    └── rag_engine.py       # RAG query → LLM (OpenAI/DeepSeek)
```

## How to Use

### 1. Setup

Run the setup script (creates venv, installs deps, copies `.env`):

```
setup.bat
```

Or manually:

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

### 2. Configure API keys

Edit `.env` — set your `OPENAI_API_KEY` (or switch to DeepSeek by setting `LLM_PROVIDER=deepseek` and providing `DEEPSEEK_API_KEY`).

### 3. Run the chatbot

```
streamlit run app.py
```

### 4. Use the app

1. In the sidebar, enter the URLs you want to index (one per line, `https://www.comrite.com/` is pre-filled).
2. Click **Build / Rebuild Index** to crawl the sites, generate embeddings, and build a FAISS vector index.
3. Ask questions in the chat input — the bot retrieves relevant chunks and answers via the configured LLM (OpenAI or DeepSeek).

## Notes

- **Embeddings** use `BAAI/bge-small-zh-v1.5` via `sentence-transformers` — runs locally, no API key needed.
- **Vector store** persists to `data/vector_store.faiss` so you only need to crawl once.
- The default embedding model is optimized for Chinese + English text.
- **For users in China:** Set `HF_ENDPOINT=https://hf-mirror.com` in `.env` to download embedding models from the HuggingFace mirror.
