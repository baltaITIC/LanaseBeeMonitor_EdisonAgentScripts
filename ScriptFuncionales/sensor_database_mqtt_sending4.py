#!/usr/bin/python
#-*- coding: latin-1 -*-

#Sys library
import sys

#Time library
import time

#Signal library
import signal

#Path for upm library
sys.path.append('/usr/lib/python2.7/site-packages/upm')

#Path for mqtt library
sys.path.append('/usr/lib/python2.7/site-packages/paho/mqtt')


#Wait for connection. 
#time.sleep(60)

#######################################################################
#IMPORTED SCRIPTS
#######################################################################
#Mosquito publisher
import mosquitto_publisher

#Used for insert into observation table
import insert_observation

#Used for insert into alert table
import insert_alert

#Used for read from the conf.ini file
import read_ini

#Script that retrieve weight
import weightAndres as weightPy

#import timeRetriever as tRet

#######################################################################
#SENSOR LIBRARIES
#######################################################################
#Light sensor library 
import pyupm_grove as grove

#Loudness sensor library
import pyupm_loudness as loudnessSensor

#Temperature sensor library
#import mraa
import HightTemp

#Vibration sensor library
import pyupm_ldt0028 as vibrationSensor

#Acecelerometer sensor library
import pyupm_mma7660 as accelerometerSensor

#import meteoro


#######################################################################
#VARIABLES
#######################################################################
#Create the light sensor object using AIO pin 0
lightValue = grove.GroveLight(0)

#Create the loudness sensor object using AIO pin 1
loudnessValue = loudnessSensor.Loudness(1, 3.0)

#Create the temperature sensor object using AIO pin 2
#tempValue2 = mraa.Aio(2)

#Create the vibration sensor object using AIO pin 3
vibrationValue = vibrationSensor.LDT0028(3)

#Create the accelerometer sensor object using I2C 0
accelerometerValue = accelerometerSensor.MMA7660(accelerometerSensor.MMA7660_DEFAULT_I2C_BUS, accelerometerSensor.MMA7660_DEFAULT_I2C_ADDR)
print(accelerometerSensor.MMA7660_DEFAULT_I2C_BUS)
#Place device in standby
accelerometerValue.setModeStandby()

#Place device into active mode
accelerometerValue.setModeActive()

ax = accelerometerSensor.new_floatp()
ay = accelerometerSensor.new_floatp()
az = accelerometerSensor.new_floatp()

#list created to know which sensors the edison have
sensor_type = ['light', 'loudness', 'vibration','temperature','accelerometer', 'weight']


#directory used for each sensor
lightDirectory = {'id0':0, 'sensor0': '', "value0":0, "unit0": ''}
loudnessDirectory = {'id0':0, 'sensor0': '', "value0":0, "unit0": ''}
vibrationDirectory = {'id0':0, 'sensor0': '', "value0":0, "unit0": ''}
accelerometerDirectory = {'id0':0, 'sensor0': '', "valueX0":0, "valueY0":0, "valueZ0":0, "unit0": ''}
temperatureDirectory = {'id0':0, 'sensor0': '', "value0":0, "unit0": ''}
weightDirectory = {'id0':0, 'sensor0': '', "value0":0, "unit0": ''}

#Read counter
countLight = 0
countLoudness = 0
countTemperature = 0
countVibration = 0
countAccelerometer = 0
countWeight = 0

#Alert counter
countLightAlert = 0
countLoudnessAlert = 0
countTemperatureAlert = 0
countVibrationAlert = 0
countAccelerometerAlert = 0
countWeightAlert = 0


#Array used for receiving values from conf.ini
arrayTime = read_ini.read()
delay = arrayTime[0]
readingTime = arrayTime[1] * arrayTime[2]
triggerAlert = arrayTime[3]
print (arrayTime)
#Dictionary size
dictionary_size = readingTime * 4 #len(dictionary)
dictionary_accelerometer = readingTime * 6 #len(dictAcc)


