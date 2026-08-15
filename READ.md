# Vector Store (vectordb)

## Description
Vector store (VectorDB) stores embeddings (fixed-dimension vectors) and associated metadata for fast semantic retrieval. In this project Qdrant is the recommended store; other providers (Pinecone, Milvus, etc.) can be used with an adapter.

## File destination
- /vectordb/manager.py  (wrapper around provider client)
- /ingestion/ -> produces chunk objects to be inserted

## Config / Environment
- QDRANT_URL: URL to the Qdrant instance (e.g. http://localhost:6333)
- QDRANT_API_KEY: API key if hosted (optional)
- VECTORDB_COLLECTION: default collection name, e.g. "rag_docs"
- VECTOR_DIM: integer embedding dimension (must match embedding model)
- DISTANCE: similarity metric, e.g. "Cosine" or "Dot" or "Euclid"

## Schema / Metadata
Each vector entry should include:
- id: stable id for the chunk (string)
- vector: embedding (list[float])
- payload / metadata: dictionary containing
  - source: original file or URL
  - file_path: path in storage
  - chunk_index: integer
  - total_chunks: integer
  - loaded_at: iso timestamp
  - any custom tags (e.g., topic, language)

## Process
1. Receive chunk objects from ingestion: {text, metadata}
2. Compute embedding using chosen model (ensure VECTOR_DIM)
3. Upsert vectors and metadata into collection
4. Provide a Retriever API that accepts query embeddings and returns top-k chunks

## Example (Python + qdrant-client)
```python
from qdrant_client import QdrantClient
from qdrant_client.http import models

client = QdrantClient(url=os.getenv("QDRANT_URL"), api_key=os.getenv("QDRANT_API_KEY"))
collection = os.getenv("VECTORDB_COLLECTION", "rag_docs")

# create collection if not exists
client.recreate_collection(
    collection_name=collection,
    vectors_config=models.VectorParams(size=int(os.getenv("VECTOR_DIM", 1536)), distance=models.Distance.COSINE),
)

# upsert a single chunk
point = models.PointStruct(
    id="doc1-chunk-0",
    vector=embedding,  # list[float]
    payload={
        "source": "file.pdf",
        "file_path": "/data/file.pdf",
        "chunk_index": 0,
        "total_chunks": 10,
        "text": chunk_text,
    },
)
client.upsert(collection_name=collection, points=[point])

# search
results = client.search(collection_name=collection, query_vector=query_embedding, limit=5)
for res in results:
    print(res.id, res.payload.get("file_path"), res.score)
```

## Retriever contract
Expose a simple Retriever interface:
- build_index(chunks: List[Chunk]) -> None
- query(query_text: str, top_k: int = 5) -> List[Chunk]

Implementation should handle batching upserts, retries, and backoff for network errors.

## Notes
- Keep VECTOR_DIM consistent with the embedding model to avoid errors
- Use chunk ids stable across re-ingestion to avoid duplicates
- Consider sharding/collections per-tenant for multi-tenancy

## References
- Qdrant: https://github.com/qdrant/qdrant
- qdrant-client docs: https://qdrant.tech/documentation/clients/python/

---
Generated following style in README.md (sections: Description, File destination, Config, Process, Example, References).