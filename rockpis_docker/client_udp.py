import socket
import sys

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

#server_address = ('localhost', 10000)
message = b'This is the message.  It will be repeated.'

try:

    # Send data
    print("sending")
    sent = sock.sendto(message, ("<broadcast>", 50000))

    # Receive response
    data, server = sock.recvfrom(4096)
    print(data)

finally:
    print('closing socket')
    sock.close()