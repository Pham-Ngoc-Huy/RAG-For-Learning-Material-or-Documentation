# Vector Store

## Purpose

The vector store module provides Qdrant-backed storage for embedding vectors and metadata. It enforces tenant isolation by mapping each user to a dedicated collection.

## Inputs

- `user_id`: tenant identifier used to isolate collections
- `chunks`: list of documents/chunks containing `text`, `metadata`, and `vector`
- `query_vector`: embedding vector for similarity search
- `metadata_filter`: optional Qdrant `Filter` object for additional filtering

## Outputs

- `upsert()`: list of point IDs written to the collection
- `search()`: list of search hits with `id`, `score`, and `payload`

## Environment Variables

- `QDRANT_URL`: optional full connection URL for Qdrant
- `QDRANT_API_KEY`: optional API key for Qdrant

## Dependencies

- `qdrant-client`

## Usage

```python
from src.vectordb.vector_store import QdrantVectorStore

store = QdrantVectorStore()
store.create_collection(user_id="user123", vector_size=1536)
store.upsert(
    user_id="user123",
    chunks=[
        {"text": "hello world", "metadata": {"source": "doc.txt"}, "vector": [0.1, 0.2, 0.3]},
    ],
)
results = store.search(user_id="user123", query_vector=[0.1, 0.2, 0.3], top_k=3)
```
