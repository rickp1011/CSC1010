from fileinput import filename
from ipaddress import ip_address
import socket, time, threading
import os

FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!disconnect"

x, y = input('Enter chat server\'s IP address and port: ').split()  # take users input for ip address and port number
SERVER = x  # set server to users choice of ip address
PORT = int(y)  # set port to users choice of port
ADDR = (SERVER, PORT)  # set address to server and port
nickname = input("Choose a nickname:")  # take users choice of name

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # initialize client with socket object
client.connect(ADDR)  # connect client and address

filename = ""


def receiveClient():
    global filename
    condition = True
    while condition:  # infinite loop
        try:
            msg1 = client.recv(4096)  # receive the message
            if msg1.decode(FORMAT) == "getNickname":
                client.send(nickname.encode(FORMAT))  # if new connection, server will ask user to send nickname

            elif '!image' in msg1.decode(FORMAT):
                image_chunk = client.recv(2048)
                file1 = open(filename, "wb")
                while image_chunk:
                    file1.write(image_chunk)  #
                    image_chunk = client.recv(2048)
                file1.close()

            else:
                print(msg1.decode(FORMAT))  # connection already establish. just print msg

        except:  # any exception = disconnect
            print("Disconnected")
            client.close()
            break
    # f.close()


def write():
    global filename
    print('Running client program...')
    print(f'Trying to connect to the server: {ADDR}')
    condition = True
    while condition:
        userInput = input("")  # get any msg wants to send across chat
        msg = f'{nickname}:{userInput}'

        userInput = userInput.lower()  # format string to lower case
        if userInput == DISCONNECT_MESSAGE:  # if user want to disconnect
            client.close()
            break
        elif "!download" in userInput:
            filename = userInput.split(' ')[-1]  # set file name
            print("IMAGE DOWNLOAD SUCCESSFULLY")
        else:
            client.send(msg.encode(FORMAT))  # send msg to server


# run both receive and write threads.
receive_thread = threading.Thread(target=receiveClient)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
