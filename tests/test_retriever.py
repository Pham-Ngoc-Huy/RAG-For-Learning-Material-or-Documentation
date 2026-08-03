from types import SimpleNamespace

from qdrant_client.models import Filter, FieldCondition, MatchValue

from src.retrieval import QdrantRetriever


class DummyEmbedder:
    def embed_query(self, query):
        return [0.5, 0.5, 0.5]


class DummyVectorStore:
    def __init__(self):
        self.search_calls = []

    def search(
        self,
        user_id,
        query_vector,
        top_k,
        collection_name,
        metadata_filter,
        with_payload,
    ):
        self.search_calls.append(
            {
                "user_id": user_id,
                "collection_name": collection_name,
                "query_vector": query_vector,
                "limit": top_k,
                "query_filter": metadata_filter,
                "with_payload": with_payload,
            }
        )
        return [
            {
                "id": "doc-1",
                "score": 0.98,
                "payload": {"text": "hello world", "source": "doc.txt"},
            }
        ]


def test_qdrant_retriever_returns_results():
    vector_store = DummyVectorStore()
    embedder = DummyEmbedder()
    retriever = QdrantRetriever(vector_store=vector_store, embedder=embedder)

    results = retriever.retrieve(user_id="user1", query="find me docs", top_k=3)

    assert len(results) == 1
    assert results[0]["id"] == "doc-1"
    assert vector_store.search_calls[0]["user_id"] == "user1"
    assert vector_store.search_calls[0]["limit"] == 3
    assert vector_store.search_calls[0]["with_payload"] is True


def test_qdrant_retriever_applies_metadata_filter():
    vector_store = DummyVectorStore()
    embedder = DummyEmbedder()
    retriever = QdrantRetriever(vector_store=vector_store, embedder=embedder)

    filter = Filter(must=[FieldCondition(key="source", match=MatchValue(value="doc.txt"))])
    retriever.retrieve(user_id="user2", query="find text", metadata_filter=filter)

    assert vector_store.search_calls[0]["user_id"] == "user2"
    assert vector_store.search_calls[0]["query_filter"] is filter
