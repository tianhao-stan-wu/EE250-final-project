import cv2

import paho.mqtt.client as mqtt
import time
import requests
from datetime import datetime
import os
import cv2

cap = cv2.VideoCapture(0)

ret, frame = cap.read()

if ret:
    # Save the captured image to a file
    cv2.imwrite('static/guest_image.jpg', frame)
    print("Image captured and saved successfully!")
else:
    print("Error: Could not capture image.")

# Release the webcam
cap.release()

# Close all OpenCV windows (if any)
cv2.destroyAllWindows()

from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image

def describe_facial_expression(image_path):
    # Load the BLIP processor and model
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

    # Open the image
    image = Image.open(image_path).convert("RGB")

    # Preprocess the image and prepare inputs for the model
    inputs = processor(images=image, return_tensors="pt")

    # Generate a caption
    caption = model.generate(**inputs)
    description = processor.decode(caption[0], skip_special_tokens=True)

    return description

if __name__ == "__main__":
    # Path to your image
    image_path = "static/guest_image.jpg"

    # Generate and print the facial expression description
    description = describe_facial_expression(image_path)
    print(f"Facial Expression Description: {description}")
