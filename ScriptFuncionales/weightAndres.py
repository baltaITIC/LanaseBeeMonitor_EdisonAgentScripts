from time import sleep
import serial
import mraa

def getWeight():
	x=mraa.Uart(0)
	ser = serial.Serial('/dev/ttyMFD1', 9600)
	ser.bytesize = serial.EIGHTBITS
	ser.parity = serial.PARITY_NONE
	ser.timeout = 2
	counter=66
	ser.write(chr(counter))
	#print("Sent: "+str(chr(counter))) 
	res = ser.readline()
	print(res+"nnnn")
	try:
		res = float(res)/1000
	except:
		res = -1
	ser.close()

	if res == -1:
		correctWeight()
	return res

def correctWeight():
	print("Correcting...")
	#while True:
		#counter +=1
	counter=70
	ser.write(chr(counter))

	print ser.readline()
