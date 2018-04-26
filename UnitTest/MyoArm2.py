#MyoArm.py
# Author: Jesse Offei-Nkansah
# Date: 4.20.2018
# Full source code for myo robotic arm control

import time
import pigpio
from servo import *

armPi = pigpio.pi()

handArm = False
reset = False

base1 = Servo(gpio=14, pulse=1500, minPulse=1000, maxPulse=1800, pwInc=15, interest=0, connected=True)
lowerArm1 = Servo(gpio=15, pulse=1500, minPulse=1140, maxPulse=1800, pwInc=20, interest=1, connected=True)
upperArm1 = Servo(gpio=18, pulse=1500, minPulse=1080, maxPulse=1800, pwInc=20, interest=2, connected=True)
wrist1 = Servo(gpio=17, pulse=1500, minPulse=1000, maxPulse=2000, pwInc=15, interest=3, connected=True)
claw1 = Servo(gpio=27, pulse=1000, minPulse=1000, maxPulse=1500, pwInc=1, interest=4, connected=True)

base2 = Servo(gpio=22, pulse=1500, minPulse=1000, maxPulse=1800, pwInc=15, interest=0, connected=True)
lowerArm2 = Servo(gpio=23, pulse=1500, minPulse=1140, maxPulse=1800, pwInc=20, interest=1, connected=True)
upperArm2 = Servo(gpio=24, pulse=1500, minPulse=1080, maxPulse=1800, pwInc=20, interest=2, connected=True)
wrist2 = Servo(gpio=10, pulse=1500, minPulse=1000, maxPulse=2000, pwInc=-15, interest=3, connected=True)
claw2 = Servo(gpio=9, pulse=1500, minPulse=1000, maxPulse=1500, pwInc=1, interest=4, connected=True)
roll2 = Servo(gpio=11, pulse=1000, minPulse=1000, maxPulse=1500, pwInc=15, interest=5, connected=True)
pitch2 = Servo(gpio=25, pulse=1500, minPulse=1000, maxPulse=1800, pwInc=25, interest=6, connected=True)

# other fingers on humanoid claw
claw2a = Servo(gpio=5, pulse=1000, minPulse=1000, maxPulse=1800, pwInc=1, interest=4, connected=True)
claw2b = Servo(gpio=6, pulse=1000, minPulse=1000, maxPulse=1800, pwInc=1, interest=4, connected=True)
claw2c = Servo(gpio=13, pulse=1000, minPulse=1000, maxPulse=1800, pwInc=1, interest=4, connected=True)
claw2d = Servo(gpio=19, pulse=1000, minPulse=1000, maxPulse=1800, pwInc=1, interest=4, connected=True)

ROBO1 = [base1, lowerArm1, upperArm1, wrist1, claw1]
ROBO2 = [base2, lowerArm2, upperArm2, wrist2, claw2, roll2, pitch2]
FINGERS = [claw2a, claw2b, claw2c, claw2d]

ROBOT = [ROBO1, ROBO2]

SERVO = None

base = base1
baseCB = None

lowerArm = lowerArm1
lowerArmCB = None

upperArm = upperArm1
upperArmCB = None

wrist = wrist1
wristCB = None

claw = claw1
clawCB = None

pitch = None
pitchCB = None

roll = None
rollCB = None


def set_arm():
    global SERVO
    global base
    global lowerArm
    global upperArm
    global wrist
    global claw
    global roll
    global pitch

    if (handArm):
        SERVO = ROBO2
    else:
        SERVO = ROBO1

    base = SERVO[0]
    lowerArm = SERVO[1]
    upperArm = SERVO[2]
    wrist = SERVO[3]
    claw = SERVO[4]
    try:
        roll = SERVO[5]
        pitch = SERVO[6]
    except IndexError:
        roll = None
        pitch = None


def switch_arm():
    global handArm
    setdown()
    handArm = not handArm
    setup()


