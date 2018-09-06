factory_sn_file = log_file = open('/factory/serial_number', 'r')
serial = str(factory_sn_file.read(16))
serial = serial.upper()	
print(serial)