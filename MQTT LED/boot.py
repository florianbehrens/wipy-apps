from network import WLAN
import machine

# configure the WLAN subsystem in station mode (the default is AP)
wlan = WLAN(mode=WLAN.STA)
nets = wlan.scan() # scan for available networks
for net in nets:
    if net.ssid == 'AndroidAP':
        wlan.connect(net.ssid, auth=(net.sec, 'micropython'), timeout=5000)

        while not wlan.isconnected():
            machine.idle() # save power while waiting

        print('WLAN connection succeeded!')
        break
