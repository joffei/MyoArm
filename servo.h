/*servo.h
Jesse Offei-Nkansah
header file for functionality of servos
*/

#ifndef SERVO_H
#define SERVO_H

class Servo{
	
	private:
		int gpio;
		int minPulse;
		int maxPulse;
		int pw;
		int pwInc;
		
	public:
		Servo(int gpio_, minPulse_, int maxPulse_, int pw_, int pwInc_);
		Servo(int gpio_, int pw_, int pwInc_);
		Servo(int gpio_);
		
		~Servo();
		
		void setGPIO(int gpio_);
		int getGPIO();
		
		void setMinPulse(int minPulse_);
		int getMinPulse();
		
		void setMaxPulse(int maxPulse_);
		int getMaxPulse();
		
		void setPulseWidth(int pw_);
		int getPulseWidth();
		
		void setIncrement(int pwInc_);
		int getIncrement();
		
		void pulse()
		void increment();
		void decrement();
		void servoLeft();
		void servoRight();
		
		Servo operator=(const Servo& rhs);
		bool operator==(const Servo& rhs);
		bool operator!=(const Servo& rhs);
	
};

#endif
