from pydantic import BaseModel, Field, ConfigDict


class CreateFunctionDTO(BaseModel):

    function_name: str = Field(min_length=3, max_length=128, description='name of function')
    project_name: str = Field(min_length=3, max_length=128, description='name of project')
    handler: str = Field(max_length=128, description='path of handler')
    memory_size: int = Field(le=2048, description='memory_size of container')
    timeout: int = Field(le=300, description='max time in seconds')

    model_config = ConfigDict(extra='forbid')