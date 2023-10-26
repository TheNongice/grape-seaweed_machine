"""
 
    Water Environment Control System for cultivating Sea Graps
    Changes Log:
        * Fixed Serial Notify System
    Author:     Wasawat Junnasaksri & Hatsathon Sachjakul - as PCSHSST
    Copyright:  2023 © Wasawat Junnasaksri and Hatsathon Sachjakul as PCSHSST
    LICENSE:    MIT License
    Editor:     TheNongice Wasawat (@_ngixx's)
    Dates:      30/8/2023 - 19:28
    
"""
import serial
import logging
import threading
import os
from Line import LINE
import time
import RPi.GPIO as GPIO
from dotenv import load_dotenv
import BlynkLib
load_dotenv()

SOLENOID1 = 11
SOLENOID2 = 13
SOLENOID3 = 15

GPIO.setmode(GPIO.BOARD)
GPIO.setup(SOLENOID1, GPIO.OUT)
GPIO.setup(SOLENOID2, GPIO.OUT)
GPIO.setup(SOLENOID3, GPIO.OUT)

GPIO.output(SOLENOID1,GPIO.LOW)
GPIO.output(SOLENOID2,GPIO.LOW)
GPIO.output(SOLENOID3,GPIO.LOW)

LINE_TOKEN = os.getenv('LINE_TOKEN')
BLYNK_AUTH = os.getenv('BLYNK_AUTH')

ser = serial.Serial('/dev/ttyACM0',9600, timeout=.1)
line_msg = LINE(LINE_TOKEN)
blynk = BlynkLib.Blynk(BLYNK_AUTH)
run_first = True

logging.basicConfig(format='%(asctime)s :: %(message)s')

def decode_text(text: str):
    enc = text.strip('\r\n')
    return enc.split()

def convert_min(sec: int):
    mins = sec*60
    return mins

def convert_hour(mins: int):
    hour = mins*3600
    return hour

def send_msg(msg: str):
    line_msg.send(msg)

time_turbi = time.time()
time_food = time.time()
time_acid = 0
time_alikine = 0

active_turbi = 0
active_food = 0
active_acid = 0
active_alikine = 0

check_NWATER = 0

@blynk.on("V0")
def alkine_blynk(value):
    if int(value[0]) == 1:
        GPIO.output(SOLENOID1, GPIO.HIGH)
    else:
        GPIO.output(SOLENOID1, GPIO.LOW)

@blynk.on("V1")
def acid_blynk(value):
    if int(value[0]) == 1:
        GPIO.output(SOLENOID2, GPIO.HIGH)
    else:
        GPIO.output(SOLENOID2, GPIO.LOW)


@blynk.on("V2")
def food_blynk(value):
    if int(value[0]) == 1:
        GPIO.output(SOLENOID3, GPIO.HIGH)
    else:
        GPIO.output(SOLENOID3, GPIO.LOW)
try:
    while True:
        blynk.run()
        current_time = time.time()
        read_ser = decode_text(ser.readline().decode("utf-8"))
        if len(read_ser) >= 1:
            print(read_ser)
            try:
                blynk.virtual_write(3, str(read_ser[1]))
                blynk.virtual_write(4, str(read_ser[2]))
                blynk.virtual_write(5, str(read_ser[3]))
            except:
                pass
        for check in read_ser:
            # Alkine Water
            if check == "AL_WATER":
                check_NWATER = 0
                # Enable ALKALINE
                blynk.virtual_write(0, 1)
                GPIO.output(SOLENOID1,GPIO.HIGH)
                active_alikine = 1
                if active_alikine == 0:
                    time_alikine = time.time()
                logging.warning("AL WATER!")
            # Acid Water
            if check == "AC_WATER":
                check_NWATER = 0
                # Enable ACID
                blynk.virtual_write(1, 1)
                GPIO.output(SOLENOID2,GPIO.HIGH)
                active_acid = 1
                if active_acid == 0:
                    time_acid = time.time()
                logging.warning("AC WATER!")
            # Normal Water
            if check == "N_WATER":  
                if active_acid == 1 or active_alikine == 1:
                    check_NWATER+=1
                    if check_NWATER >= 3:
                        # Disable SOLENOID FOR ACID & ALKALINE
                        GPIO.output(SOLENOID1,GPIO.LOW)
                        GPIO.output(SOLENOID2,GPIO.LOW)
                        blynk.virtual_write(0, 0)
                        blynk.virtual_write(1, 0)
                        time_acid = 0
                        time_alikine = 0
                        active_alikine = 0
                        active_acid = 0
                        check_NWATER = 0
                        logging.warning("CLOSE ALL SOLENOID!")
        # โซนให้อาหารสาหร่าย
        if current_time-time_food >= convert_min(3) and active_food == 1:
            active_food = 0
            blynk.virtual_write(2, 0)
            logging.warning("CLOSE FOOD!")
            t_food = threading.Thread(target=send_msg, args=[f'ให้อาหารเสร็จสิ้น'])
            t_food.start()
            # Disable feed food
            GPIO.output(SOLENOID3,GPIO.LOW)
        
        if current_time-time_food >= convert_hour(2):
            time_food = time.time()
            active_food = 1
            blynk.virtual_write(2, 1)
            logging.warning("OPEN FOOD!")
            t_food = threading.Thread(target=send_msg, args=[f'กำลังให้อาหาร'])
            t_food.start()
            # Feed food
            GPIO.output(SOLENOID3,GPIO.HIGH)
        
        # เตือนความขุ่นสาหร่ายทุกๆ x ชม.
        if current_time-time_turbi >= convert_min(2):
            time_turbi = time.time()
            # ส่งการแจ้งเตือนไปไลน์
            try:
                logging.warning("Tell to LINE for Turbidity")
                t_tur = threading.Thread(target=send_msg, args=[f'ขณะนี้น้ำมีความขุ่นที่ {read_ser[2]:.2f}'])
                t_tur.start()
            except:
                pass
except:
    GPIO.cleanup()
