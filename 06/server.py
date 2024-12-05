import argparse
import queue
import re
import socket
import threading
from collections import Counter
from logging.config import listen

import requests


class Worker(threading.Thread):
    def __init__(self, worker_id, task_queue, stats, top_k):
        super().__init__(daemon=True)
        self.worker_id = worker_id
        self.task_queue = task_queue
        self.stats = stats
        self.top_k = top_k

    def run(self):
        while True:
            url = self.task_queue.get()
            if url is None:
                break
            print(f"[Worker - {self.worker_id}] Processing URL: {url}")
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                top_words = self.word_counter(response.text)
                result = {"url": url, "top_words": top_words}
                print(f"[Worker-{self.worker_id}] Completed: {result}")
                with threading.Lock():
                    self.stats[url] = result
            except ConnectionError as e:
                print(f"[Worker-{self.worker_id}] Error processing {url}: {e}")
            finally:
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
        self.stats = {}
        self.workers = []

    def start_workers(self):
        for i in range(self.num_workers):
            worker = Worker(i, self.task_queue, self.stats, self.top_k)
            worker.start()
            self.workers.append(worker)

    def stop_workers(self):
        for _ in range(self.num_workers):
            self.task_queue.put(None)

        for worker in self.workers:
            worker.join()

    def handle_client(self, client_sock):
        with client_sock:
            data = client_sock.recv(1024).decode("utf-8").strip()
            if data:
                print(f"Received URL: {data}")
                self.task_queue.put(data)
                client_sock.sendall(b"URL received\n")

    def run(self):
        self.start_workers()

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serv_sock:
            serv_sock.bind((self.host, self.port))
            serv_sock.listen()
            print(f"Server listening on {self.host}:{self.port}")

            try:
                while True:
                    client_sock, addr = serv_sock.accept()
                    print(f"Connected by {addr}")
                    threading.Thread(
                        target=self.handle_client, args=(client_sock,), daemon=True
                    ).start()
            except KeyboardInterrupt:
                print("Shutting down Server...")
            finally:
                self.stop_workers()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Master-worker server args")
    parser.add_argument(
        "-w", "--workers", type=int, default=4,
        help="Number of workers"
    )
    parser.add_argument(
        "-k", "--top_k", type=int, default=10,
        help="Number of top frequent words"
    )
    parser.add_argument("--host", default="localhost",
                        help="Host to bind the server")
    parser.add_argument("--port", default=7777,
                        help="Port to bind the server")
    args = parser.parse_args()

    server = Master(args.host, args.port, args.workers, args.top_k)
    server.run()
