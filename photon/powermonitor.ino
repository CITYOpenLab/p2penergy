#include "math.h"

// RMS voltage
const double vRMS = 120.0;      // Assumed or measured

// Parameters for measuring RMS current
const double offset = 1.65;     // Half the ADC max voltage
const int numTurns = 2000;      // 1:2000 transformer turns
const int rBurden = 100;        // Burden resistor value
const int numSamples = 1000;    // Number of samples before calculating RMS

void setup() {
    
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
    Particle.publish("RMS Current", String(iRMS));
    Particle.publish("RMS Voltage", String(vRMS));
    Particle.publish("Apparent Power", String(apparentPower));

    delay(4000);
}