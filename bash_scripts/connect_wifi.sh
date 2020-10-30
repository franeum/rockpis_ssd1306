#!/bin/bash

# eseguire da sudo

connect() {
	nmcli r wifi on;
	nmcli d wifi list;
	nmcli d wifi connect $1 password $2;
}

connect $1 $2
