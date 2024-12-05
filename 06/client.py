import argparse
import threading
import socket
from inspect import cleandoc
from queue import Queue


class Client:
    def __init__(self, host, port, urls, num_threads):
        self.host = host
        self.port = port
        self.urls = urls
        self.num_threads = num_threads
        self.queue = Queue()

    def load_urls(self):
        for url in urls:
            self.queue.put(url)

    def worker(self, thread_id):
        while not self.queue.empty():
            url = self.queue.get()
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_sock:
                    client_sock.connect((self.host, self.port))
                    client_sock.sendall(f"{url}\n".encode("utf-8"))
                    response = client_sock.recv(1024).decode("utf-8").strip()
                    print(f"[Thread-{thread_id}] Server response: {response}")
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

        for t in threads:
            t.join()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Multithreaded client for sending urls"
    )
    parser.add_argument("file", help="path to file with urls")
    parser.add_argument("threads", type=int, help="Number of threads")
    parser.add_argument("--host", default="localhost", help="Host of the server")
    parser.add_argument("--port", default=7777, help="Port of the server")
    args = parser.parse_args()

    try:
        with open(args.file, "r") as f:
            urls = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: File {args.file} not found")
        exit(1)

    client = Client(args.host, args.port, urls, args.threads)
    client.load_urls()
    client.run()
