# Double tap to unlock
# kept unlocked until lock explicitly called
def onUnlock():
    myo.unlock("hold")
    
def onPoseEdge(pose, edge):
    #print pose + " " + edge
    if(pose == 'fist') and (edge == 'on'):
        print "Fist on"
    elif(pose == 'fist') and (edge == 'off'):
        print "Fist off"
    elif(pose == 'waveIn') and (edge == 'on'):
        print "Wave In on"
    elif(pose == 'waveIn') and (edge == 'off'):
        print "Wave In off"
    elif(pose == 'waveOut') and (edge == 'on'):
        print "Wave Out on"
    elif(pose == 'waveOut') and (edge == 'off'):
        print "Wave Out off"
    elif(pose == 'fingersSpread') and (edge == 'on'):
        print "finger Spread on"
    elif(pose == 'fingersSpread') and (edge == 'off'):
        print "fingers Spread off"
    elif(pose == 'rest') and (edge == 'on'):
        print "rest on"
    elif(pose == 'rest') and (edge == 'off'):
        print "rest off"
    elif(pose == 'doubleTap') and (edge == 'on'):
        print "double Tap on"
    elif(pose == 'doubleTap') and (edge == 'off'):
        print "double Tap off"
    elif(pose == 'unknown') and (edge == 'on'):
        print "unknown on"
    elif(pose == 'unknown') and (edge == 'off'):
        print "unknown off"