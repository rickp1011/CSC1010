import threading,socket

PORT = 5050
#socket.gethostbyname(scoket.gethostname())
SERVER = "localhost"
ADDR = (SERVER,PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

#AF_INET ipv4 addressing, SOCK_STREAM tcp socket
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(ADDR)

clients = set()
clients_lock = threading.Lock()

def handle_client(conn,addr):
    print(f"[NEW CONNECTION] {addr} Connected" )
    try:
        connected = True
        while connected:
            msg = conn.recv(1024).decode(FORMAT)
            if not msg:
                break

            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f"[{addr}] {msg}")

            with clients_lock:
                for c in clients:
                    c.sendall(f"[{addr}] {msg}".encode(FORMAT))
    finally:
        with clients_lock:
            clients.remove(conn)
        conn.close()

def start():
    print("[SERVER STARTED]")
    server.listen()
    while True:
        conn, addr = server.accept()
        #Ensure one thread is being modified one at a time
        with clients_lock:
            clients.add(conn)
        #Create a new thread so we can listen from more client to enusre its not blocked
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

start()
