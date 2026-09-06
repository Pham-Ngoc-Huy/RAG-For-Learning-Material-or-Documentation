import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routes.auth import router as auth_router
from src.api.routes.upload import router as upload_router

app = FastAPI()

# allow the React (Next.js) frontend to call this API during development
# production is same-origin (served together on Vercel), so CORS is not needed there
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in cors_origins if origin.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# using for logins and authentication
app.include_router(auth_router)

# using for uploading documents
app.include_router(upload_router)
