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

con ```alsamixer``` possiamo configurare i dac e gli adc

starting puredata with output device 3: 
```
puredata -nogui -alsa -audiodev 3,3 -inchannels 8 file.pd
```
