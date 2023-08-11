import serial
import time
import pandas as pd
import numpy as np
import RPi.GPIO as GPIO
import requests
from Line import LINE

line_msg = LINE()
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11,GPIO.OUT)

# Test Relay
for x in range(3):
    GPIO.output(11,GPIO.HIGH)
    l = line_msg.send('NOW GPIO.HIGH')
    print(l[0])
    time.sleep(1)
    GPIO.output(11,GPIO.LOW)
    l = line_msg.send('NOW GPIO.LOW')
    print(l[0])
    time.sleep(1)
GPIO.cleanup()
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
-- VISUAL --                                                                                                                             27        1,1           All