def setup():
    global baseCB
    global lowerArmCB
    global upperArmCB
    global wristCB
    global clawCB
    global rollCB
    global pitchCB

    set_arm()
    baseCB = armPi.event_callback(base.get_interest(), cb1)
    lowerArmCB = armPi.event_callback(lowerArm.get_interest(), cb1)
    upperArmCB = armPi.event_callback(upperArm.get_interest(), cb1)
    wristCB = armPi.event_callback(wrist.get_interest(), cb1)
    clawCB = armPi.event_callback(claw.get_interest(), cb1)
    if(roll is not None) and (pitch is not None):
        rollCB = armPi.event_callback(roll.get_interest(), cb1)
        pitchCB = armPi.event_callback(pitch.get_interest(), cb1)


def setdown():
    global baseCB
    global lowerArmCB
    global upperArmCB
    global wristCB
    global clawCB
    global rollCB
    global pitchCB

    baseCB.cancel()
    lowerArmCB.cancel()
    upperArmCB.cancel()
    wristCB.cancel()
    clawCB.cancel()
    if(rollCB is not None) and (pitchCB is not None):
        rollCB.cancel()
        pitchCB.cancel()


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

        armPi.set_servo_pulsewidth(SERVO[event].get_gpio(), SERVO[event].get_pulse())

        if (handArm) and (event == 4):
            if(SERVO[event].get_pulse() < SERVO[event].get_minPulse() + 30):
                for servo in FINGERS:
                    servo.set_pulse(servo.get_maxPulse())
                    armPi.set_servo_pulsewidth(servo.get_gpio(), servo.get_pulse())
            elif(SERVO[event].get_pulse() > SERVO[event].get_maxPulse() - 30):
                for servo in FINGERS:
                    servo.set_pulse(servo.get_minPulse())
                    armPi.set_servo_pulsewidth(servo.get_gpio(), servo.get_pulse())
            #armPi.set_servo_pulsewidth(claw2a.get_gpio(), SERVO[event].get_pulse())
            #armPi.set_servo_pulsewidth(claw2b.get_gpio(), SERVO[event].get_pulse())
            #armPi.set_servo_pulsewidth(claw2c.get_gpio(), SERVO[event].get_pulse())
            #armPi.set_servo_pulsewidth(claw2d.get_gpio(), SERVO[event].get_pulse())
        #print(SERVO[event].get_pulse())
        time.sleep(0.035)


def onUnlock():
    global reset
    if (not reset):
        for boto in ROBOT:
            for servo in boto:
                if (servo is not None):
                    armPi.set_servo_pulsewidth(servo.get_gpio(), servo.get_pulse())
                    reset = True
#    armPi.set_servo_pulsewidth(base.get_gpio(), base.get_pulse())
#    armPi.set_servo_pulsewidth(lowerArm.get_gpio(), lowerArm.get_pulse())
#    armPi.set_servo_pulsewidth(upperArm.get_gpio(), upperArm.get_pulse())
#    armPi.set_servo_pulsewidth(wrist.get_gpio(), wrist.get_pulse())
#    armPi.set_servo_pulsewidth(claw.get_gpio(), claw.get_pulse())
#    if(roll != None) and (pitch != None):
#        armPi.set_servo_pulsewidth(roll.get_gpio(), roll.get_pulse())
#        armPi.set_servo_pulsewidth(pitch.get_gpio(), pitch.get_pulse())
    myo.box_factor = 0.5
    myo.rotSetCenter()
    setup()
    myo.unlock("hold")


def onLock():
    for boto in ROBOT:
        for servo in boto:
            servo.disconnect()
            armPi.event_trigger(servo.get_interest())
    setdown()


