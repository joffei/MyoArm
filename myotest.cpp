/*myotest.cpp
 * Author: Jesse Offei-Nkansah
 * Date: 4.10.2018
 * Test functions to become familiar with the LinuxMyo libraries
 */
 
 #include "myolinux/myoclient.h"
#include "myolinux/serial.h"
#include <thread>
#include <chrono>

#include <cinttypes>

using namespace myolinux;

int main()
{
    myo::Client client(Serial{"/dev/ttyACM0", 115200});
    
    std::this_thread::sleep_for(std::chrono::milliseconds(1000));
    //myo::Address address = ;
    //myo::Client client(address);

    // Autoconnect to the first Myo device
    client.connect(/*"e5:3d:39:75:7b:7e"*/);
    if (!client.connected()) {
        return 1;
    }

    // Print device address
    print_address(client.address());

    // Read EMG and IMU
    client.setMode(myo::EmgMode::SendEmg, myo::ImuMode::SendEvents, myo::ClassifierMode::Enabled);
    
    // Read firmware version
    auto version = client.firmwareVersion();
    std::cout << version.major << "."
        << version.minor << "."
        << version.patch << "."
        << version.hardware_rev << std::endl;
        
    //auto info = client.info();
    //std::cout << static_cast<uint8_t>(info.active_classifier_type) << std::endl << std::endl;

    // Vibrate
    client.vibrate(myo::Vibration::Medium);

    // Read name
    auto name = client.deviceName();
    std::cout << name << std::endl;

    // Set sleep mode (otherwise the device auto disconnects after a while)
    client.setSleepMode(myo::SleepMode::NeverSleep);



    client.onEmg([](myo::EmgSample sample)
    {
        for (std::size_t i = 0; i < 8; i++) {
            std::cout << static_cast<int>(sample[i]);
            if (i != 7) {
                std::cout << ", ";
            }
        }
        std::cout << std::endl;
    });
    
    client.onImu([](myo::OrientationSample ori, myo::AccelerometerSample acc, myo::GyroscopeSample gyr)
    {
        std::cout << ori[0] << ", " << ori[1] << ", " << ori[2] << ", " <<  ori[3] << std::endl;
        std::cout << acc[0] << ", " << acc[1] << ", " << acc[2] << std::endl;
        std::cout << gyr[0] << ", " << gyr[1] << ", " << gyr[2] << std::endl;
        
        
    });

    for(int i=0; i < 5; ++i){
        
        
        //std::this_thread::sleep_for(std::chrono::milliseconds(1000));
        
        client.listen();
        
    }
    
    
    
    //auto info = client.info();
	//std::cout << info.active_classifier_type << std::endl;
	
	client.disconnect();
	
	return 0;

    
}
