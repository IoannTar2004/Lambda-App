from pydantic import BaseModel, Field


class DeleteArchivesDTO(BaseModel):
    user_id: int
    project_name: str = Field(min_length=3, max_length=64)