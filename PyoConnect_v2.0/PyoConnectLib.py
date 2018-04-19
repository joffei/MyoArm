# uncompyle6 version 3.1.3
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.5.4 (v3.5.4:3f56838, Aug  8 2017, 02:17:05) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: PyoConnectLib.py
# Compiled at: 2015-08-05 09:17:41
"""
        PyoConnect v0.1
        
        Author:
          Fernando Cosentino - fbcosentino@yahoo.com.br
          
        Official source:
          http://www.fernandocosentino.net/pyoconnect
          
        Based on the work of dzhu: https://github.com/dzhu/myo-raw
        
        License:
                Use at will, modify at will. Always keep my name in this file as original author. And that's it.
        
        Steps required (in a clean debian installation) to use this library:
                // permission to ttyACM0 - must restart linux user after this
                sudo usermod -a -G dialout $USER

                // dependencies
                apt-get install python-pip
                pip install pySerial --upgrade
                pip install enum34
                pip install PyUserInput
                apt-get install python-Xlib

                // now reboot   
"""
from __future__ import print_function
import sys, time
from subprocess import Popen, PIPE
import re, math
try:
    from pymouse import PyMouse
    pmouse = PyMouse()
except:
    print('PyMouse error: No mouse support')
    pmouse = None

try:
    from pykeyboard import PyKeyboard
    pkeyboard = PyKeyboard()
except:
    print('PyKeyboard error: No keyboard support')
    pkeyboard = None

from common import *
from myo_raw import MyoRaw, Pose, Arm, XDirection

