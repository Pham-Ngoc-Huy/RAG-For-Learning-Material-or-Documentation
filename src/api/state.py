import os
from dataclasses import dataclass
from pathlib import Path

from src.embeddings import SentenceTransformerEmbedder
from src.llm.llm_client import DeepSeekClient, LocalLLMClient, OpenAIClient
from src.prompts.prompt_templates import RAGPromptTemplate
from src.retrieval.retriever import QdrantRetriever
from src.vectordb.vector_store import QdrantVectorStore


@dataclass
class AppState:
    """Everything a route handler needs, injected instead of read off globals."""

    vector_store: QdrantVectorStore
    embedder: SentenceTransformerEmbedder
    retriever: QdrantRetriever
    prompt_template: RAGPromptTemplate
    llm: DeepSeekClient | OpenAIClient | LocalLLMClient
    upload_dir: Path
    md_store_dir: Path


def build_llm() -> DeepSeekClient | OpenAIClient | LocalLLMClient:
    """Pick an LLM backend the same way the original startup hook did."""
    if os.getenv("DEEPSEEK_API_KEY"):
        return DeepSeekClient()
    if os.getenv("OPENAI_API_KEY"):
        return OpenAIClient()
    return LocalLLMClient()