import os
import asyncio
from pathlib import Path
from unittest.mock import patch

import pytest
from sanic_testing import TestManager

from main import app, check_certs

TestManager(app)

def test_index_route():
    request, response = app.test_client.get("/")
    assert response.status == 200

def test_sw_route():
    request, response = app.test_client.get("/sw.js")
    assert response.status == 200
    assert response.headers.get("Service-Worker-Allowed") == "/"
    assert response.headers.get("Cache-Control") == "no-cache"
    assert "application/javascript" in response.content_type

def test_manifest_route():
    request, response = app.test_client.get("/manifest.json")
    assert response.status == 200
    assert "application/json" in response.content_type

@pytest.mark.asyncio
async def test_check_certs_reverse_proxy_true():
    with patch("main.REVERSE_PROXY", True):
        with patch("main.logger.info") as mock_logger_info:
            await check_certs(app, asyncio.get_event_loop())
            mock_logger_info.assert_called_once_with("Running behind reverse proxy - SSL disabled")

@pytest.mark.asyncio
async def test_check_certs_no_certs():
    with patch("main.REVERSE_PROXY", False):
        with patch("main.logger.warning") as mock_logger_warning:
            with patch.object(Path, "is_dir", return_value=False):
                await check_certs(app, asyncio.get_event_loop())
                mock_logger_warning.assert_called_once()
                assert "SSL certificates not found" in mock_logger_warning.call_args[0][0]

@pytest.mark.asyncio
async def test_check_certs_with_certs():
    with patch("main.REVERSE_PROXY", False):
        with patch("main.logger.warning") as mock_logger_warning:
            def mock_exists(self):
                return True
            with patch.object(Path, "is_dir", return_value=True):
                with patch.object(Path, "exists", new=mock_exists):
                    await check_certs(app, asyncio.get_event_loop())
                    mock_logger_warning.assert_not_called()
