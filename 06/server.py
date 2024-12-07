import argparse
import json
import queue
import re
import socket
import threading
import time
from collections import Counter
from time import perf_counter

import requests


class Worker(threading.Thread):
    def __init__(self, worker_id, task_queue, result_queue, top_k):
        super().__init__(daemon=True)
        self.worker_id = worker_id
        self.task_queue = task_queue
        self.result_queue = result_queue
        self.top_k = top_k

    def run(self):
        while True:
            task = self.task_queue.get()
            if task is None:
                break

            url, client_id = task
            print(f"[Worker - {self.worker_id}] Processing URL: {url}")
            start_time = time.perf_counter()
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                top_words = self.word_counter(response.text)
                elapsed_time = time.perf_counter() - start_time
                result = {
                    "status": "success",
                    "url": url,
                    "top_words": top_words,
                    "elapsed_time": elapsed_time,
                }
            except Exception as e:
                elapsed_time = time.perf_counter() - start_time
                result = {
                    "status": "error",
                    "url": url,
                    "error": e,
                    "elapsed_time": elapsed_time,
                }

            self.result_queue.put((client_id, result))
            self.task_queue.task_done()

    def word_counter(self, text):
        words = re.findall(r"\b\w+\b", text.lower())
        return Counter(words).most_common(self.top_k)


class Master:
    def __init__(self, host, port, num_workers, top_k):
        self.host = host
        self.port = port
        self.num_workers = num_workers
        self.top_k = top_k
        self.task_queue = queue.Queue()
        self.result_queue = queue.Queue()
        self.stats = {"processed": 0, "total_time": 0.0}
        self.stats_lock = threading.Lock()
        self.workers = []
        self.client_connections = {}

    def start_workers(self):
        for i in range(self.num_workers):
            worker = Worker(i, self.task_queue, self.result_queue, self.top_k)
            worker.start()
            self.workers.append(worker)

    def stop_workers(self):
        for _ in range(self.num_workers):
            self.task_queue.put(None)
        for worker in self.workers:
            worker.join()

    def handle_client(self, client_sock, client_id):
        try:
            data = client_sock.recv(1024).decode("utf-8").strip()
            if data:
                print(f"Received URL from Client {client_id}: {data}")

                self.task_queue.put((data, client_id))
            else:
                print(f"Client-{client_id} sent no data. Closing connection.")
                client_sock.close()
                del self.client_connections[client_id]
        except Exception as e:
            print(f"Error handling client-{client_id}: {e}")

    def send_results(self):
        while True:
            data = self.result_queue.get()
            if data is None:
                print("Nothing to send")
                break
            client_id, result = data
            conn = self.client_connections.get(client_id)
            if conn:
                try:
                    print(f"Sending result to Client-{client_id}")
                    conn.sendall(json.dumps(result).encode("utf-8"))
                except Exception as e:
                    print(f"Error sending result to Client-{client_id}: {e}")
                finally:
                    conn.close()
                    del self.client_connections[client_id]

            with self.stats_lock:
                self.stats["processed"] += 1
                self.stats["total_time"] += result.get("elapsed_time", 0.0)
                print(
                    f"Total URLs processed: {self.stats["processed"]}, "
                    f"Total time: {self.stats["total_time"]:2f} sec."
                )

    def run(self):
        self.start_workers()
        threading.Thread(target=self.send_results, daemon=True).start()

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serv_sock:
            serv_sock.bind((self.host, self.port))
            serv_sock.listen()
            print(f"Server listening on {self.host}:{self.port}\n")

            client_id = 0
            try:
                while True:
                    client_sock, addr = serv_sock.accept()
                    print(f"Connected to Client-{client_id} by {addr}")
                    self.client_connections[client_id] = client_sock
                    threading.Thread(
                        target=self.handle_client,
                        args=(client_sock, client_id),
                        daemon=True,
                    ).start()
                    client_id += 1
            except KeyboardInterrupt:
                print("Shutting down Server...")
            finally:
                self.stop_workers()
                print(
                    f"Total URLs processed: {self.stats['processed']}, "
                    f"Total time: {self.stats['total_time']:.2f} seconds"
                )


def server_arg_parse():
    parser = argparse.ArgumentParser(description="Master-worker server args")
    parser.add_argument(
        "-w", "--workers", type=int, default=4, help="Number of workers"
    )
    parser.add_argument(
        "-k", "--top_k",
        type=int,
        default=10,
        help="Number of top frequent words"
    )
    parser.add_argument(
        "--host",
        default="localhost",
        help="Host to bind the server"
    )
    parser.add_argument(
        "--port",
        default=7777,
        help="Port to bind the server"
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = server_arg_parse()
    server = Master(args.host, args.port, args.workers, args.top_k)
    server.run()
