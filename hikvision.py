#!/usr/bin/python

# Command for detection
# python detect.py --source rtsp://admin:pass@your_ip:554/Streaming/Channels/101

#Socket client example in python

import socket	#for sockets
import sys	#for exit

#create an INET, STREAMing socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
    print('Failed to create socket')
    sys.exit()
	
print('Socket Created')

host = 'www.google.com';
port = 15300;

try:
	#remote_ip = socket.gethostbyname(host)
    remote_ip = "192.168.100.23"

except socket.gaierror:
	#could not resolve
	print('Hostname could not be resolved. Exiting')
	sys.exit()

#Connect to remote server
s.connect((remote_ip , port))

print('Socket Connected to ' + host + ' on ip ' + remote_ip)

#Send some data to remote server
message = b'intrusion\r\n\r\n'

try :
	#Set the whole string
	s.sendall(message)
except socket.error:
	#Send failed
	print('Send failed')
	sys.exit()

print('people detection')

