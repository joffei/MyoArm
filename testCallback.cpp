/*testCallback.cpp
 * Author: Jesse Offei-Nkansah
 * Date: 4.6.2018
 * Test the gpioSetTimerFunctionEx function in <gpio.h> library
 */

#include <iostream>
#include <string>
#include <pigpio.h>
#include <stdlib.h>
#include <thread>
#include <chrono>

void move(void* data);

struct servo{
	int gpio;
	int pw;
	int pwInc;
	int minPulse;
	int maxPulse;
	
	servo(int gpio_, int pw_, int pwInc_, int minPulse_, int maxPulse_){
		gpio = gpio_;
		pw = pw_;
		pwInc = pwInc_;
		minPulse = minPulse_;
		maxPulse = maxPulse_;
	}
};



int main(int argc, char **argv){
	
	servo base(14, 1010, 10, 1010, 1800);
	servo lowerArm(15, 1500, 15, 1010, 1800);
	servo upperArm(18, 1500, 15, 1010, 1800);
	servo wrist(17, 1010, 10, 1010, 1800);
	
	gpioTimerFuncEx_t func = move;
	
	if (gpioInitialise() < 0) return 1;
	
	gpioSetMode(base.gpio, PI_OUTPUT);
	gpioSetMode(lowerArm.gpio, PI_OUTPUT);
	gpioSetMode(upperArm.gpio, PI_OUTPUT);
	gpioSetMode(wrist.gpio, PI_OUTPUT);
	
	gpioServo(lowerArm.gpio, 1500);
	gpioServo(upperArm.gpio, 1500);
	gpioDelay(5000000);
	
	gpioSetTimerFuncEx(1, 100, func, &upperArm);
	gpioSetTimerFuncEx(0, 100, func, &lowerArm);
	
	std::cin.get();
	func = nullptr;
	//std::this_thread::sleep_for(std::chrono::milliseconds(500));
	
	return 0;
}


void move(void* data){
	
	servo* activeServo= (static_cast<servo *>(data));
	
	activeServo->pw += activeServo->pwInc;
	//upperArm.pw += upperArm.pwInc;
	
	if(activeServo->pw >= activeServo->maxPulse ||
	activeServo->pw <= activeServo->minPulse){
		activeServo->pwInc = - activeServo->pwInc;
		activeServo->pw += 2 * activeServo->pwInc;
	}
	
	/*if(upperArm.pw > upperArm.maxPulse || upperArm.pw < upperArm.minPulse){
		upperArm.pwInc = - upperArm.pwInc;
		upperArm.pw += upperArm.pwInc*/
	
	gpioServo(activeServo->gpio, activeServo->pw);
	//gpioServo(upperArm.gpio, upperArm.pw);
}
