from time import sleep
import serial
import mraa
 
x=mraa.Uart(0)
ser = serial.Serial('/dev/ttyMFD1', 9600)
ser.bytesize = serial.EIGHTBITS
ser.parity = serial.PARITY_NONE
ser.timeout = 2
#counter = 102
print("Welcome")
#while True:
	#counter +=1
counter=70
ser.write(chr(counter))

ser.write(chr(0))
ser.write(chr(0))
ser.write(chr(8))
ser.write(chr(3))
ser.write(chr(8))
ser.write(chr(8))
ser.write(chr(6))
ser.write(chr(0))
ser.write(chr(7))
#ser.write(chr(counter))

print ser.readline() 

counter = 102
ser.write(chr(counter))
#print("Sent: "+str(chr(counter))) 
print ser.readline() 
#sleep(.1) 
#if counter == 255:
	#counter = 32
