import paho.mqtt.client as mqtt
import time
import sys

sys.path.append('./Python/')

from grovepi import *
import grovepi

# define ports here
ultra_port = 4
temp_port = 2
blue = 0 # specify kind of temp/humidity sensor

# clock variables
clock = 0
maxWait = 3

threshold = 100 # temperature threshold


def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))
    #subscribe to topics of interest here
    client.subscribe("home/temperature")
    client.subscribe("home/ultrasonic")
    client.subscribe("home/guest")

#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

def lcd_callback(client, userdata, message):
    text = str(message.payload, "utf-8")
    setText_norefresh(text)


if __name__ == '__main__':
    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="broker.hivemq.com", port=1883, keepalive=60)
    client.loop_start()

    while True:
        # Send ultrasonic ranger value to laptop sub
        ultra_val = grovepi.ultrasonicRead(ultra_port)
        client.publish("home/ultrasonic", ultra_val)

        [t,humidity] = dht(temp_port,blue)
        client.publish("home/temperature",t)

        if ultra_val < threshold:
            clock = clock + 1
            if clock == maxWait:
                client.publish("home/guest") # Guest is outside
                clock = 0
        else:
            if clock != 0:
                clock = 0


        time.sleep(1)


        