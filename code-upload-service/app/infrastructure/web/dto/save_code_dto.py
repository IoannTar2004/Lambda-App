from pydantic import BaseModel


class SaveCodeDto(BaseModel):
    filename: str
    code: str