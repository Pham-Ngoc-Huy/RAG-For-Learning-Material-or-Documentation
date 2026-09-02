import os
from abc import ABC, abstractmethod

from dotenv import load_dotenv

from config.config_loader import OmegaConfigLoader
from src.embeddings import FastEmbedder, ModelEmbedder
from src.llm import ThinkingFromKnowledgeBase
from src.prompts import PromptAssistance
from src.retrieval import QdrantRetriever
from src.vectordb import QdrantVectorStore


class ConstructorLoops(ABC):
    def __init__(self, config, user_id, user_name, model):
        self.config = config
        self.user_id = user_id
        self.user_name = user_name
        self.model = model
        self.vectordb = "qdrant"

        self.api_key_vectordb = self.config["vectordb"][self.vectordb]["api_key"]
        self.base_url_vectordb = self.config["vectordb"][self.vectordb]["endpoint"]

        self.base_url_embedded = self.config["models"][self.model]["embedded"]["base_url"]
        self.model_embedded = self.config["models"][self.model]["embedded"]["model"]
        self.api_key_embedded = self.config["models"][self.model]["embedded"]["api_key"]

        self.model_llm_client = self.config["models"][self.model]["llm_client"]["model"]
        self.base_url_llm_client = self.config["models"][self.model]["llm_client"]["base_url"]
        self.api_key_llm_client = self.config["models"][self.model]["llm_client"]["api_key"]

        self.embedded = self._build_embedder()

        self.dimensions = self.embedded.get_vectorspace_dimensions

        self.prompt_template = PromptAssistance()

        self.vector_store = QdrantVectorStore(api_key=self.api_key_vectordb, endpoint=self.base_url_vectordb)

        self.retriever = QdrantRetriever(vector_store=self.vector_store, embedder=self.embedded)

        self.llm_client = ThinkingFromKnowledgeBase(
            api_key=self.api_key_llm_client,
            base_url=self.base_url_llm_client,
            model=self.model_llm_client,
            provider=self.model,
        )

    def _build_embedder(self):
        # "local" providers (e.g. sentence-transformers) don't need an API key.
        if self.base_url_embedded == "local":
            return ModelEmbedder(
                model=self.model_embedded,
                base_url=self.base_url_embedded,
                api_key=self.api_key_embedded,
            )

        if not self.api_key_embedded:
            return FastEmbedder()

        return ModelEmbedder(
            model=self.model_embedded,
            base_url=self.base_url_embedded,
            api_key=self.api_key_embedded,
        )

    @abstractmethod
    def query(self, collection_name: str, text: str):
        pass


class AskAndAnswer(ConstructorLoops):
    def query(self, text: str, collection_name: str, top_k: int = 5):
        retrieved_chunks = self.retriever.retrieve(
            user_id=self.user_id,
            collection_name=collection_name,
            query=text,
            top_k=top_k,
        )

        if isinstance(retrieved_chunks, list) and len(retrieved_chunks) > 0 and isinstance(retrieved_chunks[0], dict):
            context_str = "\n---\n".join([chunk.get("payload", {}).get("text", "") for chunk in retrieved_chunks])
        else:
            context_str = str(retrieved_chunks)

        messages = self.prompt_template.build(template_name="rag_assistance", context=context_str, query=text)
        response = self.llm_client.generate(messages=messages, temperature=1.0)
        return response


class QdrantCollection(ConstructorLoops):
    def query(self, text: str, collection_name: str) -> None:
        pass

    def create(self, collection_name):
        return self.vector_store.create_collection(
            user_id=self.user_id,
            vector_size=self.dimensions,
            collection_name=collection_name,
        )

    def delete(self, collection_name: str):
        return self.vector_store.delete_collection(user_id=self.user_id, collection_name=collection_name)

    def upsert(self, collection_name: str, chunks: dict):
        return self.vector_store.upsert(user_id=self.user_id, collection_name=collection_name, chunks=chunks)


class Embedded(ConstructorLoops):
    def query(self, text: str, collection_name: str) -> None:
        pass

    def embed_many(self, chunks: list[dict]) -> list[dict]:
        return self.embedded.embed_many(chunks=chunks)

    def embed_query(self, query: str) -> list[float]:
        return self.embedded.embed_query(query=query)


def main():
    load_dotenv(dotenv_path=".env.example")
    model_chosen = os.getenv("MODEL_CHOSEN", "openrouter")

    # load config
    config = OmegaConfigLoader(config_path="config/config.yml").load(
        vectordb={
            "qdrant": {
                "endpoint": os.getenv("QDRANT_ENDPOINT"),
                "api_key": os.getenv("QDRANT_API_KEY"),
            }
        },
        models={
            model_chosen: {
                "embedded": {
                    "base_url": os.getenv("EMBEDDED_BASE_URL"),
                    "model": os.getenv("EMBEDDED_MODEL"),
                    "api_key": os.getenv("EMBEDDED_API_KEY"),
                },
                "llm_client": {
                    "temperature": 0.7,
                    "api_key": os.getenv(f"{model_chosen.upper()}_API_KEY"),
                },
            }
        },
    )

    user_id = "huypham"
    collection_name = "AI"
    user_name = "user_default_user_documents"
    question = "what is disturbance observer ?"

    # file_path = "temp/Tutorial_NDO.md"

    # # # Create Collection
    # qdrant_collection = QdrantCollection(config=config, user_id=user_id, user_name=user_name, model=model_chosen)

    # qdrant_collection.delete(collection_name=collection_name)
    # qdrant_collection.create(collection_name=collection_name)

    # # Chunks
    # doc_result = FileLoader(file_path=file_path).load()
    # chunks = MarkDownChunker().chunk(doc=doc_result)

    # # Embedded
    # embedder = Embedded(config=config, user_id=user_id, user_name=user_name, model=model_chosen)
    # chunks = embedder.embed_many(chunks=chunks)
    # qdrant_collection.upsert(collection_name=collection_name, chunks=chunks)

    rag_pipeline = AskAndAnswer(config=config, user_id=user_id, user_name=user_name, model=model_chosen)
    response = rag_pipeline.query(text=question, collection_name=collection_name)

    print("Response: \n")
    print(response.text)


if __name__ == "__main__":
    main()
