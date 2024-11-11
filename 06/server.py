import socket
import threading
import queue
import requests
import json
import argparse
import config
from collections import Counter
from bs4 import BeautifulSoup


class Worker(threading.Thread):

    def __init__(self, task_queue, result_lock, stats, top_k):
        super().__init__()
        self.task_queue = task_queue
        self.result_lock = result_lock
        self.stats = stats
        self.top_k = top_k

    def run(self):
        while True:
            client_socket, url = self.task_queue.get()

            if url is None:
                break

            try:
                word_count = self.process_url(url)
                response = json.dumps(word_count)
                client_socket.sendall(response.encode(config.FORMAT))
                client_socket.close()
            except Exception as e:
                print(f"URL processing error {url}: {e}")

            with self.result_lock:
                self.stats["processed_urls"] += 1
                print(f"Processed urls count: {self.stats['processed_urls']}")

            self.task_queue.task_done()

    def process_url(self, url):
        response = requests.get(url)
        text = BeautifulSoup(response.text, "html.parser").get_text()
        words = [word.lower() for word in text.split()]
        word_counts = Counter(words)
        return dict(word_counts.most_common(self.top_k))


class MasterServer:
    def __init__(self, host, port, num_workers, top_k):
        self.host = host
        self.port = port
        self.num_workers = num_workers
        self.top_k = top_k
        self.task_queue = queue.Queue()
        self.stats = {"processed_urls": 0}
        self.result_lock = threading.Lock()
        self.shutdown_event = threading.Event()

    def start(self):
        workers = [
            Worker(self.task_queue, self.result_lock, self.stats, self.top_k)
            for _ in range(self.num_workers)
        ]
        for worker in workers:
            worker.start()


        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
                server_socket.bind((self.host, self.port))
                print(f"Server has been started and listens {self.host}:{self.port}")
                server_socket.listen()

                while True:

                    client_socket, addr = server_socket.accept()
                    data = client_socket.recv(config.BUFFER_SIZE).decode(config.FORMAT)

                    if data:
                        url = data.strip()
                        print(f"[GOT URL]: {url} from {addr}")
                        self.task_queue.put((client_socket, url))
        except KeyboardInterrupt:
            print('Server is shutting down...')

        finally:
            for _ in range(self.num_workers):
                self.task_queue.put((None, None))

            for worker in workers:
                worker.join()
            print('Server has been shut down')



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--workers", type=int, required=True, help="num_workers")
    parser.add_argument("-k", "--top_k", type=int, required=True, help="num_top_words")
    args = parser.parse_args()

    server = MasterServer(config.HOST, config.PORT, args.workers, args.top_k)
    server.start()