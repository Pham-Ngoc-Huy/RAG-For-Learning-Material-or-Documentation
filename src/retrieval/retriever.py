from abc import ABC, abstractmethod
from typing import Optional
from qdrant_client.models import Filter
from src.embeddings.embedder import BaseEmbedder
from src.vectordb.vector_store import BaseVectorStore


class BaseRetriever(ABC):
    def __init__(
        self,
        vector_store: BaseVectorStore,
        embedder: BaseEmbedder,
    ):
        """
        @brief Initialize the retriever with a vector store and embedder.
        @param vector_store: tenant-aware vector store implementation
        @param embedder: embedder for query vectors
        @objective Create a retrieval layer that can query stored documents.
        @update date 2026-08-04
        @commented by Huy Pham
        """
        self.vector_store = vector_store
        self.embedder = embedder

    @abstractmethod
    def retrieve(
        self,
        user_id: str,
        query: str,
        top_k: int = 5,
        metadata_filter: Optional[Filter] = None,
        collection_name: Optional[str] = None,
    ) -> list[dict]:
        """
        @brief Retrieve relevant chunks for a user query.
        @param user_id: tenant identifier used for isolation
        @param query: user query string to embed and search
        @param top_k: number of top documents to return
        @param metadata_filter: optional additional metadata filter
        @param collection_name: optional alternate collection name suffix
        @objective Search tenant-specific vectors matching the query.
        @update date 2026-08-04
        @commented by Huy Pham
        """
        pass


class QdrantRetriever(BaseRetriever):
    def retrieve(
        self,
        user_id: str,
        query: str,
        top_k: int = 5,
        metadata_filter: Optional[Filter] = None,
        collection_name: Optional[str] = None,
    ) -> list[dict]:
        """
        @brief Retrieve nearest document chunks for a query using Qdrant.
        @param user_id: tenant identifier used for isolation
        @param query: user query string to embed and search
        @param top_k: number of top vectors to return
        @param metadata_filter: optional additional metadata filter
        @param collection_name: optional alternate collection suffix
        @objective Query the vector store through a tenant-safe retriever API.
        @update date 2026-08-04
        @commented by Huy Pham
        """
        if not query:
            return []

        query_vector = self.embedder.embed_query(query)
        return self.vector_store.search(
            user_id=user_id,
            query_vector=query_vector,
            top_k=top_k,
            collection_name=collection_name,
            metadata_filter=metadata_filter,
            with_payload=True,
        )
