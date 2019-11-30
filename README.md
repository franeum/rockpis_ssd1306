# myrockpis_test

upgrade system:
```
sudo apt-get update
sudo apt-get dist-upgrade
```
install alsa: 
```
sudo apt install alsa-utils
sudo apt install puredata
```
verificare che lo spazio sulla SDcard sia giusto:
```
df -h
```
in caso di dimensioni errate eseguire le operazioni indicate in questo tutorial:  
https://www.youtube.com/watch?v=R4VovMDnsIE

starting puredata with output device 3: 
```
puredata -nogui -alsa -audiooutdev 3 file.pd
```
