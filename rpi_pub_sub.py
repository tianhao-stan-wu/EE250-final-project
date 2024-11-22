import paho.mqtt.client as mqtt
import time

import sys
# By appending the folder of all the GrovePi libraries to the system path here,
# we are successfully `import grovepi`
sys.path.append('../../Software/Python/')
# This append is to support importing the LCD library.
sys.path.append('../../Software/Python/grove_rgb_lcd')

from grove_rgb_lcd import *
from grovepi import *
import grovepi


ultra_port = 4
# led_port = 2
temp_port = 2
# button_port = 3
# light_port = 3
# pinMode(led_port,"OUTPUT")
# pinMode(button_port, "INPUT")


def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    #subscribe to topics of interest here
    client.subscribe("home/temperature")
    client.subscribe("home/ultrasonic")
    client.message_callback_add("wutianha/lcd", lcd_callback)

#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

# def callback_led(client, userdata, message):
#     print(message.topic)
#     text = str(message.payload, "utf-8")
#     if message.topic == "wutianha/led":
#         if text == "LED_ON":
#             print("led on received")
#             digitalWrite(led_port,1)
#         elif text == "LED_OFF":
#             print("led off received")
#             digitalWrite(led_port,0)

def lcd_callback(client, userdata, message):
    
    text = str(message.payload, "utf-8")
    setText_norefresh(text)


if __name__ == '__main__':
    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = callback_led
    client.on_connect = on_connect
    client.connect(host="broker.hivemq.com", port=1883, keepalive=60)
    client.loop_start()

    while True:
        # Send ultrasonic ranger value to laptop sub
        ultra_val = grovepi.ultrasonicRead(ultra_port)
        client.publish("home/ultrasonic", ultra_val)
        # Send light sensor value to sub
        temp_val = grovepi.temp(temp_port,'1.2')
        client.publish("home/temperature",temp_val)
        # if grovepi.digitalRead(button_port):
        #     print("pressed")
        #     client.publish("wutianha/button", "Button Pressed!")
        time.sleep(1)