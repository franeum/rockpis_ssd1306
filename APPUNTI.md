## caso d'uso (primo utilizzo)

### connettere `rockpis` al wifi alla prima accensione:

1. accendo per la prima volta il `rockpis`
2. attivo l'`access point` tramite pulsante (5 secondi di pressione + reboot?):
    1. attivo un server locale per la configurazione della rete (che espone un'app web)
    2. il display mostra l'ip locale (IP1)
3. dal computer mi connetto alla rete che viene creata dall'`access point` (SSID: `rockpitest`)
4. accedo alla webapp all'indirizzo `http://IP1:300`
5. tramite la webapp invio i dati della mia rete alla `rockpis`
6. `rockpis` si connette al wifi della rete
7. riavvio `rockpis`

### dettagli implementativi di cui ai punti precedenti

2.  -   attivazione `accesspoint`: **hostapd.py**
    -   evento su pulsante: **apd_button.py**
    -   oled display: **oled.py**
3.  -   creazione della connessione al wifi: **nmpy.py**

### Attivazione dell'`access point`

1. Se esiste una connessione una connessione attiva, _catturare_ il nome del profilo di connessione

2. Se esiste, impostare il profilo di connessione per non connettersi automaticamente:

```bash
sudo nmcli con modify "$PROFILE" autoconnect no
```

3.  attivare `hostapd` e gli altri servizi connessi:

```bash
sudo -i -- sh -c 'systemctl stop dnsmasq && \
systemctl stop hostapd && \
systemctl restart dhcpcd && \
systemctl start dnsmasq && \
systemctl start hostapd'
```

```bash
sudo nmcli dev disconnect wlan0
```

```bash
sudo -i -- sh -c 'systemctl stop dnsmasq && \
systemctl stop hostapd && \
systemctl restart dhcpcd && \
systemctl start dnsmasq && \
systemctl start hostapd'
```

Prima di creare l'`acces point` accertare l'esistenza di una delle seguenti condizioni:

1.  Esiste una connessione wifi attiva
2.  Non esiste una connessione wifi attiva

Nel primo caso bisogna disattivare la connessione attiva:
nmcli dev disconnect wlan0
