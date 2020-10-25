
costruisci l'immagine e instanziala

```bash
$ docker build -t rockpis .
$ docker run -d -P --name test_sshd rockpis
$ docker port test_sshd 22
```

connettiti all'istanza tramite ssh:

```bash
$ ssh root@172.17.0.2
```
