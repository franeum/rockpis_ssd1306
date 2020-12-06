## add user to group dialout

```bash
(sudo) usermod -a -G dialout <username>
```

## set baudate of serial monitor

Open file `platformio.ini` adn add this line:
```text
monitor_speed = 115200
```

## for linux users only:

install udev rules following [this link](https://docs.platformio.org/en/latest/faq.html#platformio-udev-rules)