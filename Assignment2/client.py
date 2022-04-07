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
    '''Handles all of the reading of data being sent from the server
    Nickname getter and image handling and writer.'''
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
                # fileSize = 0
                while image_chunk:
                    file1.write(image_chunk)
                    if 'Finish' in image_chunk.decode('ISO-8859-1'):
                        print("Download Successful")
                        break
                    else:
                        image_chunk = client.recv(2048)
                    #print doenload sucessful if finish else continue downlaod
                file1.close()

            else:
                print(msg1.decode(FORMAT))  # connection already establish. just print msg

        except:  # any exception = disconnect
            print("Disconnected")
            client.close()
            break



def write():
    '''Handles all of the user input,messages & commands, and sends the input over to the server side'''
    global filename
    print('Running client program...')
    print(f'Trying to connect to the server: {ADDR}')
    condition = True
    while condition:
        userInput = input("")  # get any msg wants to send across chat
        msg = f'{nickname}:{userInput}'
        client.send(msg.encode(FORMAT))  # send msg to server
        #userInput = userInput.lower()  # format string to lower case
        if userInput == DISCONNECT_MESSAGE:  # if user want to disconnect
            client.close()
            break
        elif "!list" in userInput: # if userInput contain !list ask server to send image list
            client.send("LIST_images".encode(FORMAT))
        elif "!download" in userInput:
            filename = userInput.split(' ')[-1]  # set file name


# run both receive and write threads.
receive_thread = threading.Thread(target=receiveClient)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()