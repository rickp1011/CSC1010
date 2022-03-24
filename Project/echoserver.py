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
    global chatIdServer,checkWater,waterLevel
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
        time.sleep(2)
        telegram_bot.sendMessage(chat_id, str(now.hour)+str(":")+str(now.minute)+waterLevel)
        

"""def child(connectionSocket):
    data = connection.recv(16)
    print (sys.stderr, 'received "%s"' % data)
    connection.sendall(data)
    connection.close()"""

def getWater(data):
    global waterLevel,checkWater
    waterLevel = data
    time.sleep(2)
    checkWater=False


# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address given on the command line
server_name = sys.argv[1]
server_address = (server_name, int(sys.argv[2]))
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
            #retrieve from pi
            data = connection.recv(128)
            print (sys.stderr, 'received "%s"' % data)

            #send connected 
            if data:
                data2=data
                connection.sendall(data)
            else:
                continue

            if checkWater and data2:
                print('dataful')
                getWater(data2.decode())
            else:
                print('no data')
            
    finally:
        connection.close()







