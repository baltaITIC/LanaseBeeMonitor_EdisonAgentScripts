from serial.tools import list_ports

VID = 483
PID = 5740

device_list = list_ports.comports()
for device in device_list:
    if (device.vid != None or device.pid != None):
        if ('{:04X}'.format(device.vid) == VID and
           '{:04X}'.format(device.pid) == PID):
            port = device.device
            break
        port = None