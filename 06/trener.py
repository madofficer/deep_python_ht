import socket
import threading
import time


HEADER = 64
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT!"
PORT = 5500
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
print(SERVER)
print(socket.gethostname())

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Address Family
server.bind(ADDR)


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected", end="\n")
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)

            if msg == DISCONNECT_MSG:
                connected = False

            print(f"[{addr}], {msg}")
            conn.send("msg received".encode(FORMAT))
    conn.close()


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        print("Waiting for client...", end="\n")
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}", end="\n")


print(f"Starting server")
start()
