from time import sleep
import serial
from serial import SerialException
import mraa

def getWeight():
	ret = ""
	x=mraa.Uart(0)
	try:
		ser = serial.Serial('/dev/ttyACM0', 115200)
		ser.bytesize = serial.EIGHTBITS
		ser.parity = serial.PARITY_NONE
		ser.stopbits = serial.STOPBITS_ONE
		ser.timeout = 1
		
		ser.flush()
		ser.write("LOGIN=0047\r\n")
		counter="READ\r\n"
		ser.write(counter)
		sleep(1) 
		r =  ser.readlines()
		#print(r)
		if(len(r)>0):
			ret = r[3]
			ret = ret.replace('kg','')
			ret = ret.replace(',','.')
			print ret
		else:
			ret = "-1"
	except:
		ret="-1"
	#ser.close()

	return ret
