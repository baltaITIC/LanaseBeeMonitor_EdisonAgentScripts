#Mysql Library
import mysql.connector as mariadb

#Time Library
import time

#Data Base Connection
mariadb_connection = mariadb.connect(user = 'root',
					password = '',
					database = 'iot_sensors',
					unix_socket = '/var/lib/mysql/mysql.sock')

# prepare a cursor object using cursor() method
cursor = mariadb_connection.cursor()

#Insert data
try:
	# get the current date and time using strftime () method.
	dateTime = str(time.strftime("%Y-%m-%d %H:%M:%S"))
	
	# execute SQL query using execute() method.
	cursor.execute("SELECT ID_sensor FROM sensor, sensor_type WHERE sensor.sensor_type_ID_Sensor_Type = sensor_type.ID_Sensor_Type and Sensor_Name = 'light'")                  
	
	# Fetch a single row using fetchone() method and store the result in a variable.
	sensor_ID_Sensor = str(cursor.fetchone())

	sensor_ID_Sensor = sensor_ID_Sensor[1:(len(sensor_ID_Sensor)-2)]	

	cursor.execute("INSERT INTO observation(sensor_ID_Sensor, Value, Date_Time) VALUES(%s,%s,%s)",(sensor_ID_Sensor, 100.1 , dateTime))

except mariadb.Error as error:
	print("Error: {}".format(error))
	
print (""+dateTime)
print (""+str(sensor_ID_Sensor))

#
mariadb_connection.commit()

#Close cursor 
cursor.close()

#Close connetion
mariadb_connection.close()
