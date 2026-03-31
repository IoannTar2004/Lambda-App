from pydantic import BaseModel, Field


class CreateProjectDto(BaseModel):
    project_name: str = Field(min_length=3, max_length=64)