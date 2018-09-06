from __future__ import print_function
import time, sys, signal, atexit
from upm import pyupm_bmx055 as sensorObj

def main():
    # Instantiate a BMI055 instance using default i2c bus and address
    sensor = sensorObj.BMI055()

    ## Exit handlers ##
    # This function stops python from printing a stacktrace when you hit control-C
    def SIGINTHandler(signum, frame):
        raise SystemExit

    # This function lets you run code on exit
    def exitHandler():
        print("Exiting")
        sys.exit(0)

    # Register exit handlers
    atexit.register(exitHandler)
    signal.signal(signal.SIGINT, SIGINTHandler)

    x = sensorObj.new_floatp()
    y = sensorObj.new_floatp()
    z = sensorObj.new_floatp()

    # now output data every 250 milliseconds
    while (1):
        sensor.update()

        sensor.getAccelerometer(x, y, z)
        print("Accelerometer x:", sensorObj.floatp_value(x), end=' ')
        print(" y:", sensorObj.floatp_value(y), end=' ')
        print(" z:", sensorObj.floatp_value(z), end=' ')
        print(" g")

        sensor.getGyroscope(x, y, z)
        print("Gyroscope x:", sensorObj.floatp_value(x), end=' ')
        print(" y:", sensorObj.floatp_value(y), end=' ')
        print(" z:", sensorObj.floatp_value(z), end=' ')
        print(" degrees/s")

        print()
        time.sleep(.250)

if __name__ == '__main__':
    main()
