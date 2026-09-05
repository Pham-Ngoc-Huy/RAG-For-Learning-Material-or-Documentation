# RAG-For-Learning-Material-or-Documentation

This is supporting for students who study in VGU for documentation and ask/answer chatbot

## 1. Docker Setup

Build the container:

    docker build -t rag-learning-docs .

Run with Docker:

    docker run --rm -p 8000:8000 --env-file .env rag-learning-docs

Or use Docker Compose:

    docker compose up --build

Customize the exposed port or command as needed if your app entrypoint changes.

## 2. Knowledgable:

> _**Note**_: This must be understood when we want to build once for yourselve

```mermaid
flowchart TD
    subgraph INGESTION["1. Ingestion"]
        D[Documents] --> DL[Document Loader]
        DL --> P[Preprocessing]
        P --> C[Chunking]
        C --> E[Embedding Model]
        E --> V[(Qdrant VectorDB)]
    end

    subgraph RETRIEVAL["2. Retrieval"]
        U[User Query] --> QR[Query Rewriter]
        QR --> R[Retriever]
        R --> V
        V --> R
        R --> RC[Retrieved Chunks]
    end

    subgraph GENERATION["3. Generation"]
        RC --> PB[Prompt Builder]
        QR --> PB
        PB --> L[LLM]
        L --> A[Final Answer]
    end
```

### 2.1. Ingestion (Loader)

**Description:**

> This function is for turning the all the documents (that update to system then load to the vector database) into markdown files:

**New-Insight: We can use model from Gemini for better OCR -> from jpg or png to text** (Havent in production yet)

> [!NOTE] > **Loader**
>
> **File destination:** `/ingestion/loader.py`
>
> **Input:** `file_path` or `user-input-file`
>
> **Process:**
>
> 1. Recieve Input of Users (File-Path, File-Name, URL)
> 2. Recognize the suffix-extension of the file-type (`.pdf`, `.txt`, `.csv`, `.png`, ...)
> 3. Using the libraries to convert all-types into `.md` file (MarkItDown, pdf-inspector, ocr-libs [future consideration])
> 4. Save the text into `output-scheme` and **output-file into output-directory**
>
> **Output:**
>
> - **Datatype:** `Struct`
> - **Output Scheme:**
>
> ```json
> {
>   "text": text,
>   "metadata": {
>     "source": source,
>     "file_path": file_path,
>     "file_type": file_type,
>     "loaded_at": load_time
>   }
> }
> ```

**Example**

```python
# create main.py
from ingestion import FileLoader
file_path='file_path' # put path to file here

output=FileLoader(file_path=file_path).load()
```

### 2.2. Chunking

**Desription**

> The **Chunking** stage splits the loaded document into smaller pieces called **chunks**. These chunks are used as context windows for retrieval from the vector database

It will have 2 variable fixed `DEFAULT CHUNK SIZE` and `DEFAULT CHUNK OVERLAP`

- `DEFAULT CHUNK SIZE`: define the maximum number of characters contained in a single chunk
- `DEFAULT CHUNK OVERLAP`: define the number of characters shared between two consecutive chunks

**Example**

DEFAULT_CHUNK_SIZE = 1000
DEFAULT_CHUNK_OVERLAP = 200

The chunks will conceptually look like:

```
Chunk 1: [---------------------------------]
            1000 characters

Chunk 2:                [--------------------------------
                        1000 characters
                        <------ 200 - character overlap ------->

Chunk 3:
                                        [---------------------
                                        1000 characters
```

**Note**: The overlap helps preserve contextual information between adjacent chunks and reduces the risk of losing important information at chunk boundaries

> [!NOTE] > **Loader**
>
> **File destination:** `/chunking/chunker.py`
>
> **Input:** `doc` with `dictionary` datatype
>
> **Process:**
>
> 1. Receive the `text` and `metadata` from the Loader output.
> 2. Select a chunking strategy based on the document structure:
>    - **Fixed-Size Chunking:** Split text based on a fixed character/token limit.
>    - **Recursive Chunking:** Split text using hierarchical separators such as paragraphs, newlines, sentences, and words.
>    - **Markdown Chunking:** Split Markdown documents by headers first, then `recursively chunk` sections that exceed the configured chunk size.
> 3. Apply `DEFAULT_CHUNK_SIZE` and `DEFAULT_CHUNK_OVERLAP` to control the size of each chunk and preserve contextual information between consecutive chunks.
> 4. Generate metadata for each chunk, including the original document metadata, `chunk_index`, and `total_chunk`.
> 5. Return a list of chunk objects containing the chunked `text` and its corresponding `metadata`.
>
> **Output:**
>
> - **Datatype:** `Struct`
> - **Output Scheme:**
>
> ```json
> {
>   "text": text,
>   "metadata": {
>     "source": source,
>     "file_path": file_path,
>     "file_type": file_type,
>     "loaded_at": load_time,
>     "chunk_index": chunk_index,
>     "total_chunk": total_chunk
>   }
> }
> ```

