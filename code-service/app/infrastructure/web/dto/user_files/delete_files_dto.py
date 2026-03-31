from pydantic import BaseModel


class DeleteFilesDto(BaseModel):
    project_id: int
    keys: list[str]