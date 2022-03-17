import threading,socket

PORT = 5050
#socket.gethostbyname(scoket.gethostname())
SERVER = "172.0.0.1"
ADDR = (SERVER,PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!disconnect"

#AF_INET ipv4 addressing, SOCK_STREAM tcp socket


clients = set()
clients_lock = threading.Lock()

def handle_client(conn,addr):
    user = conn.recv(1024).decode(FORMAT)
    print(f"[NEW CONNECTION] {addr} {user} established")
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
    print("CSC1010 Chat server, please enter the listening IP address and port.")
    global SERVER, PORT, ADDR
    x,y = input().split()
    SERVER = x
    PORT = int(y)
    ADDR = (SERVER,PORT)
    
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind(ADDR)

    print(f"[SERVER STARTED :{ADDR}]")
    print("Waiting for incoming connections...")
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