### 2.3. VectorDB (Vector Store)

**Description**

> The **Vector Store** is responsible for storing document embeddings and their ssociated metadata so that relevant chunks can be retrieved efficiently during the RAG process.
>
> In this project, **Qdrant** is used as the vector database. The implementation provides a provider-independent `BaseVectorStore` interface and a `QdrantVectorStore` implementation.
>
> The Vector Store also supports **tenant isolation**, where each `user_id` receives an isolated collection and all search/delete operations are scoped to that user.

> [!NOTE] > **Vector Store**
>
> **File destination:**
>
> - `/vectordb/vector_store.py`
>
> **Input:**
>
> - `chunks`: list of chunk objects produced by the Chunking stage
> - `user_id`: identifier used for tenant isolation
> - `query_vector`: embedding vector generated from the user's query (_this is for searching function_)
>
> **Configuration / Environment:**
>
> - `QDRANT_URL`: URL of the Qdrant instance
> - `QDRANT_API_KEY`: API key for hosted Qdrant (optional)
> - `VECTOR_DIM`: dimension of the embedding vector
> - `DISTANCE`: similarity metric used by Qdrant, e.g. `Cosine`, `Dot`, or `Euclid` (in this project we use COSINE DISTANCE)
>
> **Process:**
>
> 1. Receive chunk objects from the Chunking stage.
> 2. Create or retrieve a Qdrant collection for the corresponding `user_id`.
> 3. Validate that each chunk contains an embedding vector.
> 4. Store the embedding together with the chunk text and metadata.
> 5. Attach `user_id` to the payload to enforce tenant isolation.
> 6. Provide a similarity-search interface for retrieving the most relevant chunks.
> 7. Support deletion of either all data belonging to a user or the user's
>    entire collection.
>
> **Output:**
>
> - **Datatype:** `List[Dict]`
> - **Output Scheme:**
>
> ```json
> {
>   "id": "doc1-chunk-0",
>   "score": 0.9234,
>   "payload": {
>     "text": "chunk text",
>     "source": "file.pdf",
>     "file_path": "/data/file.pdf",
>     "file_type": "pdf",
>     "chunk_index": 0,
>     "total_chunk": 10,
>     "loaded_at": "2026-08-03T10:00:00",
>     "user_id": "student_001"
>   }
> }
> ```

**Vector Store Architecture**
The Vector Store is implemented using an abstract interface so that the underlying vector database can be replaced without changing the RAG pipeline.

```mermaid
flowchart LR
    C["Chunking Stage<br/><br/>text + metadata"]
        --> E["Embedding Model<br/><br/>text → vector"]

    E --> B["BaseVectorStore<br/><br/>
        create_collection()<br/>
        upsert()<br/>
        search()<br/>
        delete_user_data()<br/>
        delete_collection()"]

    B --> Q["QdrantVectorStore<br/><br/>Qdrant"]
```

### 2.4. Embedded

**Notation:**

`Dimension of vector space` : This is the number of neural of last layer of the hidden layer when goes to output layer for final calculation.

**Description:**

> The **Embedding** stage turns the chunked text into high-dimensional **vectors** (embeddings) that capture the semantic meaning of the text. These vectors are then stored in the Vector Store and later used to compute the similarity between a user query and each chunk during retrieval.

_Input:_

- `model`: model that use for embed to vectordb purpose
- `base_url`: url connect to that model that can be `local` also for developing purpose
- `api_key`: key access to the model embedded that already authorize

_Processing:_

We have 2 type of processing:

1. Model-Embedder

2. Fast-Embedder (from `fastembed` library [this-new])

> [!NOTE]:
>
> It just different in model usage only
>
> - With Fast-Embedder -> we do not need to import model/api_key/url
> - With Model-Embedder -> we must include all the model/api_key/url -> for authentication
>
> The processing in general is the same

