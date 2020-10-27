#!/usr/bin/env python3

import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
server_address = ('', 50000)
print("start")
sock.bind(server_address)

while True:
    print('\nwaiting to receive message')
    data, address = sock.recvfrom(4096)
    
    print('received')
    print(data)
    
    if data:
        sent = sock.sendto(data, address)
        print('sent bytes back to')
