from ipaddress import ip_address
import socket,time,threading

FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!disconnect"


x, y = input('Enter chat server\'s IP address and port: ').split()
SERVER = x
PORT = int(y)
ADDR = (SERVER, PORT)
nickname = input("Choose a nickname:")

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(ADDR)


def receiveClient():
    condition=True
    while condition:
        try:
            msg1 = client.recv(1024)
            msg=msg1.decode(FORMAT)
            if msg=="getNickname":
                client.send(nickname.encode(FORMAT)) #if new connection, server will ask user to send nickname
            if msg=="toDownload":
                pass
            else:
                print(msg)  # connection already establish. just print msg

        except: #any exception = disconnect
            print("Disconnected")
            client.close()
            break
    f.close()


def write():
    print('Running client program...')
    print(f'Trying to connect to the server: {ADDR}')
    condition=True
    while condition:
        userInput=input("") #get any msg wants to send across chat
        msg = f'{nickname}:{userInput}'
        client.send(msg.encode(FORMAT)) #send msg to server
        userInput=userInput.lower() #format string to lower case
        if userInput==DISCONNECT_MESSAGE: #if user want to disconnect
            client.close()
            break
        elif userInput=="list images": #send image list to user
            getImg="getImg"
            client.send(getImg.encode(FORMAT))
        elif userInput=="download":
            toDownload="toDownload"
            client.send(toDownload.encode(FORMAT))


#run both receive and write threads.
receive_thread=threading.Thread(target=receiveClient)
receive_thread.start()

write_thread=threading.Thread(target=write)
write_thread.start()