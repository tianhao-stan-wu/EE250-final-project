# EE250-final-project

## Team Members
- Tianhao Wu
- Jojo Ibalio

---

## Instructions to Execute the Program(s)

- Connect temperature/humidity sensor to port D2 and ultrasonic ranger to D4 with your RPI
- To execute the program, run the following command in your local host terminal:
 ```
 python laptop_pub_sub.py
 python web.py
 ```
- Open a browser and use http://127.0.0.1:5050 for visualization
- Run the following command in your RPI terminal:
 ```
 python rpi_pub_sub.py
 ```

---

## External Libraries Used

1. **paho-mqtt**: Provides MQTT client functionality to send and receive messages.
2. **requests**: Enables making HTTP requests to interact with web APIs.
3. **transformers**: Offers pre-trained AI models for natural language and vision tasks.
4. **Pillow (PIL)**: Handles image processing and manipulation.
5. **GrovePi**: Interfaces with GrovePi sensors for hardware interaction.
6. **Flask**: Builds a lightweight web interface for visualizing data.
7. **pandas**: Processes and manipulates tabular data efficiently.
8. **matplotlib**: Creates plots and visualizations of data.
9. **OpenCV (cv2)**: Performs computer vision tasks like image capturing.
10. **io**: Handles in-memory file operations for data visualization.
11. **os**: Manages file paths and interactions with the operating system.
12. **datetime**: Works with date and time data for timestamps and formatting.



