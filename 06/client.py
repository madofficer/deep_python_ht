import socket
import threading
import argparse
import config


class Client(threading.Thread):
    def __init__(self, server_host, server_port, url):
        super().__init__()
        self.server_host = server_host
        self.server_port = server_port
        self.url = url

    def run(self):

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((self.server_host, self.server_port))
            client_socket.sendall((self.url.encode("utf-8")))

            response = client_socket.recv(1024).decode("utf-8")
            print(f"{self.url}: {response}")


def load_urls(filename):
    with open(filename) as f:
        return [line.strip() for line in f]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("threads", type=int, help="threads_num")
    parser.add_argument("filename", type=str, help="url_file")
    args = parser.parse_args()

    HOST = config.HOST
    PORT = config.PORT
    urls = load_urls(args.filename)

    threads = []
    for i in range(args.threads):
        for url in urls[i :: args.threads]:
            client = Client(HOST, PORT, url)
            client.start()
            threads.append(client)

    for thread in threads:
        thread.join()
