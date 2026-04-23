import sys

import cupy as cp #CuPy for GPU acceleration
import time #this is fucking obvious
import customtkinter as ctk #custom tkinter, pretty
import keyboard #keyboard input
import matplotlib.pyplot as plt #plotting
import os #os
#import torch #pytorch
import ffmpeg #ffmpeg for video processing
import av #PyAV ffmpeg wrapper
import json #json for saving and loading analysis results

from tkinter import filedialog
from scipy.ndimage import gaussian_filter1d 


## __________ TESTING CODE SNIPPETS __________ ##

footage_path = filedialog.askopenfilename(title="Select Footage", filetypes=[("Video files", "*.mov *.mp4 *.avi *.mkv *.wmv *.flv *.mxf")]) # open file dialog to select footage
lookahead_frame_count = 5 # set the number of frames to look ahead for the analysis (can be changed in the GUI later)
release_frame_count = 5 # set the number of frames to look ahead for the release of the detected change (can be changed in the GUI later)
threshold = 10 # set the threshold for detecting changes in the footage (can be changed in the GUI later)


## _____ FUNCTION DRAFTS_____ ##

# ---- function to save the analyzed data to a JSON file, which can be used for loading the analysis results in the GUI later
def save_analysis_json(analyzed_data):
    json_prepare = [] # initialize a list to store the JSON-serializable data
    for key, value in analyzed_data.items():
        try:
            json_prepare.append({key: value.tolist()}) # convert any CuPy arrays in the analyzed data to lists for JSON serialization, while keeping other data types unchanged
        except AttributeError:
            json_prepare.append({key: value}) # if the value is not a CuPy array, keep it unchanged in the JSON preparation

    json_file_path = filedialog.asksaveasfilename(title="Save Analysis Results", defaultextension=".json", filetypes=[("JSON files", "*.json")]) # open file dialog to select location to save the analysis results
    json_dump = json.dumps(json_prepare) # convert the JSON-serializable data to a JSON string for saving to a file or for use in the GUI

    with open(json_file_path, 'w') as f:
        f.write(json_dump)

# ---- function to load the analyzed data from a JSON file, which can be used for loading the analysis results in the GUI later
def load_analysis_json():
    json_file_path = filedialog.askopenfilename(title="Load Analysis Results", filetypes=[("JSON files", "*.json")]) # open file dialog to select the analysis results file to load
    with open(json_file_path, 'r') as f:
        json_data = json.load(f) # load the analysis data from the selected JSON file and return it for use in the GUI
        analysis_data = {} # initialize a dictionary to store the loaded analysis data
        for item in json_data:
            for key, value in item.items():
                analysis_data[key] = cp.array(value).get() # convert any lists in the loaded analysis data back to CuPy arrays for use in the GUI, while keeping other data types unchanged
    return analysis_data



# ---- change detection function, which takes the analyzed data and the threshold as input and returns a list of detected changes
def detect_changes(analyzed_data, threshold):
    for i in range(analyzed_data['frame_num']):
        #print(abs(analyzed_data['Y_median'][i, 1] - analyzed_data['Y_median'][i+lookahead_frame_count, 1]))
        if not change_ongoing:
            for lookahead in range(1, lookahead_frame_count):
                try:

                    
                    
                    if abs(analyzed_data['Y_median'][i, 1] - analyzed_data['Y_median'][i+lookahead_frame_count, 1]) > threshold: # if the difference in Y median between the current frame and the previous frame is greater than the threshold
                        changes[0].append(i) #store the frame number of the detected change in the changes list
                        change_ongoing = True # set the change ongoing boolean to true
                    

                    
                except IndexError:
                    break

        elif change_ongoing:
            for release in range(1, release_frame_count):
                try:          
                    if abs(analyzed_data['Y_median'][i, 1] - analyzed_data['Y_median'][i+release_frame_count, 1]) < threshold: # if a change is ongoing and the difference in Y median between the current frame and the previous frame is less than the threshold
                        changes[1].append(i) #store the frame number of the release of the detected change in the changes list
                        change_ongoing = False # set the change ongoing boolean to false
                except IndexError:
                    break   

