import paho.mqtt.client as mqtt
import time
import requests
from datetime import datetime
import os
import cv2
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
from datetime import datetime

# Load the BLIP processor and model
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Check if the webcam is opened correctly
if not cap.isOpened():
    print("Error: Could not open webcam.")
    print("Attempting alternative index...")
    cap = cv2.VideoCapture(1)
    exit()

DISTANCE_DATA_FILE = "distance_data.txt"
TEMPERATURE_DATA_FILE = "temperature_data.txt"
image_path = "static/guest_image.jpg"


def describe_facial_expression(image_path):

    image = Image.open(image_path).convert("RGB")

    # Preprocess the image and prepare inputs for the model
    inputs = processor(images=image, return_tensors="pt")

    # Generate a caption
    caption = model.generate(**inputs)
    description = processor.decode(caption[0], skip_special_tokens=True)

    return description


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
        file.write("Distance below threshold of 100 cm for 3 seconds!!! Someone is approaching!")

    # todo: use laptop camera to capture image, save it, do computer vision
    # Capture a frame
    ret, frame = cap.read()

    if ret:
        # Save the captured image to a file
        cv2.imwrite('static/guest_image.jpg', frame)
        print("Image captured and saved successfully!")
    else:
        print("Error: Could not capture image.")
        

    # describe the image we captured
    description = describe_facial_expression(image_path)
    with open(file_path, "w") as file:
        file.write("This is our previous guest:" + description)


if __name__ == '__main__':
    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="broker.hivemq.com", port=1883, keepalive=60)
    client.loop_start()

    while True:
       
        time.sleep(1)
            