class Myo(MyoRaw):

    def __init__(self, cls, tty=None):
        self.locked = True
        self.use_lock = True
        self.timed = True
        self.lock_time = 1.0
        self.time_to_lock = self.lock_time
        self.last_pose = -1
        self.last_tick = 0
        self.current_box = 0
        self.last_box = 0
        self.box_factor = 0.25
        self.current_arm = 0
        self.current_xdir = 0
        self.current_gyro = None
        self.current_accel = None
        self.current_roll = 0
        self.current_pitch = 0
        self.current_yaw = 0
        self.center_roll = 0
        self.center_pitch = 0
        self.center_yaw = 0
        self.first_rot = 0
        self.current_rot_roll = 0
        self.current_rot_pitch = 0
        self.current_rot_yaw = 0
        self.mov_history = ''
        self.gest_history = ''
        self.act_history = ''
        if pmouse != None:
            self.x_dim, self.y_dim = pmouse.screen_size()
            self.mx = self.x_dim / 2
            self.my = self.y_dim / 2
        self.centered = 0
        MyoRaw.__init__(self, tty)
        self.add_emg_handler(self.emg_handler)
        self.add_arm_handler(self.arm_handler)
        self.add_imu_handler(self.imu_handler)
        self.add_pose_handler(self.pose_handler)
        self.onEMG = None
        self.onPoseEdge = None
        self.onPoseEdgeList = []
        self.onLock = None
        self.onLockList = []
        self.onUnlock = None
        self.onUnlockList = []
        self.onPeriodic = None
        self.onPeriodicList = []
        self.onWear = None
        self.onWearList = []
        self.onUnwear = None
        self.onUnwearList = []
        self.onBoxChange = None
        self.onBoxChangeList = []
        return

    def check_myo_around(self):
        self.bt.end_scan()
        self.bt.disconnect(0)
        self.bt.disconnect(1)
        self.bt.disconnect(2)
        self.bt.discover()
        p = self.bt.recv_packet(1)
        try:
            pl = p.payload
        except:
            pl = ''

        if pl.endswith('\x06BH\x12J\x7f,HG\x04\x01\x00\x06'):
            self.bt.end_scan()
            return True
        return False

    def tick(self):
        now = time.time()
        if now - self.last_tick >= 0.01:
            if self.onPeriodic != None:
                self.onPeriodic()
            for h in self.onPeriodicList:
                h()

            if self.use_lock and self.locked == False and self.timed:
                if self.time_to_lock <= 0:
                    print('Locked')
                    self.locked = True
                    self.vibrate(1)
                    self.time_to_lock = self.lock_time
                    if self.onLock != None:
                        self.onLock()
                    for h in self.onLockList:
                        h()

                else:
                    self.time_to_lock -= 0.01
            self.last_tick = now
        return

    def clear_handle_lists(self):
        self.onPoseEdgeList = []
        self.onLockList = []
        self.onUnlockList = []
        self.onPeriodicList = []
        self.onWearList = []
        self.onUnwearList = []
        self.onBoxChangeList = []
        self.emg_handlers = []

    def Add_onPoseEdge(self, h):
        self.onPoseEdgeList.append(h)

    def Add_onLock(self, h):
        self.onLockList.append(h)

    def Add_onUnlock(self, h):
        self.onUnlockList.append(h)

    def Add_onPeriodic(self, h):
        self.onPeriodicList.append(h)

    def Add_onWear(self, h):
        self.onWearList.append(h)

    def Add_onUnwear(self, h):
        self.onUnwearList.append(h)

    def Add_onBoxChange(self, h):
        self.onBoxChangeList.append(h)

    def emg_handler(self, emg, moving):
        if self.onEMG != None:
            self.onEMG(emg, moving)
        return

    def arm_handler(self, arm, xdir):
        if arm == Arm(0):
            self.current_arm = 'unknown'
        else:
            if arm == Arm(1):
                self.current_arm = 'right'
            else:
                if arm == Arm(2):
                    self.current_arm = 'left'
        if xdir == XDirection(0):
            self.current_xdir = 'unknown'
        else:
            if xdir == XDirection(1):
                self.current_xdir = 'towardWrist'
            else:
                if xdir == XDirection(2):
                    self.current_xdir = 'towardElbow'
        if Arm(arm) == 0:
            if self.onUnwear != None:
                self.onUnwear()
            for h in self.onUnwearList:
                h()

        else:
            if self.onWear != None:
                self.onWear(self.current_arm, self.current_xdir)
            for h in self.onWearList:
                h(self.current_arm, self.current_xdir)

        return

    def imu_handler(self, quat, acc, gyro):
        q0, q1, q2, q3 = quat
        q0 = q0 / 16384.0
        q1 = q1 / 16384.0
        q2 = q2 / 16384.0
        q3 = q3 / 16384.0
        self.current_roll = math.atan2(2.0 * (q0 * q1 + q2 * q3), 1.0 - 2.0 * (q1 * q1 + q2 * q2))
        self.current_pitch = -math.asin(max(-1.0, min(1.0, 2.0 * (q0 * q2 - q3 * q1))))
        self.current_yaw = -math.atan2(2.0 * (q0 * q3 + q1 * q2), 1.0 - 2.0 * (q2 * q2 + q3 * q3))
        self.current_rot_roll = self.angle_dif(self.current_roll, self.center_roll)
        self.current_rot_yaw = self.angle_dif(self.current_yaw, self.center_yaw)
        self.current_rot_pitch = self.angle_dif(self.current_pitch, self.center_pitch)
        g0, g1, g2 = gyro
        g0 = g0 / 16.0
        g1 = g1 / 16.0
        g2 = g2 / 16.0
        self.current_gyro = (g0, g1, g2)
        ac0, ac1, ac2 = acc
        ac0 = ac0 / 2048.0
        ac1 = ac1 / 2048.0
        ac2 = ac2 / 2048.0
        self.current_accel = (ac0, ac1, ac2)
        if self.first_rot == 0:
            self.rotSetCenter()
            self.first_rot = 1
        self.current_box = self.getBox()
        if self.current_box != self.last_box:
            self.mov_history = str(self.mov_history[-100:]) + str(self.current_box)
            self.act_history = str(self.act_history[-100:]) + str(self.current_box)
            if self.onBoxChange != None:
                self.onBoxChange(self.last_box, 'off')
                self.onBoxChange(self.current_box, 'on')
            for h in self.onBoxChangeList:
                h(self.last_box, 'off')
                h(self.current_box, 'on')

            self.last_box = self.current_box
        return

    def pose_handler(self, p):
        if p == Pose(0):
            pn = 0
        else:
            if p == Pose(1):
                pn = 1
            else:
                if p == Pose(2):
                    pn = 2
                else:
                    if p == Pose(3):
                        pn = 3
                    else:
                        if p == Pose(4):
                            pn = 4
                        else:
                            if p == Pose(5):
                                pn = 5
                            else:
                                pn = 6
        if pn != self.last_pose:
            self.gest_history = str(self.gest_history[-100:]) + str(self.PoseToChar(pn))
            self.act_history = str(self.act_history[-100:]) + str(self.PoseToChar(pn))
            if self.locked == False:
                self.time_to_lock = self.lock_time
                if self.last_pose > -1:
                    if self.onPoseEdge != None:
                        self.onPoseEdge(self.PoseToStr(self.last_pose), 'off')
                    for h in self.onPoseEdgeList:
                        h(self.PoseToStr(self.last_pose), 'off')

                if self.onPoseEdge != None:
                    self.onPoseEdge(self.PoseToStr(pn), 'on')
                for h in self.onPoseEdgeList:
                    h(self.PoseToStr(pn), 'on')

            self.last_pose = pn
        if pn == 5 and self.locked and self.use_lock:
            self.locked = False
            self.vibrate(1)
            print('unlock')
            if self.onUnlock != None:
                self.onUnlock()
            for h in self.onUnlockList:
                h()

        return

    def getArm(self):
        return self.current_arm

    def getXDirection(self):
        return self.current_xdir

    def getGyro(self):
        return self.current_gyro

    def getAccel(self):
        return self.current_accel

    def getTimeMilliseconds(self):
        return round(time.time() * 1000)

    def getRoll(self):
        return self.current_roll

    def getPitch(self):
        return self.current_pitch

    def getYaw(self):
        return self.current_yaw

    def setLockingPolicy(self, policy):
        if policy == 'none':
            self.use_lock = False
        else:
            if policy == 'standard':
                self.use_lock = True

    def lock(self):
        self.locked = True
        self.vibrate(1)
        if self.onLock != None:
            self.onLock()
        for h in self.onLockList:
            h()

        return

    def unlock(self, unlock_type):
        if unlock_type == 'timed':
            self.vibrate(1)
            self.locked = False
            self.timed = True
        if unlock_type == 'hold':
            self.vibrate(1)
            self.locked = False
            self.timed = False

    def isUnlocked(self):
        if self.locked:
            return False
        return True

    def notifyUserAction(self):
        self.vibrate(1)

    def keyboard(self, kkey, kedge, kmod):
        if pkeyboard != None:
            tkey = kkey
            if tkey == 'left_arrow':
                tkey = pkeyboard.left_key
            if tkey == 'right_arrow':
                tkey = pkeyboard.right_key
            if tkey == 'up_arrow':
                tkey = pkeyboard.up_key
            if tkey == 'down_arrow':
                tkey = pkeyboard.down_key
            if tkey == 'space':
                pass
            if tkey == 'return':
                tkey = pkeyboard.return_key
            if tkey == 'escape':
                tkey = pkeyboard.escape_key
            if kmod == 'left_shift':
                pkeyboard.press_key(pkeyboard.shift_l_key)
            if kmod == 'right_shift':
                pkeyboard.press_key(pkeyboard.shift_r_key)
            if kmod == 'left_control':
                pkeyboard.press_key(pkeyboard.control_l_key)
            if kmod == 'right_control':
                pkeyboard.press_key(pkeyboard.control_r_key)
            if kmod == 'left_alt':
                pkeyboard.press_key(pkeyboard.alt_l_key)
            if kmod == 'right_alt':
                pkeyboard.press_key(pkeyboard.alt_r_key)
            if kmod == 'left_win':
                pkeyboard.press_key(pkeyboard.super_l_key)
            if kmod == 'right_win':
                pkeyboard.press_key(pkeyboard.super_r_key)
            if kedge == 'down':
                pkeyboard.press_key(tkey)
            else:
                if kedge == 'up':
                    pkeyboard.release_key(tkey)
                else:
                    if kedge == 'press':
                        pkeyboard.tap_key(tkey)
            if kmod == 'left_shift':
                pkeyboard.release_key(pkeyboard.shift_l_key)
            if kmod == 'right_shift':
                pkeyboard.release_key(pkeyboard.shift_r_key)
            if kmod == 'left_control':
                pkeyboard.release_key(pkeyboard.control_l_key)
            if kmod == 'right_control':
                pkeyboard.release_key(pkeyboard.control_r_key)
            if kmod == 'left_alt':
                pkeyboard.release_key(pkeyboard.alt_l_key)
            if kmod == 'right_alt':
                pkeyboard.release_key(pkeyboard.alt_r_key)
            if kmod == 'left_win':
                pkeyboard.release_key(pkeyboard.super_l_key)
            if kmod == 'right_win':
                pkeyboard.release_key(pkeyboard.super_r_key)
        return

    def centerMousePosition(self):
        if pmouse != None:
            x_dim, y_dim = pmouse.screen_size()
            pmouse.move(x_dim / 2, y_dim / 2)
        return

    def mouse(self, button, edge, mod):
        if pmouse != None:
            mpos = pmouse.position()
            if button == 'left':
                mbut = 1
            else:
                if button == 'right':
                    mbut = 2
                else:
                    if button == 'center':
                        mbut = 3
                    else:
                        mbut = 1
            if edge == 'down':
                pmouse.press(mpos[0], mpos[1], mbut)
            elif edge == 'up':
                pmouse.release(mpos[0], mpos[1], mbut)
            elif edge == 'click':
                pmouse.click(mpos[0], mpos[1], mbut)
        return

    def getPose(self):
        return self.PoseToStr(self.last_pose)

    def getPoseSide(self):
        if self.last_pose == 2 and self.current_arm == 'right' or self.last_pose == 3 and self.current_arm == 'left':
            return 'waveLeft'
        if self.last_pose == 3 and self.current_arm == 'right' or self.last_pose == 2 and self.current_arm == 'left':
            return 'waveRight'
        return self.PoseToStr(self.last_pose)

    def isLocked(self):
        return self.locked

    def mouseMove(self, x, y):
        if pmouse != None:
            pmouse.move(x, y)
        return

    def title_contains(self, text):
        window_str = self.get_active_window_title()
        if window_str.find(text) > -1:
            return True
        return False

    def class_contains(self, text):
        window_str = self.get_active_window_class()
        if window_str.find(text) > -1:
            return True
        return False

    def rotSetCenter(self):
        self.center_roll = self.current_roll
        self.center_pitch = self.current_pitch
        self.center_yaw = self.current_yaw

    def rotRoll(self):
        return self.current_rot_roll

    def rotPitch(self):
        return self.current_rot_pitch

    def rotYaw(self):
        return self.angle_dif(self.current_yaw, self.center_yaw)

    def getBox(self):
        if self.current_rot_pitch > self.box_factor:
            if self.current_rot_yaw > self.box_factor:
                return 2
            if self.current_rot_yaw < -self.box_factor:
                return 8
            return 1
        else:
            if self.current_rot_pitch < -self.box_factor:
                if self.current_rot_yaw > self.box_factor:
                    return 4
                if self.current_rot_yaw < -self.box_factor:
                    return 6
                return 5
            else:
                if self.current_rot_yaw > self.box_factor:
                    return 3
                if self.current_rot_yaw < -self.box_factor:
                    return 7
                return 0

    def getHBox(self):
        if self.current_rot_yaw > self.box_factor:
            return 1
        if self.current_rot_yaw < -self.box_factor:
            return -1
        return 0

    def getVBox(self):
        if self.current_rot_pitch > self.box_factor:
            return 1
        if self.current_rot_pitch < -self.box_factor:
            return -1
        return 0

    def clearHistory(self):
        self.mov_history = ''
        self.gest_history = ''
        self.act_history = ''

    def getLastMovements(self, num):
        if num >= 0:
            return self.mov_history[-num:]
        return self.mov_history

    def getLastGestures(self, num):
        if num >= 0:
            return self.gest_history[-num:]
        return self.gest_history

    def getLastActions(self, num):
        if num >= 0:
            return self.act_history[-num:]
        return self.act_history

    def PoseToStr(self, posenum):
        if posenum == 0:
            return 'rest'
        if posenum == 1:
            return 'fist'
        if posenum == 2:
            return 'waveIn'
        if posenum == 3:
            return 'waveOut'
        if posenum == 4:
            return 'fingersSpread'
        if posenum == 5:
            return 'doubleTap'
        return 'unknown'

    def PoseToChar(self, posenum):
        if posenum == 0:
            return 'R'
        if posenum == 1:
            return 'F'
        if posenum == 2:
            return 'I'
        if posenum == 3:
            return 'O'
        if posenum == 4:
            return 'S'
        if posenum == 5:
            return 'D'
        return 'U'

    def limit_angle(self, angle):
        if angle > math.pi:
            return angle - 2.0 * math.pi
        if angle < -2.0 * math.pi:
            return angle + 2.0 * math.pi
        return angle

    def angle_dif(self, angle, ref):
        if ref >= 0:
            if angle >= 0:
                return self.limit_angle(angle - ref)
            if angle >= ref - math.pi:
                return self.limit_angle(angle - ref)
            return self.limit_angle(angle + 2.0 * math.pi - ref)
        else:
            if angle <= 0:
                return self.limit_angle(angle - ref)
            if angle <= ref + math.pi:
                return self.limit_angle(angle - ref)
            return self.limit_angle(angle - 2.0 * math.pi - ref)

    def get_active_window_title(self):
        try:
            root = Popen(['xprop', '-root', '_NET_ACTIVE_WINDOW'], stdout=PIPE)
            for line in root.stdout:
                mw = re.search('^_NET_ACTIVE_WINDOW.* ([\\w]+)$', line)
                if mw != None:
                    id_ = mw.group(1)
                    id_w = Popen(['xprop', '-id', id_, 'WM_NAME'], stdout=PIPE)
                    break

            if id_w != None:
                for line in id_w.stdout:
                    match = re.match('WM_NAME\\(\\w+\\) = (?P<name>.+)$', line)
                    if match != None:
                        return match.group('name')

            return ''
        except:
            return ''

        return

    def get_active_window_class(self):
        try:
            root = Popen(['xprop', '-root', '_NET_ACTIVE_WINDOW'], stdout=PIPE)
            for line in root.stdout:
                mw = re.search('^_NET_ACTIVE_WINDOW.* ([\\w]+)$', line)
                if mw != None:
                    id_ = mw.group(1)
                    id_w = Popen(['xprop', '-id', id_, 'WM_CLASS'], stdout=PIPE)
                    break

            if id_w != None:
                for line in id_w.stdout:
                    match = re.match('WM_CLASS\\(\\w+\\) = (?P<name>.+)$', line)
                    if match != None:
                        return match.group('name')

            return ''
        except:
            return ''

        return


if __name__ == '__main__':
    m = Myo(sys.argv[1] if len(sys.argv) >= 2 else None)
    m.connect()
    while True:
        m.run()