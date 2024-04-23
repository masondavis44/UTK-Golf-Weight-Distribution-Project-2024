#!/usr/bin/python
# -*- coding:utf-8 -*-

import time
import ADS_2 as ADS1256
import RPi.GPIO as GPIO

def read_voltages(duration=3):
    adc_values = {f"Differential {i*2}-{i*2+1}": [] for i in range(4)}
    start_time = time.time()

    ADC = ADS1256.ADS1256()
    if ADC.ADS1256_init() == -1:
        return adc_values

    while time.time() - start_time < duration:
        for ch_pair in range(4):  # Iterate over channel pairs 0-3
            ADC_Value = ADC.ADS1256_GetDiffChannalValue(ch_pair)
            adc_values[f"Differential {ch_pair*2}-{ch_pair*2+1}"].append(ADC_Value)
    
    return adc_values

if __name__ == "__main__":
    try:
        adc_values = read_voltages()
        for key, value_list in adc_values.items():
            avg_adc_value = sum(value_list) / len(value_list) if value_list else 0
            print(f"{key} Raw ADC Average = {avg_adc_value:.2f}")

    except Exception as e:
        print(e)
        GPIO.cleanup()



