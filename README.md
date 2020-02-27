# rockpis for audio  
Appunti sparsi di configurazione della scheda [Rock Pi S](https://wiki.radxa.com/RockpiS)

----------

# Indice  
1. [Pinout](#pinout)
1. [Collegarsi a `rockpis` tramite `ssh`](#collegarsi-a-rockpis-via-ssh)
    * [Collegarsi a rockpis con debian](#collegare-la-*rockpis*-via-ssh-su-debian)  
    * [Collegarsi a rockpis con Mac OS X](#mac-os-x)  

2. [Aggiornare il sistema e installare il software per l'audio](#preparing-the-system)
3. [Configurazione del wifi](#configurazione-del-wifi)
5. [Installare e avviare `puredata`](#installare-e-avviare-puredata)  
6. [Avviare `puredata` al boot di rockpis](avviare-puredata-al-boot-di-rockpis)  
7. [setup di `jack`](#setup-di-jack)  
8. [`jack` in realtime priority](#jack-in-realtime-priority)  
9. [Installazione di `supercollider`](#installazione-di-supercollider)   
10. [Uso di un display virtuale con `xvfb`](#uso-di-un-display-virtuale-con-xvfb)   
    * [Installazione di `xvfb`](#installazione-di-xvfb)  
    * [avvio e test di sclang con `xvfb`](#avvio-e-test-di-sclang-con-xvfb)   
 
11. [Esecuzione di uno script sc](#esecuzione-di-uno-script-sc)    
12. [Opzione `python`](#opzione-python)

## Collegarsi a rockpis via ssh
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
l'ip potrebbe essere qualcosa come 10.0.x.x oppure 192.168.x.x. Annotare i primi 3 valori (es: 10.0.1 oppure 192.168.1). questi rappresentano l'indirizzo di sottorete (*subnet_addr*) che ci interessa. 

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




## Mac OS X

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
oppure (più comodo):
```
ssh rock@rockpis
```
* inserire la password (`rock`)





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
```
verificare che lo spazio sulla SDcard sia giusto:
```
df -h
```
in caso di dimensioni errate eseguire le operazioni indicate in questo tutorial:  
[link](https://www.youtube.com/watch?v=R4VovMDnsIE)



## Configurazione del wifi

attivare la connessione tramite il frontend ```nmtui``` di ```nm``` sull'interfaccia wireless ```wlan0```
```
sudo nmtui
```
puredata riceve tranquillamente i messaggi tramite l'oggetto ```netreceive```. 
TODO: una *patch* generica di ricezione.

Una volta che la connessione wi-fi del rockpis è attiva è possibile connettersi con lo stesso tramite il protocollo ```ssh```:

```
ssh rock@192.168.1.11
```

e scollegare quindi il cavo ethernet. Il rockpis comincia a camminare con le sue gambe!


-----------------------------


## pinout
<p align="center">
  <img src="/immagini/rockpis_audio_interface.png" alt="drawing" width="300"/>
</p>

*N.B. Nella versione 1.2 della scheda, i microfoni 3 e 4 sono stati eliminati, quindi restano attivi i microfoni 1,2,5,6,7,8*


## installare e avviare puredata

```
sudo apt install puredata
```
con ```alsamixer``` possiamo configurare i dac e gli adc

starting puredata with output device 3: 
```
puredata -nogui -alsa -audiodev 3,3 -inchannels 8 file.pd
```

Per avviare `puredata` con `jackd`:
```
puredata -nogui -jack file.pd
```
dopo aver [configurato opportunamente](#setup-di-jack) `jack`. Se `jack` non si auto-avvia all'avvio di `puredata`, eseguire da shell il coseguente comando:

``` 
bash ./.jackdrc
```


## avviare puredata al boot di rockpis

1. installare **cron** 
```
sudo apt install cron
```
2. eseguire il seguente comando:
```
crontab -e
```
3. aggiungere questa voce al file che si apre:
```
@reboot puredata -nogui -alsa -audiodev 3,3 -inchannels 8 /path/to/file.pd
```
in questo modo il file file.pd si avvia con pd all'avvio del rockpis.


## setup di jack

varificare il nome del dispositivo audio con il comando:
```
cat /proc/asound/cards
```
nel mio caso il dispositivo è ```rockchiprk3308a```.  
Per avviare `jackd` su richiesta copiare la seguente riga nel file `~/.jackdrc` (se il file non esiste, crearlo con `vim ~/.jackdrc`):
```
/usr/bin/jackd -R -P 95 -d alsa -d hw:rockchiprk3308a -r 44100 -p 256
```
l'opzione -p è 1024, verificare che il valore 256 non crei troppi dropouts. In quel caso incrementare il valore (che deve essere una potenza di 2).



## jack in realtime priority

l'opzione -R del comando precedente tendenzialmente non funziona e restituisce il seguente errore:
```
Cannot use real-time scheduling (RR/95)(1: Operation not permitted)
```
Per abilitare la priorità realtime è necessario compiere i seguenti passi:


1. Nella directory `/etc/security/limits.d/` verificare la presenza del file `audio.conf.disabled`. Se presente copiare il file con il nome `audio.conf`, tramite il seguente comando:
```
sudo cp audio.conf.disabled audio.conf
```

2. Nel file `audio.conf` verificare la presenza delle seguenti righe 
```
@audio   -  rtprio     95
@audio   -  memlock    unlimited
```

3. Verificare l'esistenza del gruppo `audio` nel sistema con il comando `groups`. Se il grouppo non esiste, crearlo tramite il seguente comando:
```
sudo groupadd audio
```

4. Aggiungere l'utente al gruppo `audio`:
```
sudo usermod -a -G audio yourUserID
```
dove yourUserID sarà presumibilmente `rock`

5. Uscire dal sistema e riloggarsi con `ssh`



## Installazione di supercollider
```
sudo apt install supercollider
```

### uso di un display virtuale con xvfb
#### installazione di xvfb
```
sudo apt update
sudo apt install [-y] xvfb --fix-missing
```

#### avvio e test di sclang con xvfb
```
xvfb-run --auto-servernum /usr/bin/sclang ["$ @"]
```

A questo punto si apre un terminale interattivo `sclang`. Avviare il server:
```
s.boot
```
Create una funzione:
```
{SinOsc.ar([440,442],0,0.5)}.play
```
Spegnere il server e uscire dalla sessione interattiva:
```
s.quit
0.quit
```

#### esecuzione di uno script sc

Per eseguire uno script sc è succifiente eseguire il seguente comando:
```
xvfb-run --auto-servernum /usr/bin/sclang file.scd
```
All'interno del file è bene incapsulare come primo argomento del metodo `.waitForBoot()`.  

Esempio:
1. con `vim` creare il file `test.scd` e scrivere al suo interno le seguenti righe:
```
Server.default.waitForBoot({
        {SinOsc.ar([440,442],0,0.5)}.play
})
```
2. salvare e uscire con `:wq`
3. eseguire il seguente comando per avviare `sclang` con `scsynth` e `jackd`:
```
xvfb-run --auto-servernum sclang test.scd  
```


### opzione python (non ancora funzionante)

Sclang ha bisogno di un display per funzionare, quindi data l'assenza dello stesso in rockpis, bisogna cercare un ambiente alternativo per guidare Scsynth. L'opzione è python e il modulo ```supercollider```. Successivamente all'installazione del software si può inviare al rockpis il file con le ```synthdefs```, avviare il motore audio (Scsynth) e iniziare a guidarlo da python.

#### installazione del software necessario

Eseguire questi comandi per installare il software:

```python
sudo apt install supercollider
sudo apt install liblo7 liblo-dev
pip3 install Cython
pip3 install liblo
pip3 install supercollider
```
*N.B. l'installazione di Cython potrebbe essere molto lunga*

### 

# TODO:
1. preparare delle synthDefs e inviarle a ```~/.local/share/SuperCollider/synthdefs```
2. installare in python il modulo ```supercollider```
3. avviare il server(```scsynth```)
4. testare 
