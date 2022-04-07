import threading, socket
import os
import glob

FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!disconnect"
# AF_INET ipv4 addressing, SOCK_STREAM tcp socket

x, y = input(
    "CSC1010 Chat server, please enter the listening IP address and port.").split()  # take users input of ip address and port
SERVER = x  # set server to users choice of ip address
PORT = int(y)  # set port to users choice of port
ADDR = (SERVER, PORT)  # set address to server and port

serverName = input("Please enter your name: ")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

print(f"[SERVER STARTED :{ADDR}]")
print("Waiting for incoming connections...")
server.listen()

# arr to store connected clients and their nicknames
clientsConnected = []
nicknames = []

# Retrieves all the images in the current working directory and stores it into a list
image_path = os.getcwd()  # return string of current work directory
image_list = []  # declare image list as an array
for filename in glob.glob(image_path + '/*.jpg'):  # assuming gif
    image_list.append(filename.replace(image_path + "\\", ""))  # append every image file


# send message to all client connected to server
def broadcast(message):
    '''Broadcast message to all the users connected to the client with the message \n
    ...\n
    Parameter \n
        message:String, message that is already encoded in the UTF-8 \n'''
    for client in clientsConnected:
        client.send(message)


def write():
    '''Broadcast the user input in the CLI to all users connected in the server \n
    ...\n'''
    userInput = input("")  # get any msg wants to send across chat
    msg = f'{serverName}:{userInput}'
    broadcast(msg.encode(FORMAT))  # send msg to server
    print(msg)


# function to handle connected user
def handle_connection(conn, addr):
    '''Function that will encompass all the reading of data for that specific user. Includes
    the functionality of decomposing message received from user with specific commands \n
    ... \n
    Parameters \n
        conn:socket, the user socket object \n
        addr:string, connection information'''
    while True:
        # try to receive the message from the user connection
        try:
            msg = conn.recv(1024)
            if "LIST_images" in msg.decode(FORMAT):  # if userInput is "list images", send connection image list
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
                conn.send('Finish'.encode(FORMAT))  # send finish signal to the client
                fileimage.close()  # close fileimage after finish sending


            else:  # if able to receive msg and is not one of the listed conditions, broadcast msg to all connected # client in clientsConnected[]
                broadcast(msg)
                printmsg = msg.decode(FORMAT)
                print(printmsg)

        # if socket is closed or shutdown, it will
        except:
            # if exception occurs, remove connected client from both nicknames[] and clientsConnected[]
            index = clientsConnected.index(conn)
            clientsConnected.remove(conn)
            conn.close()  # close connection
            nickname = nicknames[index]  # so nickname and client have the same index
            broadcast(f'{nickname} left the chat!'.encode(FORMAT))
            print(f"{nickname} disconnected")
            nicknames.remove(nickname)
            break


def receiveServer():
    '''Starts running the server with initialization and
    managing new connections read and write through multithreading.'''
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
        conn.send(("\nServer Functions:\n    Type '!list' to list images in the server".encode(FORMAT)))
        conn.send(
            "\nType '!download <filename>' to bring up the download interface\n    !disconnect to leave the chatroom".encode(
                FORMAT))

        conn.send("\n---------------------------------------------------------------------".encode(FORMAT))

        thread = threading.Thread(target=handle_connection, args=(conn, addr))
        thread.start()

        write_thread = threading.Thread(target=write)
        write_thread.start()


receiveServer()