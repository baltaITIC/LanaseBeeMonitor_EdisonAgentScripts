# -*- coding: utf-8 -*-
import mraa
import math
tempValue2 = mraa.Aio(2)

voltage_ratio = 5.0 / 3.3
analog_sum = 0
for step in range(12):
    analog_sum += tempValue2.read()
    pass
analog_value = (analog_sum / 12) * voltage_ratio
        # see the datasheet for more information
try:
    calculated_resistance = (1023 - analog_value) * 10000 / analog_value
    calculated_temperature = 1 / (math.log(calculated_resistance / 10000) / 3975 + 1 / 298.15) - 273.15

    # if the values exceed a certain threshold
    # then raise a ValueError exception
    if not (calculated_temperature >= -50.0 and calculated_temperature <= 145.0):
        raise ValueError('temperature out of range')

    # and return what we got calculated
    calculated_temperature = calculated_temperature*-1
    print(calculated_temperature)
    print('[room temperature: {:5.2f}°C]'.format(calculated_temperature))
except ZeroDivisionError:
	print("Non available")