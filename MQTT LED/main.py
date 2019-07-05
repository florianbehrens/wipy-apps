from machine import Pin, unique_id
from mqtt import MQTTClient
import pycom
import time
from ubinascii import hexlify

LED_STATE_TOPIC = "florianbehrens/feeds/led.state"

class MQTT_QoS:
    AT_MOST_ONCE = 0
    AT_LEASE_ONCE = 1
    EXACTLY_ONCE = 2  # Not supported by Adafruit IO!

button_changed = False

def sub_cb(topic_bytes, msg_bytes):
    topic = topic_bytes.decode()
    msg = msg_bytes.decode()

    if topic == LED_STATE_TOPIC:
        if msg == "ON":
            pycom.rgbled(0xff00)
        else:
            pycom.rgbled(0)

def button_cb(pin):
    global button_changed
    button_changed = True

pycom.heartbeat(False)

client = MQTTClient(hexlify(unique_id()), "io.adafruit.com", user="florianbehrens", password="a02c9559b526437b9edd51109b16077a", port=1883)
client.set_callback(sub_cb)
client.connect()
client.subscribe(topic=LED_STATE_TOPIC)

button = Pin('P14', mode=Pin.IN, pull=None)
button.callback(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=button_cb)

while True:
    client.check_msg()

    if button_changed == True:
        button_changed = False

        if button() == 0:
            msg = "ON"
        else:
            msg = "OFF"

        # Note: The retain flag is not supported by Adafruit IO!
        # https://io.adafruit.com/blog/#mqtt-get-and-the-case-of-the-missing-retain-flag
        client.publish(topic=LED_STATE_TOPIC, msg=msg.encode(), retain=True, qos=MQTT_QoS.AT_LEASE_ONCE)

    time.sleep(.1)
