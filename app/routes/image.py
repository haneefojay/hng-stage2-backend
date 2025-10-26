from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os

router = APIRouter()

@router.get("/countries/image")
async def get_summary_image():
    path = "cache/summary.png"
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Summary image not found")
    return FileResponse(path, media_type="image/png")
