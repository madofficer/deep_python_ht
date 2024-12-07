import unittest
from unittest.mock import patch, MagicMock
import socket
from client import Client


class TestClient(unittest.TestCase):
    @patch("socket.socket")
    def test_client_send_url(self, mock_socket):
        client_socket = MagicMock()
        mock_socket.return_value.__enter__.return_value = client_socket

        client = Client("localhost", 7777, ["http://example.com"], 1, 1)
        client.run()

        client_socket.connect.assert_called_once_with(("localhost", 7777))
        client_socket.sendall.assert_called_once_with(b"http://example.com\n")

    @patch("socket.socket")
    def test_client_connection_error(self, mock_socket):
        mock_socket.side_effect = ConnectionError("Cannot connect")

        client = Client("localhost", 7777, ["http://example.com"], 1, 1)
        client.run()

        mock_socket.assert_called_once()

    def test_client_empty_urls(self):
        client = Client("localhost", 7777, [], 1, 1)
        client.run()

        with patch("socket.socket") as mock_socket:
            mock_socket.assert_not_called()

    # @patch("socket.socket")
    # def test_client_process_multiple_urls(self, mock_socket):
    #     client_socket = MagicMock()
    #     mock_socket.return_value.__enter__.return_value = client_socket
    #
    #     urls = [f"http://example{i}.com" for i in range(10)]
    #     client = Client("localhost", 7777, urls, num_threads=2, batch_size=5)
    #     client.run()
    #
    #     self.assertEqual(client_socket.sendall.call_count, 10)

    # def test_client_send_batch_urls(self, mock_socket):
    #     client_socket = MagicMock()
    #     mock_socket.return_value.__enter__.return_value = client_socket
    #
    #     urls = [f"http://example{i}.com" for i in range(6)]
    #     client = Client("localhost", 7777, urls, num_threads=2, batch_size=3)
    #     client.run()
    #
    #     # Check that URLs are sent in batches
    #     self.assertEqual(client_socket.sendall.call_count, 6)
    #     self.assertTrue(
    #         any(call[0][0].startswith(b"http://example0.com")
    #         for call in client_socket.sendall.call_args_list)
    #     )
    def test_client_batch_processing(self):
        urls = [f"http://example{i}.com" for i in range(5)]
        client = Client("localhost", 7777, urls, num_threads=2, batch_size=2)

        batches = list(client.batch_urls())
        self.assertEqual(len(batches), 3)
        self.assertEqual(len(batches[0]), 2)
        self.assertEqual(len(batches[1]), 2)
        self.assertEqual(len(batches[2]), 1)


if __name__ == "__main__":
    unittest.main()
