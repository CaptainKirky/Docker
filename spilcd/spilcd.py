from luma.core.interface.serial import spi
#from luma.lcd.device import ili9341
from luma.core.render import canvas
from PIL import ImageFont

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
        rotate=1
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
20
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
    global KitchenTemp
    global KitchenHumidity
    global GWKitchenTemp
    global GWKitchenHumidity
    global OfficeTemp
    global OfficeHumidity
    global GWOfficeTemp
    global GWOfficeHumidity
    global SpareBedroomTemp
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
        LoungeTemp = "{:.1f}C".format(float(msg.payload.decode()))
    elif msg.topic == "DLLoungeHumidity":
        LoungeHumidity = "/{:.0f}%".format(float(msg.payload.decode()))
    elif msg.topic == "GWLoungeTemp":
        GWLoungeTemp = "{:.1f}C".format(float(msg.payload.decode()))
    elif msg.topic == "GWLoungeHumidity":
        GWLoungeHumidity = "/{:.0f}%".format(float(msg.payload.decode()))
    elif msg.topic == "KitchenTemp":
        KitchenTemp = "{:.1f}C".format(float(msg.payload.decode()))
    elif msg.topic == "KitchenHumidity":
        KitchenHumidity = "/{:.0f}%".format(float(msg.payload.decode()))
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
    elif msg.topic == "SpareBedroomTemp":
        SpareBedroomTemp = "{:.1f}C".format(float(msg.payload.decode()))
    elif msg.topic == "GWSpareBedroomTemp":
        GWSpareBedroomTemp = "{:.1f}C".format(float(msg.payload.decode()))
    elif msg.topic == "LoftTemp":
        LoftTemp = "{:.1f}C".format(float(msg.payload.decode()))
    elif msg.topic == "GarageInsideTemp":
        GarageInsideTemp = "{:.1f}C".format(float(msg.payload.decode()))

    with canvas(device) as draw:
        draw.text((0, 0), time.strftime("%H:%M %a, %d %b", time.gmtime()) , font=font, fill="white")
        draw.text((0, 40), "Sunrise/set  05:15/20:07" , font=font1, fill="white")

        draw.text((0, 60), "                 Drum     Green    " , font=font1, fill="white")

        draw.text((0, 80), "Pressure" , font=font1, fill="white")
        draw.text((80, 80), "1080 MPa" , font=font2, fill="white")
        draw.text((165, 80), "1100 MPa" , font=font2, fill="white")


        #draw.text((0, 56), "Main Bd" , font=font1, fill="white")
        #draw.text((80, 60), MainBedTemp + "" + MainBedHumidity , font=font2, fill="white")
        #draw.text((165, 60), GWTopFloorTemp  + GWTopFloorHumidity , font=font2, fill="white")

        #draw.text((0, 76), "Lounge" , font=font1, fill="white")
        #draw.text((80, 80), LoungeTemp  + LoungeHumidity , font=font2, fill="white")
        #draw.text((165, 80), GWLoungeTemp + GWLoungeHumidity , font=font2, fill="white")

        draw.text((0,100), "Kitchen" , font=font1, fill="white")
        draw.text((80,100), KitchenTemp + KitchenHumidity  , font=font2, fill="white")
        draw.text((165,100), GWKitchenTemp  + GWKitchenHumidity , font=font2, fill="white")

        draw.text((0,120), "K Air" , font=font1, fill="white")
        draw.text((80,120), "1023 Good"  , font=font2, fill="white")
        draw.text((165,120),"1067 Bad" , font=font2, fill="white")

        draw.text((0,140), "Office" , font=font1, fill="white")
        draw.text((80,140), OfficeTemp  + OfficeHumidity , font=font2, fill="white")
        draw.text((165,140), GWOfficeTemp  + GWOfficeHumidity , font=font2, fill="white")

        draw.text((0,160), "Spar Bd" , font=font1, fill="white")
        draw.text((80,160), SpareBedroomTemp , font=font2, fill="white")
        draw.text((165,160), GWSpareBedroomTemp + GWOfficeHumidity , font=font2, fill="white")

        draw.text((0,180), "Loft" , font=font1, fill="white")
        draw.text((90,180), LoftTemp , font=font2, fill="white")

        draw.text((0,200), "Garage" , font=font1, fill="white")
        draw.text((90,200), GarageInsideTemp , font=font2, fill="white")


        draw.text((0, 240), msg.topic + " " + msg.payload.decode() , font=font2, fill="white")


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
KitchenTemp = ""
KitchenHumidity = ""
GWKitchenTemp = ""
GWKitchenHumidity = ""
OfficeTemp = ""
OfficeHumidity = ""
GWOfficeTemp = ""
GWOfficeHumidity = ""
SpareBedroomTemp = ""
GWSpareBedroomTemp = ""
LoftTemp = ""
GarageInsideTemp = ""

client.loop_forever()
