import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

# Load the calibration data from CSV
data = pd.read_csv('calibration_data1.csv')

# Perform linear regression
slope, intercept, r_value, p_value, std_err = linregress(data['ADC Value'], data['Weight (pounds)'])

# Function to convert raw ADC value to weight
def adc_to_weight(adc_value):
    return (adc_value * slope) + intercept

# Display the calibration equation and R-squared value
print(f"Calibration Equation: weight = ({slope} * ADC Value) + {intercept}")
print(f"R-squared: {r_value**2}")

# Plotting the calibration curve
plt.figure(figsize=(10, 6))
plt.scatter(data['ADC Value'], data['Weight (pounds)'], color='blue', label='Calibration Data')
plt.plot(data['ADC Value'], slope * data['ADC Value'] + intercept, color='red', label='Fitted Line')

plt.title('Load Cell Calibration Curve')
plt.xlabel('ADC Value')
plt.ylabel('Weight (pounds)')
plt.legend()
plt.grid(True)
plt.show()

# Example conversion
example_adc_value = 7500
converted_weight = adc_to_weight(example_adc_value)
print(f"The weight for ADC value {example_adc_value} is approximately {converted_weight:.2f} pounds.")
