from pathlib import Path
from fastapi import HTTPException
from urllib.parse import urlparse
import os, uuid, textwrap
from PIL import Image, ImageDraw, ImageFont

BASE = Path(__file__).resolve().parent.parent
OUTPUTS = BASE / "outputs"
OUTPUTS.mkdir(exist_ok=True)

def valid_platform_url(raw: str, platform: str):
    parsed = urlparse(raw)
    if parsed.scheme not in ("http", "https") or not parsed.hostname:
        raise HTTPException(400, "URL tidak valid.")
    host = parsed.hostname.lower().split(":")[0]
    allowed = {
        "tiktok": ("tiktok.com", "www.tiktok.com", "m.tiktok.com", "vm.tiktok.com", "vt.tiktok.com"),
        "instagram": ("instagram.com", "www.instagram.com", "instagr.am", "www.instagr.am")
    }[platform]
    if not any(host == h or host.endswith("." + h) for h in allowed):
        raise HTTPException(400, f"URL harus berasal dari {platform}.")
    return raw

def download_with_ytdlp(raw, platform, mode="all"):
    try:
        import yt_dlp
    except ImportError:
        raise HTTPException(503, "yt-dlp belum terpasang. Jalankan pip install -r requirements.txt.")
    valid_platform_url(raw, platform)
    opts = {"quiet": True, "no_warnings": True, "skip_download": True, "noplaylist": True,
            "extract_flat": False, "socket_timeout": 15}
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(raw, download=False)
    except Exception as exc:
        raise HTTPException(502, f"Gagal mengambil metadata. Konten mungkin privat, dibatasi, atau provider berubah. Detail: {str(exc)[:180]}")
    entries = info.get("entries") or [info]
    items = []
    for entry in entries:
        if not entry:
            continue
        formats = entry.get("formats") or []
        chosen = None
        if mode == "video":
            videos = [f for f in formats if f.get("url") and f.get("vcodec") not in (None, "none")]
            if videos:
                chosen = sorted(videos, key=lambda f: (f.get("height") or 0, f.get("tbr") or 0))[-1]
        if not chosen and entry.get("url"):
            chosen = entry
        if not chosen and formats:
            chosen = next((f for f in reversed(formats) if f.get("url")), None)
        if chosen and chosen.get("url"):
            items.append({"url": chosen["url"], "filename": (entry.get("title") or "media")[:80]})
    if not items:
        raise HTTPException(502, "Provider tidak memberikan URL media yang bisa diakses.")
    return {"message": "URL media publik ditemukan. Link bisa kedaluwarsa sesuai kebijakan platform.", "items": items}

def font(size=28, bold=False):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf"
    ]
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size=size)
    return ImageFont.load_default()

def save_image(image, prefix):
    name = f"{prefix}_{uuid.uuid4().hex[:10]}.png"
    image.save(OUTPUTS / name, "PNG")
    return {"url": f"/outputs/{name}", "filename": name}

def fit_text(draw, text, max_width, start_size=60, bold=True):
    text = text or " "
    for size in range(start_size, 12, -2):
        f = font(size, bold)
        if draw.textbbox((0, 0), text, font=f)[2] <= max_width:
            return f
    return font(14, bold)

def card(title, subtitle, accent=(110,160,255), size=(900,560)):
    im = Image.new("RGB", size, (12,18,32))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((28,28,size[0]-28,size[1]-28), radius=28, fill=(20,29,49), outline=accent, width=3)
    d.rounded_rectangle((55,55,170,65), radius=5, fill=accent)
    d.text((58,100), title[:70], font=fit_text(d,title[:70],size[0]-120,44,True), fill=(245,247,255))
    d.text((60,170), subtitle[:100], font=font(24), fill=(170,185,210))
    d.text((60,size[1]-85), "SIMULASI • BUKAN DATA RESMI", font=font(18,True), fill=(255,196,111))
    return im
