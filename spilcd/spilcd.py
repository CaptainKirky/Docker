from luma.core.interface.serial import spi
#from luma.lcd.device import ili9341
from luma.core.render import canvas
from PIL import ImageFont

from astral import LocationInfo
from astral.sun import sun
import pytz
from datetime import datetime

import sys
import time

import paho.mqtt.client as mqtt

Location = sys.argv[1]
ScreenType = sys.argv[2]

print(ScreenType)

# SPI setup
serial = spi(
    port=0,
    device=0,
    gpio_DC=25,
    gpio_RST=27,
    bus_speed_hz=40000000
)

# Display setup
if ScreenType == "ili9341":
    print("ili9341")
    from luma.lcd.device import ili9341
    device = ili9341(
        serial,
        width=320,
        height=240,
        rotate=0
    )
elif ScreenType == "st7789":
    print("st7789")
    from luma.lcd.device import st7789
    device = st7789(
        serial,
        width=320,
        height=240,
        rotate=1
    )

font = ImageFont.truetype(
    "/home/pi/.local/share/fonts/FUTURAM/16020_FUTURAM.ttf",
25
)
font1 = ImageFont.truetype(
    "/home/pi/.local/share/fonts/FUTURAM/16020_FUTURAM.ttf",
17
)
font2 = ImageFont.truetype(
    "/home/pi/.local/share/fonts/FUTURAM/16020_FUTURAM.ttf",
14
)

def on_connect(client, userdata, flags, rc):
     print("Connected with result code "+str(rc))
     client.subscribe(Location)

try:
    import urandom as random
except ImportError:
    import random

def on_message(client, userdata, msg):
#Pressure
    global DLKitchenPressure
#Kitchen
    global DLKitchenTemp
    global DLKitchenHumidity
    global DLKitchenGasPercentage
#Drumaline Office
    global DLOfficeTemp
    global DLOfficeHumidity
    global DLOfficeGasPercentage
#Drumaline MainBed
    global DLMainBedTemp
    global DLMainBedHumidity
    global DLMainBedGasPercentage
#Drumaline Lounge
    global DLLoungeTemp
    global DLLoungeHumidity
#Drumaline KateBed
    global DLKateBedTemp
    global DLKateBedHumidity
#Drumaline MattBed
    global DLMattBedTemp
    global DLMattBedHumidity
#Drumaline Loft
    global DLLoftTemp
    global DLLoftHumidity
#Drumaline Garage
    global DLGarageTemp
    global DLGarageHumidity
#Greenway Kitchen
    global GWKitchenTemp
    global GWKitchenHumidity
    global GWKitchenGasPercentage
#Greenway FrontRoom    
    global GWFrontRoomTemp
    global GWFrontRoomHumidity
    global GWFrontRoomGasPercentage
