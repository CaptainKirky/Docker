
import RPi.GPIO as GPIO
import time
import sys

GPIO_LED_PIN = int(sys.argv[1])
GPIO_LED_ON_TIME = int(sys.argv[2])/1000
GPIO_LED_DELAY = int(sys.argv[3])/1000


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(GPIO_LED_PIN,GPIO.OUT)
while True:
     print ("LED on")
     GPIO.output(GPIO_LED_PIN,GPIO.HIGH)
     time.sleep(GPIO_LED_ON_TIME)
     print ("LED off")
     GPIO.output(GPIO_LED_PIN,GPIO.LOW)
     time.sleep(GPIO_LED_DELAY)

