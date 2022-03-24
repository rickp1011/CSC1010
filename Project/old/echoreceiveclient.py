from socket import *
import sys
server_address = (sys.argv[1], 10000)
clientSocket = socket(AF_INET,SOCK_STREAM)
clientSocket.connect(server_address)
while True:
    try:
        bufferSize = 2048
        data = clientSocket.recv(bufferSize)
    finally:
        clientSocket.close()
    
