from pydantic import Field, BaseModel


class ZipProjectDto(BaseModel):

    user_id: int = Field(ge=1)
    project_id: int = Field(ge=1)
    revision_id: int = Field(ge=1)
