import socket
import sys
from threading import Thread
from matplotlib import axis
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from datetime import datetime   
"""def child(connectionSocket):
    data = connection.recv(16)
    print (sys.stderr, 'received "%s"' % data)
    connection.sendall(data)
    connection.close()"""
def animate(xs, ys):
    # Limit x and y lists to 20 items
    xs = xs[-20:]
    ys = ys[-20:]

    # Draw x and y lists
    axis.clear()
    axis.plot(xs, ys)

    # Format plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('TMP102 Temperature over Time')
    plt.ylabel('Temperature (deg C)')
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
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

while True:
    print (sys.stderr, 'waiting for a connection')
    connection, client_address = sock.accept()
    ## t = Thread(target=child , args = (connectionSocket, ))
    ##t.start()
    try:
        print (sys.stderr, 'client connected:', client_address)
        while True:
            data = connection.recv(128)
            
            print (sys.stderr, 'received "%s"' % data)
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            x.append(dt_string)
            y.append(data)
            if data:
                connection.sendall(data)
            else:
                break
            ani = animation.FuncAnimation(fig, animate, interval=1000)
            plt.show()
    finally:
        connection.close()