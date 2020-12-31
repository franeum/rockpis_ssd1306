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
#include "responsive.h"


#define DEBUG 0

void begin(Responsive * resp, uint8_t pin, bool sleepEnable, float snapMultiplier){
    //pinMode(pin, INPUT ); // ensure button pin is an input
    //digitalWrite(pin, LOW ); // ensure pullup is off on button pin
    
    resp->pin = pin;
    resp->sleepEnable = sleepEnable;
    setSnapMultiplier(resp, snapMultiplier);
}

/*
void update(Responsive * resp)
{
  uint32_t raw = analogRead(pin);
  update(resp, raw);
}
*/

void update(Responsive * resp, int rawValueRead)
{
  resp->rawValue = rawValueRead;
  resp->prevResponsiveValue = resp->responsiveValue;
  resp->responsiveValue = getResponsiveValue(resp);
  resp->responsiveValueHasChanged = resp->responsiveValue != resp->prevResponsiveValue;
}

uint32_t getResponsiveValue(Responsive * resp)
{
    // if sleep and edge snap are enabled and the new value is very close to an edge, drag it a little closer to the edges
    // This'll make it easier to pull the output values right to the extremes without sleeping,
    // and it'll make movements right near the edge appear larger, making it easier to wake up

    if(resp->sleepEnable && resp->edgeSnapEnable) {
        if(resp->rawValue < resp->activityThreshold) {
            resp->rawValue = (resp->rawValue * 2) - resp->activityThreshold;
        } else if(resp->rawValue > resp->analogResolution - resp->activityThreshold) {
            resp->rawValue = (resp->rawValue * 2) - resp->analogResolution + resp->activityThreshold;
        }
    }

#if DEBUG
    printf("resp->rawValue: %d\n", resp->rawValue);
#endif 
    // get difference between new input value and current smooth value
    uint32_t diff = abs(resp->rawValue - resp->smoothValue);

#if DEBUG
    printf("diff: %d\n", diff);
#endif
    // measure the difference between the new value and current value
    // and use another exponential moving average to work out what
    // the current margin of error is
    resp->errorEMA += ((resp->rawValue - resp->smoothValue) - resp->errorEMA) * 0.4;

#if DEBUG
    printf("errorEMA: %f\n", resp->errorEMA);
#endif 

    // if sleep has been enabled, sleep when the amount of error is below the activity threshold
    if(resp->sleepEnable) {
        // recalculate sleeping status
        resp->sleeping = abs(resp->errorEMA) < resp->activityThreshold;
    }

#if DEBUG
    printf("resp->sleeping: %d\n", resp->sleeping);
    // if we're allowed to sleep, and we're sleeping
    // then don't update responsiveValue this loop
    // just output the existing responsiveValue

    printf("primo resp->smoothValue: %d\n", (uint32_t)resp->smoothValue);
#endif 

    if(resp->sleepEnable && resp->sleeping) {
        return (uint32_t)resp->smoothValue;
    }

    // use a 'snap curve' function, where we pass in the diff (x) and get back a number from 0-1.
    // We want small values of x to result in an output close to zero, so when the smooth value is close to the input value
    // it'll smooth out noise aggressively by responding slowly to sudden changes.
    // We want a small increase in x to result in a much higher output value, so medium and large movements are snappy and responsive,
    // and aren't made sluggish by unnecessarily filtering out noise. A hyperbola (f(x) = 1/x) curve is used.
    // First x has an offset of 1 applied, so x = 0 now results in a value of 1 from the hyperbola function.
    // High values of x tend toward 0, but we want an output that begins at 0 and tends toward 1, so 1-y flips this up the right way.
    // Finally the result is multiplied by 2 and capped at a maximum of one, which means that at a certain point all larger movements are maximally snappy

    // then multiply the input by SNAP_MULTIPLER so input values fit the snap curve better.
    float snap = snapCurve(diff * resp->snapMultiplier);

    // when sleep is enabled, the emphasis is stopping on a responsiveValue quickly, and it's less about easing into position.
    // If sleep is enabled, add a small amount to snap so it'll tend to snap into a more accurate position before sleeping starts.
    if(resp->sleepEnable) {
        snap *= 0.5 + 0.5;
    }

#if DEBUG
    printf("resp->snapMultiplier: %f\n", resp->snapMultiplier);
    printf("snap: %f\n", snap);
#endif 

    // calculate the exponential moving average based on the snap
    resp->smoothValue += (resp->rawValue - resp->smoothValue) * snap;

    // ensure output is in bounds
    if(resp->smoothValue < 0.0) {
        resp->smoothValue = 0.0;
    } else if(resp->smoothValue > resp->analogResolution - 1) {
        resp->smoothValue = resp->analogResolution - 1;
    }
#if DEBUG
    printf("secondo resp->smoothValue: %d\n", (uint32_t)resp->smoothValue);
#endif 

    // expected output is an integer
    return (uint32_t)resp->smoothValue;
}

float snapCurve(float x)
{
    float y = 1.0 / (x + 1.0);
    y = (1.0 - y) * 2.0;
    if(y > 1.0) {
        return 1.0;
    }
    return y;
}

void setSnapMultiplier(Responsive * resp, float newMultiplier)
{
    if(newMultiplier > 1.0) {
        newMultiplier = 1.0;
    }
    if(newMultiplier < 0.0) {
        newMultiplier = 0.0;
    }
    resp->snapMultiplier = newMultiplier;
}

uint32_t getValue(Responsive * resp) {
  return resp->responsiveValue;
}

uint32_t getRawValue(Responsive * resp) {
  return resp->rawValue;
}

bool hasChanged(Responsive * resp) {
  return resp->responsiveValueHasChanged;
}

bool isSleeping(Responsive * resp) {
  return resp->sleeping;
}

void enableSleep(Responsive * resp) {
  resp->sleepEnable = true;
}

void disableSleep(Responsive * resp) {
  resp->sleepEnable = false;
}

void enableEdgeSnap(Responsive * resp) {
  resp->edgeSnapEnable = true;
}

void disableEdgeSnap(Responsive * resp) {
  resp->edgeSnapEnable = false;
}

void setActivityThreshold(Responsive * resp, float newThreshold) {
  resp->activityThreshold = newThreshold;
}

void setAnalogResolution(Responsive * resp, int resolution) {
  resp->analogResolution = resolution;
}