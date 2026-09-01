from fastapi import APIRouter, HTTPException
from src.api.schemas.auth import LoginRequest, SignUpRequest
from src.api.services.auth import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

auth = AuthService()


@router.post("/signup")
async def signup(requests: SignUpRequest):
    try:
        await auth.signup(requests)
        return {"message": "User created successfully"}
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.post("/login")
async def login(requests: LoginRequest):
    user = await auth.login(requests)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Invalid username or password",
        )
    return {"message": "Login successful"}