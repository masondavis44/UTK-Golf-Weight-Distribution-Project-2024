This repositiory includes all necessary files to run the Dynamic Golf Board. The Dynamic Golf Board was designed to track and measure the center of mass of a player during their golf swing in order to train towards a more fluid motion seen by professional golfers. The golf board accomplishes this by using 4 load cells that are integral to a Wii board. These load cells are wired to a Raspberry Pi. The Raspberry Pi is equipped with a AD/DA Expansion board that gives the Raspberry Pi high precision capabilities. From the load cells, the output is a differential voltage value that is able to be converted to weight. For these raw ADC values to be converted to weight, we had to calibrate each load cell individually to get their calibration factors. With the load cells calibrated to measure weight accurately, we were able to read the weights from each load cell simultaneously. With this, we wrote a file to measure these weights for the duration of a swing. Center of mass calculations were done on the wii board in order to plot these weights in one line starting from the beginning of the swing to the end of the swing. In addition, we used a Oak-D camera which captures a video of the golfers swing at the same time the load cell code is run. This allows the user to pinpoint different frames of their swing to see where most of their weight is distributed. The Dynamic Golf Board is definitely effective and accurate on measuring the players center of mass, but there are still some minor improvements to the project that need to be made. 


Description of files located in this repository:
#config.py----- This is the configuration file for the ADS1256 Expansion Board, nothing was changed in this file on our end.
#ADS_2.py--------- This file defines a Python class and associated constants for interacting with the ADS1256, an analog-to-digital converter (ADC).
Imports:
config: Module containing configuration methods and constants like digital_write, spi_writebyte, etc.
RPi.GPIO: Library to handle Raspberry Pi GPIO operations.
Global Variables:
ScanMode: Tracks the scanning mode (single-ended/differential).
ADS1256_GAIN_E: Gain settings for the ADC.
ADS1256_DRATE_E: Data rate settings for the ADC.
REG_E: Register addresses used by the ADS1256.
CMD: Command codes for the ADS1256.
ADS1256 Class:
__init__: Initializes the chip select (CS), reset (RST), and data ready (DRDY) pins using config.
ADS1256_reset: Resets the ADS1256 by toggling the reset pin.
ADS1256_WriteCmd: Sends a command to the ADS1256.
ADS1256_WriteReg: Writes a value to a specific register.
ADS1256_Read_data: Reads data from a specified register.
ADS1256_WaitDRDY: Waits for the DRDY pin to indicate data availability.
ADS1256_ReadChipID: Reads the chip ID from the status register.
ADS1256_ConfigADC: Configures the ADC gain and data rate.
ADS1256_SetChannal: Selects a specific single-ended channel.
ADS1256_SetDiffChannal: Selects a differential channel pair.
ADS1256_SetMode: Sets the scanning mode.
ADS1256_init: Initializes the ADS1256, resets it, and configures it with gain and data rate.
ADS1256_Read_ADC_Data: Reads raw data from the ADC.
ADS1256_GetDiffChannalValue: Reads the value from a differential channel pair.
#newmain3.py------ This file captures the load cell data simultaneously
#finalmain2.py------This file is the first file that is run when executing a swing using the board. It calls on newmain3.py to collect the raw ADC data from the load cells, and then converts these to weights using our calibration factors. This code also includes definitions and functions for the camera to capture a video of the players swing. 
#simultaneous.py----This file is a copy of the ADS_2.py file, but is set up to read the Raw ADC values fron the load cells simultaneously for the purpose of calibration.
#calibration.py-----This file is used to calibrate each load cell seperately. When run, the files prompts the user to place specified weights on the desired load cell, and the file saves the RAW ADC data from each weight to a csv file. Each load cell should have a separate csv file, so when running the code for each load cell, the file in which the data is being saved must be changed in the code.
#calibrationcurve.py-----This file imports the Raw ADC data from the desired calibration csv file, and outputs the calibration slope and constant for the desired load cell. These values are needed for the finalmain2.py file in order to convert the ADC values to weight.
#COM.py------This file is run after the finalmain2.py file and it outputs the visuals for the swing. One figure will be the center of mass line shown on a time gradient, and the other is a side by side of the frames captured by the camera next to the center of mass at that point in time.


#How to Operate the Dynamic Golf Board
1) Ensure all wiring connections are secure and power is run to the Pi and camera
2) Use the portable HDMI to view the Pi on the tablet with the wireless keyboard and mouse
3) Navigate to the terminal and enter the directory: labuser/Documents/ADS
4) Have the player stand on the center of the board
5) Run the file "finalmain2.py" in the terminal, and when the camera makes a click noise is when the player should initiate their swing
6) Once this file has finished running, run the "COM.py" file to show the figures from the data


#Improvements to be made
1) During the design showcase, the portable HDMI overheated and was no longer functional. Some type of cooling system (fans) needs to be incorporated into the board
2) Currently, the user has to run the files through the Pi's terminal, which is not ideal for someone who does not know coding. An interface with buttons that execute these files would be ideal for simplicity.
3) The camera has good capabilites, but we did not have enough time to maximize these. The side by side camera frame to center of mass plot is not super accurate since the camera's frames per second is pretty low. Improving this is crucial for accuracy and repeatability.
4) 
