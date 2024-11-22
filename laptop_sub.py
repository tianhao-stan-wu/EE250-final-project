# Team: Tianhao Wu, Jojo Ibalio
# github: https://github.com/usc-ee250-fall2024/mqtt-tianhao/tree/lab5/ee250/lab05

"""EE 250L Lab 04 Starter Code

Run vm_subscriber.py in a separate terminal on your VM."""

import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    #subscribe to the ultrasonic ranger topic here
    client.subscribe("wutianha/ultrasonicRanger")
    client.subscribe("wutianha/button")
    client.message_callback_add("wutianha/button", button_callback)

#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))
    
def custom_callback(client, userdata, message):
    # customized callback
    # print(message.topic)
    
    print(f"VM:{str(message.payload, "utf-8")} cm")

def button_callback(client, userdata, message):
    
    print(str(message.payload, "utf-8"))


if __name__ == '__main__':
    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = custom_callback
    client.on_connect = on_connect
    client.connect(host="broker.hivemq.com", port=1883, keepalive=60)
    client.loop_start()

    while True:
       
        time.sleep(1)
            

