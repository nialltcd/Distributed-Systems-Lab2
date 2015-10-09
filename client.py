#!/usr/bin/python

import socket
import sys

port_number = int(sys.argv[1])
print port_number

#Create a socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Connect the socket to the localhost on port 8000
sock.connect(('localhost', port_number))

#Input String
input_string=str(sys.argv[2:])

#Send the request
sock.send(input_string)

#Receive the response from the server
data=sock.recv(1024)

#Close the socket
sock.close()

#Print the response to the terminal
print data

