def fill(sensor, topic, value, countlight):
	#avarage,
        if len(sensor) == 48:
		#Create the aux variable
		aux = 0

		for k in range(12):
			totalvalue = sensor['value'+str(k)]
			aux += int(totalvalue)

		aux = aux / 12

		#Publish value
		mosquitto_publisher.publisher(topic, aux)

		#Insert into observation table
		insert_observation.insert(value)                  
		
		#Empty directory
                sensor.clear()
		
		countlight = 0
		
		return sensor
	else:
		lightsensor['id'+str(countlight)]= 0
		lightsensor['sensor'+str(countlight)]= topic
		lightsensor['value'+str(countlight)]= value
		lightsensor['unit'+str(countlight)]= "lux"
		countlight += 1

		return countlight


