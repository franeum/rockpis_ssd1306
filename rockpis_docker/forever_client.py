#!/usr/bin/env python3

import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, True)
s.settimeout(5)

s.sendto(b"hello", ("<broadcast>", 5555))
try:
    print(s.recv(1024))
except socket.timeout:
    print("No server found")

s.close()
