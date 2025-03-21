
import datetime
from suntime import Sun
import time
import logging
import argparse
import RPi.GPIO as GPIO

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", action="store_true", default=False, help="Debug")

# SET SUN, COORDS AND START AND END TIMES
LATITUDE = 51.38
LONGITUDE = 0.24
SUN = Sun(LATITUDE, LONGITUDE)

# SET LOGGING LEVELS
logger = logging.getLogger(__name__)

if parser.parse_args().verbose:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)


# SET GPIO PINS
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(13, GPIO.OUT)

while True:

    now = datetime.datetime.now().replace(microsecond=0)
    # Get today's sunrise and sunset in Local time
    abd_sr = SUN.get_sunrise_time(now).replace(microsecond=0)
    abd_ss = SUN.get_sunset_time(now).replace(microsecond=0)

    if now > abd_ss.replace(tzinfo=None) or now < abd_sr.replace(tzinfo=None) :
        logger.info('Sun is down - SunRise {} SunSet {} Time {}'.format(abd_sr.strftime('%d/%m-%H:%M'), abd_ss.strftime('%d/%m-%H:%M'), now.strftime('%d/%m-%H:%M')))
        #logger.info('The sun is down')
        GPIO.output(13, GPIO.HIGH)
        # put white LED on when sun is down

    else:
        logger.info('Sun is Up - SunRise {} SunSet {} Time {}'.format(abd_sr.strftime('%d/%m-%H:%M'), abd_ss.strftime('%d/%m-%H:%M'), now.strftime('%d/%m-%H:%M')))
        GPIO.output(13, GPIO.LOW)
        # put white LED off when sun is up


    time.sleep(5)
