from fastapi import APIRouter
from pydantic import BaseModel, Field
from .common import download_with_ytdlp

router = APIRouter(prefix="/api/download", tags=["Instagram"])
class DownloadRequest(BaseModel):
    url: str = Field(min_length=8, max_length=2000)
    mode: str = "all"

@router.post("/instagram")
def download_instagram(req: DownloadRequest):
    """Ekstrak URL media dari posting Instagram publik yang dapat diakses."""
    return download_with_ytdlp(req.url, "instagram", req.mode)
