import os
import uuid
from abc import ABC, abstractmethod
from typing import Optional

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue,
)


class BaseVectorStore(ABC):
    @abstractmethod
    def create_collection(
        self,
        user_id: str,
        vector_size: int,
        distance: Distance = Distance.COSINE,
        collection_name: Optional[str] = None,
    ) -> str:
        """
        @brief Create a tenant-scoped vector collection if it does not exist.
        @param user_id: tenant identifier for multi-tenant isolation
        @param vector_size: size of each vector in the collection
        @param distance: qdrant distance metric for similarity search
        @param collection_name: optional custom collection suffix
        @objective Ensure each tenant has an isolated collection in Qdrant.
        @update date 2026-08-03
        @commented by Huy Pham
        """
        pass

    @abstractmethod
    def upsert(
        self,
        user_id: str,
        chunks: list[dict],
        collection_name: Optional[str] = None,
    ) -> list[str]:
        """
        @brief Insert or update document vectors into the vector store.
        @param user_id: tenant identifier for multi-tenant isolation
        @param chunks: list of chunk dictionaries containing text, metadata, and vector
        @param collection_name: optional custom collection suffix
        @objective Persist embedded chunks with the tenant payload enforced.
        @update date 2026-08-03
        @commented by Huy Pham
        """
        pass

    @abstractmethod
    def search(
        self,
        user_id: str,
        query_vector: list[float],
        top_k: int = 5,
        collection_name: Optional[str] = None,
        metadata_filter: Optional[Filter] = None,
        with_payload: bool = True,
    ) -> list[dict]:
        """
        @brief Search for nearest vectors within a tenant collection.
        @param user_id: tenant identifier for multi-tenant isolation
        @param query_vector: query embedding vector
        @param top_k: number of nearest neighbors to return
        @param collection_name: optional custom collection suffix
        @param metadata_filter: additional payload-based filter to apply
        @param with_payload: whether to return stored metadata payload
        @objective Return tenant-specific similarity results without cross-tenant access.
        @update date 2026-08-03
        @commented by Huy Pham
        """
        pass

    @abstractmethod
    def delete_user_data(
        self,
        user_id: str,
        collection_name: Optional[str] = None,
    ) -> None:
        """
        @brief Delete all vectors belonging to one tenant in a collection.
        @param user_id: tenant identifier for multi-tenant isolation
        @param collection_name: optional custom collection suffix
        @objective Remove tenant data without affecting other tenants.
        @update date 2026-08-03
        @commented by Huy Pham
        """
        pass

    @abstractmethod
    def delete_collection(
        self,
        user_id: str,
        collection_name: Optional[str] = None,
    ) -> None:
        """
        @brief Remove a tenant-specific Qdrant collection entirely.
        @param user_id: tenant identifier for multi-tenant isolation
        @param collection_name: optional custom collection suffix
        @objective Delete the tenant collection safely.
        @update date 2026-08-03
        @commented by Huy Pham
        """
        pass


