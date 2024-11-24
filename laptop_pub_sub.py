import paho.mqtt.client as mqtt
import time
import requests
from datetime import datetime

DISTANCE_DATA_FILE = "distance_data.txt"
TEMPERATURE_DATA_FILE = "temperature_data.txt"


def write_to_file(topic, value, file):
    """
    Function to write data to the file
    :param topic: Topic name
    :param value: Value received
    """
    with open(file, "a") as file:
        # Get current time
        timestamp = datetime.now().strftime("%H:%M:%S")
        file.write(f"{timestamp},{topic},{value}\n")
        print(f"Data stored: {timestamp},{topic},{value}")


def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    #subscribe to the ultrasonic ranger topic here
    client.subscribe("home/ultrasonic")
    client.message_callback_add("home/ultrasonic", ranger_callback)
    client.subscribe("home/temperature")
    client.message_callback_add("home/temperature", temperature_callback)
    client.subscribe("home/guest")
    client.message_callback_add("home/guest", guest_callback)


#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))


def ranger_callback(client, userdata, msg):
    
    value = str(msg.payload, "utf-8")
    write_to_file(msg.topic, value, DISTANCE_DATA_FILE)


def temperature_callback(client, userdata, msg):
    
    value = str(msg.payload, "utf-8")
    write_to_file(msg.topic, value, TEMPERATURE_DATA_FILE)


def guest_callback(client, userdata, msg):
    
    file_path = "web.txt"

    
    with open(file_path, "w") as file:
        file.write("Distance below threshold of 100 cm for 3 seconds!!!")

    # todo: use laptop camera to capture image, save it, do computer vision

    time.sleep(3)

    with open(file_path, "w") as file:
        file.write("")


if __name__ == '__main__':
    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="broker.hivemq.com", port=1883, keepalive=60)
    client.loop_start()

    while True:
       
        time.sleep(1)
            

