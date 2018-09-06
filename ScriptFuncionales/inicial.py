#!/usr/bin/env python
# coding=utf-8
import urllib, json
import psycopg2

#Comprobar que es necesario el proceso de inicializacion, si la base de datos aun se conserva como default
def comprobar ():
	conn_string = "host='127.0.0.1' dbname='iot-sensors' user='postgres' password='postgres'"
	conn = psycopg2.connect(conn_string)
	cursor = conn.cursor()
	try:
		cursor.execute("SELECT serial_number FROM agent LIMIT 1")
		result = cursor.fetchall()
		serialBD = str(result[0][0])
	except psycopg2.Error as error:
		print("Error: {}".format(error))
	#print(result[2:(len(result)-3)])
	#print(serialBD)
	return serialBD
	cursor.close()
	conn.close()

#Proceso de borrado de los datos por default de la base de datos
def procesoBorrado():
	conn_string = "host='127.0.0.1' dbname='iot-sensors' user='postgres' password='postgres'"
	conn = psycopg2.connect(conn_string)
	cursor = conn.cursor()
	try:
		cursor.execute("DELETE FROM bee_control")
		cursor.execute("DELETE FROM sensor_rfid")
		cursor.execute("DELETE FROM bees")
		cursor.execute("DELETE FROM alert")
		cursor.execute("DELETE FROM observation")
		cursor.execute("DELETE FROM sensor")
		cursor.execute("DELETE FROM sensor_type")
		cursor.execute("DELETE FROM units")
		cursor.execute("DELETE FROM agent")
		cursor.execute("DELETE FROM site")
		cursor.execute("DELETE FROM ubication")
		#cursor.execute("ALTER TABLE agent ADD COLUMN agent_description  varchar(1000)")
		conn.commit()
	except psycopg2.Error as error:
		print("Error: {}".format(error))
	cursor.close()
	conn.close()

def ubication(jsonI, conn_string):
	conn = psycopg2.connect(conn_string)
	cursor = conn.cursor()
	try:
		sql = "INSERT INTO ubication VALUES (%s,%s,%s,%s,%s)"
		data = (int(jsonI["pk_id_ubication"]),jsonI["address"].encode('utf-8'),jsonI["latitude"], jsonI["longitude"], int(jsonI["fk_id_city"])) 
		cursor.execute(sql,data)
		conn.commit()
	except psycopg2.Error as error:
		print("Error----")
		print("Error: {}".format(error))
	cursor.close()
	conn.close()

def site(jsonI, conn_string):
	conn = psycopg2.connect(conn_string)
	cursor = conn.cursor()
	try:
		sql = "INSERT INTO site VALUES (%s,%s,%s,%s,%s)"
		data = (int(jsonI["pk_id_site"]),jsonI["site_description"].encode('utf-8'),jsonI["site_date"],3, jsonI["fk_id_ubication"]) 
		cursor.execute(sql,data)
		conn.commit()
	except psycopg2.Error as error:
		print("Error----")
		print("Error: {}".format(error))
	cursor.close()
	conn.close()

def agent(jsonI, conn_string):
	conn = psycopg2.connect(conn_string)
	cursor = conn.cursor()
	try:
		sql = "INSERT INTO agent VALUES (%s,%s,%s,%s,%s,%s)"
		data = (int(jsonI["pk_id_agent"]),jsonI["model"].encode('utf-8'),jsonI["serial_number"],int(jsonI["fk_id_brand"]), int(jsonI["fk_id_site"]), jsonI["agent_description"].encode('utf-8')) 
		cursor.execute(sql,data)
		conn.commit()
	except psycopg2.Error as error:
		print("Error----")
		print("Error: {}".format(error))
	cursor.close()
	conn.close()

def units(jsonI, conn_string):
	conn = psycopg2.connect(conn_string)
	cursor = conn.cursor()
	for I in jsonI:
		try:
			sql = "INSERT INTO units VALUES (%s,%s,%s)"
			data = (int(I["pk_id_unit"]),I["unit"].encode('utf-8'),I["symbol"].encode('utf-8')) 
			cursor.execute(sql,data)
			conn.commit()
		except psycopg2.Error as error:
			print("Error----")
			print("Error: {}".format(error))
	cursor.close()
	conn.close()

def sensor_type(jsonI, conn_string):
	conn = psycopg2.connect(conn_string)
	cursor = conn.cursor()
	for I in jsonI:
		try:
			sql = "INSERT INTO sensor_type VALUES (%s,%s,%s,%s)"
			data = (int(I["pk_id_sensor_type"]),I["sensor_type"].encode('utf-8'),I["fk_id_unit"], I["communication_protocol"].encode('utf-8')) 
			cursor.execute(sql,data)
			conn.commit()
		except psycopg2.Error as error:
			print("Error----")
			print("Error: {}".format(error))
	cursor.close()
	conn.close()

def sensor(jsonI, conn_string):
	conn = psycopg2.connect(conn_string)
	cursor = conn.cursor()
	for I in jsonI:
		try:
			sql = "INSERT INTO sensor VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
			data = (int(I["pk_id_sensor"]),
				I["sensor_state"],
				I["installation_date"],
				I["description"].encode('utf-8'), 
				I["port"], 
				float(I["min_value"]),
				float(I["max_value"]),
				int(I["fk_id_sensor_type"]),
				int(I["fk_id_agent"])) 
			cursor.execute(sql,data)
			conn.commit()
		except psycopg2.Error as error:
			print("Error----")
			print("Error: {}".format(error))
	cursor.close()
	conn.close()

#Inicializar la base de datos con los datos arrojados del servidor
def procesoIncersion(json):
	conn_string = "host='127.0.0.1' dbname='iot-sensors' user='postgres' password='postgres'"
	ubication(json["ubication"], conn_string)
	site(json["site"], conn_string)
	agent(json["agent"], conn_string)
	units(json["units"], conn_string)
	sensor_type(json["sensorType"], conn_string)
	sensor(json["sensors"], conn_string)

if ("EDISON" in comprobar()):
	print("Necesario proceso de inicializacion")

	#Obtener los datos de webService/JSON con el serial del dispositivo
	factory_sn_file = log_file = open('/factory/serial_number', 'r')
	serial = str(factory_sn_file.read(16))
	serial = serial.upper()	
	#print(serial)
	url = "http://132.247.186.49:8080/get-sensors/"+serial
	response = urllib.urlopen(url)
	decoded = json.loads(response.read())
	procesoBorrado()
	#print decoded
	#print ("Agent:"+str(decoded["agent"]["pk_id_agent"]))
	procesoIncersion(decoded)
else:
	print("El sistema no requiere inicializacion")
