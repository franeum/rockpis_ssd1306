#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/uart.h"
#include "driver/gpio.h"
#include "sdkconfig.h"
#include <time.h>
#include <stdlib.h>
#include <stdbool.h>
#include "driver/adc.h"

typedef struct responsive {
    uint8_t     pin;
    uint32_t    analogResolution;// = 1024;
    float       snapMultiplier;
    bool        sleepEnable;
    float       activityThreshold;// = 4.0;
    bool        edgeSnapEnable;// = true;

    float       smoothValue;
    unsigned    long lastActivityMS;
    float       errorEMA;// = 0.0;
    bool        sleeping;// = false;

    int         rawValue;
    uint32_t    responsiveValue;
    uint32_t    prevResponsiveValue;
    bool        responsiveValueHasChanged;
} Responsive;


void begin(Responsive * resp, uint8_t pin, bool sleepEnable, float snapMultiplier); // = 0.01);  // use with default constructor to initialize 
uint32_t getValue(Responsive * resp); // { return responsiveValue; } // get the responsive value from last update
uint32_t getRawValue(Responsive * resp);// { return rawValue; } // get the raw analogRead() value from last update
bool hasChanged(Responsive * resp);// { return responsiveValueHasChanged; } // returns true if the responsive value has changed during the last update
bool isSleeping(Responsive * resp);// { return sleeping; } // returns true if the algorithm is currently in sleeping mode
//void update(); // updates the value by performing an analogRead() and calculating a responsive value based off it
void update(Responsive * resp, int rawValueRead); // updates the value accepting a value and calculating a responsive value based off it

void setSnapMultiplier(Responsive * resp, float newMultiplier);
void enableSleep(Responsive * resp);// { sleepEnable = true; }
void disableSleep(Responsive * resp);// { sleepEnable = false; }
void enableEdgeSnap(Responsive * resp);// { edgeSnapEnable = true; }
// edge snap ensures that values at the edges of the spectrum (0 and 1023) can be easily reached when sleep is enabled
void disableEdgeSnap(Responsive * resp);// { edgeSnapEnable = false; }
void setActivityThreshold(Responsive * resp, float newThreshold);// { activityThreshold = newThreshold; }
// the amount of movement that must take place to register as activity and start moving the output value. Defaults to 4.0
void setAnalogResolution(Responsive * resp, int resolution);// { analogResolution = resolution; }
// if your ADC is something other than 10bit (1024), set that here
uint32_t getResponsiveValue(Responsive * resp);
float snapCurve(float x);