#Greenway Main bed 
    global GWTopFloorTemp
    global GWTopFloorHumidity
    global GWTopFloorGasPercentage

    if msg.topic == "DLKitchenPressure":
        DLKitchenPressure = "{:.1f}hPa".format(float(msg.payload.decode()))
    elif msg.topic == "DLKitchenTemp":
        DLKitchenTemp = "{:.1f}C".format(float(msg.payload.decode()))
    elif msg.topic == "DLKitchenHumidity":
        DLKitchenHumidity = "{:.1f}%".format(float(msg.payload.decode()))
    elif msg.topic == "DLKitchenGas":
        DLKitchenGasPercentage = "{:.1f}%".format(float(msg.payload.decode())/1067)
    elif msg.topic == "DLOfficeTemp":
        DLOfficeTemp = "{:.1f}C".format(float(msg.payload.decode()))
    elif msg.topic == "DLOfficeHumidity":
        DLOfficeHumidity = "{:.1f}%".format(float(msg.payload.decode()))
    elif msg.topic == "DLOfficeGas":
        DLOfficeGasPercentage = "{:.1f}%".format(float(msg.payload.decode())/1828)
    elif msg.topic == "DLMainBedTemp":
        DLMainBedTemp = "{:.1f}C".format(float(msg.payload.decode()))
    elif msg.topic == "DLMainBedHumidity":
        DLMainBedHumidity = "{:.1f}%".format(float(msg.payload.decode()))
    elif msg.topic == "DLMainBedGasPercentage":
        DLMainBedGasPercentage = "{:.1f}%".format(float(msg.payload.decode()))
    elif msg.topic == "DLLoungeTemp":
        DLLoungeTemp = "{:.1f}C".format(float(msg.payload.decode()))
    elif msg.topic == "DLLoungeHumidity":
        DLLoungeHumidity = "{:.0f}%".format(float(msg.payload.decode()))
    elif msg.topic == "DLKateBedTemp":
        DLKateBedTemp = "{:.1f}C".format(float(msg.payload.decode()))
    elif msg.topic == "DLKateBedHumidity":
        DLKateBedHumidity = "{:.0f}%".format(float(msg.payload.decode()))
    elif msg.topic == "DLMattBedTemp":
        DLMattBedTemp = "{:.1f}C".format(float(msg.payload.decode()))
    elif msg.topic == "DLMattBedHumidity":
        DLMattBedHumidity = "{:.0f}%".format(float(msg.payload.decode()))
    elif msg.topic == "LoftTemp":
        DLLoftTemp = "{:.1f}C".format(float(msg.payload.decode()))
    elif msg.topic == "DLLoftHumidity":
        DLLoftHumidity = "{:.0f}%".format(float(msg.payload.decode()))
    elif msg.topic == "GarageInsideTemp":
        DLGarageTemp = "{:.1f}C".format(float(msg.payload.decode()))
    elif msg.topic == "DLGarageHumidity":
        DLGarageHumidity = "{:.0f}%".format(float(msg.payload.decode()))
    elif msg.topic == "GWLoungeTemp":
        GWKitchenTemp = "{:.1f}C".format(float(msg.payload.decode()))
    elif msg.topic == "GWLoungeHumidity":
        GWKitchenHumidity = "{:.0f}%".format(float(msg.payload.decode()))
    elif msg.topic == "GWLoungeGas":
        GWKitchenGasPercentage = "{:.1f}%".format(float(msg.payload.decode())/510)
    elif msg.topic == "GWFrontTemp":
        GWFrontRoomTemp = "{:.1f}%".format(float(msg.payload.decode()))
    elif msg.topic == "GWFrontHumidity":
        GWFrontRoomHumidity = "{:.0f}%".format(float(msg.payload.decode()))
    elif msg.topic == "GWFrontGas":
        GWFrontRoomGasPercentage = "{:.1f}%".format(float(msg.payload.decode())/650)
    elif msg.topic == "GWTopFloorTemp":
        GWTopFloorTemp = "{:.1f}C".format(float(msg.payload.decode()))
    elif msg.topic == "GWTopFloorHumidity":
        GWTopFloorHumidity = "{:.0f}%".format(float(msg.payload.decode()))
    elif msg.topic == "GWTopFloorGas":
        GWTopFloorGasPercentage = "{:.0f}Ohm".format(float(msg.payload.decode()))

    timezone="Europe/London"
    city = LocationInfo(latitude=51.379608, longitude=-0.243710, timezone=timezone)
    s = sun(city.observer, date=datetime.now(), tzinfo=pytz.timezone(timezone))
    now = datetime.now(pytz.timezone(timezone))

    with canvas(device) as draw:
        draw.text((0, 0), now.strftime("%H:%M %a, %d %b") , font=font, fill="white")
        draw.text((0, 30), "SunRise:" + str(s["sunrise"].hour) +  ":" + str(s["sunrise"].minute) + "  SunSet:" + str(s["sunset"].hour) + ":" + str(s["sunset"].minute) , font=font1, fill="white")
        draw.text((0, 50), "Atmospheric Press:" + DLKitchenPressure , font=font1, fill="white")
        draw.text((0, 70), "Drumaline DegC   RH%   AQ%    " , font=font1, fill="white")
        draw.text((0, 90), "Kitchen" , font=font2, fill="white")
        draw.text((93, 90), DLKitchenTemp , font=font2, fill="white")
        draw.text((142, 90), DLKitchenHumidity , font=font2, fill="white")
        draw.text((190, 90), DLKitchenGasPercentage , font=font2, fill="white")
        #Office
        draw.text((0,105), "Office" , font=font2, fill="white")
        draw.text((93, 105), DLOfficeTemp , font=font2, fill="white")
        draw.text((142, 105), DLOfficeHumidity , font=font2, fill="white")
        draw.text((190, 105), DLOfficeGasPercentage , font=font2, fill="white")
        # MainBed
        draw.text((0,120), "MainBed" , font=font2, fill="white")
        draw.text((93, 120), DLMainBedTemp , font=font2, fill="white")
        draw.text((142, 120), DLMainBedHumidity , font=font2, fill="white")
        draw.text((190, 120), DLMainBedGasPercentage , font=font2, fill="white")
        # Lounge
        draw.text((0,135), "Lounge" , font=font2, fill="white")
        draw.text((93, 135), DLLoungeTemp , font=font2, fill="white")
        draw.text((142, 135), DLLoungeHumidity , font=font2, fill="white")
        # Kate bed
        draw.text((0,150), "Kate bed" , font=font2, fill="white")
        draw.text((93, 150), DLKateBedTemp , font=font2, fill="white")
        draw.text((142, 150), DLKateBedHumidity , font=font2, fill="white")
        #  Matt bed
        draw.text((0,165), "Matt bed" , font=font2, fill="white")
        draw.text((93, 165), DLMattBedTemp , font=font2, fill="white")
        draw.text((142, 165), DLMattBedHumidity , font=font2, fill="white")
        # Loft
        draw.text((0,180), "Loft" , font=font2, fill="white")
        draw.text((93, 180), DLLoftTemp , font=font2, fill="white")
        draw.text((142, 180), DLLoftHumidity , font=font2, fill="white")
        # Garage
        draw.text((0,195), "Garage" , font=font2, fill="white")
        draw.text((93, 195), DLGarageTemp , font=font2, fill="white")
        draw.text((142, 195), DLGarageHumidity , font=font2, fill="white")
        # Greenway
        draw.text((0,230), "Greenway  DegC   RH%   AQ%" , font=font1, fill="white")
        # Kitchen
        draw.text((0,250), "Kitchen" , font=font2, fill="white")
        draw.text((93, 250), GWKitchenTemp , font=font2, fill="white")
        draw.text((142, 250), GWKitchenHumidity , font=font2, fill="white")
        draw.text((190, 250), GWKitchenGasPercentage , font=font2, fill="white")
        # FrontRoom
        draw.text((0,265), "FrontRoom" , font=font2, fill="white")
        draw.text((93, 265), GWFrontRoomTemp , font=font2, fill="white")
        draw.text((142, 265), GWFrontRoomHumidity , font=font2, fill="white")
        draw.text((190, 265), GWFrontRoomGasPercentage , font=font2, fill="white")
        # Main Bed
        draw.text((0,280), "MainBed" , font=font2, fill="white")
        draw.text((93, 280), GWTopFloorTemp , font=font2, fill="white")
        draw.text((142, 280), GWTopFloorHumidity , font=font2, fill="white")
        draw.text((190, 280), GWTopFloorGasPercentage , font=font2, fill="white")

        draw.text((0, 300), msg.topic + " " + msg.payload.decode() , font=font2, fill="white")

