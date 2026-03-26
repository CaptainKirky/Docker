import sys
import time
import datetime
import paho.mqtt.client as mqtt

import board
import busio
import adafruit_ahtx0

MOSQUITTO_HOST = '192.168.0.132'
MOSQUITTO_PORT = 1883
MOSQUITTO_TEMP_MSG = str(sys.argv[1]) # Old channel name in here
MOSQUITTO_HUMI_MSG = str(sys.argv[2]) # Old channel name now passed by argument

print('Mosquitto Temp MSG {0}'.format(MOSQUITTO_TEMP_MSG))
print('Mosquitto Humidity MSG {0}'.format(MOSQUITTO_HUMI_MSG))


print('Mosquitto Humidity MSG {0}'.format(MOSQUITTO_HUMI_MSG))

Temp = []
Humidity = []
NumberOfSamples = 32

print('Logging sensor measurements MQTT to host {0}, press Ctrl-C to quit'.format('MOSQUITTO_HOST'))

mqttc = mqtt.Client("python_pub")

# Create I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize sensor
sensor = adafruit_ahtx0.AHTx0(i2c)


while True:
        temperature = sensor.temperature
        humidity=sensor.relative_humidity
        print('humidity : {0}'.format(humidity))
        print(f"Temperature: {temperature:.2f} °C")
        print(f"Humidity: {humidity:.2f} %")
        
        if temperature is not None and temperature >-10 and temperature <50:
           Temp.append(temperature)
        else:
           print('Couldnt get a temperature reading, reading was : {0}'.format(temp))

        if humidity is not None and humidity <130 and humidity >20 :
           Humidity.append(humidity)
        else:
           print('Couldnt get a humidity reading,  reading was : {0}'.format(humidity))

        currentdate = time.strftime('%Y-%m-%d %H:%M:%S')
        print('{0} : Temperature len : {1} , Humidity len : {2} , Temperature : {3}  , Humidity : {4}'.format(currentdate, len(Temp), len(Humidity), format(temperature), format(humidity)))

        Temp.sort()
        print('Temperature ',Temp)
        Humidity.sort()
        print('Humidity ', Humidity)
        
        time.sleep(2)
        
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
             print('Humidity length after trimming {0}'.format(len(Humidity)))
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
