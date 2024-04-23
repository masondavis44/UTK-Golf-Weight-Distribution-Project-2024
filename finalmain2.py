import cv2
import depthai as dai
import pandas as pd
import newmain3  # Your module for capturing load cell data
import threading
import time

# Function to record video
def record_video(duration_1):
    pipeline = dai.Pipeline()
    camRgb = pipeline.createColorCamera()
    xoutVideo = pipeline.createXLinkOut()
    xoutVideo.setStreamName("video")
    camRgb.setBoardSocket(dai.CameraBoardSocket.RGB)  # Adjust if necessary
    camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
    camRgb.setFps(60)  # Adjust based on expected performance
    camRgb.video.link(xoutVideo.input)

    with dai.Device(pipeline) as device:
        qVideo = device.getOutputQueue(name="video", maxSize=4, blocking=False)
        frames = []
        expected_fps = 10  # Adjust based on realistic performance
        expected_frames = duration_1 * expected_fps
        
        while len(frames) < expected_frames:
            in_video = qVideo.tryGet()
            if in_video is not None:
                frame = in_video.getCvFrame()
                frames.append(frame)
                
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        # save the video
        video_writer = cv2.VideoWriter('output.mp4', fourcc, expected_fps, (frames[0].shape[1], frames[0].shape[0]))
        
        for frame in frames:
            video_writer.write(frame)
        
        video_writer.release()

# Function to collect and save load cell data
def collect_load_cell_data(duration):
    # the camera takes longer to start recording than the load cells, so we make the data collection wait so they begin at the same time.
    time.sleep(2.5)
    # the calibration factors are the slope and intercept to convert raw ADC readings to weight
    calibration_factors = {
        "Differential 0-1": (0.005255402508804553, -32.77118234095868),
        "Differential 2-3": (0.0064694839574558245, -35.8680578828282),
        "Differential 4-5": (0.006428018984246993, -134.56260257211812),
        "Differential 6-7": (0.008134870987764936, -49.37097264202684),
    }

    def voltage_to_weight(voltage, slope, intercept):
        return voltage * slope + intercept

    def convert_voltages_to_weights(voltages):
        weights_dict = {}
        for key, voltage_list in voltages.items():
            slope, intercept = calibration_factors[key]
            weights = [voltage_to_weight(voltage, slope, intercept) for voltage in voltage_list]
            weights_dict[key] = weights
        return weights_dict
    
    voltages = newmain3.read_voltages(duration)
    weights_dict = convert_voltages_to_weights(voltages)
    df_weights = pd.DataFrame.from_dict(weights_dict, orient='index').transpose()
    # save the loadcell data 
    df_weights.to_csv('load_cell_weights.csv', index=False)
    print("Weights saved to 'load_cell_weights.csv'.")

# Main function to run both tasks concurrently
def main():
    duration = 5  # Duration for load cells in seconds
    duration_1 = 5.5 # Duration for camera in seconds
    # Create threads for video recording and load cell data collection
    video_thread = threading.Thread(target=record_video, args=(duration,))
    data_thread = threading.Thread(target=collect_load_cell_data, args=(duration,))
    
    # Start the threads
    data_thread.start()
    video_thread.start()
    
    
    
    # Wait for both threads to complete
    video_thread.join()
    data_thread.join()
    print("Video recording and data collection completed.")

if __name__ == "__main__":
    main()

