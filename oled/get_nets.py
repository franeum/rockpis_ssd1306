#!/usr/bin/env python3

import subprocess

def wifi_list():
    CMD = ['nmcli','-g','SSID','device','wifi']
    wifi_list = subprocess.check_output(CMD, shell=True).decode("utf-8")
    wifi_list = [x.strip(None) for x in wifi_list.splitlines()]
    return wifi_list