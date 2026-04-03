from pydantic import BaseModel, Field


class UpdateHandlerDTO(BaseModel):
    function_id: int = Field(ge=1)
    handler_path: str = Field(max_length=256)
    handler: str = Field(max_length=64)
    memory_size: int = Field(ge=512, le=1024)
    timeout: int = Field(ge=1, le=300)
