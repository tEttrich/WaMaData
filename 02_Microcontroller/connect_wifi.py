import network
import time
import ntptime

# connect to WiFi
def connect():
    WIFI_SSID = "WLAN-ELBGAU"    # wir haben mittlwerweile einen anderen Router
    WIFI_PW = "74577562839682897270"    # mit anderen Zugangsdaten

    wlan = network.WLAN(network.STA_IF)

    if not wlan.isconnected():
        wlan.active(True)
        print("connecting to network", WIFI_SSID)
        wlan.connect(WIFI_SSID, WIFI_PW)
        while not wlan.isconnected():
            pass

    print("connected:", wlan.ifconfig())
    time.sleep(1)

# set the rtc datetime from the remote server
def synchronize_rtc():
    time.sleep(1)
    ntptime.settime()
    time.sleep(1)
