import pytest
from main import app

def test_service_worker():
    request, response = app.test_client.get("/sw.js")
    assert response.status == 200
    assert response.headers.get("Service-Worker-Allowed") == "/"
    assert response.headers.get("Cache-Control") == "no-cache"
    assert "application/javascript" in response.headers.get("Content-Type", "")
    assert "const CACHE" in response.text

def test_manifest():
    request, response = app.test_client.get("/manifest.json")
    assert response.status == 200
    assert "application/json" in response.headers.get("Content-Type", "")
    assert '"name"' in response.text
