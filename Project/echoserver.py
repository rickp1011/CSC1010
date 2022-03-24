import socket
import sys
from threading import Thread
from datetime import datetime
import time, datetime
import telepot
from telepot.loop import MessageLoop

telegram_bot = telepot.Bot('5116787822:AAGMxhOJb6esbb2rcAmAk-QgNm15ukXtDss')
checkWater=False
now = datetime.datetime.now()
chatIdServer=[]
waterLevel=""

def action(msg): #done at msgLoop
    global chatIdServer
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
        telegram_bot.sendMessage(chat_id, str(now.hour)+str(":")+str(now.minute)+"waterLvl")
        checkWater=True

"""def child(connectionSocket):
    data = connection.recv(16)
    print (sys.stderr, 'received "%s"' % data)
    connection.sendall(data)
    connection.close()"""

def getWater(data):
    global waterLevel
    waterLevel = data
    checkWater=False


# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address given on the command line
server_name = sys.argv[1]
server_address = (server_name, 10000)
print (sys.stderr, 'starting up on %s port %s' % server_address)
sock.bind(server_address)
sock.listen(1)


MessageLoop(telegram_bot, action).run_as_thread() #run on other thread
print('Server started for telegram')

while True:
    print (sys.stderr, 'waiting for a connection')
    connection, client_address = sock.accept()
    ## t = Thread(target=child , args = (connectionSocket, ))
    ##t.start()
    try:
        print (sys.stderr, 'client connected:', client_address)
        while True:
            data = connection.recv(128)
            if checkWater:
                getWater(data)


            print (sys.stderr, 'received "%s"' % data)
            if data:
                connection.sendall(data)
            else:
                break
    finally:
        connection.close()







