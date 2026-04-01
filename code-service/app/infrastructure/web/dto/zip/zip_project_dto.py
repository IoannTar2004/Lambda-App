from pydantic import Field, BaseModel


class ZipProjectDto(BaseModel):

    user_id: int = Field()
    project_id: int = Field(ge=1)
    version_number: int = Field(ge=1)