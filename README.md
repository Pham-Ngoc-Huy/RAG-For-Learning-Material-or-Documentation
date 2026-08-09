# RAG-For-Learning-Material-or-Documentation
This is supporting for students who study in VGU for documentation and ask/answer chatbot. And this is special gift for my lovely girl friend.

## Run locally (recommended: Docker Compose)

1. Create a `.env` file in the project root:

       QDRANT_ENDPOINT=http://qdrant:6333
       # optional — enables real LLM answers instead of the mock client
       # OPENAI_API_KEY=sk-...
       # DEEPSEEK_API_KEY=...

2. Start everything (Qdrant + API + UI):

       docker compose up --build

3. Open **http://localhost:8000** — chat with your documents and upload new ones from the "Kho tài liệu" tab.

Without an `OPENAI_API_KEY` or `DEEPSEEK_API_KEY`, the app falls back to a mock LLM so the pipeline is still fully testable end-to-end (retrieval works with real embeddings/Qdrant, only the final generation step is stubbed).

## Docker (manual, without Compose)

Build the container:

    docker build -t rag-learning-docs .

Run with Docker (requires a separately running Qdrant instance):

    docker run --rm -p 8000:8000 --env-file .env rag-learning-docs

## CLI demo

`main.py` runs a one-shot pipeline demo (ingest a sample PDF, retrieve, generate) against the same Qdrant instance:

    docker compose run --rm app python3 main.py

# References:
## [1] MarkItDown - Repo [Turn file-format to .md file]
```bash
https://github.com/microsoft/markitdown
```

## [2] Qdrant: Vector Database - Repo [store and embedded the data]

```bash
https://github.com/qdrant/qdrant
```