// send bytes to uart esp32 -> rockpis 

#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/uart.h"
#include "driver/gpio.h"
#include "sdkconfig.h"
#include <time.h>
#include <stdlib.h>
#include "driver/adc.h"
#include "esp_adc_cal.h"
#include "responsive.h"

#define DEBUG 1

#define DEFAULT_VREF    1100        //Use adc2_vref_to_gpio() to obtain a better estimate
#define NO_OF_SAMPLES   256

#define ECHO_TEST_TXD (4)
#define ECHO_TEST_RXD (5)
#define ECHO_TEST_RTS (UART_PIN_NO_CHANGE)
#define ECHO_TEST_CTS (UART_PIN_NO_CHANGE)

#define ECHO_UART_PORT_NUM      (0)
#define ECHO_UART_BAUD_RATE     (115200)
#define ECHO_TASK_STACK_SIZE    2048

#define BUF_SIZE (1024)


static esp_adc_cal_characteristics_t *adc_chars;
//static const adc_channel_t channel = ADC_CHANNEL_6;     //GPIO34 if ADC1, GPIO14 if ADC2
static const adc_bits_width_t width = ADC_WIDTH_BIT_9;
static const adc_atten_t atten = ADC_ATTEN_MAX; //ADC_ATTEN_DB_0;
static const adc_unit_t unit = ADC_UNIT_2;


typedef struct pot {
    uint8_t id;
    uint8_t prev;
    adc_channel_t chan;
} potentiometer;


static void check_efuse(void) {
    //Check if TP is burned into eFuse
    if (esp_adc_cal_check_efuse(ESP_ADC_CAL_VAL_EFUSE_TP) == ESP_OK) {
        printf("eFuse Two Point: Supported\n");
    } else {
        printf("eFuse Two Point: NOT supported\n");
    }
    //Check Vref is burned into eFuse
    if (esp_adc_cal_check_efuse(ESP_ADC_CAL_VAL_EFUSE_VREF) == ESP_OK) {
        printf("eFuse Vref: Supported\n");
    } else {
        printf("eFuse Vref: NOT supported\n");
    }
}


static void print_char_val_type(esp_adc_cal_value_t val_type)
{
    if (val_type == ESP_ADC_CAL_VAL_EFUSE_TP) {
        printf("Characterized using Two Point Value\n");
    } else if (val_type == ESP_ADC_CAL_VAL_EFUSE_VREF) {
        printf("Characterized using eFuse Vref\n");
    } else {
        printf("Characterized using Default Vref\n");
    }
}


static void echo_task(void *arg)
{
    potentiometer *pot = (potentiometer *)arg;
    uint8_t id = (uint8_t)pot->id;
    adc_channel_t channel = (adc_channel_t)pot->chan; //(adc_channel_t)pot->chan;
    uint8_t prev = (uint8_t)pot->prev;

    check_efuse();

    //adc1_config_width(width);
    adc2_config_channel_atten((adc2_channel_t)channel, atten);

    /*
    uart_config_t uart_config = {
        .baud_rate = ECHO_UART_BAUD_RATE,
        .data_bits = UART_DATA_8_BITS,
        .parity    = UART_PARITY_DISABLE,
        .stop_bits = UART_STOP_BITS_1,
        .flow_ctrl = UART_HW_FLOWCTRL_DISABLE,
        .source_clk = UART_SCLK_APB,
    };

    int intr_alloc_flags = 0;
    

#if CONFIG_UART_ISR_IN_IRAM
    intr_alloc_flags = ESP_INTR_FLAG_IRAM;
#endif


    ESP_ERROR_CHECK(uart_driver_install(ECHO_UART_PORT_NUM, BUF_SIZE * 2, 0, 0, NULL, intr_alloc_flags));
    ESP_ERROR_CHECK(uart_param_config(ECHO_UART_PORT_NUM, &uart_config));
    ESP_ERROR_CHECK(uart_set_pin(ECHO_UART_PORT_NUM, ECHO_TEST_TXD, ECHO_TEST_RXD, ECHO_TEST_RTS, ECHO_TEST_CTS));
*/

    //Characterize ADC
    adc_chars = calloc(1, sizeof(esp_adc_cal_characteristics_t));
    esp_adc_cal_value_t val_type = esp_adc_cal_characterize(unit, atten, width, DEFAULT_VREF, adc_chars);
    print_char_val_type(val_type);
    
    uint8_t data[] = { 0, 0 };
    data[0] = id;

    
    static Responsive resp = {
        .analogResolution = 4096,
        .activityThreshold = 8.0,
        .edgeSnapEnable = true,
        .errorEMA = 0.0,
        .sleeping = false 
    };

    begin(&resp, 0, 1, 0.01);

    while (1) {
        uint32_t adc_reading = 0;
        int raw;
        adc2_get_raw((adc2_channel_t)channel, width, &raw);
        update(&resp, raw);
        printf("%d\n", resp.responsiveValue);
        adc_reading = getValue(&resp);

#if DEBUG
            printf("%d\n", adc_reading);
#else
            uart_write_bytes(ECHO_UART_PORT_NUM, (const char *) data, sizeof(data));
#endif
        
        vTaskDelay(10 / portTICK_PERIOD_MS);
    }
}

void app_main(void) {

    static potentiometer pot1 = {
        .id = 1,
        .chan = ADC_CHANNEL_3,
        .prev = 0
    };
    
    xTaskCreate(echo_task, "uart_echo_task", ECHO_TASK_STACK_SIZE, (void *)&pot1, 2, NULL);
}