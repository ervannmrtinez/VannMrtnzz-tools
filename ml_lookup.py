from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
import os, requests

router = APIRouter(prefix="/api/mobile-legends", tags=["Mobile Legends Lookup"])
class MLLookupRequest(BaseModel):
    user_id: str = Field(min_length=1, max_length=40)
    server_id: str = Field(min_length=1, max_length=20)

@router.post("/lookup")
def mobile_legends_lookup(req: MLLookupRequest):
    endpoint = os.getenv("ML_LOOKUP_API_URL", "").strip()
    if not endpoint:
        raise HTTPException(503, "API lookup belum dikonfigurasi. Set ML_LOOKUP_API_URL ke endpoint provider yang sah.")
    if not endpoint.startswith("https://"):
        raise HTTPException(500, "ML_LOOKUP_API_URL wajib menggunakan HTTPS.")
    try:
        response = requests.get(endpoint, params={"user_id": req.user_id, "server_id": req.server_id}, timeout=12)
        response.raise_for_status()
        data = response.json()
    except Exception as exc:
        raise HTTPException(502, f"Provider lookup gagal merespons: {str(exc)[:160]}")
    return {"message":"Hasil dari provider lookup eksternal; verifikasi sebelum digunakan.","result":data}
