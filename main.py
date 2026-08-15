import os
import json
from config.config_loader import OmegaConfigLoader
from src.vectordb.vector_store import QdrantVectorStore
from src.retrieval.retriever import QdrantRetriever
from src.ingestion import FileLoader
from src.chunking import MarkDownChunker
from src.embeddings import SentenceTransformerEmbedder
from src.prompts.prompt_templates import RAGPromptTemplate
from src.llm.llm_client import LocalLLMClient, OpenAIClient, DeepSeekClient
from abc import ABC, abstractmethod
# Input Era:

model_chosen=input()
class ConstructorLoops(ABC):
    def __init__(
        self,
        config,
        user_id
    ):
        self.config=config
        self.user_id=user_id
        self.embedded=None
        self.vector_store=None
    @abstractmethod
    def query(self, text:str):
        pass 

class AskAndAnswer(ConstructorLoops):
    def query(self, text)


# load config
config = OmegaConfigLoader(
    config_path="config/config.yml",
    vectordb={
        "qdrant.endpoint": os.getenv("QDRANT_ENDPOINT"),
        "qdrant.api_key": os.getenv("QDRANT_API_KEY")
    },
    models={
        f"{model_chosen}.api_key": os.getenv(f"{model_chosen.upper()}_API_KEY")
        f"{model_chosen}.llm_client.max_tokens": 500
        f"{model_chosen}.llm_client.temperature": 0.7
    }
)

vector_store = QdrantVectorStore(
    api_key=config["vectordb"][vectordb]["api_key"],
    endpoint=config["vectordb"][vectordb]["endpoint"]
)

embedder = E

collection_name=vector_store.create_collection(
    user_id=user_id,
    vector_size=dimension
)

retriever = QdrantRetriever(
    vector_store=vector_store,
    embedder=ee
)

