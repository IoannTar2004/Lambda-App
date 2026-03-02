from fastapi import APIRouter

from infrastructure.config.usecase_config import save_code_usecase
from infrastructure.web.model.save_code_model import CodeRequest

router = APIRouter(prefix="/api/users", tags=["File Controller"])


@router.post("/save-code")
async def upload_code(data: CodeRequest):
    save_code_usecase.save(data.filename, data.code)
