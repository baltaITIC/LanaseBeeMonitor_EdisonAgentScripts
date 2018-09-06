from time import sleep
import serial
import mraa
 
#x=mraa.Uart(0)
#ser = serial.Serial('/dev/ttyACM0', 115200)
ser = serial.Serial('/dev/ttyMFD2', 115200)
ser.bytesize = serial.EIGHTBITS
ser.parity = serial.PARITY_NONE
ser.stopbits = serial.STOPBITS_ONE
ser.timeout = 1
print("Welcome")
counter = 84
#ser.flush()
#ser.write("LOGIN=3967\n")
print ser.readlines()
ser.flush()
print("Welcome")
while True:
	#counter +=1
	ser.write("LOGIN=3967\r\n")
	#ser.flush()
	counter="READ\r\n"
	ser.write(counter)
	print("Sent: "+counter)
	#sleep(1) 
	r =  ser.readlines()
	print(r)
	#ser.flush() 
	#sleep(0) 
	#if counter == 255:
		#counter = 32
