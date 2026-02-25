from pydantic import BaseModel


class UploadVideoRequest(BaseModel):
    filename: str
    title: str
    description: str
