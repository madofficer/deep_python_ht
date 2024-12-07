import argparse
import json
import threading
import socket
from queue import Queue


class Client:
    def __init__(self, host, port, urls, num_threads, batch_size):
        self.host = host
        self.port = port
        self.urls = urls
        self.num_threads = num_threads
        self.batch_size = batch_size
        self.queue = Queue(maxsize=batch_size)

    def batch_urls(self):
        for i in range(0, len(self.urls), self.batch_size):
            yield self.urls[i:i + self.batch_size]

    def load_urls(self):
        for url in self.urls:
            self.queue.put(url)

    def worker(self, thread_id):
        print(f"[Thread-{thread_id}] started")
        while True:
            url = self.queue.get()
            if url is None:
                break
            try:
                with socket.socket(
                        socket.AF_INET, socket.SOCK_STREAM
                ) as client_sock:
                    client_sock.connect((self.host, self.port))
                    client_sock.sendall(f"{url}\n".encode("utf-8"))
                    response = client_sock.recv(4096).decode("utf-8").strip()
                    json_resp = (
                        json.loads(response)
                        if response else "empty answer"
                    )
                    print(f"[Thread-{thread_id}] Server response: {json_resp}")
            except ConnectionError as e:
                print(f"[Thread-{thread_id}] Error sending URL {url} : {e}")
            finally:
                self.queue.task_done()

    def run(self):
        threads = []
        for i in range(self.num_threads):
            t = threading.Thread(target=self.worker, args=(i,), daemon=True)
            threads.append(t)
            t.start()

        for batch in self.batch_urls():
            for url in batch:
                self.queue.put(url)
            self.queue.join()

        for _ in range(self.num_threads):
            self.queue.put(None)

        for t in threads:
            t.join()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Multithreaded client for sending urls"
    )
    parser.add_argument("file", help="path to file with urls")
    parser.add_argument("threads", type=int, help="Number of threads")
    parser.add_argument(
        "--host",
        default="localhost",
        help="Host of the server"
    )
    parser.add_argument(
        "--port",
        default=7777,
        help="Port of the server")
    parser.add_argument(
        "--batch_size",
        type=int,
        default=3,
        help="Number of URLs to process per batch"
    )
    args = parser.parse_args()

    try:
        with open(args.file, "r", encoding="utf-8") as f:
            urls = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: File {args.file} not found")
        sys.exit()

    client = Client(args.host, args.port, urls, args.threads, args.batch_size)
    client.run()
