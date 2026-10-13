# VannMrtnzz Complete

## Menjalankan
Python 3.10+ direkomendasikan.

```bash
pip install -r requirements.txt
python app.py
```

Buka http://127.0.0.1:8000. Dokumentasi interaktif API tersedia di http://127.0.0.1:8000/docs.

## API routes
- `POST /api/download/tiktok` — body `{"url":"https://www.tiktok.com/...","mode":"video"}`
- `POST /api/download/instagram` — body `{"url":"https://www.instagram.com/p/...","mode":"all"}`
- `POST /api/sticker/monochrome` — body `{"text":"VannMrtnzz","style":"bold"}`
- `POST /api/sticker/brat` — body `{"text":"brat"}`
- `POST /api/mockup/fake-instagram` — body `{"name":"Vann","username":"vann","bio":"creative"}`
- `POST /api/mockup/iphone-chat` — body `{"contact":"Alex","message":"Hai","side":"right"}`
- `POST /api/mockup/free-fire` — body `{"nickname":"VANN","player_id":"123"}`
- `POST /api/mockup/mobile-legends` — body `{"nickname":"Vann","user_id":"123","rank":"Mythic"}`
- `POST /api/mobile-legends/lookup` — body `{"user_id":"123","server_id":"1234"}`

## Catatan
- `index.html` adalah frontend tunggal dengan CSS dan JavaScript inline. `app.py` dan folder `api/` tetap harus berada di server untuk fungsi backend.
- TikTok/Instagram hanya untuk media publik yang dapat diakses; tidak ada jaminan akses bila konten dibatasi atau platform berubah.
- Mockup fake IG/chat/game diberi label simulasi dan bukan data resmi.
- Lookup Mobile Legends membutuhkan provider eksternal yang sah melalui `ML_LOOKUP_API_URL`. Tidak ada endpoint API provider palsu yang ditanam.
