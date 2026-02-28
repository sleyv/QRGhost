import pytest
from sanic_testing import TestManager
from main import app

# Bind test manager to the app
TestManager(app)

def test_service_worker_endpoint():
    """Test that the /sw.js endpoint returns the correct file and headers."""
    request, response = app.test_client.get("/sw.js")

    assert response.status == 200

    # Check mime type (can be application/javascript or text/javascript depending on OS/Sanic)
    assert "javascript" in response.content_type.lower()

    # Check headers
    assert response.headers.get("Service-Worker-Allowed") == "/"
    assert response.headers.get("Cache-Control") == "no-cache"

def test_manifest_endpoint():
    """Test that the /manifest.json endpoint returns the correct file."""
    request, response = app.test_client.get("/manifest.json")

    assert response.status == 200
    assert "application/json" in response.content_type.lower()
