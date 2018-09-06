#Definition name
def insert(value):
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

	#Insert data
	try:
		#Execute SQL query using execute() method
		cursor.execute("SELECT pk_id_observation FROM observation ORDER BY pk_id_observation DESC LIMIT 1;")

		#Fetch a single row using fetchone() method and store the result in avariable
		ID_Observation = str(cursor.fetchone())

		#Slice string to obtain just characters
		ID_Observation = ID_Observation[1:(len(ID_Observation)-2)]

		#Insert into alert table using execute() method
		cursor.execute("INSERT INTO alert(fk_id_agent, fk_id_observation, priority, alert_state) VALUES(%s, %s, %s, %s)",(ID_Agent, ID_Observation, "high", 1))
		conn.commit()
		print("New Alert Inserted!!")
	except psycopg2.Error as error:
		print("Error: {}".format(error))

	

	#Close cursor
	cursor.close()

	#Close connection
	conn.close()

	priority = "high"
	state = "1"
	string = ""+priority+" "+state

	return string

