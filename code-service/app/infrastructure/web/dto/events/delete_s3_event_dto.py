from pydantic import BaseModel, Field


class DeleteS3EventDto(BaseModel):
    function_id: int = Field()
    bucket: str = Field(max_length=64)