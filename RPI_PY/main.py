"""
 
    Water Environment Control System for cultivating Sea Graps

    Changes Log:
        + Disable relay as time (approximately 30 minutes)
        * Maintenance code of Enable Relay

    Author:     Wasawat Junnasaksri & Hatsathon Sachjakul - as PCSHSST
    Copyright:  2023 © Wasawat Junnasaksri and Hatsathon Sachjakul as PCSHSST
    LICENSE:    MIT License
    Editor:     TheNongice Wasawat (@_ngixx's)
    Dates:      13/8/2023 - 21:58

"""

import os
import serial
import time
import pandas as pd 
import numpy as np
import RPi.GPIO as GPIO
import requests
from Line import LINE
from dotenv import load_dotenv

# Setup Pins Digital
SOLENOID1 = 11
SOLENOID2 = 13
SOLENOID3 = 15

# Setup Mode (Value & Tokens)
load_dotenv()
LINE_TOKEN = os.getenv('LINE_TOKEN')
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11,GPIO.OUT)
exit_pg = 0

water_time = 0
alkaline_time = 0
acid_time = 0

# Setup Mode (Class Instances)
line_msg = LINE(LINE_TOKEN)

# Function to easily manages programing
def decode_text(text: str):
    enc = text.decode('utf-8')
    enc = enc.strip('\r\n')
    return enc

def convert_sec(mins: int):
    return mins*60

# Main core to handle process
if __name__ == "__main__" and exit_pg == 0:
    ser = serial.Serial('/dev/ttyACM0',9600)
    while True:
        data = ser.readline()
        data = decode_text(data)
        print(data)
        current_time = time.time()

        # Disable device on time (approx 30 minutes)
        if current_time - water_time > convert_sec(30):
            GPIO.output(SOLENOID1, GPIO.LOW)
        if current_time - alkaline_time > convert_sec(30):
            GPIO.output(SOLENOID2, GPIO.LOW)
        if current_time - acid_time > convert_sec(30):
            GPIO.output(SOLENOID3, GPIO.LOW)

        # Enable Device
        if data == "N_WATER":
            line_msg.send('Change Water')
            GPIO.output(SOLENOID1, GPIO.HIGH)
            water_time = time.time()
        elif data == "N_ALKALINE":
            line_msg.send('Alkaline Water')
            GPIO.output(SOLENOID2, GPIO.HIGH)
            alkaline_time = time.time()
        elif data == "N_ACID":
            line_msg.send('Acid Water')
            GPIO.output(SOLENOID3, GPIO.HIGH)
            acid_time = time.time()
        else:
            # If Serial return as "Normally"
            GPIO.output(SOLENOID1, GPIO.LOW)
            GPIO.output(SOLENOID2, GPIO.LOW)
            GPIO.output(SOLENOID3, GPIO.LOW)


GPIO.cleanup()
