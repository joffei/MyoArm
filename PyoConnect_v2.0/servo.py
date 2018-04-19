#servo.py
# Author: Jesse Offei-Nkansah
# Date: 4.10.2018
# Creates a servo class for controlling servos on GPIO

class Servo:
    """This class defines a servo object referenced by its GPIO location"""

    __gpio = None
    __pulse = None
    __maxPulse = None
    __minPulse = None
    __pwInc = None

    def __init__(self, gpio=2, pulse=1500, maxPulse=1850, minPulse=1080, pwInc=15):
        if (not self.set_gpio(gpio)):
            print("Setting to gpio 2")
            self.__gpio = 2

        if (not self.set_minPulse(minPulse)):
            print("Setting to 1080")
            self.__minPulse = 1080

        if (not self.set_maxPulse(maxPulse)):
            print("Setting to 1850")
            self.__maxPulse = 1850

        if(not self.set_pulse(pulse)):
            print("Setting to 1500")
            self.__pulse = 1500

        if(not self.set_pwInc(pwInc)):
            print("Setting to 15")
            self.__pwInc = 15

    def get_gpio(self):
        return self.__gpio

    def set_gpio(self, gpio):
        if (gpio >= 2) and (gpio <= 27):
            self.__gpio = gpio
            return True
        else:
            print("GPIO cannot be set to " + gpio + ".")
            return False

    def get_minPulse(self):
        return self.__minPulse

    def set_minPulse(self, minPulse):
        if (minPulse >= 1000) and (minPulse < 2000):
            self.__minPulse = minPulse
            return True
        else:
            print("Minimim Pulse cannot be set to " + minPulse + ".")
            return False

    def get_maxPulse(self):
        return self.__maxPulse

    def set_maxPulse(self, maxPulse):
        if (maxPulse > self.__minPulse) and (maxPulse <= 2000):
            self.__maxPulse = maxPulse
            return True
        else:
            print("Maximim Pulse cannot be set to " + maxPulse + ".")
            return False

    def get_pulse(self):
        return self.__pulse

    def set_pulse(self, pulse):
        if (pulse >= self.__minPulse) and (pulse <= self.__maxPulse):
            self.__pulse = pulse
            return True
        else:
            print("Pulse cannot be set to " + pulse + ".")
            return False

    def get_pwInc(self):
        return self.__pwInc

    def set_pwInc(self, pwInc):
        if (abs(pwInc) <= self.__maxPulse - self.__minPulse) and (pwInc != 0):
            self.__pwInc = pwInc
            return True
        else:
            print("Pulse Increment cannot be set to " + pwInc + ".")
            return False

    def increment(self):
        """'increment' function adds the value of pwInc to pulse"""
        if(self.__pulse + self.__pwInc <= self.__maxPulse):
            self.__pulse += self.__pwInc
            return True
        else:
            return False

    def decrement(self):
        """'decrement' function subtracts the value of pwInc from pulse"""
        if (self.__pulse - self.__pwInc >= self.__maxPulse):
            self.__pulse -= self.__pwInc
            return True
        else:
            return False

    def servoLeft(self):
        """'servoLeft' function increases the value of pulse by pwInc, effectively turning the servo to the left.  This does not pulse the servo.  A call to 'pi.set_servo_pulsewidth()' must be made."""
        if(self.__pwInc < 0):
            self.__pulse += (self.__pwInc * -1)
        else:
            self.__pulse += self.__pwInc

    def servoRight(self):
        """'servoRight' function decreases the value of pulse by pwInc, effectively turning the servo to the right.  This does not pulse the servo.  A call to 'pi.set_servo_pulsewidth()' must be made."""
        if (self.__pwInc > 0):
            self.__pulse += (self.__pwInc * -1)
        else:
            self.__pulse += self.__pwInc

    def __eq__(self, other):
        if(self.__gpio == other.__gpio) and (self.__pulse == other.__pulse) and (self.__maxPulse == other.__maxPulse) and (self.__minPulse == other.__minPulse) and (self.__pwInc == other.__pwInc):
            return True
        else:
            return False

    def __ne__(self, other):
        if (not self.__eq__(other)):
            return True
        else:
            return False


