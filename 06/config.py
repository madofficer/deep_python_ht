import socket


HOST = socket.gethostbyname(socket.gethostname())
PORT = 8000
FORMAT = "utf-8"
BUFFER_SIZE = 1024

NUM_WORKERS = 5
TOP_K = 5
NUM_THREADS = 5
