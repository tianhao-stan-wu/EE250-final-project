import paho.mqtt.client as mqtt
import time
from pynput import keyboard
import threading

led = "wutianha/led"
lcd = "wutianha/lcd"

client = mqtt.Client()

def kbd_thread():
    while True:
        # must hit enter to complete the input
        k = input("")
        if(k == 'a'):
                print("Got an a")
                client.publish(led, "LED_ON")
                client.publish(lcd, "a")

        elif(k == 'd'):
                print("Got an d")
                client.publish(led, "LED_OFF")
                client.publish(lcd, "d")

        elif(k == 'w'):
                print("Got an w")
                client.publish(lcd, "w")

        elif(k == 's'):
                print("Got an s")
                client.publish(lcd, "s")

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    #subscribe to topics of interest here

#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

def on_press(key):
    try: 
        k = key.char # single-char keys
    except: 
        k = key.name # other keys
    
    if k == 'w':
        print("w")
        #send "w" character to rpi
        # client.publish(lcd, "w")
    elif k == 'a':
        print("clicked a")
        # send "a" character to rpi
        # client.publish(lcd, "a")
        #send "LED_ON"
        client.publish(led, "LED_ON")
    elif k == 's':
        print("s")
        # send "s" character to rpi
        # client.publish(lcd, "s")
    elif k == 'd':
        print("clicked d")
        # send "d" character to rpi
        # client.publish(lcd, "d")
        # send "LED_OFF"
        client.publish(led, "LED_OFF")

if __name__ == '__main__':
    #setup the keyboard event listener
    # lis = keyboard.Listener(on_press=on_press)
    # lis.start() # start to listen on a separate thread
    thread = threading.Thread(target=kbd_thread)
    thread.start()

    #this section is covered in publisher_and_subscriber_example.py
    
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="broker.hivemq.com", port=1883, keepalive=60)
    client.loop_start()

    while True:
        
        time.sleep(1)

            

