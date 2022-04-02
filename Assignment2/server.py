from multiprocessing.connection import Client
import threading, socket
import os
import glob

FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!disconnect"
# AF_INET ipv4 addressing, SOCK_STREAM tcp socket

x, y = input("CSC1010 Chat server, please enter the listening IP address and port.").split() #take users input of ip address and port
SERVER = x #set server to users choice of ip address
PORT = int(y) #set port to users choice of port
ADDR = (SERVER, PORT) #set address to server and port
# nickname = input("Choose a nickname: ")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

print(f"[SERVER STARTED :{ADDR}]")
print("Waiting for incoming connections...")
server.listen()

# arr to store connected clients and their nicknames
clientsConnected = []
nicknames = []

# images
image_path = os.getcwd() #return string of current work directory
image_list = [] #declare image list as an array
for filename in glob.glob(image_path+'/*.jpg'): #assuming gif
    image_list.append(filename.replace(image_path+"/","")) #append every image file

# send message to all client connected to server
def broadcast(message):
    for client in clientsConnected:
        client.send(message)


def write():
    userInput = input("")  # get any msg wants to send across chat
    msg = f'{"Server"}:{userInput}'
    broadcast(msg.encode(FORMAT))  # send msg to server
    print(msg)


# function to handle connected user
def handle_connection(conn, addr):
    while True:
        try:
            msg = conn.recv(1024)
            if "!list" in msg.decode(FORMAT) :  # if userInput is "list images", send connection image list
                for i in image_list:
                    broadcast(i.encode(FORMAT))
                    print(i)

            elif "!download" in msg.decode(FORMAT):
                conn.send('!image'.encode(FORMAT))
                x = msg.decode(FORMAT).split(' ')
                fileimage = open(x[-1], 'rb')
                image_data = fileimage.read(2048)
                while image_data:
                    conn.send(image_data)
                    image_data = fileimage.read(2048)
                fileimage.close()

            else:  # if able to receive msg and is not one of the listed conditions, broadcast msg to all connected # client in clientsConnected[]
                broadcast(msg)
                printmsg = msg.decode(FORMAT)
                print(printmsg)

        except:
            #if exception occurs, remove connected client from both nicknames[] and clientsConnected[]
            index = clientsConnected.index(conn)
            clientsConnected.remove(conn)
            conn.close()  # close connection
            nickname = nicknames[index]  # so nickname and client have the same index
            broadcast(f'{nickname} left the chat!'.encode(FORMAT))
            print(f"{nickname} disconnected")
            nicknames.remove(nickname)
            break


def receiveServer():
    while True:
        conn, addr = server.accept()
        print(f"Connect with {str(addr)}")
        conn.send("getNickname".encode(FORMAT))  # getNickname to inform client.py to send nickname to server. to
        # server to identify client
        nickname = conn.recv(1024).decode(FORMAT)  # get nickname from client
        nicknames.append(nickname)  # append to nicknames[]
        clientsConnected.append(conn)  # append to clientsConnected[]
        print(f"Client {nickname} has joined")
        broadcast("{} joined the chat!\n".format(nickname).encode(FORMAT))
        conn.send("Connected to chat room".encode(FORMAT))
        conn.send("\n---------------------------------------------------------------------".encode(FORMAT))
        conn.send(("\nServer Functions: Type '!list' to list images in the server".encode(FORMAT)))
        conn.send("\nType '!download <filename>' to bring up the download interface".encode(FORMAT))
        conn.send("\n---------------------------------------------------------------------".encode(FORMAT))

        thread = threading.Thread(target=handle_connection, args=(conn, addr))
        thread.start()
        write_thread = threading.Thread(target=write)
        write_thread.start()



receiveServer()
# handle_client()
