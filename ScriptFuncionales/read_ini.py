import configparser

def read():
	#Instiate array
	array = [0,0,0,0]

	#Instantiate
	config = configparser.ConfigParser()

	#Parse existing file
	config.read('conf.ini')

	#Read values from a section and save in the array
	array[0] = config.getint('time', 'delay')
	array[1] = int(60 / array[0])
	array[2] = config.getint('time', 'minutes')

	array[3] = config.getint('alert', 'trigger')
	
	#Return the array with the values read from conf.ini
	return array
