#Sys Library
#import sys

#
#sys.path.append('/usr/lib/python2.7/site-packages/paho/mqtt')

#######################################################################
#PAHO-MQTT LIBRARY
#######################################################################
#Mqtt library
#import client as mqtt
import paho.mqtt.client as mqtt
import os
from  time import sleep

def publisher(topic, value):

	def on_publish(client, topic, value):

        	p = client.publish("/id_site_1/"+topic, value)
        	print("/id_site_1/"+topic, value)
        	p.wait_for_publish()
        	client.disconnect()
        	#client.disconnect()

    
	# 
	client = mqtt.Client()
    
	#
	failConn = 0
	while failConn<=11:
		try:
			client.connect("132.247.186.49",1883,60)
			break
		except:
			failConn = failConn + 1
			if failConn>=10:
				os.system('reboot')
		sleep(1)
	#
	client.on_publish = on_publish(client, topic, value)

	#
	client.loop_start() 
    
