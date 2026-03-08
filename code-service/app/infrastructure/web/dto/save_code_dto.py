from pydantic import BaseModel


class SaveCodeDto(BaseModel):
    path: str
    code: str