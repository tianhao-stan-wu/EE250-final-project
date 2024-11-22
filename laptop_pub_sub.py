import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    #subscribe to the ultrasonic ranger topic here
    client.subscribe("home/ultrasonic")
    client.message_callback_add("home/ultrasonic", ranger_callback)
    client.subscribe("home/temperature")
    client.message_callback_add("home/temperature", temperature_callback)

#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

def ranger_callback(client, userdata, msg):
    
    print(msg.topic, str(msg.payload, "utf-8"))

def temperature_callback(client, userdata, msg):
    
    print(msg.topic, str(msg.payload, "utf-8"))


if __name__ == '__main__':
    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="broker.hivemq.com", port=1883, keepalive=60)
    client.loop_start()

    while True:
       
        time.sleep(1)
            

