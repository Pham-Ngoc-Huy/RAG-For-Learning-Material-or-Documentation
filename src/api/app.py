import os
from collections import OrderedDict
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from src.chunking import MarkDownChunker
from src.embeddings import SentenceTransformerEmbedder
from src.ingestion.loader import SUPPORT_EXTENSIONS, FileLoader
from src.llm.llm_client import DeepSeekClient, LocalLLMClient, OpenAIClient
from src.prompts.prompt_templates import RAGPromptTemplate
from src.retrieval.retriever import QdrantRetriever
from src.vectordb.vector_store import QdrantVectorStore

REPO_ROOT = Path(__file__).resolve().parents[2]
STATIC_DIR = REPO_ROOT / "static"
UPLOAD_DIR = REPO_ROOT / "temp" / "uploads"

USER_ID = "default_user"
EMBEDDING_DIMENSION = 384
MAX_HISTORY_TURNS = 6
TOP_K = 3

app = FastAPI(title="RAG-For-Learning-Material-or-Documentation")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

vector_store: Optional[QdrantVectorStore] = None
embedder: Optional[SentenceTransformerEmbedder] = None
retriever: Optional[QdrantRetriever] = None
prompt_template: Optional[RAGPromptTemplate] = None
llm = None


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    message: str
    history: list[ChatMessage] = []


@app.on_event("startup")
def startup() -> None:
    global vector_store, embedder, retriever, prompt_template, llm

    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    vector_store = QdrantVectorStore()
    vector_store.create_collection(user_id=USER_ID, vector_size=EMBEDDING_DIMENSION)

    embedder = SentenceTransformerEmbedder()
    retriever = QdrantRetriever(vector_store=vector_store, embedder=embedder)
    prompt_template = RAGPromptTemplate()

    if os.getenv("DEEPSEEK_API_KEY"):
        llm = DeepSeekClient()
    elif os.getenv("OPENAI_API_KEY"):
        llm = OpenAIClient()
    else:
        llm = LocalLLMClient()


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok", "llm_model": getattr(llm, "model", None)}


@app.get("/api/documents")
def list_documents() -> list[dict]:
    chunks = vector_store.list_chunks(user_id=USER_ID)

    documents: "OrderedDict[str, dict]" = OrderedDict()
    for chunk in chunks:
        payload = chunk.get("payload") or {}
        source = payload.get("source", "unknown")
        entry = documents.setdefault(
            source,
            {
                "source": source,
                "file_type": payload.get("file_type"),
                "loaded_at": payload.get("loaded_at"),
                "chunk_count": 0,
            },
        )
        entry["chunk_count"] += 1

    return list(documents.values())


@app.post("/api/documents")
async def upload_document(file: UploadFile = File(...)) -> dict:
    suffix = Path(file.filename).suffix.lower()
    if suffix not in SUPPORT_EXTENSIONS:
        raise HTTPException(status_code=422, detail=f"Unsupported file type: {suffix}")

    dest_path = UPLOAD_DIR / file.filename
    content = await file.read()
    dest_path.write_bytes(content)

    try:
        doc = FileLoader(str(dest_path)).load()
        if doc is None:
            raise HTTPException(status_code=422, detail="Could not extract any text from this file")

        chunks = MarkDownChunker().chunk(doc=doc)
        if not chunks:
            raise HTTPException(status_code=422, detail="Document produced no chunks")

        chunks = embedder.embed_many(chunks)
        vector_store.upsert(user_id=USER_ID, chunks=chunks)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {exc}") from exc

    return {
        "source": doc["metadata"]["source"],
        "file_type": doc["metadata"]["file_type"],
        "chunk_count": len(chunks),
    }


@app.delete("/api/documents/{source}")
def delete_document(source: str) -> dict:
    vector_store.delete_by_source(user_id=USER_ID, source=source)

    uploaded_path = UPLOAD_DIR / source
    if uploaded_path.exists():
        uploaded_path.unlink()

    md_path = REPO_ROOT / "md_store" / f"{Path(source).stem}.md"
    if md_path.exists():
        md_path.unlink()

    return {"deleted": source}


@app.post("/api/chat")
def chat(request: ChatRequest) -> dict:
    if not request.message.strip():
        raise HTTPException(status_code=422, detail="message must not be empty")

    retrieved_chunks = retriever.retrieve(user_id=USER_ID, query=request.message, top_k=TOP_K)
    formatted_prompt = prompt_template.build(query=request.message, retrieved_chunks=retrieved_chunks)

    history = request.history[-MAX_HISTORY_TURNS:]
    messages = [{"role": m.role, "content": m.content} for m in history]
    messages.append({"role": "user", "content": formatted_prompt})

    response = llm.generate(messages=messages, max_tokens=600, temperature=0.7)

    citations = [
        {
            "source": (chunk.get("payload") or {}).get("source", "unknown"),
            "score": chunk.get("score"),
            "snippet": (chunk.get("payload") or {}).get("text", "")[:220],
        }
        for chunk in retrieved_chunks
    ]

    return {
        "answer": response.get("response"),
        "citations": citations,
        "tokens_used": response.get("tokens_used"),
        "model": response.get("model"),
    }


app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")
