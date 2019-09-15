# myrockpis_test

upgrade system:
```
sudo apt-get update
sudo apt-get dist-upgrade
```
install alsa: 
```
sudo apt install alsa-tools
sudo apt install puredata
```
starting puredata with output device 3: 
```
puredata -nogui -alsa -outchannels 3 file.pd
```
