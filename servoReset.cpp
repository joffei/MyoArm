/*Reset Servos to 50%*/

#include <iostream>
#include <stdlib.h>
#include <string>
#include <pigpio.h>

#define SERVO_PIN 15
#define CENTER_PULSE 1500

int main(int argc, char *argv[]){
	
	unsigned int pulse = 1010;

	while(pulse != 0){

	std::cout << "number between 1000 and 2000, 0 to exit: ";
	std::cin >> pulse;
	
	if(pulse > 2000){
		std::cout << "too high" << std::endl;
		pulse = 1010;
	}else if(pulse == 0){
		break;
	}else if (pulse < 1010){
		std::cout << "too low" << std::endl;
		pulse = 1010;
	}else{	
	if(gpioInitialise() >= 0){
		
		std::cout << "init OK" << std :: endl << gpioGetMode(SERVO_PIN) << std::endl;
		
		if(gpioGetMode(SERVO_PIN) != PI_OUTPUT){
			gpioSetMode(SERVO_PIN, PI_OUTPUT);
		}
		gpioSetPWMfrequency(SERVO_PIN, 50);
		gpioSetPWMrange(SERVO_PIN, 20000);
		
		gpioServo(SERVO_PIN, pulse);
		gpioDelay(1000000);
		
		/*while (gpioGetServoPulsewidth(SERVO_PIN) != CENTER_PULSE){
			gpioServo(SERVO_PIN, CENTER_PULSE);	//Center Servo
			gpioDelay(100);
		}*/
	}
	}
	}
	
	gpioTerminate();
	std::cout << "Terminated" << std::endl;
	
	return 0;
}
