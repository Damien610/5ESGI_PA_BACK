from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from app.services.storage_service import storage_service

router = APIRouter(prefix="/storage", tags=["storage"])

@router.post("/upload")
async def upload_file(
    path: str,
    file: UploadFile = File(...)
):
    try:
        file_data = await file.read()
        object_name = storage_service.upload_file(file_data, file.filename, path)
        return {
            "message": "File uploaded successfully",
            "object_name": object_name,
            "path": path,
            "filename": file.filename,
            "url": f"/storage/files/{object_name}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/files/{file_path:path}")
async def get_file(file_path: str):
    try:
        file_data, content_type = storage_service.get_file(file_path)
        return StreamingResponse(file_data, media_type=content_type)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
