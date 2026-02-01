from datetime import datetime
from astral import LocationInfo
from astral.sun import sun
import pytz
import RPi.GPIO as GPIO
import time

# SET GPIO PINS
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(13, GPIO.OUT)


def is_sun_down(latitude, longitude, timezone):
    city = LocationInfo(latitude=latitude, longitude=longitude, timezone=timezone)
    s = sun(city.observer, date=datetime.now(), tzinfo=pytz.timezone(timezone))
    now = datetime.now(pytz.timezone(timezone))
    return now < s["sunrise"] or now > s["sunset"]


while True:
    if is_sun_down(51.379608, -0.243710, "Europe/London"):
        #print("🌙 Sun is down")
        GPIO.output(13, GPIO.HIGH)
    else:
        #print("☀️ Sun is up")
        GPIO.output(13, GPIO.LOW)
    time.sleep(5)