#######################################################################
#READING VALUES IN AN INFINITE LOOP (WHILE)
#######################################################################
while True:
	for i in range(readingTime):
		#######################################################################
		#READINGS	
		#######################################################################
		#Read the input from AIO 0 (Light sensor)
		light = lightValue.value()
	
		#Read the input sensor AIO 1 (Loudness sensor) 	
		loudness = loudnessValue.loudness()

		#Read the input from AIO 2 (Temperature sensor)
		temperature = HightTemp.read(2) 
		#temp = tempValue.read()

		#Read the input sensor AIO 3 (Vibration sensor)
		vibration = vibrationValue.getSample()

		#Read the input sensor I2C 0 (Accelerometer sensor)
		accelerometerValue.getAcceleration(ax, ay, az)

		#Read weight from serial
		weight = weightPy.getWeight()

		#FIXME: ADD TEMPERATURE AND HUMIDITY SENSORS
        	
		#######################################################################
		#PRINTING
		#######################################################################
		#print Light values
		print ("Light is now "+str(light))
	
		#print Loudness values
		print ("Loudness is now "+str(loudness))

		#CONVERSIONS
		#Temperature in celsius
		tempC = str(temperature)

		#Temperature in Farenheit
		#Is not used...

		print("Temperature is now "+tempC+"°C")

		#print Vibration values
		print ("Vibration is now "+str(vibration))

		#print Accelerometer values
		#string = ("Acceleration: x = {0}""g y = {1}""g z = {2}g").format(accelerometerSensor.floatp_value(ax), accelerometerSensor.floatp_value(ay), accelerometerSensor.floatp_value(az))
		print ("Acceleration: x = "+str(accelerometerSensor.floatp_value(ax))+"g  y = "+str(accelerometerSensor.floatp_value(ay))+"g  z = "+str(accelerometerSensor.floatp_value(az)))

		print("Weight is now: "+str(weight))

		#SPACE
		print("")
	

		#######################################################################
		#SENDING VALUES TO SUBSCRIBERS (MQTT)
		#######################################################################
		#iterate over sensor_type to get values of each sensor
		for j in range(len(sensor_type)):
			#FIXME: USE SWITCH AND DEFINE ALL THE CASES (NO NECESSARY)
			if sensor_type[j] == 'light':
				topic = str(sensor_type[j])
				value = str(light)

				#FIXME: retrieve from database
				#Fill dictionary
				lightDirectory['id' + str(countLight)]= 0
				lightDirectory['sensor' + str(countLight)]= topic
				lightDirectory['value' + str(countLight)]= value
				lightDirectory['unit' + str(countLight)]= "lux"
				
				countLight += 1
				
				#Compare values to detect alerts
				#FIXME: retrieve values from database
				#Adapt to Solar Light Levels (before installing)
				if int(value) < 34 or int(value) > 200:

					countLightAlert += 1
					#FIXME: put this value as a variable in conf.ini (DONE)
					if countLightAlert > triggerAlert:
						#Insert alert into observation table
						string_observation = insert_observation.insert(value, topic)
						#print string_observation

						#Insert into alert table
						string_observation = string_observation+" "+insert_alert.insert(value)
						
						#Publish alert
						mosquitto_publisher.publisher("alert/"+topic, string_observation)

						countLightAlert = 0

				#print lightDirectory['value'+str(countLight - 1)]
				#FIXME: VERIFY IF IT IS CORRECT
				elif countLightAlert > 0 and lightDirectory['value'+str(countLight - 1)] != value:
					countAlert = 0

				#avarage,
				if len(lightDirectory) == dictionary_size:
					#Create an aux variable
					average = 0
        
					for k in range(readingTime):
						totalvalue = lightDirectory['value' + str(k)]
						average += int(totalvalue)
		
					average = average / readingTime
					
					#Insert into observation table and save the observation values
					string = insert_observation.insert(average, topic)
					
					#Empty directory
					lightDirectory.clear()
        				
					#Publish value
					if(tRet.isTimeToSend()):
						mosquitto_publisher.publisher(topic, string)
					else:
						print("Not time yet")

					countLight = 0
				
				#FIXME:REVISAR
				j += 1


			elif sensor_type[j] == 'loudness':
				topic = str(sensor_type[j])
				value = str(loudness)
				
				#Filling dictionary
				loudnessDirectory['id' + str(countLoudness)]= 0
				loudnessDirectory['sensor' + str(countLoudness)]= topic
				loudnessDirectory['value' + str(countLoudness)]= value
				loudnessDirectory['unit' + str(countLoudness)]= "dB"
				
				countLoudness += 1

				#Comparing values to detect alerts
				if float(value) < 0.00005 or float(value) > 40.0:
					countLoudnessAlert += 1

					if countLoudnessAlert > triggerAlert:
						#Insert alert into observation table
						string_observation = insert_observation.insert(value, topic)

						#Insert into alert table
						string_observation = string_observation+" "+insert_alert.insert(value)

						#Publish alert
						mosquitto_publisher.publisher("alert/"+topic, string_observation)

						countLoudnessAlert = 0


				#avarage,
				if len(loudnessDirectory) == dictionary_size:
					#Create the aux variable
					average = 0

					for k in range(readingTime):
						totalvalue = loudnessDirectory['value' + str(k)]
						average += float(totalvalue)
					
					average = average / readingTime
                                        
					#Insert into observation table and save the observation values
					string = insert_observation.insert(average, topic)
					
					#Empty directory
					loudnessDirectory.clear()
                                        
					#Publish value
					if(tRet.isTimeToSend()):
						mosquitto_publisher.publisher(topic, string)
					else:
						print("Not time yet")

					countLoudness = 0

					j += 1
        	

			elif sensor_type[j] == 'vibration':
				topic = str(sensor_type[j])
				value = str(vibration)
				
				#Filling dictionary
				vibrationDirectory['id' + str(countVibration)]= 0
				vibrationDirectory['sensor' + str(countVibration)]= topic
				vibrationDirectory['value' + str(countVibration)]= value
				vibrationDirectory['unit' + str(countVibration)]= "vibration"
				                                
				countVibration += 1
				
				#Comparing values to detect alerts
				if int(value) < 10 or int(value) > 800:
					countVibrationAlert += 1

					if countVibrationAlert > triggerAlert:
						#Insert alert into observation table
						string_observation = insert_observation.insert(value, topic)

						#Insert into alert table
						string_observation = string_observation+" "+insert_alert.insert(value)

						#Publish alert
						mosquitto_publisher.publisher("alert/"+topic, string_observation)

						countVibrationAlert = 0

				#avarage,
				if len(vibrationDirectory) == dictionary_size:
					#Create the aux variable
					average = 0

					for k in range(readingTime):
						totalValue = vibrationDirectory['value' + str(k)]
						average += float(totalValue)

					average = average / readingTime
					
					#Insert into observation table and save the observation value
					string = insert_observation.insert(average, topic)
					
					#Empty directory
					vibrationDirectory.clear()
                                        
					#Publish value
					if(tRet.isTimeToSend()):
						mosquitto_publisher.publisher(topic, string)

					countVibration = 0

				j += 1

                        elif sensor_type[j] == 'temperature':
                                topic = str(sensor_type[j])
                                value = str(tempC)

                                #Filling dictionary
                                temperatureDirectory['id' + str(countTemperature)]= 0
                                temperatureDirectory['sensor' +str(countTemperature)]= topic
                                temperatureDirectory['value' +str(countTemperature)]= value
                                temperatureDirectory['unit' +str(countTemperature)]= "Â°"

                                countTemperature += 1

                                #Comparing values to detect alerts
                                if temperature < 10 or temperature > 40:
                                        countTemperatureAlert += 1

                                        if countTemperatureAlert > triggerAlert:
                                                #Insert alert into observation table
                                                string_observation = insert_observation.insert(value, topic)

                                                #Insert into alert table
                                                string_observation = string_observation+" "+insert_alert.insert(value)

                                                #Publish alert
                                                mosquitto_publisher.publisher("alert/"+topic,string_observation)

                                                countTemperatureAlert = 0

                                #avarage,
                                if len(temperatureDirectory) == dictionary_size:
                                        #Create the aux variable
                                        average = 0

                                        for k in range(readingTime):
                                                totalValue = temperatureDirectory['value' + str(k)]
                                                average += float(totalValue)

                                        average = average / readingTime

                                        #Insert into observation table and save the observation value
                                        string = insert_observation.insert(average, topic)

                                        #Empty directory
                                        temperatureDirectory.clear()

                                        #Publish value
                                        if(tRet.isTimeToSend()):
                                        	mosquitto_publisher.publisher(topic, string)
                                        else:
											print("Not time yet")

                                        countTemperature = 0

                                j += 1








			elif sensor_type[j] == 'accelerometer':
				topic = str(sensor_type[j])
				valueX = accelerometerSensor.floatp_value(ax)
				valueY = accelerometerSensor.floatp_value(ay)
				valueZ = accelerometerSensor.floatp_value(az)

				#Filling dictionary
				accelerometerDirectory['id' + str(countAccelerometer)]= 0
				accelerometerDirectory['sensor' + str(countAccelerometer)]= topic
				accelerometerDirectory['valueX' + str(countAccelerometer)]= valueX
				accelerometerDirectory['valueY' + str(countAccelerometer)]= valueY
				accelerometerDirectory['valueZ' + str(countAccelerometer)]= valueZ
				accelerometerDirectory['unit' + str(countAccelerometer)]= "g"
                                
				countAccelerometer += 1


				#Comparing values to detect alerts
				#Define how to take alerts from accelerometer
				"""if int(valueX) < 10 or int(valueY) > 800:
					countAccelerometerAlert += 1

					if countAccelerometerAlert > 3:
						#Insert alert into observation table
						string_observation = insert_observation.insert(valueY, topic)

						#Insert into alert table
						string_observation = string_observation+" "+insert_alert.insert(value)

						#Publish alert
						mosquitto_publisher.publisher("alert/"+topic, string_observation)

						countAccelerometerAlert = 0"""



				#Condition used for get the value avarage
				if len(accelerometerDirectory) == dictionary_accelerometer:
					#Create the aux variables
					averageX = 0
					averageY = 0
					averageZ = 0

					for k in range(readingTime):
						totalValueX = accelerometerDirectory['valueX' + str(k)]
						totalValueY = accelerometerDirectory['valueY' + str(k)]
						totalValueZ = accelerometerDirectory['valueZ' + str(k)]
						averageX += float(totalValueX)
						averageY += float(totalValueY)
						averageZ += float(totalValueZ)

					averageX = averageX / readingTime
					averageY = averageY / readingTime
					averageZ = averageZ / readingTime

					average = str(averageX) + "_" + str(averageY) + "_" + str(averageZ)

					#Insert into observation table and save the observation value
					string = insert_observation.insert(average, topic)
                                        
					#Empty directory
					accelerometerDirectory.clear()
                                        
					#Publish value
					if(tRet.isTimeToSend()):
						mosquitto_publisher.publisher(topic, string)
					else:
						print("Not time yet")

					countAccelerometer = 0
				
				j += 1


			elif sensor_type[j] == 'weight':
				topic = str(sensor_type[j])
				value = str(weight)
				
				#Filling dictionary
				weightDirectory['id' + str(countWeight)]= 0
				weightDirectory['sensor' + str(countWeight)]= topic
				weightDirectory['value' + str(countWeight)]= value
				weightDirectory['unit' + str(countWeight)]= "Kg"
				
				countWeight += 1

				#Comparing values to detect alerts
				if float(value) < 0 or float(value) > 300:
					countWeightAlert += 1
					#Incluir llamada a inizializador del sistema en la balanza
					weightPy.correctWeight()
					if countWeightAlert > triggerAlert:
						#Insert alert into observation table
						string_observation = insert_observation.insert(value, topic)

						#Insert into alert table
						string_observation = string_observation+" "+insert_alert.insert(value)

						#Publish alert
						mosquitto_publisher.publisher("alert/"+topic, string_observation)

						countWeightAlert = 0


				#avarage,
				if len(weightDirectory) == dictionary_size:
					#Create the aux variable
					average = 0

					for k in range(readingTime):
						totalvalue = weightDirectory['value' + str(k)]
						average += float(totalvalue)
					
					average = average / readingTime
                                        
					#Insert into observation table and save the observation values
					string = insert_observation.insert(average, topic)
					meteoro.meteoroData()
					
					#Empty directory
					weightDirectory.clear()
                                        
					#Publish value
					if(tRet.isTimeToSend()):
						mosquitto_publisher.publisher(topic, string)
					else:
						print("Not time yet")

					countWeight = 0

					j = 0

		#Delay in seconds
		time.sleep(delay)
