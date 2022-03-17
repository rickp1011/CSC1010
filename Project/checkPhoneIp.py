import os
from time import sleep

import os
from time import sleep

#junhao's phone static ip
phoneIP = "192.168.0.192" # Change this to match your phone's static IP

while True:
	response = os.system("ping -c 1 " + phoneIP)

	if response == 0:
		print("Phone is online!")
	else:
		print("No phone detected")
	sleep(2)