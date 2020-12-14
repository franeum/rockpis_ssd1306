#!/usr/bin/env python3

import re
import subprocess as sp 
from functools import wraps

WIFI_DEVICE = re.compile(r'^w.+0$')

def get_uuid():
    res = sp.check_output(['nmcli','-g','DEVICE,UUID','con','show'])
    res = res.splitlines()

    for dev in res:
        device = dev.decode('utf-8').split(':')
        if re.search(WIFI_DEVICE, device[0]):
            return device[1]


def wifi_device_name():
    res = [i.decode('utf-8') for i in sp.check_output(['nmcli','-g','DEVICE','con','show']).splitlines() if re.search(WIFI_DEVICE, i.decode('utf-8'))]
    device_name = res[0]
    return device_name 





def get_connection_string(ssid, password, device):
    return f"nmcli d wifi connect {ssid} password {password} ifname {device}"


def connect_wifi(ssid, password, device):
    return sp.check_output(get_connection_string(ssid, password, device)) 


def get_disconnection_string(uuid):
    return f"sudo nmcli con down id {uuid}"


def disconnetc_wifi():
    uuid = get_uuid()
    res = sp.check_output(get_disconnection_string())
    return res 



def set_nmcli_command(decorated):
    @wraps(decorated)
    def wrapper(*string):
        print(string)
        #list_of_string = string.split()
        #return sp.check_output(list_of_string) 
        # TODO
    return wrapper 

@set_nmcli_command
def connect_wifi(ssid, password, device):
    return get_connection_string(ssid, password, device)

@set_nmcli_command
def disconnect_wifi(uuid):
    return get_disconnection_string(uuid)

if __name__ == "__main__":
    connect_wifi("vodafone", "antani", "stocazzo")
