from pydantic import BaseModel, Field


class UpdateHandlerDTO(BaseModel):
    function_id: int = Field(ge=1)
    function_path: str = Field(max_length=256)
    function_name: str = Field(max_length=64)
    memory_size: int = Field(ge=512, le=1024)
    timeout: int = Field(ge=1, le=300)
