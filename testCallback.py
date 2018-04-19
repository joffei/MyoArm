#testCallback.py
# Author: Jesse Offei-Nkansah
# Date: 4.8.2018
# recreation of testCallback.cpp in python

import pigpio
import time

SERVO = [15, 18]
PULSE = [1500, 1500]
MIN = [1080, 1080]
MAX = [1800, 1800]
INC = [25, 25]

pi = pigpio.pi()

def moveLower(event, tick):
    global pi
    PULSE[0] += INC[0]
    
    if(PULSE[0] >= MAX[0]) or (PULSE[0] <= MIN[0]):
        INC[0] = -INC[0]
        PULSE[0] += INC[0] * 2
        
    pi.set_servo_pulsewidth(SERVO[0], PULSE[0])
    
def moveUpper(event, tick):
    global pi
    PULSE[1] += INC[1]
    
    if(PULSE[1] >= MAX[1]) or (PULSE[1] <= MIN[1]):
        INC[1] = -INC[1]
        PULSE[1] += INC[1] * 2
        
    pi.set_servo_pulsewidth(SERVO[1], PULSE[1])
    
cb1 = pi.event_callback(SERVO[0], moveLower)
cb2 = pi.event_callback(SERVO[1], moveUpper)
    
    
if (not pi.connected):
    print("Pi not connected")
    exit()
    
for x in SERVO:
    pi.set_mode(x, pigpio.OUTPUT)
    
pi.set_servo_pulsewidth(SERVO[0], 1500)
pi.set_servo_pulsewidth(SERVO[1], 1500)
time.sleep(5)
try:
    while True:
        pi.event_trigger(SERVO[0])
        pi.event_trigger(SERVO[1])
        time.sleep(0.1)
    raise KeyboardInterrupt
finally:
    pi.stop()
    print("disconnected")
