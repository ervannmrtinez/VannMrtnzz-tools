from fastapi import APIRouter
from pydantic import BaseModel, Field
from PIL import Image, ImageDraw
from .common import font, fit_text, save_image

router = APIRouter(prefix="/api/mockup", tags=["Fake Instagram"])
class FakeIGRequest(BaseModel):
    name: str = Field(default="VannMrtnzz", max_length=50)
    username: str = Field(default="vannmrtnzz", max_length=50)
    bio: str = Field(default="creative studio", max_length=100)

@router.post("/fake-instagram")
def fake_instagram(req: FakeIGRequest):
    im = Image.new("RGB",(900,700),(248,248,250)); d=ImageDraw.Draw(im)
    d.text((45,30),"Instagram",font=font(38,True),fill=(25,25,30))
    d.ellipse((55,110,205,260),fill=(216,220,230),outline=(150,155,170),width=4)
    d.ellipse((103,135,157,189),fill=(120,130,150)); d.rounded_rectangle((82,190,178,242),radius=24,fill=(120,130,150))
    d.text((235,115),req.name,font=fit_text(d,req.name,600,32,True),fill=(20,20,25))
    d.text((235,160),"12 posts     1.2K followers     320 following",font=font(20),fill=(40,40,45))
    d.text((55,285),"@"+req.username.lstrip("@"),font=font(22,True),fill=(30,30,35))
    for i,line in enumerate(__import__("textwrap").wrap(req.bio,width=55)[:2]): d.text((55,322+i*30),line,font=font(20),fill=(45,45,50))
    d.line((45,390,855,390),fill=(220,220,225),width=2)
    for i in range(3):
        x=50+i*275
        d.rectangle((x,420,x+250,625),fill=[(232,215,204),(213,225,236),(229,218,239)][i])
        d.text((x+16,590),f"POST {i+1}",font=font(18,True),fill=(60,60,70))
    d.text((50,655),"MOCKUP FIKTIF — BUKAN AKUN NYATA",font=font(16,True),fill=(190,70,70))
    return {**save_image(im,"fake_ig"),"message":"Mockup profil Instagram fiktif berhasil dibuat."}
