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

2.  attivazione `accesspoint`: hostapd.py
