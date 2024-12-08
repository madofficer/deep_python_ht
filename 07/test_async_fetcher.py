import unittest
from unittest.mock import patch, AsyncMock, MagicMock
import asyncio
import aiohttp
import aiofiles
from async_url_fetcher import fetch_url, process_urls, parse_fetcher_args


class TestURLFetcher(unittest.IsolatedAsyncioTestCase):
    @patch("aiohttp.ClientSession.get")
    async def test_fetch_url_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.text.return_value = asyncio.Future()
        mock_response.text.return_value.set_result("response content")
        mock_get.return_value.__aenter__.return_value = mock_response

        async with aiohttp.ClientSession() as session:
            content = await fetch_url(session, "http://example.com")

        self.assertEqual(content, "response content")

    @patch("aiohttp.ClientSession.get")
    async def test_fetch_url_failure(self, mock_get):
        mock_get.side_effect = Exception("Network error")

        async with aiohttp.ClientSession() as session:
            content = await fetch_url(session, "http://example.com")

        self.assertIsNone(content)

    @patch("async_url_fetcher.fetch_url")
    async def test_process_urls(self, mock_fetch_url):
        await process_urls("urls.txt", 2)
        self.assertEqual(mock_fetch_url.call_count, 5)

    @patch("async_url_fetcher.fetch_url")
    async def test_process_urls_with_empty_file(self, mock_fetch_url):
        with open("empty_urls.txt", "w", encoding='utf-8'):
            pass
        await process_urls("empty_urls.txt", 2)
        self.assertEqual(mock_fetch_url.call_count, 0)

    @patch("argparse.ArgumentParser.parse_args")
    def test_parse_fetcher_args(self, mock_parse_args):
        mock_parse_args.return_value.file = "dummy.txt"
        mock_parse_args.return_value.concurrent = 5

        args = parse_fetcher_args()

        self.assertEqual(args.file, "dummy.txt")
        self.assertEqual(args.concurrent, 5)


if __name__ == "__main__":
    unittest.main()
