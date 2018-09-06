#FIXME: validate database connection and send an alert if it is offline
#This Script Takes the id of the site where the edison is, the only one in site table and the agent ID 
#The only one in agent table
#Definition name
#FIXME: SEPARATE THIS METHOD TO MAKE IT ATOMIC
def select():
	#Python Library
	import psycopg2

	#Time Library
	import time

	conn_string = "host='127.0.0.1' dbname='iot-sensors' user='postgres' password='postgres'"
	
	cnX = 0
	#Data Base Connection
	#while cnX==0:
		#try:	
	conn = psycopg2.connect(conn_string)
	#Prepare a cursor object using cursor() method
	cursor = conn.cursor()
			#cnX = 1
		#except:
			#print ("Cannot connect, we are trying again :)")
			#cnX=0

	array = [0,0]

	#Select data
	try:
				
		#Select ID_Site               
		#Execute SQL query using execute() method
		cursor.execute("SELECT pk_id_site FROM site LIMIT 1")

		#Fetch a single row using fetchone() method and store the result in a vari$
		ID_Site = str(cursor.fetchone())

		#Slice string to obtain just characters
		array[0] = ID_Site[1:(len(ID_Site)-2)]

		
		#Select ID_Agent
		#Execute SQL query using execute() method
		cursor.execute("SELECT pk_id_agent FROM agent LIMIT 1")

		#Fetch a single row using fetchone() method and store the result in a vari$
		ID_Agent = str(cursor.fetchone())

		#Slice string to obtain just characters
		array[1] = ID_Agent[1:(len(ID_Agent)-2)]
		conn.commit()

	except psycopg2.Error as error:
		print("Error: {}".format(error))
		conn.commit()

	

	#Close cursor
	cursor.close()

	#Close connetion
	conn.close()
	#send alert
	return array
