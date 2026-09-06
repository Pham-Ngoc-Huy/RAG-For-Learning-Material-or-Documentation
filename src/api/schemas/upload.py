from datetime import datetime

from pydantic import BaseModel


class UploadFileSchema(BaseModel):
    user_id: str
    user_name: str
    collection_name: str
    file_path: str
    model: str


class UploadFileResponse(BaseModel):
    user_id: str
    user_name: str
    collection_name: str
    file_path: str
    model: str
    total_chunks: int
    upload_date: datetime
