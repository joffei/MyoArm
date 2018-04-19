#servoTest.py
# Author: Jesse Offei-Nkansah
# Date: 4.8.2018
# A program to test pigpio library's servo capabilities

#import pigpio
#import time
#
#pi = pigpio.pi()
#
#def upper(event, tick):
#    while cb1:
#        #pulse = 1500
#        #pi.
#        print(event)
#        time.sleep(0.1)
#
#SERVO_BASE = 14
#SERVO_LOWER_ARM = 15
#SERVO_UPPER_ARM = 18
#SERVO_WRIST = 17
#
#pi.set_mode(SERVO_BASE, pigpio.OUTPUT)
#pi.set_mode(SERVO_LOWER_ARM, pigpio.OUTPUT)
#pi.set_mode(SERVO_UPPER_ARM, pigpio.OUTPUT)
#pi.set_mode(SERVO_WRIST, pigpio.OUTPUT)
#
#cb1 = pi.event_callback(SERVO_UPPER_ARM, upper)
#
#raw_input("Press ENTER to begin")
#
#if (not pi.connected):
#    print("Pi not Connected")
#    exit()
#    
#pi.event_trigger(SERVO_UPPER_ARM)
#
#raw_input()
#
#cb1.cancel()
#
#print("\n\n\n\n\n\n\n\n\n\n\n\n\n")
#
#raw_input()
#
#pi.event_trigger(SERVO_UPPER_ARM)
#
#raw_input()
#
#cb1.cancel()
#
#pi.stop()
#print("disconnected")

#!/usr/bin/env python

import time

import pigpio

SERVO = [15, 18]     # Servos connected to gpios 15 and 18.
DIR   = [1, -1]
PW    = [1500, 1500]
SPEED = [50, 100]

pi = pigpio.pi() # Connect to local Pi.

for x in SERVO:
   pi.set_mode(x, pigpio.OUTPUT) # Set gpio as an output.
   
for x in SERVO:
    pi.set_servo_pulsewidth(x, 1500)
    time.sleep(1)
   
start = time.time()

while (time.time() - start) < 60: # Spin for 60 seconds.

   for x in range (len(SERVO)): # For each servo.

      print("Servo {} pulsewidth {} microseconds.".format(x, PW[x]))

      pi.set_servo_pulsewidth(SERVO[x], PW[x])

      PW[x] += (DIR[x] * SPEED[x])

      if (PW[x] < 1100) or (PW[x] > 1900): # Bounce back at safe limits.
         DIR[x] = - DIR[x]

      time.sleep(0.5)
      
for x in SERVO:
   pi.set_servo_pulsewidth(x, 0) # Switch servo pulses off.

pi.stop()

