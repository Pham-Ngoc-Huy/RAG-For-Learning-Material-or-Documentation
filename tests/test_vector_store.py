from types import SimpleNamespace

from src.vectordb.vector_store import Distance, QdrantVectorStore


class DummyQdrantClient:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.created_collections = []
        self.upserted_points = []
        self.searched = []
        self.deleted = []
        self.existing_collections = set()

    def get_collection(self, collection_name):
        if collection_name not in self.existing_collections:
            raise ValueError("Collection not found")
        return SimpleNamespace(name=collection_name)

    def create_collection(self, collection_name, vectors_config):
        self.created_collections.append((collection_name, vectors_config))
        self.existing_collections.add(collection_name)

    def upsert(self, collection_name, points):
        self.upserted_points.append((collection_name, points))

    def search(self, collection_name, query_vector, limit, query_filter, with_payload):
        self.searched.append((collection_name, query_vector, limit, query_filter, with_payload))
        return [SimpleNamespace(id="point-123", score=0.95, payload={"text": "hello"})]

    def delete(self, collection_name, filter):
        self.deleted.append((collection_name, filter))


def test_qdrant_vector_store_uses_env_url_and_api_key(monkeypatch):
    monkeypatch.setenv("QDRANT_URL", "http://localhost:6333")
    monkeypatch.setenv("QDRANT_API_KEY", "secret")

    def dummy_client_factory(**kwargs):
        return DummyQdrantClient(**kwargs)

    monkeypatch.setattr("src.vectordb.vector_store.QdrantClient", dummy_client_factory)
    store = QdrantVectorStore()

    assert store.client.kwargs["url"] == "http://localhost:6333"
    assert store.client.kwargs["api_key"] == "secret"


def test_create_collection_creates_new_collection_when_missing(monkeypatch):
    client = DummyQdrantClient()
    monkeypatch.setattr("src.vectordb.vector_store.QdrantClient", lambda **kwargs: client)

    store = QdrantVectorStore()
    store.create_collection(user_id="user1", vector_size=16, distance=Distance.COSINE)

    assert len(client.created_collections) == 1
    assert client.created_collections[0][0] == "user_user1_documents"
    assert client.created_collections[0][1].size == 16


def test_upsert_stores_points_with_payload_and_user_id(monkeypatch):
    client = DummyQdrantClient()
    monkeypatch.setattr("src.vectordb.vector_store.QdrantClient", lambda **kwargs: client)

    store = QdrantVectorStore()
    store.create_collection(user_id="alice", vector_size=3)

    chunks = [
        {
            "text": "hello world",
            "metadata": {"source": "doc.txt"},
            "vector": [0.1, 0.2, 0.3],
        },
        {
            "text": "second chunk",
            "metadata": {"source": "doc.txt"},
            "vector": [0.2, 0.4, 0.6],
        },
    ]

    ids = store.upsert(user_id="alice", chunks=chunks)

    assert len(ids) == 2
    collection_name, points = client.upserted_points[0]
    assert collection_name == "user_alice_documents"
    assert points[0].payload["user_id"] == "alice"
    assert points[0].payload["text"] == "hello world"
    assert points[0].payload["source"] == "doc.txt"


def test_search_filters_by_user_id(monkeypatch):
    client = DummyQdrantClient()
    monkeypatch.setattr("src.vectordb.vector_store.QdrantClient", lambda **kwargs: client)

    store = QdrantVectorStore()
    store.create_collection(user_id="user42", vector_size=4)

    results = store.search(user_id="user42", query_vector=[0.1, 0.2, 0.3, 0.4], top_k=1)

    assert len(results) == 1
    assert results[0]["id"] == "point-123"
    assert client.searched[0][0] == "user_user42_documents"
    assert client.searched[0][2] == 1
    assert client.searched[0][4] is True


def test_delete_user_data_uses_user_id_filter(monkeypatch):
    client = DummyQdrantClient()
    monkeypatch.setattr("src.vectordb.vector_store.QdrantClient", lambda **kwargs: client)

    store = QdrantVectorStore()
    store.delete_user_data(user_id="tenantA")

    assert client.deleted[0][0] == "user_tenantA_documents"
    assert client.deleted[0][1].must[0].key == "user_id"
    assert client.deleted[0][1].must[0].match.value == "tenantA"
