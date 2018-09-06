import socket
import sys
import os
import thread
 
HOST = ''   # Symbolic name, meaning all available interfaces
PORT = 5000 # Arbitrary non-privileged port
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'
 
#Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
     
print 'Socket bind complete'
 
#Start listening on socket
s.listen(10)
print 'Socket now listening'
 
#now keep talking with the client
while 1:
    print("wait to accept a connection - blocking call")
    conn, addr = s.accept()
    try:
	#conn, addr = s.accept()
    	print('Started SSH, request origin ' + addr[0] + ':' + str(addr[1]))
	#thread.start_new_thread(os.system, ("./reverseTunel.sh",))
	os.system("./reverseTunel.sh")
    except:
	print("Not started ssh") 

    print("Closing connection")
    s.close()
