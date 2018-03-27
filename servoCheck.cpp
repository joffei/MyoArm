//Jesse Offei-Nkansah
#include <iostream>
#include <string>
#include <pigpio.h>
#include <thread>
#include <vector>

#define BASE_SERVO 15
#define LOWER_ARM_SERVO 16
#define UPPER_ARM_SERVO 17
#define ROLL_SERVO 19
#define PITCH_SERVO 20
#define YAW_SERVO 21

#define SEC 1000000

void servoForward(int servo);
void servoReverse(int servo);

bool swap = false;

int main(int argc, char *argv[]){
	
	std::vector<int> servoArr = {BASE_SERVO, LOWER_ARM_SERVO, UPPER_ARM_SERVO, ROLL_SERVO, PITCH_SERVO, YAW_SERVO};

	std::cout << "Press ENTER to begin";
	std::cin.get();

	if(gpioInitialise() >= 0){
		for(int i=0; i < servoArr.size(); ++i){
			std::thread t(servoForward, servoArr[i]);
			std::cin.get();
			t.join();
			swap = true;
			std::thread u(servoReverse, servoArr[i]);
			cin.get();
			swap = true;
			u.join();
		}
	}

	gpioTerminate();
	
	return 0;
}

void servoForward(int servo){
	
	pulse = gpioGetServoPulseWidth(servo);

	while(!swap){
		pulse += 5;
		std::cout << "\rnumber: " << pulse;
		gpioServo(servo, pulse);
		gpioDelay(5 * SEC\100);
	}
}


void servoReverse(int servo){

	pulse = gpioGetServoPulseWidth(servo);

	while(!swap){
		pulse -= 5;
		std::cout << "\rnumber: " << pulse;
		gpioServo(servo, pulse);
		gpioDelay(5 * SEC\100);
	}
}
