from pydantic import Field, BaseModel


class ZipProjectDto(BaseModel):

    user_id: int = Field()
    project_name: str | None = Field(min_length=3, max_length=32)
    function_name: str = Field(min_length=3, max_length=64)
    version_number: int = Field(ge=1)