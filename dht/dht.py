import json
import requests
import sys
import time
import datetime
import paho.mqtt.client as mqtt
from pigpio_dht import DHT11, DHT22
#import RPi.GPIO as GPIO

#GPIO.setmode(GPIO.BCM)
#GPIO.setwarnings(False)
#GPIO.setup(6,GPIO.OUT)

# Type of sensor, can be Adafruit_DHT.DHT11, Adafruit_DHT.DHT22, or Adafruit_DHT.AM2302.
sensortype = (sys.argv[1])
gpio = int(sys.argv[2])

if sensortype == "DHT22":
     sensor = DHT22(gpio)
elif sensortype == "DHT11":     
     sensor = DHT11(gpio)


if (len(sys.argv) < 3):
   raise  ValueError('Input arguments of mqtt channel temperature humidity not passed')

MOSQUITTO_HOST = '192.168.0.132'
MOSQUITTO_PORT = 1883
MOSQUITTO_TEMP_MSG = str(sys.argv[3]) # Old channel name in here
MOSQUITTO_HUMI_MSG = str(sys.argv[4]) # Old channel name now passed by argument

print('Mosquitto Temp MSG {0}'.format(MOSQUITTO_TEMP_MSG))
print('Mosquitto Humidity MSG {0}'.format(MOSQUITTO_HUMI_MSG))

Temp = []
Humidity = []
NumberOfSamples = 32

print('Logging sensor measurements MQTT to host {0}, press Ctrl-C to quit'.format('MOSQUITTO_HOST'))

mqttc = mqtt.Client("python_pub")


while True:
        
        # Put the GPIO 6 on, usually blue
 #       GPIO.output(6,GPIO.HIGH)
        # Attempt to get sensor reading.
        time.sleep(1)
        result = sensor.read()
        print(result)
#        key, tempc = result.items()[0]
        tempc=list(result.values())[0]
        humidity=list(result.values())[2]
        validresult=list(result.values())[3]
        #, tempf, humidity, validresult = result 
        time.sleep(3)
        print('tempc : {0}'.format(tempc))   
        print('humidity : {0}'.format(humidity))   
        print('validresult : {0}'.format(validresult))   
 #       GPIO.output(6,GPIO.LOW)
        temp = float(tempc)

        if temp is not None and temp >-10 and temp <50 and validresult:
           Temp.append(temp)
        else:
           print('Couldnt get a temperature reading, reading was : {0}'.format(temp))   
        
        if humidity is not None and humidity <130 and humidity >20 and validresult:
           Humidity.append(humidity)
        else:
           print('Couldnt get a humidity reading,  reading was : {0}'.format(humidity)) 

        currentdate = time.strftime('%Y-%m-%d %H:%M:%S')
        print('{0} : Temperature len : {1} , Humidity len : {2} , Temperature : {3}  , Humidity : {4}'.format(currentdate, len(Temp), len(Humidity), format(temp), format(humidity)))
        Temp.sort()
        print('Temperature ',Temp)
        Humidity.sort()  
        print('Humidity ', Humidity)
       
        if len(Temp)>=NumberOfSamples:
             print('Temperature Length is > NumberOfSamples, sort, trim off first/last third, average the rest')
             del Temp[:3] # delete first x entries
             del Temp[-3:] # delete last x entries
             print('Temperature list after sort & trim ', Temp)
             print('Temperature length after trimming {0}'.format(len(Temp)))
             avg = round(sum(Temp)/len(Temp),2)
             print('Average Temperature {0}'.format(avg))
             try:
                  mqttc.username_pw_set(username="bckMQTT", password="bckBrAaI")
                  mqttc.connect(MOSQUITTO_HOST,MOSQUITTO_PORT);
                  (result1,mid) = mqttc.publish(MOSQUITTO_TEMP_MSG,avg)
                  mqttc.disconnect()
                  print ('MQTT Updating {0} with {1}'.format(MOSQUITTO_TEMP_MSG,avg))
             except:
                  print("MQTT ERROR : An error occurred while trying to publish the avg temperature to MQTT")     
 
        if len(Humidity)>=NumberOfSamples:
             print('Humidity Length is > NumberOfSamples, sort, trim off first/last third, average the rest')
             del Humidity[:3] # delete first x entries
             del Humidity[-3:] # delete last x entries
             print('Humidity list after sort and trim ' , Humidity)
             print('Humidity length after trimming {0}'.format(len(Temp)))
             avg = round(sum(Humidity)/len(Humidity),2)
             print('Average Humidity {0}'.format(avg))
             try:
                  mqttc.username_pw_set(username="bckMQTT", password="bckBrAaI")
                  mqttc.connect(MOSQUITTO_HOST,MOSQUITTO_PORT);
                  (result1,mid) = mqttc.publish(MOSQUITTO_HUMI_MSG,avg)
                  mqttc.disconnect()
                  print ('MQTT Updating {0} with {1}'.format(MOSQUITTO_HUMI_MSG,avg))
             except:
                  print("MQTT ERROR : An error occurred while trying to publish the avg humidity to MQTT") 

