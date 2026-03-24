from pydantic import BaseModel, Field


class DeleteArchiveDto(BaseModel):
    user_id: int = Field(ge=1)
    project_id: int = Field(ge=1)
    version_number: int = Field(ge=1)