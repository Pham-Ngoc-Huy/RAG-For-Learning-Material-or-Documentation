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

!!! note "Loader"

    **File destination:** `/ingestion/loader.py`

    **Input:** `file_path` or `user-input-file`

    **Process:** 
    1. Recieve Input of Users (File-Path, File-Name, URL)
    2. Recognize the suffix-extension of the file-type (`.pdf`, `.txt`, `.csv`, `.png`, ...)
    3. Using the libraries to convert all-types into `.md` file (MarkItDown, pdf-inspector, ocr-libs [future consideration])
    4. Save the text into `output-scheme` and **output-file into output-directory**

    **Output:**

    - **Datatype:** `Struct`
    - **Output Scheme:**

      ```json
      {
        "text": text,
        "metadata": {
          "source": source,
          "file_path": file_path,
          "file_type": file_type,
          "loaded_at": load_time
        }
      }
      ```
!!! Example
    ```python
    # create main.py 
    from ingestion import FileLoader
    file_path='file_path' # put path to file here

    output=FileLoader(file_path=file_path).load()
    ```
### 2.2. Chunking
**Desription**
> This will chunk the query input into several context windows and this will support the `query` in `vector-db` (this is the also the factor make the prompt become for efficiency if the context-windows is splitting right. )


# References:
## [1] MarkItDown - Repo [Turn file-format to .md file]
!!! url https://github.com/microsoft/markitdown

## [2] Qdrant: Vector Database - Repo [store and embedded the data]
!!!url https://github.com/qdrant/qdrant

## [3] pdf_inspector - Repo [99% valid-rate from turning `.pdf` to `markdown-file`]
!!!url https://github.com/firecrawl/pdf-inspector