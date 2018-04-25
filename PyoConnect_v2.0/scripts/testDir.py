# Double tap to unlock
# kept unlocked until lock explicitly called

import time

cnt = 0

def onUnlock():
    myo.unlock("hold")
    myo.box_factor = 0.5
    myo.rotSetCenter()
    
def onPoseEdge(pose, edge):
    print pose + " " + edge
#    if(pose == 'fist') and (edge == 'on'):
#        print "Fist on"
#    elif(pose == 'fist') and (edge == 'off'):
#        print "Fist off"
#    elif(pose == 'waveIn') and (edge == 'on'):
#        print "Wave In on"
#    elif(pose == 'waveIn') and (edge == 'off'):
#        print "Wave In off"
#    elif(pose == 'waveOut') and (edge == 'on'):
#        print "Wave Out on"
#    elif(pose == 'waveOut') and (edge == 'off'):
#        print "Wave Out off"
#    elif(pose == 'fingersSpread') and (edge == 'on'):
#        print "finger Spread on"
#    elif(pose == 'fingersSpread') and (edge == 'off'):
#        print "fingers Spread off"
#    elif(pose == 'rest') and (edge == 'on'):
#        print "rest on"
#    elif(pose == 'rest') and (edge == 'off'):
#        print "rest off"
#    elif(pose == 'doubleTap') and (edge == 'on'):
#        print "double Tap on"
#    elif(pose == 'doubleTap') and (edge == 'off'):
#        print "double Tap off"
#    elif(pose == 'unknown') and (edge == 'on'):
#        print "unknown on"
#    elif(pose == 'unknown') and (edge == 'off'):
#        print "unknown off"
#        
#def onBoxChange(boxNumber, state):
#    print(myo.getHBox(), myo.getVBox(), state)
#    if (myo.getHBox() == 1): #((boxNumber == 8) or (boxNumber == 1) or (boxNumber == 2)) and (state == 'on'):
#        lowerArm.reverse()
#        lowerArm.connect()
#        armPi.event_trigger(lowerArm.get_interest())
#    elif (myo.getHBox() == 0): #((boxNumber == 7) or (boxNumber == 0) or (boxNumber == 3)) and (state == 'on'):
#        lowerArm.set_pwInc(abs(lowerArm.get_pwInc()))
#        lowerArm.disconnect()
#        armPi.event_trigger(lowerArm.get_interest())
#    elif (myo.getHBox() == -1): #((boxNumber == 6) or (boxNumber == 5) or (boxNumber == 4)) and (state == 'on')
#        lowerArm.connect()
#        armPi.event_trigger(lowerArm.get_interest())
        
    
#    if (myo.getVBox() == 1): #((boxNumber == 2) or (boxNumber == 3) or (boxNumber == 4)) and (state == 'on'):
#        upperArm.connect()
#        armPi.event_trigger(upperArm.get_interest())
#    elif (myo.getVBox() == 0): #((boxNumber == 1) or (boxNumber == 0) or (boxNumber == 5)) and (state == 'on')
#        upperArm.set_pwInc(abs(upperArm.get_pwInc()))
#        upperArm.disconnect()
#        armPi.event_trigger(upperArm.get_interest())
#    elif (myo.getVBox() == -1): #((boxNumber == 8) or (boxNumber == 7) or (boxNumber == 6)) and (state == 'on'):
#        upperArm.reverse()
#        upperArm.connect()
#        armPi.event_trigger(upperArm.get_interest())

#def onPeriodic():
#    global cnt
#    
#    if (cnt >= 100):
#        print(myo.rotRoll(), myo.rotPitch(), myo.rotYaw())
#        cnt = 0
#    else:
#        cnt += 1
        
#def onEMG(emg, moving):
#    print(emg, moving)
#    time.sleep(0.25)