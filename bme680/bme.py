# python bme.py OfficeTemp OfficeHumidity OfficePressure OfficeGas
import sys
import time
import datetime
import paho.mqtt.client as mqtt

import bme680

MOSQUITTO_HOST = '192.168.0.132'
MOSQUITTO_PORT = 1883
MOSQUITTO_TEMP_MSG = str(sys.argv[1]) # Old channel name in here
MOSQUITTO_HUMI_MSG = str(sys.argv[2]) # Old channel name now passed by argument
MOSQUITTO_PRESS_MSG = str(sys.argv[3]) # Old channel name now passed by argument
MOSQUITTO_GAS_MSG = str(sys.argv[4]) # Old channel name now passed by argument

print('Mosquitto Temp MSG {0}'.format(MOSQUITTO_TEMP_MSG))
print('Mosquitto Humidity MSG {0}'.format(MOSQUITTO_HUMI_MSG))


# Create sensor object (default I2C address 0x76 or 0x77)
sensor = bme680.BME680(i2c_addr=0x77)

# Configure oversampling
sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)

# Configure gas sensor
sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)
sensor.set_gas_heater_temperature(320)
sensor.set_gas_heater_duration(150)

print("Reading BME680 values...\n")

mqttc = mqtt.Client("python_pub")


TempList = []
HumidityList = []
PressureList = []
GasList = []

NumberOfSamples = 32

while True:
    if sensor.get_sensor_data():
        data = sensor.data

        print(f"Temp: {data.temperature:.2f} °C")
        if data.temperature is not None and data.temperature >-10 and data.temperature <50:
           TempList.append(data.temperature)
        else:
           print('Couldnt get a temperature reading, reading was : {0}'.format(temp))   

        if len(TempList)>=NumberOfSamples:
             print('Temperature Length is > NumberOfSamples, sort, trim off first/last third, average the rest')
             del TempList[:3] # delete first x entries
             del TempList[-3:] # delete last x entries
             print('Temperature list after sort & trim ', TempList)
             print('Temperature length after trimming {0}'.format(len(TempList)))
             TempAvg = round(sum(TempList)/len(TempList),2)
             print('Average Temperature {0}'.format(TempAvg))
             try:
                 mqttc.username_pw_set(username="bckMQTT", password="bckBrAaI")
                 mqttc.connect(MOSQUITTO_HOST,MOSQUITTO_PORT);
                 (result1,mid) = mqttc.publish(MOSQUITTO_TEMP_MSG,TempAvg)
                 mqttc.disconnect()
                 print ('MQTT Updating {0} with {1}'.format(MOSQUITTO_TEMP_MSG,TempAvg))
             except:
                 print("MQTT ERROR : An error occurred while trying to publish the avg temperature to MQTT")


        print(f"Humidity: {data.humidity:.2f} hPa")
        if data.humidity is not None and data.humidity >10 and data.humidity <110:
           HumidityList.append(data.humidity)
        else:
           print('Couldnt get a temperature reading, reading was : {0}'.format(data.humidity))   

        if len(HumidityList)>=NumberOfSamples:
             print('Humidity Length is > NumberOfSamples, sort, trim off first/last third, average the rest')
             del HumidityList[:3] # delete first x entries
             del HumidityList[-3:] # delete last x entries
             print('Humidity list after sort & trim ', HumidityList)
             print('Humidity length after trimming {0}'.format(len(HumidityList)))
             HumidityAvg = round(sum(HumidityList)/len(HumidityList),2)
             print('Average Humidity {0}'.format(TempAvg))
             try:
                 mqttc.username_pw_set(username="bckMQTT", password="bckBrAaI")
                 mqttc.connect(MOSQUITTO_HOST,MOSQUITTO_PORT);
                 (result1,mid) = mqttc.publish(MOSQUITTO_HUMI_MSG,HumidityAvg)
                 mqttc.disconnect()
                 print ('MQTT Updating {0} with {1}'.format(MOSQUITTO_HUMI_MSG,HumidityAvg))
             except:
                 print("MQTT ERROR : An error occurred while trying to publish the avg humidity to MQTT")


        print(f"Pressure: {data.pressure:.2f} %")
        if data.pressure is not None and data.pressure >-10 and data.pressure <1200:
           PressureList.append(data.pressure)
        else:
           print('Couldnt get a pressure reading, reading was : {0}'.format(data.pressure))   

        if len(PressureList)>=NumberOfSamples:
             print('PressureList Length is > NumberOfSamples, sort, trim off first/last third, average the rest')
             del PressureList[:3] # delete first x entries
             del PressureList[-3:] # delete last x entries
             print('Pressure list after sort & trim ', PressureList)
             print('Pressure length after trimming {0}'.format(len(PressureList)))
             PressureAvg = round(sum(PressureList)/len(PressureList),2)
             print('Average Pressure {0}'.format(PressureAvg))
             try:
                 mqttc.username_pw_set(username="bckMQTT", password="bckBrAaI")
                 mqttc.connect(MOSQUITTO_HOST,MOSQUITTO_PORT);
                 (result1,mid) = mqttc.publish(MOSQUITTO_PRESS_MSG,PressureAvg)
                 mqttc.disconnect()
                 print ('MQTT Updating {0} with {1}'.format(MOSQUITTO_PRESS_MSG,PressureAvg))
             except:
                 print("MQTT ERROR : An error occurred while trying to publish the avg pressure to MQTT")


        if data.heat_stable:
             print(f"Gas Resistance: {data.gas_resistance} Ω")
             if data.gas_resistance is not None and data.gas_resistance >10 and data.gas_resistance <150000:
                 GasList.append(data.gas_resistance)
             else:
                 print('Couldnt get a gas_resistance reading, reading was : {0}'.format(temp))   

             if len(GasList)>=NumberOfSamples:
                 print('GasList Length is > NumberOfSamples, sort, trim off first/last third, average the rest')
                 del GasList[:3] # delete first x entries
                 del GasList[-3:] # delete last x entries
                 print('Gas list after sort & trim ', GasList)
                 print('Gas length after trimming {0}'.format(len(GasList)))
                 GasAvg = round(sum(GasList)/len(GasList),2)
                 print('Average GasAvg {0}'.format(GasAvg))
                 try:
                     mqttc.username_pw_set(username="bckMQTT", password="bckBrAaI")
                     mqttc.connect(MOSQUITTO_HOST,MOSQUITTO_PORT);
                     (result1,mid) = mqttc.publish(MOSQUITTO_GAS_MSG,GasAvg)
                     mqttc.disconnect()
                     print ('MQTT Updating {0} with {1}'.format(MOSQUITTO_GAS_MSG,GasAvg))
                 except:
                     print("MQTT ERROR : An error occurred while trying to publish the avg GasAvg to MQTT")


        print("-" * 30)

    time.sleep(3)

