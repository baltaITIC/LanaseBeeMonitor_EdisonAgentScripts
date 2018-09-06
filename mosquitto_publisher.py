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

def publisher(topic, value):

	def on_publish(client, topic, value):
		
		client.publish("/id_site_1/"+topic, value)
		print("/id_site_1/"+topic, value)
    
	# 
	client = mqtt.Client()
    
	#
	client.connect("132.247.186.49",1883,60)
	#
	client.on_publish = on_publish(client, topic, value)

	#
	client.loop_start() 
    
