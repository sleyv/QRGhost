import pytest
from unittest.mock import patch, MagicMock
import main

@pytest.mark.asyncio
async def test_check_certs_reverse_proxy():
    with patch('main.REVERSE_PROXY', True), \
         patch('main.logger') as mock_logger:
        await main.check_certs(None, None)
        mock_logger.info.assert_called_once_with("Running behind reverse proxy - SSL disabled")
        mock_logger.warning.assert_not_called()

@pytest.mark.asyncio
async def test_check_certs_missing_certs_dir():
    with patch('main.REVERSE_PROXY', False), \
         patch('main.CERTS_DIR', 'fake_certs'), \
         patch('main.Path') as mock_path, \
         patch('main.logger') as mock_logger:

        # Setup Path mock to return False for is_dir()
        mock_path_instance = MagicMock()
        mock_path_instance.is_dir.return_value = False
        mock_path.return_value = mock_path_instance

        await main.check_certs(None, None)

        mock_logger.warning.assert_called_once()
        assert "SSL certificates not found" in mock_logger.warning.call_args[0][0]

@pytest.mark.asyncio
async def test_check_certs_missing_fullchain():
    with patch('main.REVERSE_PROXY', False), \
         patch('main.CERTS_DIR', 'fake_certs'), \
         patch('main.Path') as mock_path, \
         patch('main.logger') as mock_logger:

        def path_side_effect(arg):
            mock = MagicMock()
            if arg == 'fake_certs':
                mock.is_dir.return_value = True
            elif arg == 'fake_certs/fullchain.pem':
                mock.exists.return_value = False
            elif arg == 'fake_certs/privkey.pem':
                mock.exists.return_value = True
            return mock

        mock_path.side_effect = path_side_effect

        await main.check_certs(None, None)
        mock_logger.warning.assert_called_once()

@pytest.mark.asyncio
async def test_check_certs_missing_privkey():
    with patch('main.REVERSE_PROXY', False), \
         patch('main.CERTS_DIR', 'fake_certs'), \
         patch('main.Path') as mock_path, \
         patch('main.logger') as mock_logger:

        def path_side_effect(arg):
            mock = MagicMock()
            if arg == 'fake_certs':
                mock.is_dir.return_value = True
            elif arg == 'fake_certs/fullchain.pem':
                mock.exists.return_value = True
            elif arg == 'fake_certs/privkey.pem':
                mock.exists.return_value = False
            return mock

        mock_path.side_effect = path_side_effect

        await main.check_certs(None, None)
        mock_logger.warning.assert_called_once()

@pytest.mark.asyncio
async def test_check_certs_all_present():
    with patch('main.REVERSE_PROXY', False), \
         patch('main.CERTS_DIR', 'fake_certs'), \
         patch('main.Path') as mock_path, \
         patch('main.logger') as mock_logger:

        def path_side_effect(arg):
            mock = MagicMock()
            if arg == 'fake_certs':
                mock.is_dir.return_value = True
            elif arg == 'fake_certs/fullchain.pem':
                mock.exists.return_value = True
            elif arg == 'fake_certs/privkey.pem':
                mock.exists.return_value = True
            return mock

        mock_path.side_effect = path_side_effect

        await main.check_certs(None, None)
        mock_logger.warning.assert_not_called()
        mock_logger.info.assert_not_called()
