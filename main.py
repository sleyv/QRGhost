import os
import ssl
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

app.static("/", BASE_DIR, index="index.html", name="root")

if __name__ == "__main__":
    ssl_context = None
    
    if not REVERSE_PROXY:
        cert_path = Path(f"{CERTS_DIR}/fullchain.pem")
        key_path = Path(f"{CERTS_DIR}/privkey.pem")

        if Path(CERTS_DIR).is_dir() and cert_path.exists() and key_path.exists():
            try:
                ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
                ssl_context.load_cert_chain(certfile=str(cert_path), keyfile=str(key_path))
            except Exception as e:
                logger.error(f"Failed to load SSL certificates: {e}")
                ssl_context = None
    
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8222)),
        ssl=ssl_context,
        single_process=True
    )
