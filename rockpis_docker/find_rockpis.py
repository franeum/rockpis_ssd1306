#!/usr/bin/env python3

## using it to find rockpis ip

import socket
import json
import sys 


PORT = 37020
broadcast = '<broadcast>'


def set_broadcast_address(arg):
    if arg == 'dev':
        b = '192.168.4.255'
    else:
        b = '<broadcast>'
    return b


def create_socket():
    client = socket.socket(socket.AF_INET, 
                            socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    client.settimeout(0.5)
    return client 


def send_code(cl, broadcast, port):
    cl.sendto(b'1', (broadcast, port))
    return None 


def get_response(cl):
    while True:
        try:
            data, addr = client.recvfrom(1024)
            data = json.loads(data.decode('utf-8'))
            machine = data.get('machine', None)

            if machine and machine == 'rockpis':
                print(addr[0])
                client.close()
                exit(0)
        except KeyboardInterrupt:
            print("chiudo mestamente")
            client.close()
            exit(1)


if __name__ == "__main__":
    arg = sys.argv[1]
    broadcast = set_broadcast_address(arg)

    while True:
        try:
            client = create_socket()
            send_code(client, broadcast, PORT)
            get_response(client)
        except socket.timeout:
            continue 
