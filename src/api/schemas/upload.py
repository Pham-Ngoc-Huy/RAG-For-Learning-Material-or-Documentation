from datetime import datetime

from fastapi import BaseModel


class UploadFileSchema(BaseModel):
    file: bytes
    username: str
    filename: str
    content: str
    upload_date: datetime
