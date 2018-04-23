#clawUnit.pyd
# Author: Jesse Offei-Nkansah
# Date: 4.15.2018
# Test capabilities of the claw feature on the basic robotic arm

import time
import pigpio
from servo import *

armPi = pigpio.pi()

base = Servo(gpio=14, pulse=1500, minPulse=1000, maxPulse=1800, pwInc=15, interest=0, connected=True)
lowerArm = Servo(gpio=15, pulse=1500, minPulse=1080, maxPulse=1800, pwInc=20, interest=1, connected=True)
upperArm = Servo(gpio=18, pulse=1500, minPulse=1080, maxPulse=1800, pwInc=20, interest=2, connected=True)
wrist = Servo(gpio=17, pulse=1500, minPulse=1000, maxPulse=2000, pwInc=15, interest=3, connected=True)
claw = Servo(gpio=17, pulse=1500, minPulse=1000, maxPulse=2000, pwInc=15, interest=4, connected=True)
   
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
        if (SERVO[event].get_pulse() > SERVO[event].get_minPulse()+abs(SERVO[event].get_pwInc())) and (SERVO[event].get_pulse() < SERVO[event].get_maxPulse()-abs(SERVO[event].get_pwInc())):
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

def onPoseEdge(pose, edge):
    global armPi
    
    claw.connect()
    
    if (pose == "fist") and (edge == "on"):
        
        claw.set_pulse(claw.get_maxPulse())
    
    elif (pose == "fist") and (edge == "off"):
    
        claw.set_pulse(claw.get_minPulse())
        
    armPi.event_trigger(claw.get_interest())
    time.sleep(0.075)
    claw.disconnect()
    
    