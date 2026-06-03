import os
import sys

import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.crawler import crawl_site
from src.vector_store import VectorStore
from src.rag_engine import RAGEngine

st.set_page_config(page_title="Customer Service RAG Chatbot", layout="wide")

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
INDEX_PATH = os.path.join(DATA_DIR, "vector_store.faiss")


def init_vector_store() -> VectorStore:
    vs = VectorStore()
    if os.path.exists(INDEX_PATH):
        vs.load(INDEX_PATH)
    return vs


def build_index(urls: list):
    all_pages = []
    progress = st.progress(0, text="Starting crawl...")
    for i, url in enumerate(urls):
        st.info(f"Crawling {url} ...")
        pages = crawl_site(url)
        all_pages.extend(pages)
        progress.progress((i + 1) / len(urls), text=f"Crawled {len(all_pages)} pages")

    if not all_pages:
        st.error("No content found from the provided URLs.")
        return

    vs = VectorStore()
    progress.progress(0.9, text="Building embeddings...")
    vs.build_from_pages(all_pages)
    vs.save(INDEX_PATH)
    st.session_state["vector_store"] = vs
    progress.progress(1.0, text="Done!")
    st.success(f"Indexed {len(all_pages)} pages from {len(urls)} site(s).")


if "vector_store" not in st.session_state:
    st.session_state["vector_store"] = init_vector_store()
if "rag_engine" not in st.session_state:
    if st.session_state["vector_store"].index is not None:
        st.session_state["rag_engine"] = RAGEngine(st.session_state["vector_store"])
    else:
        st.session_state["rag_engine"] = None
if "messages" not in st.session_state:
    st.session_state["messages"] = []

st.title(" Customer Service RAG Chatbot")

with st.sidebar:
    st.header("Configuration")

    st.subheader("1. Index URLs")
    urls_input = st.text_area(
        "Enter URLs (one per line)",
        "https://www.comrite.com/",
        height=120,
    )

    if st.button("Build / Rebuild Index", type="primary", use_container_width=True):
        urls = [u.strip() for u in urls_input.splitlines() if u.strip()]
        if urls:
            with st.spinner("Crawling & indexing..."):
                build_index(urls)
            st.session_state["rag_engine"] = RAGEngine(
                st.session_state["vector_store"]
            )
            st.rerun()
        else:
            st.warning("Please enter at least one URL.")

    if st.session_state["vector_store"].index is not None:
        st.success(
            f"Index ready: {st.session_state['vector_store'].index.ntotal} vectors"
        )
    else:
        st.warning("No index found. Add URLs and click 'Build Index'.")

    st.divider()
    if st.button("Clear Chat", use_container_width=True):
        st.session_state["messages"] = []
        st.rerun()

st.divider()

for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "sources" in msg and msg["sources"]:
            with st.expander("Sources"):
                for s in msg["sources"]:
                    st.write(f"- [{s['url']}]({s['url']}) (score: {s['score']:.3f})")

if prompt := st.chat_input("Ask a question about the company..."):
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    if st.session_state["rag_engine"] is None:
        response = "I'm sorry, the knowledge base hasn't been built yet. Please add URLs and click 'Build Index' first."
        st.session_state["messages"].append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)
    else:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                result = st.session_state["rag_engine"].query(prompt)
            st.markdown(result["answer"])
            if result["sources"]:
                with st.expander("Sources"):
                    for s in result["sources"]:
                        st.write(
                            f"- [{s['url']}]({s['url']}) (score: {s['score']:.3f})"
                        )
        st.session_state["messages"].append(
            {
                "role": "assistant",
                "content": result["answer"],
                "sources": result["sources"],
            }
        )
