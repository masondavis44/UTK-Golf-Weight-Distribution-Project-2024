import simultaneous as ADS1256
import time
import os  # Import os module to check for file existence

# Initialize ADC
ADC = ADS1256.ADS1256()
if ADC.ADS1256_init() == -1:
    exit()

# Calibration data
weights = [0, 5, 10, 25, 50]  # Example weights in grams

# Check if the file already exists
file_exists = os.path.isfile('calibration_data3.csv')

# Open a file to save or append the calibration data
with open('calibration_data3.csv', 'a') as file:  # 'a' opens the file in append mode
    # Write the header row if the file is new
    if not file_exists:
        file.write("Weight (pounds),ADC Value\n")

    print("Place each weight on the load cell and press Enter to record its value.")
    for weight in weights:
        input("Place {} pounds on the load cell. Then press Enter...".format(weight))
        raw_adc = ADC.ADS1256_GetDiffChannalValue()
        print("Recorded value for {} pounds: {}".format(weight, raw_adc))
        
        # Append the weight and raw ADC value to the file
        file.write("{},{}\n".format(weight, raw_adc))

        time.sleep(1)  # Short delay to stabilize

print("Calibration data saved to 'calibration_data3.csv'.")


