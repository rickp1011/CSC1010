import socket
import sys
from tokenize import String
# Project: Smart Water Tank
# Created by: Jitesh Saini

# you can use the setup_cron.sh bash script to install a cron job to automatically execute this file every minute.

import RPi.GPIO as GPIO
import time, os

import datetime

TRIG = 4
ECHO = 17
ALARM = 20
NOALARM = 21

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.output(TRIG, False)

GPIO.setup(ALARM, GPIO.OUT)
GPIO.output(ALARM, False)
GPIO.setup(NOALARM, GPIO.OUT)
GPIO.output(NOALARM, True)

print("Waiting For Sensor To Settle")
time.sleep(1)  # settling time


def get_distance():
    dist_add = 0
    k = 0
    for x in range(10):
        try:
            GPIO.output(TRIG, True)
            time.sleep(0.00001)
            GPIO.output(TRIG, False)

            while GPIO.input(ECHO) == 0:
                pulse_start = time.time()

            while GPIO.input(ECHO) == 1:
                pulse_end = time.time()

            pulse_duration = pulse_end - pulse_start

            distance = pulse_duration * 17150

            distance = round(distance, 3)
            print(x, "distance: ", distance)

            dist_add = dist_add + distance
            # print "dist_add: ", dist_add
            time.sleep(0.5)  # 100ms interval between readings

        except Exception as e:

            pass

    print("x: ", x + 1)
    print("k: ", k)

    avg_dist = dist_add / (x + 1 - k)
    dist = round(avg_dist, 3)
    # print ("dist: ", dist)
    return dist


#def sendData_to_remoteServer(dist):
    #url_remote = "http://192.168.1.2/water-tank/insert_data.php?dist=" + str(dist)
    #cmd = "curl -s " + url_remote
    #result = os.popen(cmd).read()
    #print(cmd)


def low_level_warning(dist):
    tank_height = 22  # set your tank height here
    level = tank_height - dist
    if level < 6:
        print("level low : ", level)
        GPIO.output(ALARM, True)
        GPIO.output(NOALARM, False)
    else:
        GPIO.output(ALARM, False)
        GPIO.output(NOALARM, True)
        print("level ok")
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port on the server given by the caller
server_address = (sys.argv[1], 10000)
print (sys.stderr, 'connecting to %s port %s' % server_address)
sock.connect(server_address)

try:
    while True:
        # print('ur message')
        # message = input().encode()
        distance = 23 - get_distance() #23 is height of bottle, getdistance() returns distance from sensor to water
        output="Water Level in cm: "
        message=str(distance)
        message=message.encode()
        output=output.encode()

        print(output, distance)
        #sendData_to_remoteServer(distance)
        low_level_warning(distance)
        print("---------------------")
        print (sys.stderr, 'sending "%s"' % message)
        sock.sendall(output, message) #nt sure if string need to encode, to test

        amount_received = 0
        amount_expected = len(message)
        while amount_received < amount_expected:
            data = sock.recv(128)
            amount_received += len(data)
            print (sys.stderr, 'received "%s"' % data)

finally:
    sock.close() 