> [!NOTE] > **Embedder**
>
> **File destination:**
>
> - `/src/embeddings/embedder.py`
>
> **Input:**
>
> - `chunks`: list of chunk objects produced by the Chunking stage (each chunk contains `text` and `metadata`)
> - `query`: the user query string (_this is for embedding a query before searching_)
>
> **Implementations:**
>
> - **`BaseEmbedder`:** abstract interface that defines `embed_one()`, `embed_many()`, `embed_query()` and `get_vectorspace_dimensions`.
> - **`ModelEmbedder`:** connects to a remote OpenAI-compatible embedding endpoint via `base_url` + `api_key`, or loads a local model with `SentenceTransformer` when `base_url="local"`.
> - **`FastEmbedder`:** local, API-key-free embedder backed by the `fastembed` library, used as a fallback when no API key is configured (default model: `BAAI/bge-small-en-v1.5`).
>
> **Configuration / Environment:**
>
> - `EMBEDDING_MODEL`: the embedding model name (e.g. `bge-m3`, `text-embedding-3-small`, ...)
> - `EMBEDDING_BASE_URL`: the endpoint of the OpenAI-compatible embedding server, or the reserved value `local`
> - `EMBEDDING_API_KEY`: the API key used for authentication (optional when using `local` or `FastEmbedder`)
> - `VECTOR_DIM`: must match the output dimension of the chosen model
>
> **Process:**
>
> 1. Receive chunk objects from the Chunking stage.
> 2. Collect the `text` of each chunk into a list.
> 3. Embed the texts through `_batch_embed()` (a true batch call when the underlying client supports it).
> 4. Attach each produced vector to its chunk under the key `vector`.
> 5. Expose `embed_query()` to embed the user query separately, since some models use different instructions for queries vs documents.
> 6. Expose `get_vectorspace_dimensions` so the Vector Store can create a collection with the correct `VECTOR_DIM`.
>
> **Output:**
>
> - **Datatype:** `List[Dict]` _(the input chunks mutated with their vectors)_
> - **Output Scheme:**
>
> ```json
> {
>   "text": "chunk text",
>   "metadata": {
>     "source": "file.pdf",
>     "file_path": "/data/file.pdf",
>     "file_type": "pdf",
>     "chunk_index": 0,
>     "total_chunk": 10
>   },
>   "vector": [0.0123, -0.0456, 0.0789, "..."]
> }
> ```

**Embedder Architecture**
Both embedders inherit from the abstract `BaseEmbedder` interface, so the embedding backend can be swapped without touching the rest of the RAG pipeline.

```mermaid
flowchart LR
    C["Chunking Stage<br/><br/>text + metadata"]
        --> B["BaseEmbedder<br/><br/>
            embed_one()<br/>
            embed_many()<br/>
            embed_query()<br/>
            get_vectorspace_dimensions"]

    B --> M["ModelEmbedder<br/><br/>remote (OpenAI-compatible)<br/>or local SentenceTransformer"]
    B --> F["FastEmbedder<br/><br/>fastembed (local, no API key)"]

    M --> E["Vector Embedding"]
    F --> E
```

**Workflows:**

```python
from src.embeddings import FastEmbedder, ModelEmbedder

# 1. Fast-Embedder -> local, no api_key / base_url needed
fast_embedder = FastEmbedder(model="BAAI/bge-small-en-v1.5")

dim = fast_embedder.get_vectorspace_dimensions


# 2. Model-Embedder -> remote endpoint
model_embedder = ModelEmbedder(
    model="bge-m3",
    base_url="http://localhost:6333",  # or your embedding server URL
    api_key="your-api-key",
)

# 3. Model-Embedder -> local model for developing purpose
local_embedder = ModelEmbedder(
    model="BAAI/bge-small-en-v1.5",
    base_url="local",
)

# Embed a batch of chunks (adds "vector" to each chunk dict)
chunks = [{"text": "The cell membrane is selectively permeable.", "metadata": {}}]
embedded_chunks = model_embedder.embed_many(chunks)

# Embed a single user query for searching
query_vector = model_embedder.embed_query("What is the cell membrane?")
```

### 2.5. Retrieval

**Description:**

> The **Retrieval** stage turns the user's natural-language query into a vector, searches the tenant-aware vector store for the most similar chunks, and returns the top-`k` results as context for the Generation stage.
>
> In this project, **Qdrant** is used as the vector database through a provider-independent `BaseRetriever` interface and a `QdrantRetriever` implementation. All searches are scoped to a `user_id` to enforce tenant isolation.

