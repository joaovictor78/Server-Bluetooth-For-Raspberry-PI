import RPi.GPIO as GPIO
import time
from bluedot.btcomm import BluetoothServer
from signal import pause
GREEN_LED = 26
RED_LED = 5
frequencyInSecconds = 1
isPowerSystem = False
ledSelected = RED_LED
lastLedSelected = RED_LED

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(GREEN_LED, GPIO.OUT)
GPIO.setup(RED_LED, GPIO.OUT)

GPIO.output(GREEN_LED, GPIO.LOW)
GPIO.output(RED_LED, GPIO.LOW)
        
def data_received(data):
    print(type(data))
    formatedData = data.split()[0]
    print(data)
    global isPowerSystem, RED_LED, GREEN_LED, ledSelected, frequencyInSecconds
    if('FREQ' in formatedData and isPowerSystem):
        frequencyInSecconds = int(data.split()[1])
        print("freq", frequencyInSecconds)
    if('H' == formatedData and isPowerSystem == False):
        print("SYTEM ON")
        isPowerSystem = True
        for x in range(0, 3):
            GPIO.output(GREEN_LED, GPIO.HIGH)
            GPIO.output(RED_LED, GPIO.HIGH)
            time.sleep(1)
            GPIO.output(GREEN_LED, GPIO.LOW)
            GPIO.output(RED_LED, GPIO.LOW)
            time.sleep(1)
    elif('L' == formatedData and isPowerSystem == True):
        print("SYSTEM OFF")
        isPowerSystem = False
        GPIO.output(ledSelected, GPIO.LOW)
    elif('R' == formatedData and isPowerSystem == True):
        GPIO.output(GREEN_LED, GPIO.LOW)
        GPIO.output(RED_LED, GPIO.HIGH)
        ledSelected = RED_LED
    elif('G' == formatedData and isPowerSystem == True):
        GPIO.output(RED_LED, GPIO.LOW)
        GPIO.output(GREEN_LED, GPIO.HIGH)
        ledSelected = GREEN_LED
    time.sleep(5)
s = BluetoothServer(data_received)
while True:
    while isPowerSystem:
        GPIO.output(ledSelected, GPIO.HIGH)
        time.sleep(frequencyInSecconds)
        GPIO.output(ledSelected, GPIO.LOW)
        time.sleep(frequencyInSecconds)