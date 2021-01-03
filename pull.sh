#!/usr/bin/env bash

for d in ROCKPIS-*; do
	echo "Pulling ${d}"
	cd $d
	git pull
	cd .. 
done
