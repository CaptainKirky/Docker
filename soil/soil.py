import json
#import requests
import sys
import time
import datetime
import paho.mqtt.client as mqtt
#import adafruit_dht
import board
import RPi.GPIO as GPIO



MOSQUITTO_HOST = '82.14.146.123'
MOSQUITTO_PORT = 1883
MOSQUITTO_MOISTURE_MSG = str(sys.argv[1]) # Old channel name in here

print('Mosquitto Temp MSG {0}'.format(MOSQUITTO_MOISTURE_MSG))

Moisture = []
NumberOfSamples = 128

print('Logging sensor measurements MQTT to host {0}, press Ctrl-C to quit'.format('MOSQUITTO_HOST'))

mqttc = mqtt.Client("python_pub")


import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D22)
mcp = MCP.MCP3008(spi, cs)
channel = AnalogIn(mcp, MCP.P0)
adc = 1/channel.value*180000
adcv = 1/channel.voltage*180000
other = 1/(channel.value/1850000)
print('Raw ADC Value: ', channel.value)
print('ADC Voltage: ' + str(channel.voltage) + 'V')
print('Adjusted ADC Value: ', adc)
print('Adjusted ADC Voltage: ', adcv)
print('New Calc Value: ', other)


while True:
    channel = AnalogIn(mcp, MCP.P0)
    moisture = 1/(channel.value/1850000)
    print('Moisture Reading: ', moisture)
    Moisture.append(moisture)
    time.sleep(1)
    if len(Moisture)>=NumberOfSamples:
        print('Moisture Length is > NumberOfSamples, sort, trim off first/last third, average the rest')
        del Moisture[:32] # delete first x entries
        del Moisture[-32:] # delete last x entries
        print('Moisture list after sort & trim ', Moisture)
        print('Temperature length after trimming {0}'.format(len(Moisture)))
        avg = round(sum(Moisture)/len(Moisture),3)
        print('Average Moisture {0}'.format(avg))
        try:
            mqttc.username_pw_set(username="bckMQTT", password="bckBrAaI")
            mqttc.connect(MOSQUITTO_HOST,MOSQUITTO_PORT);
            (result1,mid) = mqttc.publish(MOSQUITTO_MOISTURE_MSG,avg)
            mqttc.disconnect()
            print ('MQTT Updating {0} with {1}'.format(MOSQUITTO_MOISTURE_MSG,avg))
        except:
            print("MQTT ERROR : An error occurred while trying to publish the avg temperature to MQTT")