client = mqtt.Client()
client.username_pw_set(username="bckMQTT", password="bckBrAaI")
client.connect("192.168.0.132",1883,60)

client.on_connect = on_connect
client.on_message = on_message


from luma.core.render import canvas

#Pressure
DLKitchenPressure = ""
#Kitchen
DLKitchenTemp = ""
DLKitchenHumidity = ""
DLKitchenGasPercentage = ""
#Drumaline Office
DLOfficeTemp = ""
DLOfficeHumidity = ""
DLOfficeGasPercentage = ""
#Drumaline MainBed
DLMainBedTemp = ""
DLMainBedHumidity = ""
DLMainBedGasPercentage = ""
#Drumaline Lounge
DLLoungeTemp = ""
DLLoungeHumidity = ""
#Drumaline KateBed
DLKateBedTemp = ""
DLKateBedHumidity = ""
#Drumaline MattBed
DLMattBedTemp = ""
DLMattBedHumidity = ""
#Drumaline Loft
DLLoftTemp = ""
DLLoftHumidity = ""
#Drumaline Garage
DLGarageTemp = ""
DLGarageHumidity = ""
#Greenway Kitchen
GWKitchenTemp = ""
GWKitchenHumidity = ""
GWKitchenGasPercentage = ""
#Greenway FrontRoom    
GWFrontRoomTemp = ""
GWFrontRoomHumidity = ""
GWFrontRoomGasPercentage = ""
#Greenway Main bed  
GWTopFloorTemp = ""
GWTopFloorHumidity = ""
GWTopFloorGasPercentage = ""

client.loop_forever()
