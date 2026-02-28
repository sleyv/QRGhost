import os
from sanic import Sanic, response
from sanic.response import file
from sanic.log import logger
from pathlib import Path

app = Sanic("QRGhost")

BASE_DIR = os.getenv("BASE_DIR", ".")
CERTS_DIR = os.getenv("CERTS_DIR", "certs")
REVERSE_PROXY = os.getenv("REVERSE_PROXY", "false").lower() == "true"

@app.main_process_start
async def check_certs(app, loop):
    if REVERSE_PROXY:
        logger.info("Running behind reverse proxy - SSL disabled")
        return
    
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

@app.get("/", name="root")
@app.get("/index.html", name="index_html")
async def index(request):
    return await file(f"{BASE_DIR}/index.html", mime_type="text/html")

@app.get("/icon-192.png")
async def icon_192(request):
    return await file(f"{BASE_DIR}/icon-192.png", mime_type="image/png")

@app.get("/icon-512.png")
async def icon_512(request):
    return await file(f"{BASE_DIR}/icon-512.png", mime_type="image/png")

if __name__ == "__main__":
    ssl_enabled = False
    
    if not REVERSE_PROXY:
        if Path(CERTS_DIR).is_dir() and Path(f"{CERTS_DIR}/fullchain.pem").exists() and Path(f"{CERTS_DIR}/privkey.pem").exists():
            ssl_enabled = True
    
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8222)),
        ssl=CERTS_DIR if ssl_enabled else None
    )

