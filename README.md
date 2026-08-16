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

> [!NOTE]
> **Loader**
>
> **File destination:** `/ingestion/loader.py`
>
> **Input:** `file_path` or `user-input-file`
>
> **Process:**
> 1. Recieve Input of Users (File-Path, File-Name, URL)
> 2. Recognize the suffix-extension of the file-type (`.pdf`, `.txt`, `.csv`, `.png`, ...)
> 3. Using the libraries to convert all-types into `.md` file (MarkItDown, pdf-inspector, ocr-libs [future consideration])
> 4. Save the text into `output-scheme` and **output-file into output-directory**
>
> **Output:**
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

> [!NOTE]
> **Loader**
>
> **File destination:** `/chunking/chunker.py`
>
> **Input:** `doc` with `dictionary` datatype
>
> **Process:**
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

> [!NOTE]
> **Vector Store**
>
> **File destination:**
> - `/vectordb/vector_store.py`
>
> **Input:**
> - `chunks`: list of chunk objects produced by the Chunking stage
> - `user_id`: identifier used for tenant isolation
> - `query_vector`: embedding vector generated from the user's query (_this is for searching function_)
>
> **Configuration / Environment:**
> - `QDRANT_URL`: URL of the Qdrant instance
> - `QDRANT_API_KEY`: API key for hosted Qdrant (optional)
> - `VECTOR_DIM`: dimension of the embedding vector
> - `DISTANCE`: similarity metric used by Qdrant, e.g. `Cosine`, `Dot`, or `Euclid` (in this project we use COSINE DISTANCE)
>
> **Process:**
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
# References

## [1] MarkItDown — Repo
> Turn file formats into `.md` files.
>
> **URL:** https://github.com/microsoft/markitdown

## [2] Qdrant — Vector Database
> Store and embed vector data.
>
> **Repository:** https://github.com/qdrant/qdrant  
> **Python Client Documentation:** https://qdrant.tech/documentation/clients/python/

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