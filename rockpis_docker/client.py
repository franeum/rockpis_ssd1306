#!/usr/bin/env python3

import socket

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
client.bind(("", 37020))

while True:
    data, addr = client.recvfrom(1024)
    if data: 
        client.sendto(b"ciao ciao", (addr[0],addr[1]))
        print("received message: ", data, addr)
