#import necessary libraries for data manipulation and figure display
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
import sys
import cv2
import os
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm

# this code creates two visuals, one is a graph of the entire swing duration. The other is a graph for every data point next to the picture the camera captured
# for simplicity the entire swing will be referenced as (ES) and each data point as (DP)

fig_width = 14  # Figure width in inches (DP)
fig_height = 6  # Figure height in inches (DP)
inset_ratio = 0.8  # The proportion of the figure to use for the image altering this changes the white space to the right of the plots (DP)

# Function to split video into frames (DP)
def split_video_to_frames(input_video_path, output_folder_path, df):
    # Open the video file
    video_capture = cv2.VideoCapture(input_video_path)

    # Get the total number of frames in the video
    total_frames = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))

    # Calculate frame indices based on DataFrame length
    frame_indices = [int(i * total_frames / len(df)) for i in range(len(df))]

    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    # Read and save frames at the specified indices
    for idx, frame_idx in enumerate(frame_indices):
        # Set the frame position
        video_capture.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)

        # Read the frame
        ret, frame = video_capture.read()

        # Check if frame is read successfully
        if ret:
            # Save the frame as an image
            output_path = os.path.join(output_folder_path, f"frame_{idx}.jpg")
            cv2.imwrite(output_path, frame)
        else:
            print(f"Error reading frame {idx}")

    # Release the VideoCapture object
    video_capture.release()

# insert the load cell data
df = pd.read_csv(r'/home/labuser/Documents/ADS/load_cell_weights.csv')
# make the length of the df divisible by 4 by removing end datapoints
remainder = len(df) % 4
if remainder != 0:
    df = df[:-remainder]

# Calculate the average of every 5 rows for each column to condense data
df = df.groupby(df.index // 4).mean()
# calculate the center of mass in the x and y direction
row_sums = df.sum(axis=1)
df['Row_Sums'] = row_sums
X_1 = (df.iloc[:, 0] * -8.25 + df.iloc[:, 1] * -8.25 + df.iloc[:, 2] * 8.25 + df.iloc[:, 3] * 8.25) / df.iloc[:, 4]
Y_1 = (df.iloc[:, 0] * 4.5 + df.iloc[:, 1] * -4.5 + df.iloc[:, 2] * 4.5 + df.iloc[:, 3] * -4.5) / df.iloc[:, 4]

# this is the location of the video recorded from finalmain2.py
input_video_path = r'/home/labuser/Documents/ADS/output.mp4'

# Video is split into individual frames and stored in this location
output_folder_path = r'/home/labuser/Documents/ADS/Pictures'

# Split the video into frames
split_video_to_frames(input_video_path, output_folder_path, df)

# Add the new column to the DataFrame
df['x'] = X_1
df['y'] = Y_1

df.to_csv('/home/labuser/Documents/ADS/COM.csv', index=False)

# make the plot for the graph (ES)
points = np.array([df['x'], df['y']]).T.reshape(-1, 1, 2)
segments = np.concatenate([points[:-1], points[1:]], axis=1)

# Create a LineCollection (ES)
lc = LineCollection(segments, cmap='viridis', norm=plt.Normalize(0, 10))

# Set the values used for colormapping (ES)
lc.set_array(np.linspace(0, 10, len(df['x']) - 1))
lc.set_linewidth(2)

fig, ax = plt.subplots()
ax.add_collection(lc)
ax.autoscale()
# set axis to the dimensions of the board (ES)
ax.set_xlim(-8.25, 8.25)
ax.set_ylim(-4.5, 4.5)

# Creating a colorbar as a legend for representation of time (ES)
cbar = plt.colorbar(lc, orientation='vertical')
cbar.set_label('Time Progression')

plt.title('Line Gradient with Colorbar')
plt.xlabel('X Axis')
plt.ylabel('Y Axis')
plt.show()

# Function to plot a single data point (DP)
def plot_point_with_image(ax, x, y, image_path):
    ax.scatter(x, y)
    ax.set_title(f'Point ({x}, {y})')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_xlim(-8.25, 8.25)
    ax.set_ylim(-4.5, 4.5)

    # Load and display the image from video frames
    img = plt.imread(image_path)

    inset_ratio_width = 0.4  # You can increase this if you want the image to be wider
    inset_ratio_height = 1.1  # You can adjust this based on your desired image height
    inset_x_start = 1.05  # You can increase this to move the image further to the right
    inset_y_start = 0.0  # You can adjust this to move the image up or down

    ax_image = ax.inset_axes([inset_x_start, inset_y_start, inset_ratio_width, inset_ratio_height], transform=ax.transAxes)
    ax_image.imshow(img)
    ax_image.axis('off')

# Function to create and display plots (DP)
def create_plots():
    # Create a Tkinter window with adjusted width
    root = tk.Tk()
    root.title("Scrolled Window")
    root.geometry("1600x1200")  # Adjust the width and height as needed

    # Create a canvas to hold the plots
    canvas = tk.Canvas(root)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Add a scrollbar
    scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    # Create a frame to contain the plots
    frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor=tk.NW)

    # Plot each data point in the DataFrame
    for index, row in df.iterrows():
        fig, ax = plt.subplots(figsize=(fig_width, fig_height))
        fig.subplots_adjust(right=0.7)
        plot_point_with_image(ax, row['x'], row['y'], os.path.join(output_folder_path, f"frame_{index}.jpg"))
        fig_canvas = FigureCanvasTkAgg(fig, master=frame)
        fig_canvas.draw()
        fig_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # Allow the window to be scrolled
    canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(-1*(event.delta), "units"))

    # Function to close the window and end the script
    def close_window():
        root.destroy()
        sys.exit()

    # Button to close the window
    close_button = tk.Button(root, text="Close", command=close_window)
    close_button.pack()

    # Run the Tkinter event loop
    root.mainloop()

# Call the function to create plots
create_plots()
