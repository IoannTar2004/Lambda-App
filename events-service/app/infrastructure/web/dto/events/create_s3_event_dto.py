from pydantic import BaseModel, Field


class CreateS3EventDto(BaseModel):
    function_id: int = Field(ge=1)
    bucket: str = Field(max_length=64)
    events: list[str] = Field(max_length=256)
    prefix: str = Field(default="", max_length=256)
    suffix: str = Field(default="", max_length=256)
