#!/usr/bin/env python3 

import paramiko 

IP = '192.168.4.1'
USERNAME = 'rock'
PASSWORD = 'rock'


def send_credential(ssid, pwd, timestamp):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=IP,
                        username=USERNAME, 
                        password=PASSWORD)
    ssh_client.exec_command(f"echo {ssid} {pwd} > {timestamp}_credenziali.txt")
    stdin, stdout, stderr = ssh_client.exec_command(f'if test -f {timestamp}_credenziali.txt; then echo 0; else echo 1; fi')
    #stdin, stdout, stderr = ssh_client.exec_command(f'ls -la') 
    response = stdout.readlines()
    ssh_client.close()
    #print(response)
    return int(response[0])