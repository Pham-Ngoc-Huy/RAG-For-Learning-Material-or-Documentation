# RAG-For-Learning-Material-or-Documentation
This is supporting for students who study in VGU for documentation and ask/answer chatbot

## Docker

Build the container:

    docker build -t rag-learning-docs .

Run with Docker:

    docker run --rm -p 8000:8000 --env-file .env rag-learning-docs

Or use Docker Compose:

    docker compose up --build

Customize the exposed port or command as needed if your app entrypoint changes.

# References:
## [1] MarkItDown - Repo [Turn file-format to .md file]
```bash
https://github.com/microsoft/markitdown
```

## [2] Qdrant: Vector Database - Repo [store and embedded the data]

```bash
https://github.com/qdrant/qdrant
```