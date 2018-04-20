#baseUnit.py
# Author: Jesse Offei-Nkansah
# Date: 4.19.2018
# Unit test for capabilites of robot base feature

import time
import pigpio
from servo import Servo

armPi = pigpio.pi()

base = Servo(gpio=14, pulse=1500, minPulse=1000, maxPulse=1800, pwInc=15, interest=0, connected=True)
lowerArm = Servo(gpio=15, pulse=1500, minPulse=1080, maxPulse=1800, pwInc=15, interest=1, connected=True)
upperArm = Servo(gpio=18, pulse=1500, minPulse=1080, maxPulse=1800, pwInc=15, interest=2, connected=True)
wrist = Servo(gpio=18, pulse=1500, minPulse=1080, maxPulse=1800, pwInc=15, interest=3, connected=True)

baseCB=None
lowerArmCB=None
upperArmCB=None
wristCB=None
   
SERVO = [base, lowerArm, upperArm, wrist]

def setup():
    global baseCB
    global lowerArmCB
    global upperArmCB
    global wristCB
    
    baseCB = armPi.event_callback(base.get_interest(), cb1)
    lowerArmCB = armPi.event_callback(lowerArm.get_interest(), cb1)
    upperArmCB = armPi.event_callback(upperArm.get_interest(), cb1)
    wristCB = armPi.event_callback(wrist.get_interest(), cb1)
        
def cb1(event, tick):
    global armPi
    
    while (SERVO[event].connected()):
        SERVO[event].set_pulse(SERVO[event].get_pulse() + SERVO[event].get_pwInc())
        
        armPi.set_servo_pulsewidth(SERVO[event].get_gpio(), SERVO[event].get_pulse())
        time.sleep(0.035)

def onUnlock():
    armPi.set_servo_pulsewidth(base.get_gpio(), base.get_pulse())
    armPi.set_servo_pulsewidth(lowerArm.get_gpio(), lowerArm.get_pulse())
    armPi.set_servo_pulsewidth(upperArm.get_gpio(), upperArm.get_pulse())
    armPi.set_servo_pulsewidth(wrist.get_gpio(), wrist.get_pulse())
    myo.rotSetCenter()
    setup()
    myo.unlock("hold")
    
def onPoseEdge(pose, edge):
    if(pose == "waveIn") and (edge == "on"):
        base.connect()
        armPi.event_trigger(base.get_interest())
    elif(pose == "waveIn") and (edge == "off"):
        base.disconnect()
        armPi.event_trigger(base.get_interest())
        
    if(pose == "waveOut") and (edge == "on"):
        base.reverse()
        base.connect()
        armPi.event_trigger(base.get_interest())
    elif(pose == "waveOut") and (edge == "off"):
        base.reverse()
        base.disconnect()
        armPi.event_trigger(base.get_interest())

