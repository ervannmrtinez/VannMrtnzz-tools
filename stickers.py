from fastapi import APIRouter
from pydantic import BaseModel, Field
from PIL import Image, ImageDraw
from .common import font, fit_text, save_image

router = APIRouter(prefix="/api/sticker", tags=["Sticker Generator"])
class TextRequest(BaseModel):
    text: str = Field(default="VannMrtnzz", max_length=280)
    style: str = "bold"

@router.post("/monochrome")
def monochrome_sticker(req: TextRequest):
    im = Image.new("RGBA", (1000, 420), (0,0,0,0))
    d = ImageDraw.Draw(im)
    text = req.text.strip() or "VannMrtnzz"
    f = fit_text(d, text, 900, 76, True)
    box = d.textbbox((0,0), text, font=f, stroke_width=2)
    x, y = (1000-(box[2]-box[0]))//2, (420-(box[3]-box[1]))//2 - box[1]
    if req.style == "outline":
        d.text((x,y), text, font=f, fill=(255,255,255,255), stroke_width=4, stroke_fill=(15,15,15,255))
    elif req.style == "minimal":
        d.text((x,y), text, font=font(max(20, f.size-8), False), fill=(20,20,20,255))
    else:
        d.text((x,y), text, font=f, fill=(255,255,255,255), stroke_width=5, stroke_fill=(10,10,10,255))
    return {**save_image(im, "monochrome"), "message":"Stiker monochrome berhasil dibuat."}

@router.post("/brat")
def brat_sticker(req: TextRequest):
    im = Image.new("RGB", (900, 900), (184,255,77))
    d = ImageDraw.Draw(im)
    text = req.text.strip() or "brat"
    words = text.split()
    lines, line = [], ""
    for word in words:
        trial = (line + " " + word).strip()
        if d.textbbox((0,0), trial, font=font(100, True))[2] > 800 and line:
            lines.append(line); line = word
        else:
            line = trial
    if line: lines.append(line)
    lines = lines[:5]
    sizes = [fit_text(d, ln, 800, 100, True) for ln in lines]
    heights = [d.textbbox((0,0), ln, font=f)[3] for ln,f in zip(lines,sizes)]
    y = (900-sum(heights)-12*(len(lines)-1))//2
    for ln,f,h in zip(lines,sizes,heights):
        d.text((50,y), ln, font=f, fill=(18,20,14)); y += h+12
    return {**save_image(im, "brat"), "message":"Stiker BRAT berhasil dibuat."}
