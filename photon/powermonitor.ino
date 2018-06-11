#include <MQTT.h>
#include "math.h"

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

void setup() 
{
    RGB.control(true);
    
    // connect to the server(unique id by Time.now())
    client.connect("photon_" + String(Time.now()));
    
    // publish/subscribe
    if (client.isConnected()) 
    {
        client.publish("p2penergy/photon/events", "hello world");
        client.subscribe("p2penergy/photon/input");
    }
    
}

void loop() {
    
    int sample;
    double voltage;
    double iPrimary;
    double acc = 0;
    double iRMS;
    double apparentPower;
    
    // Take a number of samples and calculate RMS current
    for ( int i = 0; i < numSamples; i++ ) {
        
        // Read ADC, convert to voltage, remove offset
        sample = analogRead(A0);
        voltage = (sample * 3.3) / 4096;
        voltage = voltage - offset;
        
        // Calculate the sensed current
        iPrimary = (voltage / rBurden) * numTurns;
        
        // Square current and add to accumulator
        acc += pow(iPrimary, 2);
    }
    
    // Calculate RMS from accumulated values
    iRMS = sqrt(acc / numSamples);
    
    // Calculate apparent power and publish it
    apparentPower = vRMS * iRMS;
    Particle.publish("rms_current", String(iRMS));
    Particle.publish("rms_voltage", String(vRMS));
    Particle.publish("power", String(apparentPower));
    
    // publish via mqtt
    client.publish("p2penergy/photon/events", String(iRMS));
    client.publish("p2penergy/photon/events", String(vRMS));
    client.publish("p2penergy/photon/events", String(apparentPower));
    
    delay(4000);
    
    if (client.isConnected()) {
        client.loop();
    }
    
}