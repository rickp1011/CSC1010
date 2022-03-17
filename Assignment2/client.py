from ipaddress import ip_address
import socket,time

PORT = 5050
#socket.gethostbyname(scoket.gethostname())
SERVER = "localhost"
ADDR = (SERVER,PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!disconnect"

def connect():
    #AF_INET ipv4 addressing, SOCK_STREAM tcp socket
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect(ADDR)
    return client

def send(client,msg):
    message = msg.encode(FORMAT)
    client.send(message)

def start():  
    global PORT,SERVER,ADDR
    print('Running client program...')
    x,y = input('Enter chat server\'s IP address and port: ').split()
    SERVER = x
    PORT = int(y)
    ADDR = (SERVER,PORT)
    user = input('Enter this client\'s name: ')
    print(f'Trying to connect to the server: {ADDR}')
    connection = connect()
    print('...Server connected...')
    send(connection,user)
    print('Type !disconnect to close the client program')
    while True:
        msg = input(f"{user}: ")
        if msg == '!disconnect':
            break
        send(connection,msg)

    send(connection,DISCONNECT_MESSAGE)
    time.sleep(1)
    print("Disconnected from chatroom")

start()