from pydantic import BaseModel


class CodeRequest(BaseModel):
    filename: str
    code: str