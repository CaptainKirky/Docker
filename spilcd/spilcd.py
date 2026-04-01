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
        rotate=1      # try 0, 90, 180, 270
#    offset_left=0,   # some displays need offsets
#    offset_top=0
    )


font = ImageFont.truetype(
    "/home/pi/.local/share/fonts/FUTURAM/16020_FUTURAM.ttf",
34
)

font1 = ImageFont.truetype(
    "/home/pi/.local/share/fonts/FUTURAM/16020_FUTURAM.ttf",
18
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
    global MainBedTemp
    global MainBedHumidity
    global GWTopFloorTemp
    global GWTopFloorHumidity
    global LoungeTemp
    global LoungeHumidity
    global GWLoungeTemp
    global GWLoungeHumidity
    global DLKitchenTemp
    global DLKitchenHumidity
    global DLKitchenPressure
    global DLKitchenGas
    global GWKitchenTemp
    global GWKitchenHumidity
    global OfficeTemp
    global OfficeHumidity
    global GWOfficeTemp
    global GWOfficeHumidity
    global SpareBedTemp
    global GWSpareBedroomTemp
    global LoftTemp
    global GarageInsideTemp

    if msg.topic == "MainBedTemp":
        MainBedTemp = "{:.1f}C".format(float(msg.payload.decode()))
    elif msg.topic == "MainBedHumidity":
        MainBedHumidity = "/{:.0f}%".format(float(msg.payload.decode()))
    elif msg.topic == "GWTopFloorTemp":
        GWTopFloorTemp = "{:.1f}C".format(float(msg.payload.decode()))
    elif msg.topic == "GWTopFloorHumidity":
        GWTopFloorHumidity = "/{:.0f}%".format(float(msg.payload.decode()))
    elif msg.topic == "DLLoungeTemp":
        DLLoungeTemp = "{:.1f}C".format(float(msg.payload.decode()))
    elif msg.topic == "DLLoungeHumidity":
        DLLoungeHumidity = "/{:.0f}%".format(float(msg.payload.decode()))
    elif msg.topic == "GWLoungeTemp":
        GWLoungeTemp = "{:.1f}C".format(float(msg.payload.decode()))
    elif msg.topic == "GWLoungeHumidity":
        GWLoungeHumidity = "/{:.0f}%".format(float(msg.payload.decode()))
    elif msg.topic == "DLKitchenTemp":
        DLKitchenTemp = "{:.1f}C".format(float(msg.payload.decode()))
    elif msg.topic == "DLKitchenHumidity":
        DLKitchenHumidity = "/{:.0f}%".format(float(msg.payload.decode()))
    elif msg.topic == "DLKitchenPressure":
        DLKitchenPressure = "{:.0f}Mpa".format(float(msg.payload.decode()))
    elif msg.topic == "DLKitchenGas":
        DLKitchenGas = "{:.0f}Ohm".format(float(msg.payload.decode()))
    elif msg.topic == "GWKitchenTemp":
        GWKitchenTemp = "{:.1f}C".format(float(msg.payload.decode()))
    elif msg.topic == "GWKitchenHumidity":
        GWKitchenHumidity = "/{:.0f}%".format(float(msg.payload.decode()))
    elif msg.topic == "OfficeTemp":
        OfficeTemp = "{:.1f}C".format(float(msg.payload.decode()))
    elif msg.topic == "OfficeHumidity":
        OfficeHumidity = "/{:.0f}%".format(float(msg.payload.decode()))
    elif msg.topic == "GWOfficeTemp":
        GWOfficeTemp = "{:.1f}C".format(float(msg.payload.decode()))
    elif msg.topic == "GWOfficeHumidity":
        GWOfficeHumidity = "/{:.0f}%".format(float(msg.payload.decode()))
    elif msg.topic == "SpareBedTemp":
        SpareBedTemp = "{:.1f}C".format(float(msg.payload.decode()))
    elif msg.topic == "GWSpareBedroomTemp":
        GWSpareBedroomTemp = "{:.1f}C".format(float(msg.payload.decode()))
    elif msg.topic == "LoftTemp":
        LoftTemp = "{:.1f}C".format(float(msg.payload.decode()))
    elif msg.topic == "GarageInsideTemp":
        GarageInsideTemp = "{:.1f}C".format(float(msg.payload.decode()))

    timezone="Europe/London"
    city = LocationInfo(latitude=51.379608, longitude=-0.243710, timezone=timezone)
    s = sun(city.observer, date=datetime.now(), tzinfo=pytz.timezone(timezone))
    now = datetime.now(pytz.timezone(timezone))
    #print(str(now.time))
    print(" xya" + now.strftime("%Y-%m-%d %H:%M:%S %Z%z"))
    print(s["sunrise"])
    print("Sunrise  at %s:%s" % (s["sunrise"].hour, s["sunrise"].minute))
    print(s["sunset"])
    print("Sunset  at %s:%s" % (s["sunset"].hour, s["sunset"].minute))


    with canvas(device) as draw:
        draw.text((0, 0), now.strftime("%H:%M %a, %d %b") , font=font, fill="white")
#        draw.text((0, 0), time.strftime("%H:%M %a, %d %b", time.gmtime()) , font=font, fill="white")
        draw.text((0, 40), "SunRise:" + str(s["sunrise"].hour) +  ":" + str(s["sunrise"].minute) + "  SunSet:" + str(s["sunset"].hour) + ":" + str(s["sunset"].minute) , font=font1, fill="white")
        draw.text((0, 60), "            Drumaline Greenway    " , font=font1, fill="white")

        draw.text((0,73), "Kitchen" , font=font1, fill="white")
        draw.text((80,80), DLKitchenTemp + DLKitchenHumidity  , font=font2, fill="white")
        draw.text((165,80), GWKitchenTemp  + GWKitchenHumidity , font=font2, fill="white")

        draw.text((0, 93), "K Pres" , font=font1, fill="white")
        draw.text((80, 100), DLKitchenPressure + "" , font=font2, fill="white")
        draw.text((165, 100), "" , font=font2, fill="white")

        draw.text((0, 113), "K Gas" , font=font1, fill="white")
        draw.text((80, 120), DLKitchenGas + "" , font=font2, fill="white")
        draw.text((165, 120), "" , font=font2, fill="white")



        draw.text((0,133), "Office" , font=font1, fill="white")
        draw.text((80,140), OfficeTemp  + OfficeHumidity , font=font2, fill="white")
        draw.text((165,140), GWOfficeTemp  + GWOfficeHumidity , font=font2, fill="white")

        draw.text((0,153), "Spar Bd" , font=font1, fill="white")
        draw.text((80,160), SpareBedTemp , font=font2, fill="white")
        draw.text((165,160), GWSpareBedroomTemp + GWOfficeHumidity , font=font2, fill="white")

        draw.text((0,173), "Loft" , font=font1, fill="white")
        draw.text((80,180), LoftTemp , font=font2, fill="white")

        draw.text((0,193), "Garage" , font=font1, fill="white")
        draw.text((80,200), GarageInsideTemp , font=font2, fill="white")


        draw.text((0, 300), msg.topic + " " + msg.payload.decode() , font=font2, fill="white")


client = mqtt.Client()
client.username_pw_set(username="bckMQTT", password="bckBrAaI")
client.connect("192.168.0.132",1883,60)

client.on_connect = on_connect
client.on_message = on_message


from luma.core.render import canvas

MainBedTemp = ""
MainBedHumidity = ""
GWTopFloorTemp = ""
GWTopFloorHumidity = ""
LoungeTemp = ""
LoungeHumidity = ""
GWLoungeTemp = ""
GWLoungeHumidity = ""
DLKitchenTemp = ""
DLKitchenHumidity = ""
DLKitchenPressure = ""
DLKitchenGas = ""

GWKitchenTemp = ""
GWKitchenHumidity = ""
OfficeTemp = ""
OfficeHumidity = ""
GWOfficeTemp = ""
GWOfficeHumidity = ""
SpareBedTemp = ""
GWSpareBedroomTemp = ""
LoftTemp = ""
GarageInsideTemp = ""

client.loop_forever()
