#LowerArmUnit.py
# Author: Jesse Offei-Nkansah
# Date: 4.19.2018
# Unit test for capabilities of robot lower arm feature

import time
import pigpio
from servo import *

armPi = pigpio.pi()

base = Servo(gpio=14, pulse=1500, minPulse=1000, maxPulse=1800, pwInc=15, interest=0, connected=True)
lowerArm = Servo(gpio=15, pulse=1500, minPulse=1140, maxPulse=1800, pwInc=20, interest=1, connected=True)
upperArm = Servo(gpio=18, pulse=1500, minPulse=1080, maxPulse=1800, pwInc=20, interest=2, connected=True)
wrist = Servo(gpio=17, pulse=1500, minPulse=1000, maxPulse=2000, pwInc=15, interest=3, connected=True)
claw = Servo(gpio=27, pulse=1000, minPulse=1000, maxPulse=1500, pwInc=1, interest=4, connected=True)

SERVO = [base, lowerArm, upperArm, wrist, claw]

def setup():
    armPi.event_callback(base.get_interest(), cb1)
    armPi.event_callback(lowerArm.get_interest(), cb1)
    armPi.event_callback(upperArm.get_interest(), cb1)
    armPi.event_callback(wrist.get_interest(), cb1)
    armPi.event_callback(claw.get_interest(), cb1)
        
def cb1(event, tick):
    global armPi
    
    while (SERVO[event].connected()):
        if (SERVO[event].get_pulse() < SERVO[event].get_minPulse()):
            SERVO[event].set_pulse(SERVO[event].get_min_Pulse())
            break
        elif (SERVO[event].get_pulse() > SERVO[event].get_maxPulse()):
            SERVO[event].set_pulse(SERVO[event].get_maxPulse())
            break
        else:
            SERVO[event].set_pulse(SERVO[event].get_pulse() + SERVO[event].get_pwInc())
        
        #print(SERVO[event].get_pulse())
        armPi.set_servo_pulsewidth(SERVO[event].get_gpio(), SERVO[event].get_pulse())
        time.sleep(0.035)
        
#def cb2(event, tick):
#    global armPi
#    
#    if (SERVO[event].connected()):
#        if (SERVO[event].get_pulse() < SERVO[event].get_minPulse()):
#            SERVO[event].set_pulse(SERVO[event].get_min_Pulse())
#            return
#        elif (SERVO[event].get_pulse() > SERVO[event].get_maxPulse()):
#            SERVO[event].set_pulse(SERVO[event].get_maxPulse())
#            return
#        else:
#            SERVO[event].set_pulse(SERVO[event].get_pulse() + SERVO[event].get_pwInc())
#        
#        #print(SERVO[event].get_pulse())
#        armPi.set_servo_pulsewidth(SERVO[event].get_gpio(), SERVO[event].get_pulse())
#        time.sleep(0.035)

def onUnlock():
    armPi.set_servo_pulsewidth(base.get_gpio(), base.get_pulse())
    armPi.set_servo_pulsewidth(lowerArm.get_gpio(), lowerArm.get_pulse())
    armPi.set_servo_pulsewidth(upperArm.get_gpio(), upperArm.get_pulse())
    armPi.set_servo_pulsewidth(wrist.get_gpio(), wrist.get_pulse())
    armPi.set_servo_pulsewidth(claw.get_gpio(), claw.get_pulse())
    myo.box_factor = 0.5
    myo.rotSetCenter()
    setup()
    myo.unlock("hold")
    
def onBoxChange(boxNumber, state):
    
    global armPi
    
