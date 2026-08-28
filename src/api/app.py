from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.api.routes import router
from src.api.state import AppState, build_llm
from src.embeddings import SentenceTransformerEmbedder
from src.prompts.prompt_templates import RAGPromptTemplate
from src.retrieval.retriever import QdrantRetriever
from src.vectordb.vector_store import QdrantVectorStore

REPO_ROOT = Path(__file__).resolve().parents[2]
STATIC_DIR = REPO_ROOT / "static"
UPLOAD_DIR = REPO_ROOT / "temp" / "uploads"
MD_STORE_DIR = REPO_ROOT / "md_store"

USER_ID = "default_user"
EMBEDDING_DIMENSION = 384


@asynccontextmanager
async def lifespan(app: FastAPI):
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    MD_STORE_DIR.mkdir(parents=True, exist_ok=True)

    vector_store = QdrantVectorStore()
    vector_store.create_collection(user_id=USER_ID, vector_size=EMBEDDING_DIMENSION)

    embedder = SentenceTransformerEmbedder()
    retriever = QdrantRetriever(vector_store=vector_store, embedder=embedder)
    prompt_template = RAGPromptTemplate()
    llm = build_llm()

    app.state.rag = AppState(
        vector_store=vector_store,
        embedder=embedder,
        retriever=retriever,
        prompt_template=prompt_template,
        llm=llm,
        upload_dir=UPLOAD_DIR,
        md_store_dir=MD_STORE_DIR,
    )

    yield

    # No teardown today — add client.close() calls here if your
    # QdrantVectorStore / LLM clients grow one later.


def create_app() -> FastAPI:
    app = FastAPI(title="RAG-For-Learning-Material-or-Documentation", lifespan=lifespan)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(router)
    # Must come last: it's a catch-all mount at "/".
    app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")
    return app


app = create_app()
