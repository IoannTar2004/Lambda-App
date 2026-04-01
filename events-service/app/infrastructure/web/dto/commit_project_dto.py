from pydantic import BaseModel, Field



class CommitProjectDTO(BaseModel):
    class FunctionHandlerDto(BaseModel):
        function_path: str = Field(max_length=256, description='path of handler')
        function_name: str = Field(max_length=128, description='name of function')

    project_id: int = Field(ge=1)
    functions: dict[int, FunctionHandlerDto]
