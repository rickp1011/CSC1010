import socket
import sys
from threading import Thread
from folium import Figure
import plotly.graph_objs as go
from datetime import datetime   
"""def child(connectionSocket):
    data = connection.recv(16)
    print (sys.stderr, 'received "%s"' % data)
    connection.sendall(data)
    connection.close()"""

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address given on the command line
server_name = sys.argv[1]
server_address = (server_name, 10000)
print (sys.stderr, 'starting up on %s port %s' % server_address)
sock.bind(server_address)
sock.listen(1)
x =[]
y=[]

while True:
    print (sys.stderr, 'waiting for a connection')
    connection, client_address = sock.accept()
    ## t = Thread(target=child , args = (connectionSocket, ))
    ##t.start()
    try:
        print (sys.stderr, 'client connected:', client_address)
        while True:
            data = connection.recv(16)
            
            print (sys.stderr, 'received "%s"' % data)
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            x.append(dt_string)
            y.append(data)
            Figure.add_trace(go.Scatter(
            x,
            y,
            xperiod="M1",
            xperiodalignment="middle",
            hovertemplate="%{y}%{_xother}"))
            if data:
                connection.sendall(data)
            else:
                break
    finally:
        connection.close()