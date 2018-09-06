import mraa
import math
tempValue2 = mraa.Aio(3)

#temperature = tempValue2.read()

sum = 0

for i in range(0,32):
    
	sum = sum + tempValue2.read()
	print(sum)
sum = sum>>5
print(sum)
a = sum*50/33                                # 3.3V supply
resistance=(1023-a)*10000/a                           # get the resistance of the sensor;
temperature=1/(math.log(resistance/10000)/3975+1/298.15)-273.15   # convert to temperature via datasheet

print(temperature)
