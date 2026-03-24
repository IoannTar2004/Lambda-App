from pydantic import Field, BaseModel


class ZipProjectDto(BaseModel):

    user_id: int = Field()
    project_id: int = Field(ge=1)
    project_name: str = Field(min_length=3, max_length=32)
    version_number: int = Field(ge=1)