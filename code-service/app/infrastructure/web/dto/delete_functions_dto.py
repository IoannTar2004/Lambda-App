from pydantic import BaseModel, Field


class DeleteFunctionsDTO(BaseModel):
    user_id: int
    function_name: str = Field(min_length=3, max_length=32)