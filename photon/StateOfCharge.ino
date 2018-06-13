
// This #include statement was automatically added by the Particle IDE.
#include <PowerShield.h>
#include <MQTT.h>
#include "math.h"
#include "PowerShield/PowerShield.h"

PowerShield batteryMonitor;

double cellVoltage;
double stateOfCharge;

// RMS voltage
const double vRMS = 120.0;      // Assumed or measured

// Parameters for measuring RMS current
const double offset = 1.65;     // Half the ADC max voltage
const int numTurns = 2000;      // 1:2000 transformer turns
const int rBurden = 100;        // Burden resistor value
const int numSamples = 1000;    // Number of samples before calculating RMS

void callback(char* topic, byte* payload, unsigned int length);
MQTT client("broker.hivemq.com", 1883, callback);

// recieve message
void callback(char* topic, byte* payload, unsigned int length) 
{
    char p[length + 1];
    memcpy(p, payload, length);
    p[length] = NULL;
    
    if (!strcmp(p, "RED"))
    {
        RGB.color(255, 0, 0);
    }
    else if (!strcmp(p, "GREEN"))
    {
        RGB.color(0, 255, 0);
    }
    else if (!strcmp(p, "BLUE"))
    {
        RGB.color(0, 0, 255);
    }
    else
    {
        RGB.color(255, 255, 255);
    }
    delay(1000);
}


void setup() {
    
    Serial.begin(9600); 
    // This essentially starts the I2C bus
    batteryMonitor.begin(); 
    // This sets up the fuel gauge
    batteryMonitor.quickStart();
    // Wait for it to settle down
    delay(500);
    Particle.variable("V", cellVoltage);
    Particle.variable("SoC", stateOfCharge);

}

void loop() {
    
    // Read the volatge of the  LiPo
    cellVoltage = batteryMonitor.getVCell();
    // Read the State of Charge of the LiPo
    stateOfCharge = batteryMonitor.getSoC();
    
    // Send the Voltage and SoC readings over serial
    //Serial.println(cellVoltage);
    //Serial.println(stateOfCharge);
    //Particle.publish("P2P_Voltage", String(cellVoltage));
    Particle.publish("P2P_State_of_Charge", String(stateOfCharge));
    
    // publish via mqtt
    //client.publish("p2penergy/photon/events", String(cellVoltage));
    client.publish("p2penergy/photon/events", String(stateOfCharge));
    
    delay(5000);
    
    if (client.isConnected()) {
        client.loop();
    }

}
