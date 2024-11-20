import time
import RPi.GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

import sys
import time
# By appending the folder of all the GrovePi libraries to the system path here,
# we are successfully `import grovepi`
sys.path.append('./Python/')

import grovepi


#define ports here, subject to change
green_led = 11
red_led = 12
ultrasonic_port = 4

#using physical pin to blink an LED

GPIO.setmode(GPIO.BOARD)
chan_list = [green_led, red_led]
GPIO.setup(chan_list, GPIO.OUT)

# Hardware SPI configuration:
# Communicate light sensor over SPI
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

# brightness threshold
lux_threshold=300  

while True: 

  brightness = mcp.read_adc(0)
  distance = grovepi.ultrasonicRead(ultrasonic_port)

  # MQTT topics: (1) brightness (2) distance (3) dialog box/text
  # todo: send brightness and distance data to laptop over MQTT (1)(2)

  time.sleep(0.5)

  if brightness < lux_threshold:
    # todo: send “too dark! system may be breached” to laptop over MQTT (3)
    pass

  else:
    # todo: send “system operating” to laptop over MQTT (3)


    if distance <= 50:




