import socket
import sys
import threading
from threading import Thread
from datetime import datetime
import time, datetime
import telepot
from telepot.loop import MessageLoop

x, y = input("CSC1010 Project server, please enter the listening IP address and port.").split()
SERVER = x
PORT = int(y)
ADDR = (SERVER, PORT)
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket to the address given on the command line
sock.bind(ADDR)

print(f"[SERVER STARTED :{ADDR}]")
print("Waiting for incoming connections...")
sock.listen()

# telegram region (start)
telegram_bot = telepot.Bot('5116787822:AAGMxhOJb6esbb2rcAmAk-QgNm15ukXtDss')
checkWater=False
now = datetime.datetime.now()
chatIdServer=[]
waterLevel=""

def action(msg): #done at msgLoop
    global chatIdServer,checkWater
    chat_id = msg['chat']['id'] # auto get current chat id
    command = msg['text']

    print ('Received: %s' % command)
    if command == '/start':
        telegram_bot.sendMessage (chat_id, str("initializing start for pet water bottle"))
        if chat_id not in chatIdServer:
            chatIdServer.append(chat_id)
    # elif command == '/list':
    #     telegram_bot.sendMessage (chat_id, str("listing all chat id")+str(chatIdServer))
    elif command == '/check':
        checkWater=True
        telegram_bot.sendMessage(chat_id, str(now.hour)+str(":")+str(now.minute)+waterLevel)
        print(waterLevel) # test output



MessageLoop(telegram_bot, action).run_as_thread() #run on other thread
print('SERVER STARTED : Telegram')
# telegram region (end)

def handle_connection(conn):
    global waterLevel
    while True:
        try:
            data = conn.recv(128).decode()
            # print(sys.stderr, 'received "%s"' % data) #TODO what is this uh?
            print(f"Received test: {data}")
            waterLevel=data # keep overwrite till sender stop sending
            print("test")
            conn.send(data.encode())

        except:
            conn.close()
            print(f"{conn} Disconnected")
            break

def receiveServer():
    while True:
        conn, addr = sock.accept()
        print(f"Connect with {str(addr)}")
        thread = threading.Thread(target=handle_connection,args=(conn,))
        thread.start()
receiveServer()


