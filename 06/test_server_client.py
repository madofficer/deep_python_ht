import unittest
from unittest.mock import patch, MagicMock
import socket
import threading
import queue
import json
import requests
from server import Master, Worker


class TestWorker(unittest.TestCase):
    def setUp(self):
        self.task_queue = queue.Queue()
        self.result_queue = queue.Queue()
        self.worker = Worker(
            worker_id=1,
            task_queue=self.task_queue,
            result_queue=self.result_queue,
            top_k=3,
        )

    def test_word_counter_empty_text(self):
        self.assertEqual(self.worker.word_counter(""), [])

    def test_word_counter(self):
        text = "hello world! Hello world world."
        expected = [("world", 3), ("hello", 2)]
        self.assertEqual(self.worker.word_counter(text), expected)

    @patch("server.requests.get")
    def test_worker_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = "test test example example example"

        self.task_queue.put(("http://example.com", 1))
        self.task_queue.put(None)  # Signal worker to stop

        self.worker.run()
        client_id, result = self.result_queue.get()

        self.assertEqual(client_id, 1)
        self.assertEqual(result["status"], "success")
        self.assertIn("top_words", result)
        self.assertEqual(result["top_words"], [("example", 3), ("test", 2)])

    @patch("server.requests.get")
    def test_worker_failure(self, mock_get):
        mock_get.side_effect = Exception("Connection error")

        self.task_queue.put(("http://invalid-url", 1))
        self.task_queue.put(None)  # Signal worker to stop

        self.worker.run()
        client_id, result = self.result_queue.get()

        self.assertEqual(client_id, 1)
        self.assertEqual(result["status"], "error")
        self.assertIn("error", result)

    @patch("server.requests.get")
    def test_worker_large_response(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = "word " * 1000

        self.task_queue.put(("http://example.com", 1))
        self.task_queue.put(None)

        self.worker.run()

        _, result = self.result_queue.get_nowait()
        self.assertEqual(result["top_words"], [("word", 1000)])

    @patch("server.requests.get")
    def test_worker_http_error(self, mock_get):
        mock_get.side_effect = requests.exceptions.HTTPError("404 Not Found")

        self.task_queue.put(("http://example.com", 1))
        self.task_queue.put(None)

        self.worker.run()

        _, result = self.result_queue.get_nowait()
        self.assertEqual(result["status"], "error")
        self.assertIn("error", result)


class TestMaster(unittest.TestCase):
    def setUp(self):
        self.master = Master(
            host="localhost",
            port=7777,
            num_workers=2,
            top_k=5
        )
        self.master.start_workers()

    def tearDown(self):
        self.master.stop_workers()

    def test_master_initialization(self):
        master = Master(host="127.0.0.1", port=8888, num_workers=5, top_k=10)
        self.assertEqual(master.host, "127.0.0.1")
        self.assertEqual(master.port, 8888)
        self.assertEqual(master.num_workers, 5)
        self.assertEqual(master.top_k, 10)

    def test_send_results_updates_statistics(self):
        result = {
            "status": "success",
            "url": "http://example.com",
            "top_words": [("test", 3)],
            "elapsed_time": 2.5,
        }
        self.master.result_queue.put((1, result))
        self.master.result_queue.put(None)

        send_thread = threading.Thread(
            target=self.master.send_results,
            daemon=True
        )
        send_thread.start()
        send_thread.join()

        self.assertEqual(self.master.stats["processed"], 1)
        self.assertAlmostEqual(self.master.stats["total_time"], 2.5)


class TestMasterHandleClient(unittest.TestCase):
    def setUp(self):
        self.master = Master(
            host="localhost",
            port=7777,
            num_workers=1,
            top_k=3
        )

    def test_handle_client_with_valid_data(self):
        client_mock = MagicMock()
        client_mock.recv.return_value = b"http://example.com\n"

        self.master.handle_client(client_mock, client_id=1)

        # Проверяем, что URL добавлен в очередь задач
        task = self.master.task_queue.get_nowait()
        self.assertEqual(task, ("http://example.com", 1))

    def test_handle_client_with_empty_data(self):
        client_mock = MagicMock()
        client_mock.recv.return_value = b""

        self.master.handle_client(client_mock, client_id=1)

        # Проверяем, что клиент был закрыт
        client_mock.close.assert_called()

    def test_handle_client_with_invalid_data(self):
        client_mock = MagicMock()
        client_mock.recv.return_value = b""

        self.master.handle_client(client_mock, client_id=1)

        client_mock.close.assert_called_once()
        self.assertNotIn(1, self.master.client_connections)

    # def test_handle_client_with_exception(self):
    #     client_mock = MagicMock()
    #     client_mock.recv.side_effect = Exception("Socket error")
    #
    #     self.master.handle_client(client_mock, client_id=1)
    #
    #     client_mock.close.assert_called_once()
    #     self.assertNotIn(1, self.master.client_connections)


class TestMasterWorkers(unittest.TestCase):
    def test_start_and_stop_workers(self):
        master = Master(host="localhost", port=7777, num_workers=2, top_k=3)

        master.start_workers()
        self.assertEqual(len(master.workers), 2)

        for worker in master.workers:
            self.assertTrue(worker.is_alive())

        master.stop_workers()
        for worker in master.workers:
            self.assertFalse(worker.is_alive())


class TestMasterSendResults(unittest.TestCase):
    def setUp(self):
        self.master = Master(
            host="localhost",
            port=7777,
            num_workers=1,
            top_k=3
        )
        self.client_mock = MagicMock()
        self.master.client_connections[1] = self.client_mock

    def test_send_results_success(self):
        result = {
            "status": "success",
            "url": "http://example.com",
            "top_words": [("test", 5)],
            "elapsed_time": 1.23,
        }
        self.master.result_queue.put((1, result))
        self.master.result_queue.put(None)

        self.master.send_results()

        self.client_mock.sendall.assert_called_once()
        sent_data = self.client_mock.sendall.call_args[0][0].decode("utf-8")
        self.assertIn('"status": "success"', sent_data)

        self.client_mock.close.assert_called_once()


class TestWorkerBatchProcessing(unittest.TestCase):
    @patch("server.requests.get")
    def test_worker_processing_batches(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = "word " * 10

        task_queue = queue.Queue()
        result_queue = queue.Queue()

        worker = Worker(
            worker_id=1,
            task_queue=task_queue,
            result_queue=result_queue,
            top_k=5
        )
        tasks = [("http://example1.com", 1), ("http://example2.com", 2)]
        for task in tasks:
            task_queue.put(task)

        task_queue.put(None)
        worker.run()

        results = []
        while not result_queue.empty():
            results.append(result_queue.get_nowait())

        self.assertEqual(len(results), 2)
        self.assertTrue(
            all(result[1]["status"] == "success" for result in results)
        )


if __name__ == "__main__":
    unittest.main()
