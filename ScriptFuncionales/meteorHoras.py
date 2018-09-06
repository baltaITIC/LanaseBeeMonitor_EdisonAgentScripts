import serial
import mraa
from time import sleep
import mosquitto_publisher
import insert_observation
import timeRetriever as tRet


def meteoroData():
	
	failed = 0
	try:
		x=mraa.Uart(0)
		#------- Opening port and sending command------
		ser = serial.Serial('/dev/ttyACM0', 115200)
		ser.bytesize = serial.EIGHTBITS
		ser.parity = serial.PARITY_NONE
		ser.stopbits = serial.STOPBITS_ONE
		ser.timeout = 2

		ser.write("LOGIN=0047\r\n")
		counter="READ\r\n"
		ser.write(counter)
		print("Sent: "+str(counter))

		#-------Lecturas----------
		r =  ser.readlines()
		temp = r[4].replace("\xb0C\r\n","").replace(",",".")
		hum = r[5].replace("%\r\n","").replace(",",".")
		brood = r[6].replace("\xb0C B\r\n","").replace(",",".")
		lit = r[7].replace("l/h\r\n","").replace(",",".")
		km = r[8].replace("km/h\r\n","").replace(",",".")
		print("Weight: "+r[3].replace("kg\r\n",""))
		print("Temperature: "+temp)
		print("Humidity: "+hum)
		print("Brood: "+brood)
		print("Liters per hour: "+lit)
		print("Kilometers per hour: "+km)
		print("Failed: "+str(failed))

		ser.close()
		
		#------Comprobacion------
		float(temp)
		float(hum)
		float(brood)
		float(lit)
		float(km)

		#-----Insercion---------
		pubTempI = insert_observation.insert(temp, "Temperature Int")
		pubHum = insert_observation.insert(hum, "Humidity")
		pubBrood = insert_observation.insert(brood, "Brood")
		pubPluvi = insert_observation.insert(lit, "Pluviometer")
		pubAnemo = insert_observation.insert(km, "Anemometer")

		#--------Publicacion a horas---------
		if(tRet.isTimeToSend()):
			mosquitto_publisher.publisher("TemperatureI", pubTempI)
			mosquitto_publisher.publisher("Humidity", pubHum)
			mosquitto_publisher.publisher("Brood", pubBrood)
			mosquitto_publisher.publisher("Pluviometer", pubPluvi)
			mosquitto_publisher.publisher("Anemometer", pubAnemo)


	except:
		print("Something went wrong, comunication or data, nothing done.")
		failed = failed + 1
	
	
