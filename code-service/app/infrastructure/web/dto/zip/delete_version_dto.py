from pydantic import Field, BaseModel


class DeleteVersionDto(BaseModel):

    user_id: int = Field()
    project_id: int = Field(ge=1)
    revision_id: int = Field(ge=1)