# myrockpis_test

## Collegare la *rockpis* via ssh su Debian

### creare una connessione tramite la porta ethernet
1. avviare una finestra di terminale e cercare il nome dell'interfaccia ethernet del computer:
```
ip a
```
l'interfaccia sarà **eth0** oppure qualcosa come **enxx**. Questo rappresenta il nostro *eth-device-name*  

2. creare una connessione con il seguente comando:
```
nmcli con add con-name my-eth-1 ifname <eth-device-name> type ethernet ipv4.method shared
```
3. attivare la connessione:
```
nmcli con up my-eth-1
```
4. verificare che la connessione sia attiva:
```
nmcli con show
```
5. ottenere l'ip dell'interfaccia ethernet:
```
ip a
```
l'ip potrebbe essere qualcosa come 10.0.x.x oppure 192.168.x.x. Annotare i primi 3 valori (es: 10.0.1 oppure 192.168.1). questi rappresentano l'indirizzo di sottorete (*subnet_addr*) che ci interessa
6. collegare la *rockpis* alla porta ethernet e pingare l'intera sottorete:
```
fping -r 1 -g subnet_addr.0/24
```
Nel mio caso l'ip della porta ethernet è 10.42.0.1, quindi per pingare la sottorete eseguirò il comando:  
```
fping -r 1 -g 10.42.0.0/24
```
Se tutto ha funzionato il comando dovrebbe restituire almeno due ip, quello della scheda ethernet del computer e quello della rockpis, nel mio caso:
```
$ fping -r 1 -g 10.42.0.0/24 2> /dev/null | grep -v -i unreachable 
10.42.0.1 is alive
10.42.0.250 is alive
```
7. il primo ip è quello locale, il secondo è quello della rockpis, a questo punto possiamo connetterci (l'utente di default è *rock*) alla scheda con il protocollo ssh:
```
ssh rock@10.42.0.250
```
e inserire la password ```rock```




## Mac

connessione con la rockpis:
lato Mac:
* attivare la condivisione internet e il bridge
* da terminale cercare l'ip della scheda:
```
fping -g 192.168.x.0/24
```
* connettersi alla scheda via ssh:
```
ssh rock@192.168.x.x
```
* inserire la password


## Preparing the system

upgrade system:
```
sudo apt-get update
sudo apt-get dist-upgrade
```
install alsa: 
```
sudo apt install alsa-utils
sudo apt install jackd2
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

*TODO: using jackd2 instead of alsamixer*

## pinout

![](/immagini/rockpis_audio_interface.png)

*N.B. Nella versione 1.2 della scheda, i microfoni 3 e 4 sono stati eliminati, quindi restano attivi i microfoni 1,2,5,6,7,8*
