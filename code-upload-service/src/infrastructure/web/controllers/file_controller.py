from fastapi import APIRouter, UploadFile

router = APIRouter()


@router.post("/upload-code")
async def upload_code(uploaded: UploadFile):
    file = uploaded.file
    return uploaded.filename