def onPoseEdge(pose, edge):
    global armPi

    myo.box_factor = 0.25

    if(pose == "waveIn") and (edge == "on") and (handArm) and ((myo.getBox() == 2) or (myo.getBox() == 4) or (myo.getBox() == 6) or (myo.getBox() == 8)):
        pitch.reverse()
        pitch.connect()
        armPi.event_trigger(pitch.get_interest())
        print("wrist")
    elif(pose == "waveIn") and (edge == "off") and (handArm) and ((myo.getBox() == 2) or (myo.getBox() == 4) or (myo.getBox() == 6) or (myo.getBox() == 8)):
        pitch.reverse()
        pitch.disconnect()
        armPi.event_trigger(pitch.get_interest())
    elif(pose == "waveOut") and (edge == "on") and (handArm) and ((myo.getBox() == 2) or (myo.getBox() == 4) or (myo.getBox() == 6) or (myo.getBox() == 8)):
        pitch.connect()
        armPi.event_trigger(pitch.get_interest())
        print("wrist")
    elif (pose == "waveOut") and (edge == "off") and (handArm) and ((myo.getBox() == 2) or (myo.getBox() == 4) or (myo.getBox() == 6) or (myo.getBox() == 8)):
        pitch.disconnect()
        armPi.event_trigger(pitch.get_interest())
    elif(pose == "waveIn") and (edge == "on"):
        base.connect()
        armPi.event_trigger(base.get_interest())
    elif(pose == "waveIn") and (edge == "off"):
        base.disconnect()
        armPi.event_trigger(base.get_interest())

    elif(pose == "waveOut") and (edge == "on"):
        base.reverse()
        base.connect()
        armPi.event_trigger(base.get_interest())
    elif(pose == "waveOut") and (edge == "off"):
        base.reverse()
        base.disconnect()
        armPi.event_trigger(base.get_interest())

    elif (pose == "fist") and (edge == "on") and handArm:
        claw.connect()
        claw.set_pulse(claw.get_minPulse())
        armPi.event_trigger(claw.get_interest())
        time.sleep(0.1)
        claw.disconnect()
        armPi.event_trigger(claw.get_interest())
        print("fist")
    elif (pose == "fist") and (edge == "off") and handArm:
        claw.connect()
        claw.set_pulse(claw.get_maxPulse())
        armPi.event_trigger(claw.get_interest())
        time.sleep(0.1)
        claw.disconnect()
        armPi.event_trigger(claw.get_interest())
    elif (pose == "fist") and (edge == "on") and not handArm:
        claw.connect()
        claw.set_pulse(claw.get_maxPulse())
        armPi.event_trigger(claw.get_interest())
        time.sleep(0.1)
        claw.disconnect()
        armPi.event_trigger(claw.get_interest())
        print("fist")
    elif (pose == "fist") and (edge == "off") and not handArm:
        claw.connect()
        claw.set_pulse(claw.get_minPulse())
        armPi.event_trigger(claw.get_interest())
        time.sleep(0.1)
        claw.disconnect()
        armPi.event_trigger(claw.get_interest())
    elif (pose == "fingersSpread") and (edge == "on"):
        switch_arm()
        myo.vibrate(1)
    #elif (pose == "doubleTap") and (edge == "on") and (myo.isUnlocked()):
    #    time.sleep(0.5)
    #    myo.lock()
    #    myo.vibrate(1)
    myo.box_factor = 0.5



