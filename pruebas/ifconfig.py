import os

f = os.popen('ifconfig wlan0')
now = f.read().split('\n')[1].find('10.99.10.175')
if now != -1:
	os.system("reboot")
else:
	print("Wlan0 caida")
