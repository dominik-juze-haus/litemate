#### !!!!! RUNS ON PYTHON 3.12 !!!!!

import sys

from turtle import width # sys for system functions
import cupy as cp #CuPy for GPU acceleration
import time #this is fucking obvious
import customtkinter as ctk #custom tkinter, pretty
import keyboard #keyboard input
import matplotlib.pyplot as plt #plotting
import os #os
import torch #pytorch
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

    
    def opendata(self, analysis_path):
        self.analysis_path = analysis_path #path to the selected analysis results file
        with open(self.analysis_path, 'r') as f: #open the selected analysis results file
            self.analysis_data = json.load(f) #load the analysis data from the file and store it in a variable for use in the GUI
        return self.analysis_data #return the analysis data for use in the GUI
    
    ## ANALYSE FOOTAGE FUNCTION ##
    def analyze_footage(self, reference_frame_num):
        Y_median_array = cp.zeros((self.frame_count, 2)) #create an array to store the Y median values for each frame
        RGB_median_array = cp.zeros((self.frame_count, 4)) #create an array to store the RGB median values for each frame
        ref_frame_flag = cp.zeros((self.frame_count, 2)) #create an array to store the reference frame flag for each frame


        for frame, i in zip(self.container.decode(self.stream), range(self.frame_count)):
            frame_array = cp.frombuffer(frame.to_ndarray(format='rgb24'), cp.uint8).reshape([self.height, self.width, 3]) # convert the frame to a CuPy array in RGB format

            Y_plane = 0.299 * frame_array[:, :, 0] + 0.587 * frame_array[:, :, 1] + 0.114 * frame_array[:, :, 2] # calculate the Y (luminance) plane from the RGB values using the standard formula for converting RGB to grayscale

            if i == reference_frame_num: #if the current frame is the reference frame, perform the analysis and return the results
                ref_frame_flag[i, 0] = i #set a flag to indicate that this is the reference frame
                ref_frame_flag[i, 1] = 1 #set a flag to indicate that this frame is the reference frame
            
            Y_median_array[i, 0] = i #store the frame number in the Y median array
            Y_median_array[i, 1] = cp.median(Y_plane) #luminance median of the current frame

            RGB_median_array[i, 0] = i #store the frame number in the RGB median array
            RGB_median_array[i, 1:] = cp.median(frame_array, axis=(0, 1)) #RGB median of the current frame

            



        analyzed_data = {
            'frame_num': int(i),
            'Y_median': Y_median_array.get(), # convert CuPy scalar to Python float
            'RGB_median': RGB_median_array.get(), # convert each channel from CuPy scalar to Python float
            'reference_frame_flag': ref_frame_flag.get() # convert CuPy scalar to Python int
        }

        
        return analyzed_data #return the analyzed data for use in the GUI



'''
analysis = Analysis(footage_path) # create an instance of the Analysis class with the selected footage
analyzed_data = analysis.analyze_footage(reference_frame_num) # perform the analysis on the footage with the specified reference frame number
print(analyzed_data) # print the analyzed data to the console for testing purposes
'''