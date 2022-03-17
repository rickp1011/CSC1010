import socket,time

PORT = 5050
#socket.gethostbyname(scoket.gethostname())
SERVER = "172.20.10.8"
ADDR = (SERVER,PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

def connect():
    #AF_INET ipv4 addressing, SOCK_STREAM tcp socket
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect(ADDR)
    return client

def start():
    connection = connect()
    while True:
        msg = connection.recv(1024).decode(FORMAT)
        print(msg)

start()