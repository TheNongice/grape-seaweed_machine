import os
import serial
import time
import pandas as pd 
import numpy as np
import RPi.GPIO as GPIO
import requests
from Line import LINE
from dotenv import load_dotenv

# Setup Mode (Value & Tokens)
load_dotenv()
LINE_TOKEN = os.getenv('LINE_TOKEN')
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11,GPIO.OUT)
exit_pg = 0

# Setup Mode (Class Instances)
line_msg = LINE(LINE_TOKEN)

# Function to easily manages programing
def decode_text(text: str):
    enc = text.decode('utf-8')
    enc = enc.strip('\r\n')
    return enc

if __name__ == "__main__" and exit_pg == 0:
    ser = serial.Serial('/dev/ttyACM0',9600)
    while True:
        data = ser.readline()
        data = decode_text(data)
        print(data)
        time.sleep(2)
        if data == "N_WATER":
            line_msg.send('Change Water')
        else:
            line_msg.send('Test Service')

GPIO.cleanup()
