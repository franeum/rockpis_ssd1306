#!/bin/bash

# eseguire da sudo

conn=$(nmcli --terse d wifi | grep "*:")

# args: ssid, ssid_connessa

compare() {
    #connessione=$1
    IFS=':'
    read -ra ADDR <<< $1
    if [ "${ADDR[1]}" = "$2" ]; then
        echo Sei già connesso alla rete preferita
    else
        echo Non sei connesso alla tua rete preferita
    fi        
}

: '
nmcli --terse d wifi | grep "*:"

if [ $? -eq 0 ]; then
    nmcli d wifi list	
else
    if [ $# -ge 2 ]; then 
        compare $1
        nmcli r wifi on 
        nmcli d wifi connect $1 password $2
        nmcli d wifi list
    else
        echo you must provide SSID name and PASSWORD
    fi
fi 
'

compare $conn $1 
