# Generic libraries
from random import randint, random
import time
import datetime
from suntime import Sun, SunTimeException
import sys

NumPixels = int(sys.argv[1])

# Set latitude and Longtude for Worcester Park
latitude = 51.38
longitude = 0.24

# Libraries needed for Neopixel strip
import board
import neopixel
pixels = neopixel.NeoPixel(board.D18, NumPixels)

# LED Strip pixels per meter
PixPerMeter = 30
SnowFlakeMinlength = 4
SnowFlakeMaxlength = 8

startTime = 23
endTime = 5

class Snowdrop:
    snowflakeList = []
    def __init__(self):
        self.StartDateTime = datetime.datetime.now()
        self.SnowFlakespeed = 0.444444444 + (random() * (1.777777778  - 0.444444444))
        self.SnowFlakeLength = randint(SnowFlakeMinlength, SnowFlakeMaxlength)


# Generate number of snowdrops that will be created
NumberSnowFlakes = randint(3,3)
print('Number of SnowFlakes generated {0}' .format(NumberSnowFlakes))

# Create List that will contain all active snowdrops
Snowdrops = []

LEDDict = {}
LEDDictOld = {}

for i in range(0,NumPixels):
    LEDDictOld[i] = 0

print('Create the first snowdrop')
Snowdrops.append(Snowdrop())

print('Now run the loop')
while True:
    #print('Create Dict Start {0} '.format(datetime.datetime.now()))
    for i in range(0,NumPixels):
        LEDDict[i] = 0
    #print('Snowdrops Loop start {0} '.format(datetime.datetime.now()))
    for obj in Snowdrops:
        delta = datetime.datetime.now()-obj.StartDateTime
        deltams = int(delta.total_seconds() * 1000)
        LEDPosition = deltams * obj.SnowFlakespeed * PixPerMeter/1000
        LEDDict[max(int(LEDPosition)-3,0)] = 1
        LEDDict[max(int(LEDPosition)-2,0)] = 3
        LEDDict[max(int(LEDPosition)-1,0)] = 10
        LEDDict[int(LEDPosition)] = 125
        #print ('Born {0} Life/ms {1}, Speed/m/s {2},  LEDPos {3} '.format(obj.StartDateTime,deltams, obj.SnowFlakespeed,LEDPosition ))
        if LEDPosition > NumPixels:
            print (' Get rid of this object, Born {0}, LED is position  {1} '.format(obj.StartDateTime, LEDPosition ))
            Snowdrops.remove(obj)

    sun = Sun(latitude, longitude)
    now = datetime.datetime.now()
    # Get today's sunrise and sunset in Local time
    abd_sr = sun.get_local_sunrise_time(now)
    abd_ss = sun.get_local_sunset_time(now)
    #print('Today in Worcester Park the sun rose at {} and set at {} Local time'.format(abd_sr.strftime('%H:%M'), abd_ss.strftime('%H:%M')))
    #print('Current time {} Local London time'.        format(now.strftime('%H:%M')))

 #   if abd_sr.replace(tzinfo=None) < now < abd_ss.replace(tzinfo=None) :
    if (abd_sr.replace(tzinfo=None) < now < abd_ss.replace(tzinfo=None)) or (int(datetime.datetime.now().strftime("%H")) >= startTime or int(datetime.datetime.now().strftime("%H")) <= endTime):
        print ('Window for LEDS to be off, Power off LED(s)')
        for i in range(0,NumPixels):
             LEDDict[i] = 0
        time.sleep(10)


    #print(LEDDict)
    #print('Populate Pixels start {0} '.format(datetime.datetime.now()))
    for i in range(0,NumPixels):
        if LEDDict[(i)] != LEDDictOld[(i)]:
             #print('id {0}Value {1} '.format(i,LEDDict[(i)]))
             #pixels[(i)] = (LEDDict[i],LEDDict[i],LEDDict[i])
             pixels[(i)] = (LEDDict[i],0,0)
        else:
             pass
    #    pixels.show()

    for i in range(0,NumPixels):
        LEDDictOld[i] = LEDDict[i]


    #print('Snowdrops Loop start {0} '.format(datetime.datetime.now()))


    #print('Work out of we need to add snowflakes start {0} '.format(datetime.datetime.now()))

    if len(Snowdrops)  < NumberSnowFlakes :
        print ('Adding snowflake object {0} '.format(datetime.datetime.now()))
        Snowdrops.append(Snowdrop())
    #else :
        #print ('No need to add snowflakes ')
