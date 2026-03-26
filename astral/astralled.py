from datetime import datetime
from astral import LocationInfo
from astral.sun import sun
import pytz
# import RPi.GPIO as GPIO # Old library not compatible with Pi5
import lgpio
import time

GPIO_LED_PIN = 13

# Open GPIO chip (0 is usually correct for Raspberry Pi)
chip = lgpio.gpiochip_open(0)

# Claim the pin as output
lgpio.gpio_claim_output(chip, GPIO_LED_PIN)

def is_sun_down(latitude, longitude, timezone):
    city = LocationInfo(latitude=latitude, longitude=longitude, timezone=timezone)
    s = sun(city.observer, date=datetime.now(), tzinfo=pytz.timezone(timezone))
    now = datetime.now(pytz.timezone(timezone))
    return now < s["sunrise"] or now > s["sunset"]


while True:
    if is_sun_down(51.379608, -0.243710, "Europe/London"):
        print("🌙 Sun is down")
        lgpio.gpio_write(chip, GPIO_LED_PIN, 1)  # LED ON
    else:
        print("☀️ Sun is up")
        lgpio.gpio_write(chip, GPIO_LED_PIN, 0)  # LED OFF
    time.sleep(5)

lgpio.gpiochip_close(chip)
