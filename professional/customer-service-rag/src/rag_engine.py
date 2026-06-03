from typing import List, Dict

from openai import OpenAI

from src.config import config
from src.vector_store import VectorStore


SYSTEM_PROMPT = """You are a helpful customer service assistant. Answer the user's question based on the provided context from the company's website. If the context doesn't contain enough information, say so honestly. Always cite the source URL when you use specific information from the context.

Context:
{context}"""


def format_context(results: List[Dict]) -> str:
    parts = []
    for i, r in enumerate(results, 1):
        parts.append(f"[Source {i}] URL: {r['url']}\n{r['text']}\n")
    return "\n---\n".join(parts)


class RAGEngine:
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store
        self.client = OpenAI(
            api_key=config.llm_api_key,
            base_url=config.llm_base_url,
        )

    def query(self, question: str, top_k: int = None) -> Dict:
        if top_k is None:
            top_k = config.top_k

        results = self.vector_store.search(question, top_k)
        context = format_context(results)

        response = self.client.chat.completions.create(
            model=config.llm_model,
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT.format(context=context),
                },
                {"role": "user", "content": question},
            ],
            temperature=0.3,
            max_tokens=1024,
        )

        answer = response.choices[0].message.content

        sources = [
            {"url": r["url"], "score": r["score"]}
            for r in results
        ]

        return {"answer": answer, "sources": sources}
