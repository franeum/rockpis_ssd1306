#!/usr/bin/env python3 

import paramiko 

IP = '10.42.0.70'
USERNAME = 'rock'
PASSWORD = 'rock'


def send_credential(ssid, pwd, timestamp):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=IP, username=USERNAME, password=PASSWORD)
    stdin, stdout, stderr = ssh_client.exec_command("""nmcli r wifi on; nmcli d wifi list; nmcli d wifi connect VodafoneA66208560 password bbzmecflaht7y2f5;""")
    #ssh_client.exec_command(f"echo {ssid} {pwd} > {timestamp}_credenziali.txt")
    #stdin, stdout, stderr = ssh_client.exec_command(f'if test -f {timestamp}_credenziali.txt; then echo 0; else echo 1; fi')
    #response = stdout.readlines()
    ssh_client.close()
    return 0 #int(response[0])