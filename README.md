# EE250-final-project

## Team Member Names
- Member 1: [Tianhao Wu]
- Member 2: [Jojo Ibalio]

---

## Instructions to Compile/Execute the Program(s)

**Running the Program**:
   - Connect temperature/humidity sensor to port D2 and ultrasonic ranger to D4 with your RPI
   - To execute the program, run the following command in your local host terminal:
     ```
     python laptop_pub_sub.py
     python web.py
     ```
   - Run the following command in your RPI terminal:
     ```
     python rpi_pub_sub.py
     ```

---

## External Libraries Used

1. **paho-mqtt**:
   - Description: A client library for connecting to MQTT brokers to send and receive messages.
   - Purpose: Enables communication between devices using the MQTT protocol.

2. **requests**:
   - Description: A library for making HTTP requests in Python.
   - Purpose: Used to interact with web APIs for data retrieval.

3. **transformers**:
   - Description: Hugging Face library for natural language processing and vision-language tasks.
   - Purpose: Used for image captioning and conditional generation tasks with pre-trained models.

4. **Pillow (PIL)**:
   - Description: A Python Imaging Library fork for image processing.
   - Purpose: Processes and handles images for tasks like input to AI models.

5. **GrovePi**:
   - Description: A library for interfacing with GrovePi sensors.
   - Purpose: Enables communication with GrovePi sensors like ultrasonic rangers.

6. **Flask**:
   - Description: A lightweight web framework for building web applications.
   - Purpose: Serves the web interface for visualizing data.

7. **pandas**:
   - Description: A powerful data analysis and manipulation library.
   - Purpose: Handles tabular data and file processing for data visualization.

8. **matplotlib**:
   - Description: A plotting library for creating static, animated, and interactive visualizations.
   - Purpose: Used to generate real-time visualizations and plots of sensor data.

9. **OpenCV (cv2)**:
   - Description: A library for computer vision tasks.
   - Purpose: Handles image capturing and processing tasks.

10. **io**:
    - Description: A standard library module for handling streams and file operations.
    - Purpose: Generates in-memory files for visualizations.

11. **os**:
    - Description: A standard library module for interacting with the operating system.
    - Purpose: Manages file paths, directories, and environment variables.

12. **datetime**:
    - Description: A standard library module for working with dates and times.
    - Purpose: Handles timestamps and formatting of date-time values.


