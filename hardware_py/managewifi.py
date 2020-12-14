#!/usr/bin/env python3

import re
import subprocess as sp 

DEBUG                   = 1
WIFI_DEVICE             = re.compile(r'^w.+0$')
CONNECTION_STRING       = "nmcli d wifi connect {} password {} ifname {}"
DISCONNECTION_STRING    = "nmcli con down id {}"
UUID_QUERY              = "nmcli -g DEVICE,UUID con show"
DEVICE_NAME_QUERY       = "nmcli -g DEVICE con show"


def get_uuid():
    res = _nmcli_command(UUID_QUERY)
    res = res.splitlines()

    for dev in res:
        device = dev.decode('utf-8').split(':')
        if re.search(WIFI_DEVICE, device[0]):
            return device[1]


def wifi_device_name():
    res = [i.decode('utf-8') for i in sp.check_output(DEVICE_NAME_QUERY).splitlines() if re.search(WIFI_DEVICE, i.decode('utf-8'))]
    device_name = res[0]
    return device_name 


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


if __name__ == "__main__":
    connect_wifi("vodafone", "antani", "stocazzo")