#### __________ANALYSIS___________________________________________________________________________
### ANALYSIS CLASS pulled out of the AnalysisScript.py file
class Analysis:
    ## ________ FFMPEG-PYTHON VERSION ________ ##
    '''
    def __init__(self, shot_path):
        self.shot_path = shot_path #path to the selected shot
        self.analysis_data = None #variable to store the analysis data for use in the GUI
        self.probe = ffmpeg.probe(self.shot_path)
        self.video_stream = next((stream for stream in self.probe['streams'] if stream['codec_type'] == 'video'), None)
        self.width = int(self.video_stream['width'])
        self.height = int(self.video_stream['height'])
    '''

    ## ________ PYAV VERSION ________ ##
    def __init__(self, shot_path):
        self.shot_path = shot_path #path to the selected shot
        self.analysis_data = None #variable to store the analysis data for use in the GUI
        self.container = av.open(self.shot_path) # open the selected footage with PyAV
        self.stream = self.container.streams.video[0] # get the first video stream from the container
        self.width = self.stream.width # get the width of the video
        self.height = self.stream.height # get the height of the video
        self.fps = float(self.stream.average_rate) # get the frame rate of the video as a float for easier calculations
        self.frame_count = self.stream.frames # get the total number of frames in the video
        self.stream.thread_type = "AUTO" # set the thread type to auto for optimal performance
        self.stream.thread_count = 0  # 0 = auto (use all cores)

    
    def opendata(self, analysis_path):
        with open(analysis_path, 'r') as f: #open the selected analysis results file
            analysis_data = json.load(f) #load the analysis data from the file and store it in a variable for use in the GUI
        return analysis_data #return the analysis data for use in the GUI
    
    ## ANALYSE FOOTAGE FUNCTION ##
    def analyze_footage(self):
        Y_median_array = cp.zeros((self.frame_count, 2)) #create an array to store the Y median values for each frame
        RGB_median_array = cp.zeros((self.frame_count, 4)) #create an array to store the RGB median values for each frame


        for frame, i in zip(self.container.decode(self.stream), range(self.frame_count)):
            frame_array = cp.frombuffer(frame.to_ndarray(format='rgb24'), cp.uint8).reshape([self.height, self.width, 3]) # convert the frame to a CuPy array in RGB format

            #RGB_histogram = cp.histogramdd(frame_array.reshape(-1, 3), bins=256, range=((0, 255), (0, 255), (0, 255))) # calculate the histogram of the RGB values for the current frame


            Y_plane = 0.299 * frame_array[:, :, 0] + 0.587 * frame_array[:, :, 1] + 0.114 * frame_array[:, :, 2] # calculate the Y (luminance) plane from the RGB values using the standard formula for converting RGB to grayscale
            #Y_histogram, _ = cp.histogram(Y_plane, bins=256, range=(0, 255)) # calculate the histogram of the Y plane for the current frame


            Y_median_array[i, 0] = i #store the frame number in the Y median array
            Y_median_array[i, 1] = cp.median(Y_plane) #luminance median of the current frame

            RGB_median_array[i, 0] = i #store the frame number in the RGB median array
            RGB_median_array[i, 1:] = cp.median(frame_array, axis=(0, 1)) #RGB median of the current frame           



        analyzed_data = {
            'frame_num': int(i),
            'Y_median': Y_median_array.get(), # convert CuPy scalar to Python float
            'RGB_median': RGB_median_array.get(), # convert each channel from CuPy scalar to Python float
        }

        
        return analyzed_data #return the analyzed data for use in the GUI

'''
analysis = Analysis(footage_path) # create an instance of the Analysis class with the selected footage

analyzed_data = analysis.analyze_footage() # perform the analysis on the footage with the specified reference frame number
Y_median_array_smooth = gaussian_filter1d(analyzed_data['Y_median'][:, 1], sigma=2) # apply a Gaussian filter to the Y median data for smoothing, can be adjusted in the GUI later
analyzed_data.update({'Y_median_smooth': Y_median_array_smooth}) # add the smoothed Y median data to the analyzed data for use in the GUI later
'''


analyzed_data = load_analysis_json() # load the analyzed data from a JSON file for testing purposes, will be replaced with the actual analysis function in the GUI later

print(analyzed_data) # print the analyzed data to the console for testing purposes
print(analyzed_data['Y_median_smooth']) # print the smoothed Y median data to the console for testing purposes

#save_analysis_json(analyzed_data) # save the analyzed data to a JSON file for use in the GUI later

#### __________________________CHANGE DETECTION___________________________________________________________________________

changes = [[], []] #list to store the detected changes
change_ongoing = False #boolean to track whether a change is currently ongoing



#detect_changes(analyzed_data, threshold) # perform change detection on the analyzed data with the specified threshold

        
print(changes) #print the detected changes to the console for testing purposes, will be replaced with the actual function to display the detected changes in the GUI


#### __________________________PLOTTING___________________________________________________________________________

plot_data = analyzed_data['Y_median_smooth'] # get the Y median data from the analyzed data
plt.plot(plot_data) # plot the Y median data
plt.xlabel('Frame Number') # set the x-axis label
plt.ylabel('Y Median') # set the y-axis label
plt.title('Y Median Over Time') # set the title of the plot
if changes: # if there are detected changes, add vertical lines to the plot to indicate the start and end of the detected changes
    for change in changes[0]:
            plt.axvline(x=change, color='r', linestyle='--') # add a vertical line to indicate the start of the detected change
    for change in changes[1]:
            plt.axvline(x=change, color='g', linestyle='--') # add a vertical line to indicate the end of the detected change
plt.show() # display the plot




 