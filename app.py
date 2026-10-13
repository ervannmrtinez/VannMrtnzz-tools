import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from api import tiktok, instagram, stickers, fake_ig, fake_iphone_chat, fake_free_fire, fake_mobile_legends, ml_lookup

BASE = Path(__file__).resolve().parent
app = FastAPI(title="VannMrtnzz API", version="1.1.0",
              description="Downloader publik, sticker generator, mockup kreatif, dan endpoint lookup eksternal.")
app.include_router(tiktok.router)
app.include_router(instagram.router)
app.include_router(stickers.router)
app.include_router(fake_ig.router)
app.include_router(fake_iphone_chat.router)
app.include_router(fake_free_fire.router)
app.include_router(fake_mobile_legends.router)
app.include_router(ml_lookup.router)
app.mount("/outputs", StaticFiles(directory=BASE / "outputs"), name="outputs")

@app.get("/")
def home():
    return FileResponse(BASE / "index.html")

@app.get("/api/health")
def health():
    return {"ok": True, "service": "VannMrtnzz API", "version": "1.1.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=int(os.getenv("PORT", "8000")), reload=False)
