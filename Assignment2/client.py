import socket,time

PORT = 5050
#socket.gethostbyname(scoket.gethostname())
SERVER = "localhost"
ADDR = (SERVER,PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

def connect():
    #AF_INET ipv4 addressing, SOCK_STREAM tcp socket
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect(ADDR)
    return client

def send(client,msg):
    message = msg.encode(FORMAT)
    client.send(message)

def start():   
    ans = input('Would you like to connect (yes/no)? ')
    if ans.lower() != 'yes':
        return

    connection = connect()
    while True:
        msg = input("Message (q for quit): ")
        if msg == 'q':
            break
        send(connection,msg)

    send(connection,DISCONNECT_MESSAGE)
    time.sleep(1)
    print("Disconnected from chatroom")

start()