> [!NOTE] > **Retriever**
>
> **File destination:**
>
> - `/src/retrieval/retriever.py`
>
> **Input:**
>
> - `user_id`: tenant identifier used for isolation
> - `query`: the user query string to embed and search
> - `top_k`: number of top documents to return (default: `5`)
> - `metadata_filter`: optional additional Qdrant metadata filter (e.g. filter by `file_path`)
> - `collection_name`: optional alternate collection name suffix
>
> **Process:**
>
> 1. Receive the user's `query` and `user_id`.
> 2. Embed the query into a vector using `embedder.embed_query()`.
> 3. Search the vector store for the `top_k` nearest vectors within the user's tenant collection.
> 4. Apply the optional `metadata_filter` (e.g. restrict results to a specific document).
> 5. Return the retrieved chunks together with their payload and similarity score.
>
> **Output:**
>
> - **Datatype:** `List[Dict]`
> - **Output Scheme:**
>
> ```json
> {
>   "id": "doc1-chunk-0",
>   "score": 0.9234,
>   "payload": {
>     "text": "chunk text",
>     "source": "file.pdf",
>     "file_path": "/data/file.pdf",
>     "file_type": "pdf",
>     "chunk_index": 0,
>     "total_chunk": 10,
>     "loaded_at": "2026-08-03T10:00:00",
>     "user_id": "student_001"
>   }
> }
> ```

**Retriever Architecture**
The retriever is built on an abstract interface so the underlying vector database can be replaced without changing the retrieval logic.

```mermaid
flowchart LR
    Q["User Query"]
        --> E["Embedder<br/><br/>embed_query()</br>→ query vector"]

    E --> B["BaseRetriever<br/><br/>retrieve()"]

    B --> QR["QdrantRetriever<br/><br/>Qdrant search<br/>+ tenant isolation"]

    QR --> R["Retrieved Chunks<br/><br/>top_k results"]
```

**Workflows:**

```python
from src.retrieval import QdrantRetriever
from qdrant_client.models import Filter, FieldCondition, MatchValue

retriever = QdrantRetriever(
    vector_store=vector_store,
    embedder=embedder,
)

# Simple retrieval
results = retriever.retrieve(
    user_id="student_001",
    query="What is the cell membrane?",
    top_k=5,
)

# Retrieval with a metadata filter (e.g. only from one document)
query_filter = Filter(
    must=[
        FieldCondition(key="file_path", match=MatchValue(value="/data/biology.pdf")),
    ]
)
results = retriever.retrieve(
    user_id="student_001",
    query="What is the cell membrane?",
    top_k=5,
    metadata_filter=query_filter,
)
```

### 2.6. Prompt (Prompt Builder)

**Description:**

> The **Prompt Builder** constructs the final prompt that is sent to the LLM. It loads a prompt template (as a `.yml` file), injects the retrieved chunks as context and the user's query, then formats it into the chat message structure (`system` + `user`).
>
> In this project, `PromptTemplate` is an abstract interface and `PromptAssistance` is the concrete implementation that reads templates from `src/prompts/`.

> [!NOTE] > **Prompt Builder**
>
> **File destination:**
>
> - `/src/prompts/prompt_templates.py` (implementation)
> - `/src/prompts/*.yml` (templates, e.g. `rag_assistance.yml`, `extractor.yml`)
>
> **Input:**
>
> - `template_name`: name of the YAML template to load (without the `.yml` extension)
> - `**kwargs`: template variables used for formatting, such as `context` and `query`
>
> **Template structure (`.yml`):**
>
> - `system_message`: the system prompt; may contain placeholders like `{context}` (formatted if possible, skipped otherwise)
> - `user_message_template`: the user prompt; `{context}` and `{query}` are injected here
>
> **Process:**
>
> 1. Load the YAML template via a config loader (`NormalLoader`).
> 2. Format the `system_message` with the provided `kwargs` (ignores missing keys).
> 3. Format the `user_message_template` with the provided `kwargs` (raises `ValueError` if a parameter is missing).
> 4. Return the list of messages in chat format.
>
> **Output:**
>
> - **Datatype:** `List[Dict[str, str]]`
> - **Output Scheme:**
>
> ```json
> [
>   {
>     "role": "system",
>     "content": "You are an AI assistant whose task is to answer questions based on the provided context. ..."
>   },
>   {
>     "role": "user",
>     "content": "[PROVIDED CONTEXT]\n{context}\n\n[USER QUESTION]\n{query}"
>   }
> ]
> ```

**Workflows:**