def onBoxChange(boxNumber, state):
    global armPi

    if (lowerArm.get_pulse() >= lowerArm.get_maxPulse() - abs(lowerArm.get_pwInc())):
        lowerArm.disconnect()
        lowerArm.set_pulse(lowerArm.get_maxPulse() - 2 * abs(lowerArm.get_pwInc()))
        lowerArm.set_pwInc(abs(lowerArm.get_pwInc()))

        armPi.set_servo_pulsewidth(lowerArm.get_gpio(), lowerArm.get_pulse())

    elif (lowerArm.get_pulse() <= lowerArm.get_minPulse() + abs(lowerArm.get_pwInc())):
        lowerArm.disconnect()
        lowerArm.set_pulse(lowerArm.get_minPulse() + 2 * abs(lowerArm.get_pwInc()))
        lowerArm.set_pwInc(abs(lowerArm.get_pwInc()))
        # add correcting pulses here
        armPi.set_servo_pulsewidth(lowerArm.get_gpio(), lowerArm.get_pulse())

    elif (boxNumber == 3) and (state == "on"):  # ((boxNumber == 8) or (boxNumber == 1) or (boxNumber == 2)) and (state == 'on'):
        lowerArm.reverse()
        lowerArm.connect()
    elif (boxNumber == 0) and (state == "on"):  # ((boxNumber == 7) or (boxNumber == 0) or (boxNumber == 3)) and (state == 'on'):
        lowerArm.disconnect()
        lowerArm.set_pwInc(abs(lowerArm.get_pwInc()))
    elif (boxNumber == 7) and (state == "on"):  # ((boxNumber == 6) or (boxNumber == 5) or (boxNumber == 4)) and (state == 'on')
        lowerArm.connect()

    armPi.event_trigger(lowerArm.get_interest())

    if (upperArm.get_pulse() >= upperArm.get_maxPulse() - upperArm.get_pwInc()):
        upperArm.disconnect()
        upperArm.set_pulse(upperArm.get_maxPulse() - 2 * abs(upperArm.get_pwInc()))
        upperArm.set_pwInc(abs(upperArm.get_pwInc()))
        # add correcting pulses here
        armPi.set_servo_pulsewidth(upperArm.get_gpio(), upperArm.get_pulse())

    elif (upperArm.get_pulse() <= upperArm.get_minPulse() + upperArm.get_pwInc()):
        upperArm.disconnect()
        upperArm.set_pulse(upperArm.get_minPulse() + 2 * abs(upperArm.get_pwInc()))
        upperArm.set_pwInc(abs(upperArm.get_pwInc()))
        # add correcting pulses here
        armPi.set_servo_pulsewidth(upperArm.get_gpio(), upperArm.get_pulse())

    elif (boxNumber == 1) and (state == "on"):  # ((boxNumber == 2) or (boxNumber == 3) or (boxNumber == 4)) and (state == 'on'):
        upperArm.connect()
    elif (boxNumber == 0) and (state == "on"):  # ((boxNumber == 1) or (boxNumber == 0) or (boxNumber == 5)) and (state == 'on')
        upperArm.set_pwInc(abs(upperArm.get_pwInc()))
        upperArm.disconnect()
    elif (boxNumber == 5) and (state == "on"):  # ((boxNumber == 8) or (boxNumber == 7) or (boxNumber == 6)) and (state == 'on'):
        upperArm.reverse()
        upperArm.connect()

    armPi.event_trigger(upperArm.get_interest())




def onPeriodic():
    global armPi

    if(myo.isUnlocked()):
        if (wrist.get_pulse() >= wrist.get_maxPulse() - abs(wrist.get_pwInc())):
            wrist.disconnect()
            armPi.event_trigger(wrist.get_interest())
            wrist.set_pulse(wrist.get_maxPulse() - 2 * abs(wrist.get_pwInc()))
            wrist.set_pwInc(abs(wrist.get_pwInc()))

            armPi.set_servo_pulsewidth(wrist.get_gpio(), wrist.get_pulse())
            # time.sleep(0.1)
        elif (wrist.get_pulse() <= wrist.get_minPulse() + abs(wrist.get_pwInc())):
            wrist.disconnect()
            armPi.event_trigger(wrist.get_interest())
            wrist.set_pulse(wrist.get_minPulse() + 2 * abs(wrist.get_pwInc()))
            wrist.set_pwInc(abs(wrist.get_pwInc()))
            # add correcting pulses here
            armPi.set_servo_pulsewidth(wrist.get_gpio(), wrist.get_pulse())
            # time.sleep(0.1)
        elif (not wrist.connected()) and (myo.rotRoll() >= 0.3):
            # turn left
            wrist.reverse()
            wrist.connect()
            armPi.event_trigger(wrist.get_interest())
        elif (wrist.connected()) and (myo.rotRoll() <= 0.15) and (myo.rotRoll() >= -0.15):
            # stop
            wrist.disconnect()
            wrist.set_pwInc(abs(wrist.get_pwInc()))
            armPi.event_trigger(wrist.get_interest())
        elif (not wrist.connected()) and (myo.rotRoll() <= -0.3):
            # turn right
            wrist.connect()
            armPi.event_trigger(wrist.get_interest())
            
