import threading,socket


FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!disconnect"
#AF_INET ipv4 addressing, SOCK_STREAM tcp socket

x, y = input("CSC1010 Chat server, please enter the listening IP address and port.").split()
SERVER = x
PORT = int(y)
ADDR = (SERVER, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

print(f"[SERVER STARTED :{ADDR}]")
print("Waiting for incoming connections...")
server.listen()

# arr to store connected clients and their nicknames
clientsConnected = []
nicknames = []

# send message to all client connected to server
def broadcast(message):
    for client in clientsConnected:
        client.send(message)

# function to handle connected user
def handle_connection(conn):
    while True:
        try:
            #if able to recieve msg, broadcast msg to all connected client in clientsConnected[]
            msg = conn.recv(1024)
            broadcast(msg)
            printmsg=msg.decode(FORMAT)
            print(printmsg)
        except:
            #if expection occur, remove connected client from both nicknames[] and clientsConnected[]
            index = clientsConnected.index(conn)
            clientsConnected.remove(conn)
            conn.close() #close connection
            nickname=nicknames[index] # so nickname and client have the same index
            broadcast(f'{nickname} left the chat!'.encode(FORMAT))
            print(f"{nickname} disconnected")
            nicknames.remove(nickname)
            break


def receiveServer():
    while True:
        conn, addr = server.accept()
        print(f"Connect with {str(addr)}")
        conn.send("getNickname".encode(FORMAT))     #getNickname to inform client.py to send nickname to server. to
                                                    #server to identify client
        nickname = conn.recv(1024).decode(FORMAT) #get nickname from client
        nicknames.append(nickname)  #append to nicknames[]
        clientsConnected.append(conn) #append to clientsConnected[]

        print(f"Client is {nickname}")
        broadcast("{} joined the chat!".format(nickname).encode(FORMAT))
        conn.send("Connected to chat room".encode(FORMAT))
        thread = threading.Thread(target=handle_connection, args=(conn,))
        thread.start()

receiveServer()
