from pydantic import BaseModel, Field

class LoginRequest(BaseModel):
    username: str
    password: str = Field(..., max_length=72)


class LoginResponse(BaseModel):
    user_id: str
    username: str


class SignUpRequest(BaseModel):
    username: str
    password: str = Field(..., max_length=72)


class SignUpResponse(BaseModel):
    user_id: str
    username: str
