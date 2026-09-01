from fastapi import APIRouter, HTTPException

from src.api.schemas.auth import LoginRequest
from src.api.services.auth import authenticate_user

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/login")
def login(requests: LoginRequest):
    user = authenticate_user(
        username=requests.username,
        password=requests.password,
    )
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
        )

    return user


@router.post("/logout")
def logout(username: str, logout: bool):
    return {"username": username, "message": "logout successful"}
