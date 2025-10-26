from fastapi import APIRouter
from fastapi.responses import FileResponse
import os
from app.utils.errors import NotFoundError

router = APIRouter()

@router.get("/countries/image")
async def get_summary_image():
    path = "cache/summary.png"
    if not os.path.exists(path):
        raise NotFoundError()
    return FileResponse(path, media_type="image/png")
