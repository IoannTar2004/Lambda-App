from pydantic import Field, BaseModel


class DeleteVersionDto(BaseModel):

    user_id: int = Field()
    function_name: str = Field(min_length=3, max_length=32)
    version_number: int = Field(ge=1)