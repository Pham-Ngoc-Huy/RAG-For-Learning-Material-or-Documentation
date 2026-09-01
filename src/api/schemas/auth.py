from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    username: str
    password: str = Field(..., max_length=72)


class LoginResponse(BaseModel):
    username: str
    password: str


class SignUpRequest(BaseModel):
    username: str
    password: str = Field(..., max_length=72)