class QdrantVectorStore(BaseVectorStore):
    DEFAULT_COLLECTION = "documents"

    def __init__(
        self,
        host: str = "localhost",
        port: int = 5000,
        api_key: Optional[str] = None,
        url: Optional[str] = None,
        prefer_grpc: bool = False,
    ):
        """
        @brief Initialize a Qdrant-backed vector store client.
        @param host: Qdrant host when URL is not provided
        @param port: Qdrant port when URL is not provided
        @param api_key: optional Qdrant API key
        @param url: optional full Qdrant URL, overrides host/port
        @param prefer_grpc: whether to use the Qdrant gRPC transport
        @objective Create a tenant-aware vector store connection.
        @update date 2026-08-03
        @commented by Huy Pham
        """
        target_url = url or os.getenv("QDRANT_URL") or f"http://{host}:{port}"
        resolved_api_key = api_key or os.getenv("QDRANT_API_KEY")
        self.client = QdrantClient(url=target_url, api_key=resolved_api_key, prefer_grpc=prefer_grpc)

    def _collection_name(self, user_id: str, collection_name: Optional[str] = None) -> str:
        """
        @brief Compute a tenant-isolated collection name.
        @param user_id: tenant identifier
        @param collection_name: optional suffix for the collection
        @objective Keep tenant collections separate by naming convention.
        @update date 2026-08-03
        @commented by Huy Pham
        """
        if not user_id or not str(user_id).strip():
            raise ValueError("user_id must be provided")

        safe_user_id = str(user_id).strip().replace(" ", "_")
        suffix = collection_name or self.DEFAULT_COLLECTION
        return f"user_{safe_user_id}_{suffix}"

    def _build_user_filter(
        self,
        user_id: str,
        metadata_filter: Optional[Filter] = None,
    ) -> Filter:
        """
        @brief Build a Qdrant filter enforcing tenant isolation.
        @param user_id: tenant identifier
        @param metadata_filter: optional additional filter
        @objective Always scope search and delete operations by tenant.
        @update date 2026-08-03
        @commented by Huy Pham
        """
        conditions = [FieldCondition(key="user_id", match=MatchValue(value=user_id))]

        if metadata_filter is None:
            return Filter(must=conditions)

        must_conditions = []
        if metadata_filter.must:
            must_conditions.extend(metadata_filter.must)
        if metadata_filter.should:
            return Filter(
                must=conditions + must_conditions,
                should=metadata_filter.should,
                must_not=metadata_filter.must_not,
            )

        return Filter(
            must=conditions + must_conditions,
            must_not=metadata_filter.must_not,
        )

    def create_collection(
        self,
        user_id: str,
        vector_size: int,
        distance: Distance = Distance.COSINE,
        collection_name: Optional[str] = None,
    ) -> str:
        collection = self._collection_name(user_id, collection_name)
        vectors_config = VectorParams(size=vector_size, distance=distance)
        try:
            self.client.get_collection(collection_name=collection)
            return collection
        except Exception:
            self.client.create_collection(collection_name=collection, vectors_config=vectors_config)
            return collection

    def upsert(
        self,
        user_id: str,
        chunks: list[dict],
        collection_name: Optional[str] = None,
    ) -> list[str]:
        if not chunks:
            return []

        collection = self._collection_name(user_id, collection_name)
        try:
            self.client.get_collection(collection_name=collection)
        except Exception:
            self.create_collection(user_id=user_id, vector_size=len(chunks[0]["vector"]), collection_name=collection_name)

        points = []
        for chunk in chunks:
            if "vector" not in chunk:
                raise ValueError("Each chunk must include a 'vector' field")

            point_id = chunk.get("id") or uuid.uuid4().hex
            payload = {"text": chunk.get("text", ""), **chunk.get("metadata", {})}
            payload["user_id"] = user_id

            points.append(
                PointStruct(
                    id=point_id,
                    vector=chunk["vector"],
                    payload=payload,
                )
            )

        self.client.upsert(collection_name=collection, points=points)
        return [point.id for point in points]

    def search(
        self,
        user_id: str,
        query_vector: list[float],
        top_k: int = 5,
        collection_name: Optional[str] = None,
        metadata_filter: Optional[Filter] = None,
        with_payload: bool = True,
    ) -> list[dict]:
        collection = self._collection_name(user_id, collection_name)
        query_filter = self._build_user_filter(user_id=user_id, metadata_filter=metadata_filter)

        results = self.client.search(
            collection_name=collection,
            query_vector=query_vector,
            limit=top_k,
            query_filter=query_filter,
            with_payload=with_payload,
        )

        return [
            {
                "id": getattr(hit, "id", None),
                "score": getattr(hit, "score", None),
                "payload": getattr(hit, "payload", None),
            }
            for hit in results
        ]

    def delete_user_data(
        self,
        user_id: str,
        collection_name: Optional[str] = None,
    ) -> None:
        collection = self._collection_name(user_id, collection_name)
        query_filter = self._build_user_filter(user_id=user_id)
        self.client.delete(collection_name=collection, filter=query_filter)

    def delete_collection(
        self,
        user_id: str,
        collection_name: Optional[str] = None,
    ) -> None:
        collection = self._collection_name(user_id, collection_name)
        self.client.delete_collection(collection_name=collection)
    