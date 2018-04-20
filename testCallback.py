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
CONN = [1, 0]

pi = pigpio.pi()

def moveLower(event, tick):
    global pi
    
    if(CONN[event]):
        PULSE[event] += INC[event]
        
        if(PULSE[event] >= MAX[event]) or (PULSE[event] <= MIN[event]):
            INC[event] = -INC[event]
            PULSE[event] += INC[event] * 2
        
        pi.set_servo_pulsewidth(SERVO[event], PULSE[event])
    
def moveUpper(event, tick):
    global pi
    PULSE[1] += INC[1]
    
    if(PULSE[1] >= MAX[1]) or (PULSE[1] <= MIN[1]):
        INC[1] = -INC[1]
        PULSE[1] += INC[1] * 2
        
    pi.set_servo_pulsewidth(SERVO[1], PULSE[1])
    
cb1 = pi.event_callback(0, moveLower)
cb2 = pi.event_callback(1, moveLower)
    
    
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
        pi.event_trigger(0)
        pi.event_trigger(1)
        time.sleep(0.1)
    raise KeyboardInterrupt
finally:
    pi.stop()
    print("disconnected")
