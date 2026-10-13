from fastapi import APIRouter
from pydantic import BaseModel, Field
from PIL import ImageDraw
from .common import card, font, save_image

router = APIRouter(prefix="/api/mockup", tags=["Fake Mobile Legends"])
class MLMockRequest(BaseModel):
    nickname: str = Field(default="VannMrtnzz", max_length=50)
    user_id: str = Field(default="123456789", max_length=40)
    rank: str = "Mythic"

@router.post("/mobile-legends")
def fake_mobile_legends(req: MLMockRequest):
    im=card("MOBILE LEGENDS",req.nickname,accent=(85,174,255)); d=ImageDraw.Draw(im)
    d.text((60,255),"USER ID",font=font(20,True),fill=(120,190,255))
    d.text((60,295),req.user_id,font=font(38,True),fill=(250,250,255))
    d.text((60,380),"RANK • "+req.rank[:30],font=font(30,True),fill=(255,220,130))
    d.text((60,440),"Rank dan profil adalah data contoh.",font=font(22),fill=(180,192,215))
    return {**save_image(im,"fake_ml"),"message":"Mockup Mobile Legends fiktif berhasil dibuat."}
