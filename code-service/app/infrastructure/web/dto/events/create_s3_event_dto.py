from pydantic import BaseModel, Field


class CreateS3EventDto(BaseModel):
    function_id: int = Field()
    bucket: str = Field(max_length=64)
    events: list[str] = Field()
    prefix: str = Field(default="")
    suffix: str = Field(default="")
