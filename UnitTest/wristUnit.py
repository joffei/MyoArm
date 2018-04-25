#wristUnit.py
# Author: Jesse Offei-Nkansah
# Date: 2.19.2018
# Unit test for capabilities of robot wrist feature

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
    
def onPeriodic():
    global armPi
    
    if(myo.isUnlocked()):
        if (wrist.get_pulse() >= wrist.get_maxPulse() - abs(wrist.get_pwInc())):
            wrist.disconnect()
            armPi.event_trigger(wrist.get_interest())
            wrist.set_pulse(wrist.get_maxPulse() - 2 * abs(wrist.get_pwInc()))
            wrist.set_pwInc(abs(wrist.get_pwInc()))
            
            armPi.set_servo_pulsewidth(wrist.get_gpio(), wrist.get_pulse())
            #time.sleep(0.1)
        elif (wrist.get_pulse() <= wrist.get_minPulse() + abs(wrist.get_pwInc())):
            wrist.disconnect()
            armPi.event_trigger(wrist.get_interest())
            wrist.set_pulse(wrist.get_minPulse() + 2 * abs(wrist.get_pwInc()))
            wrist.set_pwInc(abs(wrist.get_pwInc()))
            #add correcting pulses here
            armPi.set_servo_pulsewidth(wrist.get_gpio(), wrist.get_pulse())
            #time.sleep(0.1)
        elif (not wrist.connected()) and (myo.rotRoll() >= 0.3):
            #turn left
            wrist.reverse()
            wrist.connect()
            armPi.event_trigger(wrist.get_interest())
        elif (wrist.connected()) and (myo.rotRoll() <= 0.15) and (myo.rotRoll() >= -0.15):
            #stop
            wrist.disconnect()
            wrist.set_pwInc(abs(wrist.get_pwInc()))
            armPi.event_trigger(wrist.get_interest())
        elif (not wrist.connected()) and (myo.rotRoll() <= -0.3):
            #turn right
            wrist.connect()
            armPi.event_trigger(wrist.get_interest())
            