#    limit = False
#    
#    
#    if (lowerArm.get_pulse() >= lowerArm.get_maxPulse() - abs(lowerArm.get_pwInc())):
#        lowerArm.disconnect()
#        lowerArm.set_pulse(lowerArm.get_maxPulse() - 2 * abs(lowerArm.get_pwInc()))
#        lowerArm.set_pwInc(abs(lowerArm.get_pwInc()))
#        
#        armPi.set_servo_pulsewidth(lowerArm.get_gpio(), lowerArm.get_pulse())
#        limit = True
#        #time.sleep(0.1)
#    elif (lowerArm.get_pulse() <= lowerArm.get_minPulse() + abs(lowerArm.get_pwInc())):
#        lowerArm.disconnect()
#        lowerArm.set_pulse(lowerArm.get_minPulse() + 2 * abs(lowerArm.get_pwInc()))
#        lowerArm.set_pwInc(abs(lowerArm.get_pwInc()))
#        #add correcting pulses here
#        armPi.set_servo_pulsewidth(lowerArm.get_gpio(), lowerArm.get_pulse())
#        limit = True
#        #time.sleep(0.1)
#    if (upperArm.get_pulse() >= upperArm.get_maxPulse() - upperArm.get_pwInc()):
#        upperArm.disconnect()
#        upperArm.set_pulse(upperArm.get_maxPulse() - 2 * abs(upperArm.get_pwInc()))
#        upperArm.set_pwInc(abs(upperArm.get_pwInc()))
#        #add correcting pulses here
#        armPi.set_servo_pulsewidth(upperArm.get_gpio(), upperArm.get_pulse())
#        limit = True
#        #time.sleep(0.1)
#    elif (upperArm.get_pulse() <= upperArm.get_minPulse() + upperArm.get_pwInc()):
#        upperArm.disconnect()
#        upperArm.set_pulse(upperArm.get_minPulse() + 2 * abs(upperArm.get_pwInc()))
#        upperArm.set_pwInc(abs(upperArm.get_pwInc()))
#        #add correcting pulses here
#        armPi.set_servo_pulsewidth(upperArm.get_gpio(), upperArm.get_pulse())
#        limit = True
#        #time.sleep(0.1)
#        
#    if(limit):
#        return
#        
#    while (boxNumber == 0) and (state == "on"):
#        lowerArm.disconnect()
#        upperArm.disconnect()
#        armPi.event_trigger(lowerArm.get_interest())
#        armPi.event_trigger(upperArm.get_interest())
#        lowerArm.set_pwInc(abs(lowerArm.get_pwInc()))
#        upperArm.set_pwInc(abs(upperArm.get_pwInc()))
#        #time.sleep(0.035)
#    while (boxNumber == 1) and (state == "on"):
#        lowerArm.disconnect()
#        upperArm.connect()
#        armPi.event_trigger(lowerArm.get_interest())
#        armPi.event_trigger(upperArm.get_interest())
#        lowerArm.set_pwInc(abs(lowerArm.get_pwInc()))
#        #time.sleep(0.035)
#    while (boxNumber == 2) and (state == "on"):
#        lowerArm.connect()
#        upperArm.connect()
#        armPi.event_trigger(lowerArm.get_interest())
#        armPi.event_trigger(upperArm.get_interest())
#        #time.sleep(0.035)
#    while (boxNumber == 3) and (state == "on"):
#        lowerArm.connect()
#        upperArm.disconnect()
#        armPi.event_trigger(lowerArm.get_interest())
#        armPi.event_trigger(upperArm.get_interest())
#        upperArm.set_pwInc(abs(upperArm.get_pwInc()))
#        #time.sleep(0.035)
#    while (boxNumber == 4) and (state == "on"):
#        lowerArm.connect()
#        upperArm.connect()
#        upperArm.reverese()
#        armPi.event_trigger(lowerArm.get_interest())
#        armPi.event_trigger(upperArm.get_interest())
#        #time.sleep(0.035)
#    while (boxNumber == 5) and (state == "on"):
#        lowerArm.disconnect()
#        upperArm.connect()
#        upperArm.reverse()
#        armPi.event_trigger(lowerArm.get_interest())
#        armPi.event_trigger(upperArm.get_interest())
#        lowerArm.set_pwInc(abs(lowerArm.get_pwInc()))
#        #time.sleep(0.035)
#    while (boxNumber == 6) and (state == "on"):
#        lowerArm.connect()
#        lowerArm.reverse()
#        upperArm.connect()
#        upperArm.reverse()
#        armPi.event_trigger(lowerArm.get_interest())
#        armPi.event_trigger(upperArm.get_interest())
#        #time.sleep(0.035)
#    while (boxNumber == 7) and (state == "on"):
#        lowerArm.connect()
#        lowerArm.reverse()
#        upperArm.disconnect()
#        armPi.event_trigger(lowerArm.get_interest())
#        armPi.event_trigger(upperArm.get_interest())
#        upperArm.set_pwInc(abs(upperArm.get_pwInc()))
#        #time.sleep(0.035)
#    while (boxNumber == 8) and (state == "on"):
#        lowerArm.connect()
#        lowerArm.reverse()
#        upperArm.connect()
#        armPi.event_trigger(lowerArm.get_interest())
#        armPi.event_trigger(upperArm.get_interest())
#        #time.sleep(0.035)
#    
#
#    
    
    
    if (lowerArm.get_pulse() >= lowerArm.get_maxPulse() - abs(lowerArm.get_pwInc())):
        lowerArm.disconnect()
        lowerArm.set_pulse(lowerArm.get_maxPulse() - 2 * abs(lowerArm.get_pwInc()))
        lowerArm.set_pwInc(abs(lowerArm.get_pwInc()))
        
        armPi.set_servo_pulsewidth(lowerArm.get_gpio(), lowerArm.get_pulse())
        #time.sleep(0.1)
    elif (lowerArm.get_pulse() <= lowerArm.get_minPulse() + abs(lowerArm.get_pwInc())):
        lowerArm.disconnect()
        lowerArm.set_pulse(lowerArm.get_minPulse() + 2 * abs(lowerArm.get_pwInc()))
        lowerArm.set_pwInc(abs(lowerArm.get_pwInc()))
        #add correcting pulses here
        armPi.set_servo_pulsewidth(lowerArm.get_gpio(), lowerArm.get_pulse())
        #time.sleep(0.1)
    elif (myo.getHBox() == 1) and (state == "on"): #((boxNumber == 8) or (boxNumber == 1) or (boxNumber == 2)) and (state == 'on'):
        lowerArm.reverse()
        lowerArm.connect()
    elif (myo.getHBox() == 0) and (state == "on"): #((boxNumber == 7) or (boxNumber == 0) or (boxNumber == 3)) and (state == 'on'):
        lowerArm.disconnect()
        lowerArm.set_pwInc(abs(lowerArm.get_pwInc()))
    elif (myo.getHBox() == -1) and (state == "on"): #((boxNumber == 6) or (boxNumber == 5) or (boxNumber == 4)) and (state == 'on')
        lowerArm.connect()
        
    armPi.event_trigger(lowerArm.get_interest())
        
    
    if (upperArm.get_pulse() >= upperArm.get_maxPulse() - upperArm.get_pwInc()):
        upperArm.disconnect()
        upperArm.set_pulse(upperArm.get_maxPulse() - 2 * abs(upperArm.get_pwInc()))
        upperArm.set_pwInc(abs(upperArm.get_pwInc()))
        #add correcting pulses here
        armPi.set_servo_pulsewidth(upperArm.get_gpio(), upperArm.get_pulse())
        #time.sleep(0.1)
    elif (upperArm.get_pulse() <= upperArm.get_minPulse() + upperArm.get_pwInc()):
        upperArm.disconnect()
        upperArm.set_pulse(upperArm.get_minPulse() + 2 * abs(upperArm.get_pwInc()))
        upperArm.set_pwInc(abs(upperArm.get_pwInc()))
        #add correcting pulses here
        armPi.set_servo_pulsewidth(upperArm.get_gpio(), upperArm.get_pulse())
        #time.sleep(0.1)
    elif (myo.getVBox() == 1) and (state == "on"): #((boxNumber == 2) or (boxNumber == 3) or (boxNumber == 4)) and (state == 'on'):
        upperArm.connect()
    elif (myo.getVBox() == 0) and (state == "on"): #((boxNumber == 1) or (boxNumber == 0) or (boxNumber == 5)) and (state == 'on')
        upperArm.set_pwInc(abs(upperArm.get_pwInc()))
        upperArm.disconnect()
    elif (myo.getVBox() == -1) and (state == "on"): #((boxNumber == 8) or (boxNumber == 7) or (boxNumber == 6)) and (state == 'on'):
        upperArm.reverse()
        upperArm.connect()
        
    armPi.event_trigger(upperArm.get_interest())
    
    #time.sleep(0.03)
   
