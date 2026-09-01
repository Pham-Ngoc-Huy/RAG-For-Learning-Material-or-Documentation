from fastapi import BaseModel
from datetime import datetime

class UploadFileSchema(BaseModel):
    file: bytes
    username: str
    filename: str
    content: str
    upload_date: datetime
    