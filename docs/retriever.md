# Retriever

## Purpose

The retriever module provides a query layer that embeds user questions and fetches relevant document chunks from the vector store. It enforces tenant isolation by using the underlying vector store's tenant-scoped search.

## Inputs

- `user_id`: tenant identifier used to isolate search to the user's data
- `query`: user query text
- `top_k`: maximum number of results to return
- `metadata_filter`: optional Qdrant `Filter` for additional payload constraints

## Outputs

- `retrieve()`: list of search hits with `id`, `score`, and `payload`

## Usage

```python
from src.embeddings.embedder import SentenceTransformerEmbedder
from src.retrieval import QdrantRetriever
from src.vectordb.vector_store import QdrantVectorStore

vector_store = QdrantVectorStore()
embedder = SentenceTransformerEmbedder()
retriever = QdrantRetriever(vector_store=vector_store, embedder=embedder)
results = retriever.retrieve(user_id="user1", query="What is the document about?", top_k=5)
```
