import time

def isTimeToSend ():
	send = False
	year, month, day, hour, minute = time.strftime("%Y,%m,%d,%H,%M").split(',')
	#print (year, month, day, hour, minute)
	if ((7 == int(hour) or 11 == int(hour) or 20 == int(hour)) and int(minute) <= 5):
		send = True
	return send

#print(isTimeToSend())