import pytest
from unittest.mock import patch
import main

@pytest.mark.asyncio
async def test_check_certs_reverse_proxy_true():
    with patch('main.REVERSE_PROXY', True):
        with patch('main.logger.info') as mock_info:
            await main.check_certs(main.app, None)
            mock_info.assert_called_once_with("Running behind reverse proxy - SSL disabled")

@pytest.mark.asyncio
async def test_check_certs_reverse_proxy_false_no_certs():
    with patch('main.REVERSE_PROXY', False):
        with patch('main.CERTS_DIR', 'nonexistent_certs_dir'):
            with patch('main.logger.warning') as mock_warning:
                await main.check_certs(main.app, None)
                mock_warning.assert_called_once()
                assert "SSL certificates not found" in mock_warning.call_args[0][0]

@pytest.mark.asyncio
async def test_check_certs_reverse_proxy_false_with_certs(tmp_path):
    certs_dir = tmp_path / "certs"
    certs_dir.mkdir()
    (certs_dir / "fullchain.pem").touch()
    (certs_dir / "privkey.pem").touch()

    with patch('main.REVERSE_PROXY', False):
        with patch('main.CERTS_DIR', str(certs_dir)):
            with patch('main.logger.warning') as mock_warning:
                await main.check_certs(main.app, None)
                mock_warning.assert_not_called()

@pytest.mark.asyncio
async def test_check_certs_reverse_proxy_false_missing_privkey(tmp_path):
    certs_dir = tmp_path / "certs"
    certs_dir.mkdir()
    (certs_dir / "fullchain.pem").touch()

    with patch('main.REVERSE_PROXY', False):
        with patch('main.CERTS_DIR', str(certs_dir)):
            with patch('main.logger.warning') as mock_warning:
                await main.check_certs(main.app, None)
                mock_warning.assert_called_once()
                assert "SSL certificates not found" in mock_warning.call_args[0][0]

@pytest.mark.asyncio
async def test_check_certs_reverse_proxy_false_missing_fullchain(tmp_path):
    certs_dir = tmp_path / "certs"
    certs_dir.mkdir()
    (certs_dir / "privkey.pem").touch()

    with patch('main.REVERSE_PROXY', False):
        with patch('main.CERTS_DIR', str(certs_dir)):
            with patch('main.logger.warning') as mock_warning:
                await main.check_certs(main.app, None)
                mock_warning.assert_called_once()
                assert "SSL certificates not found" in mock_warning.call_args[0][0]
