import time
import board
import adafruit_mpu6050
import busio
from digitalio import DigitalInOut, Direction

leds = [DigitalInOut(board.GP16), DigitalInOut(board.GP17), DigitalInOut(board.GP18), DigitalInOut(board.GP19),
        DigitalInOut(board.GP20), DigitalInOut(board.GP21), DigitalInOut(board.GP22), DigitalInOut(board.GP26)]

for led in leds:
    led.direction = Direction.OUTPUT

i2c = busio.I2C(board.GP9, board.GP8)
mpu = adafruit_mpu6050.MPU6050(i2c)

msg = [254, 9, 9, 254, 9]

swingPeriod = getSwingPeriod()
interval = swingPeriod / len(msg)
index = 0;

while True:
    light_column(index)
    if index == len(msg) - 1:
        index = 0
    else:
        index++
    time.sleep(interval)
    

def light_column(input):
    for led in leds:
        led.value = input % 2 == 1;
        input = (int) (input / 2)


def getSwingPeriod():
    prevZ = currZ = mpu.acceleration[2]
    initTime = time.time()
    while currZ >= prevZ:
        currZ = mpu.acceleration[2]
    endTime = time.time()
    return endTime - initTime

"""
while True:
    temp, temp, currZ = mpu.acceleration
    
    if swingingLeft != (currZ>initialZ):
        if currZ>initialZ:
            minZ = initialZ
        elif currZ<initialZ:
            maxZ = initialZ
        swingingLeft=(currZ>initialZ)
        swingLength = maxZ-minZ
        interval= swingLength / 5
    #print(swingLength)
    if (minZ <= currZ and currZ <= minZ + interval) or (minZ + (interval * 4) <= currZ and currZ <= maxZ):
        light_column(254)
    elif minZ + interval <= currZ and currZ <= minZ + (interval * 4):
        light_column(9)
#     if currZ > maxZ:
#         maxZ = currZ
#         swingLength = maxZ-minZ
#     else if currZ < minZ:
#         minZ = currZ
#         swingLength = maxZ-minZ
    
    initialZ = currZ
    time.sleep(0.1)
"""