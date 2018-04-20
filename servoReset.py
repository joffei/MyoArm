#servoReset.py
# Author: Jesse Offei-Nkansah
# Date: 4.9.2018
# Test pulsing to the servo

import pigpio
import time

SERVO_PIN = 15
CENTER_PULSE = 1500

pulse = 1010
pi = pigpio.pi()
print("initializing pi")

while(pulse != 0):
    
    
    
    pulse = (int(input("number between 1010 and 2000, 0 to exit: ")))
    
    if(pulse > 2000):
        print("too high")
        pulse = 1010
    elif(pulse == 0):
        break
    elif(pulse < 1010):
        print("too low")
        pulse = 1010
    else:
        if (not pi.connected):
            print("Pi not connected")
            exit()
        print("Init OK")
        print(pi.get_mode(SERVO_PIN))
        
        if (pi.get_mode(SERVO_PIN) != pigpio.OUTPUT):
            pi.set_mode(SERVO_PIN, pigpio.OUTPUT)
            
        pi.set_servo_pulsewidth(SERVO_PIN, pulse)
        time.sleep(1)
        
while (pi.connected):
    pi.stop()
    
print("disconnected")
