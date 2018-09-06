# -*- coding: utf-8 -*-
def read(port):

    import mraa
    import math
    """tempValue2 = mraa.Aio(port)
    voltage_ratio = 5.0 / 3.3
    analog_sum = 0
    for step in range(12):
        analog_sum += tempValue2.read()
	#print(analog_sum)
        pass
    analog_value = (analog_sum / 12) * voltage_ratio
            # see the datasheet for more information
    #print(analog_value)"""
    try:
        """calculated_resistance = (1023 - analog_value) * 10000 / analog_value
        #print(calculated_resistance)
	calculated_temperature = 1/ (math.log(calculated_resistance / 10000) / 3975 + 1 / 298.15) - 273.15
    
        # if the values exceed a certain threshold
        # then raise a ValueError exception
        if not (calculated_temperature >= -50.0 and calculated_temperature <= 145.0):
            raise ValueError('temperature out of range')
    
        # and return what we got calculated
        calculated_temperature = (calculated_temperature*-1
)+7
        #print(calculated_temperature)
        #print('[room temperature: {:5.2f}°C]'.format(calculated_temperature))"""

        B=3975
        ain = mraa.Aio(2)
        a = ain.read()
        resistance = (1023-a)*10000.0/a
        temp = 1/(math.log(resistance/10000.0)/B+1/298.15)-273.15
        #print "Temperature now is " + str(temp)
        return float("{0:.2f}".format(temp*-1))
    except:
    	print("Non available")
        return 0