import os
from sanic import Sanic, response
from sanic.response import file
from sanic.log import logger
from pathlib import Path
app = Sanic("QRGhost")

BASE_DIR = os.getenv("BASE_DIR", ".")
CERTS_DIR = os.getenv("CERTS_DIR", "certs")

@app.main_process_start
async def check_certs(app, loop):
    if not (Path(CERTS_DIR).is_dir() and Path(f"{CERTS_DIR}/fullchain.pem").exists() and Path(f"{CERTS_DIR}/privkey.pem").exists()):
                logger.warning("!!! SSL certificates not found (fullchain.pem/privkey.pem in certs/).\nIgnore this if running on localhost or with reverse proxy certs")
                

@app.get("/sw.js")
async def service_worker(request):
    resp = await file(f"{BASE_DIR}/sw.js", mime_type="application/javascript")
    resp.headers["Service-Worker-Allowed"] = "/"
    resp.headers["Cache-Control"] = "no-cache"
    return resp

@app.get("/manifest.json")
async def manifest(request):
    return await file(f"{BASE_DIR}/manifest.json", mime_type="application/json")

app.static("/", BASE_DIR, index="index.html", name="root")

if __name__ == "__main__":
    
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8222)),
        ssl=CERTS_DIR if (Path(CERTS_DIR).is_dir() and Path(f"{CERTS_DIR}/fullchain.pem").exists() and Path(f"{CERTS_DIR}/privkey.pem").exists()) else None
    
)
