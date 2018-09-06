# Mysql Library
import psycopg2
    conn_string = "host='127.0.0.1' dbname='iot-sensors' user='postgres' password='postgres'"
    #Time Library
    import time

    #Data Base Connection
    conn = psycopg2.connect(conn_string)
    #Prepare a cursor object using cursor() method
    cursor = conn.cursor()

    array = [0,0]

# Select data
try:
    # Select ID_Site
    # Execute SQL query using execute() method
        cursor.execute("SELECT COUNT(pk_id_sensor) FROM sensor")

        # Fetch a single row using fetchone() method and store the result in a vari$
        totalSensor = str(cursor.fetchone())

        # Slice string to obtain just characters
        totalSensor = totalSensor[1:(len(totalSensor) - 2)]


        # Select ID_Agent
        # Execute SQL query using execute() method
        cursor.execute("SELECT pk_id_sensor from sensor;")

        # Fetch all rows using fetchone() method and store the result in a vari$
        list(cursor.fetchall())





except psycopg2.Error as error:
    print("Error: {}".format(error))

conn.commit()

# Close cursor
cursor.close()

# Close connetion
conn.close()

# send alert
#return array