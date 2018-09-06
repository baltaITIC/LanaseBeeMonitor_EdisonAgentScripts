
#!/bin/bash

echo "Initializing network"
#Change to initialize GSM communication
#ifconfig wlan0 192.168.43.67 netmask 255.255.255.0
#ifconfig wlan0 10.99.10.175 netmask 255.255.252.0
#route add default gw 10.99.8.1 wlan0
#route add default gw 192.168.43.1 wlan0
ifconfig wlan0

echo "Welcome to Edison Bee Monitor"
echo "Initializing system"

echo "Data base server starting..."
systemctl start postgres
systemctl status postgres

echo "Inicialization server starting..."
systemctl start inicial
systemctl status inicial

echo "RFID daemon stating..."
systemctl start pyru824
systemctl status pyru824

echo "Starting monitor and MQTT Protocol"
systemctl start sensorMQTT.service
systemctl status sensorMQTT.service

echo "We are ready to work!!!"
