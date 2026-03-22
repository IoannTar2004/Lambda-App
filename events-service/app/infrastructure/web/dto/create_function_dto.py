from pydantic import BaseModel, Field, ConfigDict


class CreateFunctionDTO(BaseModel):

    name: str = Field(min_length=3, max_length=64, description='name of function')
    project_id: int = Field(ge=1, description='project id')
    language: str = Field(default="python", max_length=32, description='name of language')
    function_path: str = Field(max_length=256, description='path of handler')
    function_name: str = Field(max_length=128, description='name of function')
    memory_size: int = Field(le=2048, description='memory_size of container')
    timeout: int = Field(le=300, description='max time in seconds')

    model_config = ConfigDict(extra='forbid')