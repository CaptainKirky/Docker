import time
from datetime import date

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import subprocess

# Raspberry Pi pin configuration:
RST = None     # on the PiOLED this pin isnt used
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

# 128x32 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)


# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0


# Load default font.
font = ImageFont.load_default()

# Alternatively load a TTF font.  Make sure the .ttf font file is in the same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
# font = ImageFont.truetype('Minecraftia.ttf', 8)

mqttMainBedTemp = 0
mqttKitchenTemp = 0
mqttGarageInsideTemp = 0

mqttGWOfficeTemp = 0
mqttGWFrontTemp = 0
mqttGWLoungeTemp = 0


def on_connect(client, userdata, flags, rc):
     print("Connected with result code "+str(rc))
     client.subscribe("#")



def on_message(client, userdata, msg):
    global mqttMainBedTemp
    global mqttKitchenTemp
    global mqttGarageInsideTemp
    global mqttGWOfficeTemp
    global mqttGWFrontTemp
    global mqttGWLoungeTemp


    draw.rectangle((0,0,width,height), outline=0, fill=0)
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    today = str(date.today())
    mqqttemp =  msg.payload.decode() 
    print("Topic "+str(msg.topic) + " Value " + str(msg.payload.decode()) )
    if msg.topic == "MainBedTemp":
        mqttMainBedTemp = round(float(mqqttemp),1)
    elif msg.topic == "KitchenTemp":
        mqttKitchenTemp = round(float(mqqttemp),1)
    elif msg.topic == "GarageInsideTemp":
        mqttGarageInsideTemp = round(float(mqqttemp),1)
    elif msg.topic == "GWOfficeTemp":
        mqttGWOfficeTemp = round(float(mqqttemp),1)
    elif msg.topic == "GWFrontTemp":
        mqttGWFrontTemp = round(float(mqqttemp),1)
    elif msg.topic == "GWLoungeTemp":
        mqttGWLoungeTemp = round(float(mqqttemp),1)
    draw.text((x, top),       "Bed"+ str(mqttMainBedTemp) + "| Kit "+ str(mqttKitchenTemp) + " |OS "+ str(mqttGarageInsideTemp),  font=font, fill=255)
    draw.text((x, top+12),    "Off"+ str(mqttGWOfficeTemp) + "| Frn "+ str(mqttGWFrontTemp) + " |Kit "+ str(mqttGWLoungeTemp),  font=font, fill=255)
    draw.text((x, top+24),     str(today) + "   " + str(current_time), font=font, fill=255)
    disp.image(image)
    disp.display()
    time.sleep(.1)

    
client = mqtt.Client()
client.username_pw_set(username="bckMQTT", password="bckBrAaI")
client.connect("192.168.0.149",1883,60)

client.on_connect = on_connect
client.on_message = on_message

client.loop_forever()


