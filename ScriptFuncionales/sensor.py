#!/usr/bin/python
#-*- coding: latin-1 -*-

#
import sys 
import time
import signal

#
sys.path.append('/usr/lib/python2.7/site-packages/upm')

#SENSOR LIBRARIES
#Light sensor library 
import pyupm_grove as grove

#Loudness sensor library
import pyupm_loudness as loudnessSensor

#Temperature sensor library
#import mraa

#Vibration sensor library
import pyupm_ldt0028 as vibrationSensor

#Acecelerometer sensor library
import pyupm_mma7660 as accelerometerSensor

#VARIABLES
#Create the light sensor object using AIO pin 0
lightValue = grove.GroveLight(0)

#Create the loudness sensor object using AIO pin 1
loudnessValue = loudnessSensor.Loudness(1, 3.0)

#Create the temperature sensor object using AIO pin 3
#tempValue = mraa.Aio(0)

#Create the vibration sensor object using AIO pin 2
vibrationValue = vibrationSensor.LDT0028(2)

#Create the accelerometer snesor object using I2C 0
accelerometerValue = accelerometerSensor.MMA7660(accelerometerSensor.MMA7660_DEFAULT_I2C_BUS, accelerometerSensor.MMA7660_DEFAULT_I2C_ADDR)

#Place device in standby
accelerometerValue.setModeStandby()

#Place device into active mode
accelerometerValue.setModeActive()

ax = accelerometerSensor.new_floatp()
ay = accelerometerSensor.new_floatp()
az = accelerometerSensor.new_floatp()

while True:
	#READINGS
	#Read the input from AIO 0 (Light sensor)
        light = lightValue.value()	
	
	#Read the input sensor AIO 1 (Loudness sensor) 	
	loudness = loudnessValue.loudness()

	#Read the input from AIO 2 (Temperature sensor)
        #temp = tempValue.read()

	#Read the input sensor AIO 3 (Vibration sensor)
	vibration = vibrationValue.getSample()

	#Read the input sensor I2C 0 (Acceletometer sensor)
	accelerometerValue.getAcceleration(ax, ay, az)


	#CONVERSIONS
	#Temperature in celsius
	#tempC = str(temp - 60)
	
	#Temperature in fahrenheit
	#tempF = str(int(tempC) * 9 / 5 + 32)	

	
	#PRINTING
	#print Light values
	print ("Ligh is now "+str(light))
	
	#print Loudness values
	print ("Loudness is now "+str(loudness))
	
	#print Degrees
	#print("Temperature is now "+tempC+"° " +tempF+"°F")

	#print Vibration values
	print ("Vibration is now "+str(vibration))

	#print Accelerometer values
	string = ("Acceleration: x = {0}""g y = {1}""g z = {2}g").format(accelerometerSensor.floatp_value(ax), accelerometerSensor.floatp_value(ay), accelerometerSensor.floatp_value(az))
	print (string)

	#Space
	print ("")

	#1 sec. delay
	time.sleep(5)
