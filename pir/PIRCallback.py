#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
import sys
import paho.mqtt.client as paho


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)



GPIO_PIN_SENSOR = int(sys.argv[1])
MQTT_TOPIC = str(sys.argv[2])
GPIO.setup(GPIO_PIN_SENSOR, GPIO.IN)
GPIO_PIN_LED = int(sys.argv[3])

GPIO.setup(GPIO_PIN_LED,GPIO.OUT)

current_time = time.strftime("%d%m%y_%H%M%S_", time.localtime())
print (current_time + "Setup MQTT to publish to broker on 192.168.0.132,1883,60 " )
mqttc = paho.Client()


def MOTION(GPIO_PIN_SENSOR):
    if GPIO.input(GPIO_PIN_SENSOR):     # True = Rising
          sendmqtt("ON")
          GPIO.output(GPIO_PIN_LED,GPIO.HIGH)
    else:                        # Otherwise falling
          sendmqtt("OFF")
          GPIO.output(GPIO_PIN_LED,GPIO.LOW)


def sendmqtt(mess):
    current_time = time.strftime("%d%m%y_%H%M%S ", time.localtime())
    print ((current_time + "Send MQTT Message on topic {1} with value " + mess) .format(GPIO_PIN_SENSOR,MQTT_TOPIC))
    mqttc.username_pw_set(username="bckMQTT", password="bckBrAaI")
    mqttc.connect("192.168.0.132",1883,60)
    mqttc.publish(MQTT_TOPIC,mess)
    mqttc.disconnect()


print ("PIR Module Test (CTRL+C to exit), PIN {0} Publishing on topic {1}"  .format(GPIO_PIN_SENSOR,MQTT_TOPIC))
time.sleep(2)
print ("Ready")

try:
     GPIO.add_event_detect(GPIO_PIN_SENSOR, GPIO.BOTH, callback=MOTION)
     while 1:
          time.sleep(100)
except KeyboardInterrupt:
     print ("Quit")
     sendmqtt("END")
     GPIO.cleanup()

