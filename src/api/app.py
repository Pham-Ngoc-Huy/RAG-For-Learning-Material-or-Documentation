from fastapi import FastAPI

from src.api.routes.auth import router as auth_router

app = FastAPI()

# using for logins and authentication
app.include_router(auth_router)
