from pydantic import BaseModel, Field


class DeleteS3EventDto(BaseModel):
    function_id: int = Field(ge=1)
    bucket: str = Field(max_length=64)