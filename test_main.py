import pytest
from main import app

def test_service_worker():
    request, response = app.test_client.get("/sw.js")
    assert response.status == 200
    assert "application/javascript" in response.content_type
    assert response.headers["Service-Worker-Allowed"] == "/"
    assert response.headers["Cache-Control"] == "no-cache"

def test_manifest():
    request, response = app.test_client.get("/manifest.json")
    assert response.status == 200
    assert "application/json" in response.content_type

def test_index():
    request, response = app.test_client.get("/")
    assert response.status == 200
    assert "text/html" in response.content_type

    request, response = app.test_client.get("/index.html")
    assert response.status == 200
    assert "text/html" in response.content_type

def test_icon_192():
    request, response = app.test_client.get("/icon-192.png")
    assert response.status == 200
    assert "image/png" in response.content_type

def test_icon_512():
    request, response = app.test_client.get("/icon-512.png")
    assert response.status == 200
    assert "image/png" in response.content_type
