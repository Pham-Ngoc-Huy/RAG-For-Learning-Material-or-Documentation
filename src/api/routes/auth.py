from fastapi import APIRouter, HTTPException

from src.api.schemas.auth import LoginRequest, LoginResponse, SignUpRequest, SignUpResponse
from src.api.services import AuthServiceImpl

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

auth = AuthServiceImpl()


@router.post("/signup", response_model=SignUpResponse)
async def signup(requests: SignUpRequest):
    try:
        user = await auth.signup(requests)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
    return SignUpResponse(user_id=user["user_id"], username=user["username"])


@router.post("/login", response_model=LoginResponse)
async def login(requests: LoginRequest):
    user = await auth.login(requests)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Invalid username or password",
        )
    return LoginResponse(user_id=user["user_id"], username=user["username"])
