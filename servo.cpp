/*servo.cpp
 * Author: Jesse Offei-Nkansah
 * Date: 4.8.2018
 * Implementation file for Servo class
 */

#include <iostream>
#include <pigpio.h>
#include "Servo.h"

Servo::Servo(int gpio_, int minPulse_, int maxPulse_, int pw_, int pwInc_){
	if (gpio_ >= 2 && gpio_ <= 27){
		gpio = gpio_;
	}else{
		gpio = -1;
	}
	
	if (minPulse_ >= 1000 && minPulse_ < 2000){
		minPulse = minPulse_;
	}else{
		minPulse = 1010;
	}
	
	if (maxPulse_ > minPulse && maxPulse_ <= 2000){
		maxPulse = maxPulse_;
	}else{
		maxPulse = 1800;
	}
	
	if(pw_ >= minPulse && pw_ <= maxPulse){
		pw = pw_;
	}else{
		pw = 1500;	
	}
	
	if(pwInc_ <= maxPulse - minPulse){
		pwInc = pwInc_;
	}else{
		pwInc = 15;
	}
}

Servo::Servo(int gpio_, int pw_, int pwInc_)
	: minPulse(1010), maxPulse(1800)
{
	if (gpio_ >= 2 && gpio_ <= 27){
		gpio = gpio_;
	}else{
		gpio = -1;
	}
	
	if(pw_ >= minPulse && pw_ <= maxPulse){
		pw = pw_;
	}else{
		pw = 1500;	
	}
	
	if(pwInc_ <= (maxPulse - minPulse)/2){
		pwInc = pwInc_;
	}else{
		pwInc = 15;
	}
}

Servo::Servo(int gpio_)
	: minPulse(1010), maxPulse(1800), pw(1500), pwInc(15)
{
	if (gpio_ >= 2 && gpio_ <= 27){
		gpio = gpio_;
	}else{
		gpio = -1;
	}
}


void Servo::setGPIO(int gpio_){
	if (gpio_ >= 2 && gpio_ <= 27){
		gpio = gpio_;
	}else{
		std::cerr << "Invalid GPIO.  No Change." << std::endl;
	}
}

int Servo::getGPIO(){
	return gpio;
}

void Servo::setMinPulse(int minPulse_){
	if (minPulse_ >= 1000 && minPulse_ < 2000){
		minPulse = minPulse_;
	}else{
		std::cerr << "Invalid Min Pulse.  No Change." << std::endl;
	}
}

int Servo::getMinPulse(){
	return minPulse;
}

void Servo::setMaxPulse(int maxPulse_){
	if (maxPulse_ > minPulse && maxPulse_ <= 2000){
		maxPulse = maxPulse_;
	}else{
		std::cerr << "Invallid Max Pulse. No Change." << std::endl;
	}
}

int Servo::getMaxPulse(){
	return maxPulse;
}

void Servo::setPulseWidth(int pw_){
	pw = pw_;
}

int Servo::getPulseWidth(){
	return pw;
}

void Servo::setIncrement(int pwInc_){
	pwInc = pwInc_;
}

int Servo::getIncrement(){
	return pwInc;
}

void Servo::pulse(){
	gpioServo(gpio, pw);
}

void Servo::increment(){
	pw += pwInc;
}

void Servo::decrement(){
	pw -= pwInc;
}

void Servo::servoLeft(){
	if(pwInc < 0){
		pw += (pwInc * -1);
	}else{
		pw += pwInc;
	}
}

void Servo::servoRight(){
	if(pwInc > 0){
		pw += (pwInc * -1);
	}else{
		pw += pwInc;
	}
}

Servo Servo::operator =(Servo& rhs){
	gpio = rhs.gpio;
	minPulse = rhs.minPulse;
	maxPulse = rhs.maxPulse;
	pw = rhs.pw;
	pwInc = rhs.pwInc;
}

bool Servo::operator ==(Servo& rhs){
	if(gpio == rhs.gpio && minPulse == rhs.minPulse &&
		maxPulse == rhs.maxPulse && pw == rhs.pw &&
		pwInc = rhs.pwInc){
		return true;
	}else{
		return false;
	}
}

bool Servo::operator !=(Servo& rhs){
	if(gpio == rhs.gpio && minPulse == rhs.minPulse &&
		maxPulse == rhs.maxPulse && pw == rhs.pw &&
		pwInc = rhs.pwInc){
		return false;
	}else{
		return true;
	}
}
