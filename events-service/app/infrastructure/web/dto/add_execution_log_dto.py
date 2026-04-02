from pydantic import BaseModel, Field


class AddExecutionLogDTO(BaseModel):

    id: str = Field(max_length=32)
    function_id: int = Field(ge=1)
    execution_time: float