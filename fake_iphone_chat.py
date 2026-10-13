from fastapi import APIRouter
from pydantic import BaseModel, Field
from PIL import Image, ImageDraw
from .common import font, save_image

router = APIRouter(prefix="/api/mockup", tags=["Fake iPhone Chat"])
class ChatRequest(BaseModel):
    contact: str = Field(default="Alex", max_length=50)
    message: str = Field(default="Sampai ketemu nanti ya!", max_length=280)
    side: str = "right"

@router.post("/iphone-chat")
def iphone_chat(req: ChatRequest):
    im=Image.new("RGB",(720,900),(235,235,240)); d=ImageDraw.Draw(im)
    d.rounded_rectangle((110,35,610,865),radius=58,fill=(250,250,252),outline=(50,50,55),width=5)
    d.rounded_rectangle((280,48,440,72),radius=12,fill=(20,20,25))
    d.text((160,105),req.contact[:40],font=font(28,True),fill=(20,20,25))
    d.line((130,150,590,150),fill=(220,220,225),width=2)
    import textwrap
    wrapped=textwrap.wrap(req.message.strip() or "Pesan contoh",width=25)[:7]
    bubble_w=min(390,max(180,max(d.textbbox((0,0),ln,font=font(22))[2] for ln in wrapped)+36))
    bubble_h=28*len(wrapped)+28
    x=590-bubble_w if req.side=="right" else 135
    y=230; color=(36,132,255) if req.side=="right" else (220,222,228)
    txt=(255,255,255) if req.side=="right" else (25,25,30)
    d.rounded_rectangle((x,y,x+bubble_w,y+bubble_h),radius=23,fill=color)
    for i,ln in enumerate(wrapped): d.text((x+18,y+13+i*28),ln,font=font(22),fill=txt)
    d.text((190,785),"Mockup pesan fiktif",font=font(18),fill=(130,130,140))
    d.text((165,820),"SIMULASI • BUKAN BUKTI CHAT",font=font(16,True),fill=(190,70,70))
    return {**save_image(im,"iphone_chat"),"message":"Mockup chat fiktif berhasil dibuat."}
