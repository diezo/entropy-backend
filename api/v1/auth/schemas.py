from pydantic import BaseModel


class AjaxRequest(BaseModel):
    username: str
    password: str
