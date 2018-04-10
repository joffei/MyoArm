//Servo Check
//Jesse Offei-Nkansah
#include <iostream>
#include <string>
#include <pigpio.h>
#include <thread>
#include <chrono>
#include <vector>

#define BASE_SERVO 14
#define LOWER_ARM_SERVO 15
#define UPPER_ARM_SERVO 18
#define ROLL_SERVO 17
#define PITCH_SERVO 27
#define YAW_SERVO 22

#define SEC 1000000

void servoForward(void* servo);
void servoReverse(void* servo);

gpioTimerFuncEx_t function = servoForward;

int main(int argc, char *argv[]){
	
	std::vector<int> servoArr = {BASE_SERVO, LOWER_ARM_SERVO, UPPER_ARM_SERVO, ROLL_SERVO, PITCH_SERVO, YAW_SERVO};

	std::cout << "Press ENTER to begin";
	std::cin.get();

	if(gpioInitialise() >= 0){
		gpioSetMode(UPPER_ARM_SERVO, PI_OUTPUT);
		
		gpioSetTimerFuncEx(0, 1000, function, (void*)UPPER_ARM_SERVO);
		while(1){std::this_thread::sleep_for(std::chrono::milliseconds(1000));}
	}

	gpioTerminate();
	
	return 0;
}

void servoForward(void* servo){
	
	int pulse = 1500;

	do{
		pulse += 1;
		//std::cout << "\rnumber: " << pulse;
		gpioServo(static_cast<int>(reinterpret_cast<std::uintptr_t>(servo)), pulse);
	}while(gpioGetServoPulsewidth(static_cast<int>(reinterpret_cast<std::uintptr_t>(servo))) < 2495);
	

}


void servoReverse(void* servo){


	int pulse = 1500;

	do{
		pulse -= 1;
		std::cout << "\rnumber: " << pulse;
		gpioServo(static_cast<int>(reinterpret_cast<std::uintptr_t>(servo)), pulse);
	}while(gpioGetServoPulsewidth(static_cast<int>(reinterpret_cast<std::uintptr_t>(servo))) > 505);
}
