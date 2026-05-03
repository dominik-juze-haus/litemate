#### !!!!! RUNS ON PYTHON 3.12 !!!!!

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


## __________ TESTING CODE SNIPPETS __________ ##
'''
footage_path = filedialog.askopenfilename(title="Select Footage", filetypes=[("Video files", "*.mov *.mp4 *.avi *.mkv *.wmv *.flv *.mxf")]) # open file dialog to select footage
reference_frame_num = 100 # set the reference frame number for the analysis (can be changed in the GUI later)
'''





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

    ## LOAD ANALYSIS FUNCTION TO LOAD ANALYSIS RESULTS FROM A JSON FILE ##
    def load_analysis_json(self):
        json_file_path = filedialog.askopenfilename(title="Load Analysis Results", filetypes=[("JSON files", "*.json")]) # open file dialog to select the analysis results file to load
        with open(json_file_path, 'r') as f:
            json_data = json.load(f) # load the analysis data from the selected JSON file and return it for use in the GUI
            analysis_data = {} # initialize a dictionary to store the loaded analysis data
            for item in json_data:
                for key, value in item.items():
                    analysis_data[key] = cp.array(value).get() # convert any lists in the loaded analysis data back to CuPy arrays for use in the GUI, while keeping other data types unchanged
        return analysis_data
    
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

    ## CHANGE DETECTION FUNCTION ##
    def detect_changes(self, analyzed_data, threshold):
        change = [] #list to store the detected changes
       

        return analyzed_data #return the list of detected changes for use in the GUI 





'''
analysis = Analysis(footage_path) # create an instance of the Analysis class with the selected footage
analyzed_data = analysis.analyze_footage(reference_frame_num) # perform the analysis on the footage with the specified reference frame number
print(analyzed_data) # print the analyzed data to the console for testing purposes
'''