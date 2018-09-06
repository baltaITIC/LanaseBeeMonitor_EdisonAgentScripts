#Definition name
def insert(value, topic):
	
	#Mysql Library
	import psycopg2

	#Time Library
	import time
	
	#import script
	import database_info

	#Data Base Connection
	conn_string = "host='127.0.0.1' dbname='iot-sensors' user='postgres' password='postgres'"
	conn = psycopg2.connect(conn_string)

	#Prepare a cursor object using cursor() method
	cursor = conn.cursor()


	#Array used for recover ID_Site and ID_Agent	
	array = [0,0]
	array = database_info.select()
	
	ID_Site = array[0]
	ID_Agent = array[1]
	topic = topic.capitalize();

	if(topic=="Temperature"):
		topic += " Ext"

	#Insert data
	try:
		#Get the current date and time using strftime () method
		dateTime = str(time.strftime("%Y-%m-%d %H:%M:%S"))

		#Execute SQL query using execute() method
		cursor.execute("""SELECT pk_id_sensor FROM sensor, sensor_type WHERE sensor.fk_id_sensor_type = sensor_type.pk_id_sensor_type and sensor_type = '%s'; """ % (topic))

		#Fetch a single row using fetchone() method and store the result in avariable
		ID_Sensor = str(cursor.fetchone())
		#Split string to obtain just characters
		ID_Sensor = ID_Sensor[1:(len(ID_Sensor)-2)]

		print (ID_Sensor,topic)
		#Fetch a single row using fetchone() method and store the result in avariable
		cursor.execute("INSERT INTO observation(observation_value,observation_date,fk_id_agent,fk_id_sensor) VALUES(%s,%s,%s,%s);",(value,  dateTime, ID_Agent, ID_Sensor))
		conn.commit()
		print("New Observation Inserted!!")
	except psycopg2.Error as error:
		print("Error: {}".format(error))

	

	#Close cursor
	cursor.close()

	#Close connection
	conn.close()
	
	#string = ""+str(ID_Site)+" "+str(ID_Agent)+" "+str(ID_Sensor)+" "+str(value)+" "+str(dateTime)
	string = ""+str(ID_Agent)+" "+str(ID_Sensor)+" "+str(value)+" "+str(dateTime)
	
	return string
