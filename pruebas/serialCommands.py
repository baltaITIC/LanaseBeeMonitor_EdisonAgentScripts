from time import sleep
import serial
import mraa
 
x=mraa.Uart(0)
ser = serial.Serial('/dev/ttyMFD2', 115200)
ser.bytesize = serial.EIGHTBITS
ser.parity = serial.PARITY_NONE
ser.timeout = 1
#counter = 102
print("Welcome")
while True:
	var = input()
	ser.write(bytes(var))
	print((str(int(var))))
	print ser.readline()