```python
from src.prompts import PromptAssistance

prompt_builder = PromptAssistance(prompts_dir="src/prompts")

messages = prompt_builder.build(
    template_name="rag_assistance",
    context=retrieved_chunks_text,
    query="What is the cell membrane?",
)
```

### 2.7. LLM (LLM Client)

**Description:**

> The **LLM Client** sends the formatted prompt (or message history) to a large language model and returns the generated answer. It is built on an abstract `BaseLLMClient` interface so different providers (OpenAI, Google, OpenRouter-style APIs, ...) can be plugged in without changing the RAG pipeline.
>
> In this project, `ThinkingFromKnowledgeBase` is the concrete implementation that calls any OpenAI-compatible chat-completions endpoint.

> [!NOTE] > **LLM Client**
>
> **File destination:**
>
> - `/src/llm/llm_client.py`
>
> **Input:**
>
> - `prompt`: the formatted prompt text (usually produced by the Prompt Builder)
> - `messages`: optional chat message history for OpenRouter-style APIs (used instead of `prompt` if provided)
> - `temperature`: sampling temperature, `0.0` = deterministic, `1.0` = creative (default: `0.7`)
>
> **Configuration / Environment:**
>
> - `LLM_API_KEY`: API key used for authentication (required by `ThinkingFromKnowledgeBase`)
> - `LLM_BASE_URL`: base URL of the chat-completions endpoint
> - `LLM_MODEL`: model name to call, e.g. `gpt-4o`, `gemini-2.0-flash`, ...
> - `LLM_PROVIDER`: provider label stored in the response, e.g. `openai`, `google`, `openrouter`
>
> **Process:**
>
> 1. Receive a formatted `prompt` or a `messages` history.
> 2. Build the payload messages (`messages` if given, otherwise a single user message from `prompt`).
> 3. Call `client.chat.completions.create()` with the configured model and temperature.
> 4. Wrap the answer into an `LLMResponse` dataclass.
> 5. On failure, return an `LLMResponse` containing the error message instead of raising.
>
> **Output:**
>
> - **Datatype:** `LLMResponse` _(dataclass)_
> - **Output Scheme:**
>
> ```json
> {
>   "text": "the generated answer",
>   "provider": "openai",
>   "model": "gpt-4o",
>   "response": {
>     "id": "chatcmpl-...",
>     "...": "raw API response"
>   }
> }
> ```

**LLM Client Architecture**

```mermaid
flowchart LR
    PB["Prompt Builder<br/><br/>system + user messages"]
        --> B["BaseLLMClient<br/><br/>generate()"]

    B --> T["ThinkingFromKnowledgeBase<br/><br/>OpenAI-compatible API"]

    T --> L["LLM Response<br/><br/>LLMResponse dataclass"]
```

**Workflows:**

```python
from src.llm import ThinkingFromKnowledgeBase
from src.prompts import PromptAssistance

llm_client = ThinkingFromKnowledgeBase(
    api_key="your-api-key",
    base_url="https://api.openai.com/v1",
    model="gpt-4o",
    provider="openai",
)

# 1. Generate from a formatted prompt
prompt_builder = PromptAssistance(prompts_dir="src/prompts")
messages = prompt_builder.build(
    template_name="rag_assistance",
    context=retrieved_chunks_text,
    query="What is the cell membrane?",
)

answer = llm_client.generate(messages=messages)

# 2. Generate from a simple prompt string
answer = llm_client.generate(prompt="What is the cell membrane?")
print(answer.text)
```

# References

## [1] MarkItDown — Repo

> Turn file formats into `.md` files.
>
> **URL:** https://github.com/microsoft/markitdown

## [2] Qdrant — Vector Database

> Store and embed vector data.
>
> **Repository:** https://github.com/qdrant/qdrant > **Python Client Documentation:** https://qdrant.tech/documentation/clients/python/

## [3] pdf_inspector — Repo

> 99% valid-rate for converting `.pdf` files to Markdown.
>
> **URL:** https://github.com/firecrawl/pdf-inspector

## [4] PaddleOCR — OCR Engine

> Near-future add-in for OCR processing of scanned/image-based documents.
>
> **URL:** https://github.com/PaddlePaddle/PaddleOCR

## [5] Unlimited OCR [Near future add-in]

> [!NOTE]
> OCR support for scanned PDFs and image-based documents.
> Planned as a fallback when MarkItDown / pdf_inspector cannot
> extract the document content reliably.

## [6] Conventional Commits

> A specification for adding human and machine-readable meaning to commit messages.
>
> **URL:** https://www.conventionalcommits.org/en/v1.0.0/
