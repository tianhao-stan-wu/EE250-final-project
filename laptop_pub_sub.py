import paho.mqtt.client as mqtt
import time
import requests
from datetime import datetime
import os

DISTANCE_DATA_FILE = "distance_data.txt"
TEMPERATURE_DATA_FILE = "temperature_data.txt"


from datetime import datetime

def write_to_file(topic, value, file):
    """
    Function to write data to the file while ensuring it has no more than 10 lines.
    :param topic: Topic name
    :param value: Value received
    :param file: File path
    """
    try:
        # Read all lines from the file if it exists
        if os.path.exists(file):
            with open(file, "r") as f:
                lines = f.readlines()
        else:
            lines = []

        # If more than 10 lines, remove the first line
        if len(lines) >= 10:
            lines = lines[1:]  # Remove the first line

        # Add the new data to the last line
        timestamp = datetime.now().strftime("%H:%M:%S")
        new_line = f"{timestamp},{topic},{value}\n"
        lines.append(new_line)

        # Write the updated lines back to the file
        with open(file, "w") as f:
            f.writelines(lines)

        print(f"Data stored: {new_line.strip()}")

    except Exception as e:
        print(f"Error writing to file: {e}")


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
    print(msg.topic, value)
    write_to_file(msg.topic, value, DISTANCE_DATA_FILE)


def temperature_callback(client, userdata, msg):
    
    value = str(msg.payload, "utf-8")
    print(msg.topic, value)
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
            

