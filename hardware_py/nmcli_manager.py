#!/usr/bin/env python3

import re
import json 
import subprocess as sp 


DEBUG                   = 0
EXPORT_JSON             = 1
WIFI_DEVICE             = re.compile(r'^w.+0$')
CONNECTION_STRING       = "nmcli d wifi connect {} password {} ifname {}"
DISCONNECTION_STRING    = "nmcli con down id {}"
GET_DEVICE_QUERY        = "nmcli -g GENERAL.DEVICE,GENERAL.TYPE --mode multiline dev show"
GET_UUID_QUERY          = "nmcli -g DEVICE,UUID con show --active"
GET_WIFI_LIST_QUERY     = "nmcli -g SSID,SIGNAL dev wifi list"
WIFI_STATUS             = "nmcli r wifi"
ENABLE_WIFI_QUERY       = "nmcli r wifi on"


def _run_process(query):
    res = sp.run(query.split())
    return res.returncode


def wifi_status():
    res = _nmcli_command(WIFI_STATUS)
    return res.decode('utf-8').strip(None) == 'enabled'


def jsonize(fn):
    def wrapper(*args):
        if EXPORT_JSON == 1:
            if args:
                return json.dumps(fn(args))
            else:
                return json.dumps(fn())
        return fn()
    return wrapper 


def format_name(dotted):
    return dotted.split('.')[1]


def get_device():
    """get wifi device name"""
    res = _nmcli_command(GET_DEVICE_QUERY)
    devices = [dev.decode('utf-8').split(':') for dev \
        in res.splitlines() if dev.decode('utf-8') != '']
    container = {}
    
    for n,d in enumerate(devices):
        container[format_name(d[0])] = d[1]
        if n % 2 == 1:
            if container['TYPE'] == 'wifi':
                return container['DEVICE']
    

def get_uuid():
    res = _nmcli_command(GET_UUID_QUERY)
    res = res.splitlines()

    for dev in res:
        device = dev.decode('utf-8').split(':')
        if re.search(WIFI_DEVICE, device[0]):
            return device[1]


def _nmcli_command(string):
    if DEBUG:
        print(string)
    else:
        return sp.check_output(string.split())


def connect_wifi(ssid, password, device):
    string = CONNECTION_STRING.format(ssid, password, device)
    return _nmcli_command(string) 


def disconnect_wifi():
    uuid = get_uuid()
    string = DISCONNECTION_STRING.format(uuid)
    return _nmcli_command(string)


@jsonize 
def get_wifi_list():
    res = _nmcli_command(GET_WIFI_LIST_QUERY)
    res = [i.decode("utf-8").split(':') for i in res.splitlines()]
    formatted_data = {}

    for item in res:
        if item[1].isdigit():
            signal = int(item[1])
        else:
            signal = item[1]
        formatted_data[item[0]] = signal 
    return formatted_data


if __name__ == "__main__":
    print(wifi_status())