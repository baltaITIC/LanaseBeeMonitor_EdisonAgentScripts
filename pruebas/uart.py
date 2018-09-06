from time import sleep
import serial
import mraa
 
x=mraa.Uart(0)
ser = serial.Serial('/dev/ttyMFD1', 9600)
ser.bytesize = serial.EIGHTBITS
ser.parity = serial.PARITY_NONE
ser.timeout = 2
counter = 84
print("Welcome")
while True:
	#counter +=1
	counter=66
	ser.write(chr(counter))
	print("Sent: "+str(chr(counter))) 
	print ser.readline() 
	sleep(.1) 
	#if counter == 255:
		#counter = 32
