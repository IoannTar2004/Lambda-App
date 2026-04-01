from pydantic import BaseModel, Field, ConfigDict


class CreateFunctionDTO(BaseModel):

    name: str = Field(min_length=3, max_length=64, description='name of function')
    project_id: int = Field(ge=1, description='project id')
    environment: str = Field(default="Python 3", max_length=32, description='name of environment')
    function_path: str = Field(max_length=256, description='path of handler')
    function_name: str = Field(max_length=128, description='name of function')
    memory_size: int = Field(ge=128, le=1024, default=512, description='memory_size of container')
    timeout: int = Field(ge=1, le=300, default=5, description='max time in seconds')

    model_config = ConfigDict(extra='forbid')