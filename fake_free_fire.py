from fastapi import APIRouter
from pydantic import BaseModel, Field
from PIL import ImageDraw
from .common import card, font, save_image

router = APIRouter(prefix="/api/mockup", tags=["Fake Free Fire"])
class FFRequest(BaseModel):
    nickname: str = Field(default="VANN•MRTNZZ", max_length=50)
    player_id: str = Field(default="123456789", max_length=40)

@router.post("/free-fire")
def fake_free_fire(req: FFRequest):
    im=card("FREE FIRE PROFILE",req.nickname,accent=(255,151,61)); d=ImageDraw.Draw(im)
    d.text((60,255),"PLAYER ID",font=font(20,True),fill=(255,185,110))
    d.text((60,295),req.player_id,font=font(38,True),fill=(250,250,255))
    d.text((60,380),"LEVEL • 68      RANK • HEROIC",font=font(26,True),fill=(255,220,170))
    d.text((60,440),"Stats dan rank hanya contoh desain.",font=font(22),fill=(180,192,215))
    return {**save_image(im,"fake_ff"),"message":"Mockup Free Fire fiktif berhasil dibuat."}
