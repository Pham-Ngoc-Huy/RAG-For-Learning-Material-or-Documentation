from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    user_id: str
    user_name: str
    collection_name: str
    question: str = Field(..., min_length=1)
    model: str


class ChatResponse(BaseModel):
    user_id: str
    user_name: str
    collection_name: str
    question: str
    answer: str
