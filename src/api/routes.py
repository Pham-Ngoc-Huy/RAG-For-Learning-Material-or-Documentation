from collections import OrderedDict
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from pydantic import BaseModel

from src.api.deps import get_state
from src.api.state import AppState
from src.chunking import MarkDownChunker
from src.ingestion.loader import SUPPORT_EXTENSIONS, FileLoader

router = APIRouter(prefix="/api", tags=["rag"])

USER_ID = "default_user"
MAX_HISTORY_TURNS = 6
TOP_K = 3

StateDep = Annotated[AppState, Depends(get_state)]


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    message: str
    history: list[ChatMessage] = []


@router.get("/health")
def health(state: StateDep) -> dict:
    return {"status": "ok", "llm_model": getattr(state.llm, "model", None)}


@router.get("/documents")
def list_documents(state: StateDep) -> list[dict]:
    chunks = state.vector_store.list_chunks(user_id=USER_ID)

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


@router.post("/documents", status_code=201)
async def upload_document(state: StateDep, file: UploadFile = File(...)) -> dict:
    suffix = Path(file.filename).suffix.lower()
    if suffix not in SUPPORT_EXTENSIONS:
        raise HTTPException(status_code=422, detail=f"Unsupported file type: {suffix}")

    dest_path = state.upload_dir / file.filename
    content = await file.read()
    dest_path.write_bytes(content)

    try:
        doc = FileLoader(str(dest_path)).load()
        if doc is None:
            raise HTTPException(status_code=422, detail="Could not extract any text from this file")

        chunks = MarkDownChunker().chunk(doc=doc)
        if not chunks:
            raise HTTPException(status_code=422, detail="Document produced no chunks")

        chunks = state.embedder.embed_many(chunks)
        state.vector_store.upsert(user_id=USER_ID, chunks=chunks)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {exc}") from exc

    return {
        "source": doc["metadata"]["source"],
        "file_type": doc["metadata"]["file_type"],
        "chunk_count": len(chunks),
    }


@router.delete("/documents/{source}")
def delete_document(source: str, state: StateDep) -> dict:
    state.vector_store.delete_by_source(user_id=USER_ID, source=source)

    uploaded_path = state.upload_dir / source
    if uploaded_path.exists():
        uploaded_path.unlink()

    md_path = state.md_store_dir / f"{Path(source).stem}.md"
    if md_path.exists():
        md_path.unlink()

    return {"deleted": source}


@router.post("/chat")
def chat(request: ChatRequest, state: StateDep) -> dict:
    if not request.message.strip():
        raise HTTPException(status_code=422, detail="message must not be empty")

    retrieved_chunks = state.retriever.retrieve(user_id=USER_ID, query=request.message, top_k=TOP_K)
    formatted_prompt = state.prompt_template.build(query=request.message, retrieved_chunks=retrieved_chunks)

    history = request.history[-MAX_HISTORY_TURNS:]
    messages = [{"role": m.role, "content": m.content} for m in history]
    messages.append({"role": "user", "content": formatted_prompt})

    response = state.llm.generate(messages=messages, max_tokens=600, temperature=0.7)

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