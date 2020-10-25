#!/usr/bin/env python3

import subprocess 
import os 
import re 

GETNIX = re.compile(r'ix$') 

def get_available_wifi():
    if re.search(GETNIX, os.name): 
        wifi_list = subprocess.check_output(["nmcli","-g","SSID","dev","wifi"]) 
    else:
        return "NOT YET IMPLEMENTED for other OS than Linux"
    
    wifi_list = [x.strip(None) for x in wifi_list.decode('utf-8').split('\n') if x != ''] 
    return wifi_list 


def enumerate_wifi(lst):
    return [(n,m) for n,m in enumerate(lst)]


if __name__=='__main__':
    enum_lst = enumerate_wifi(get_available_wifi())
    print(enum_lst)
