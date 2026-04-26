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
import math
import json #json for saving and loading analysis results

from tkinter import filedialog
from scipy.ndimage import gaussian_filter1d 


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

      

# ---- function to calculate the derivative of the analyzed data
def derivative(data, frame_num):
    derivative = cp.zeros(frame_num - 1) # initialize an array to store the derivative values
    for i in range(frame_num - 1): # loop through the data starting from the second frame
        derivative[i] = data[i + 1] - data[i] # calculate the difference between the current frame and the next frame and store it in the derivative array
    
    return derivative # return the calculated derivative values for use in change detection


# ---- change detection function, which takes the analyzed data and the threshold as input and returns a list of detected changes
def detect_changes(analyzed_data, threshold, lookahead_frames, release_frames):
    #Y_median_smooth = analyzed_data['Y_median_smooth'] # get the smoothed Y median data from the analyzed data
    #print(Y_median_smooth) # print the smoothed Y median data for debugging purposes
    Y_feed = analyzed_data['Y_median']# get the Y median data from the analyzed data
    #print(Y_feed) # print the Y median data for debugging purposes
    changes = [[], []] #list to store the detected changes
    change_ongoing_flag = False # initialize a flag to track whether a change is currently ongoing
    derived_data = derivative(Y_feed[:,1], analyzed_data['frame_num']) # calculate the derivative of the Y median data for use in change detection
    direction = 0 # initialize a variable to track the direction of the change, 0 = no change, 1 = positive change, -1 = negative change
    i = 0

    
    # --- flooring of noise data
    '''
    for i in range(analyzed_data['frame_num'] -1):
        if abs(derived_data[i]) < 0.12:
            derived_data[i] = 0
    '''
    
    zerotolerance = 0.012


    while i < analyzed_data['frame_num'] - 1: # loop through the smoothed Y median data starting from the second frame
        #segment_diff = Y_median_smooth[i + 1] - Y_median_smooth[i] # calculate the absolute difference between the current frame and the next frame
        if not change_ongoing_flag and abs(derived_data[i]) > zerotolerance: # if there is no ongoing change and threshold was exceeded
            
            for j in range(lookahead_frames):
                if i + j >= analyzed_data['frame_num'] - 1: # if we have reached the end of the data during lookahead, break out of the loop
                        break
                if abs(derived_data[i+j]) < zerotolerance: # if the change stabilizes in the lookahead, ignore the change
                     change_ongoing_flag = False
                     break
                if abs(derived_data[i]) > threshold:
                     change_ongoing_flag = True
            if change_ongoing_flag: #if the change occurs in the entire lookahead
                direction = 1 if derived_data[i] > 0 else -1 # determine the direction of the change based on the sign of the derivative
                changes[0].append(i) #mark the change start
            
        elif change_ongoing_flag: # if the change is currently ongoing
            if abs(derived_data[i]) <= zerotolerance: # if the change seems to have stopped
                stabilization_flag = True # initialize a flag to track whether the change has stabilized
                for j in range(release_frames): # look ahead for the specified number of frames to see if the change stopped 
                    if i + j >= analyzed_data['frame_num'] - 1: # if we have reached the end of the data during lookahead, break out of the loop
                        break
                    if abs(derived_data[i + j]) > threshold: # if the change continues within the lookahead period, consider it to be ongoing
                        stabilization_flag = False # reset the stabilization flag
                        break
                if stabilization_flag: # if the value has stabilized
                    changes[1].append(i) # mark the change end
                    change_ongoing_flag = False # reset the change ongoing flag
                    direction = 0 # reset the change direction variable 

            elif (direction == 1 and derived_data[i] < 0) or (direction == -1 and derived_data[i] > 0): # if the change direction reversed
                changes[1].append(i) # if the change continues, consider it to have ended and add the current frame to the list of detected changes
                i += 1    
                changes[0].append(i) # if the change continues, consider it to have started again and add the current frame to the list of detected changes
                direction = -direction # flip the change direction variable to reflect the change in direction
        
        i += 1 # if there is no change, move to the next frame
    return changes

analyzed_data = load_analysis_json() # load the analyzed data from a JSON file for testing purposes, will be replaced with the actual analysis function in the GUI later
for key in analyzed_data:
    print(key) # print the loaded analysis data keys

derived_data = derivative(analyzed_data['Y_median_smooth'], analyzed_data['frame_num']) # calculate the derivative of the smoothed Y median data for use in change detection

#powerful filter method, implement!
'''
for i in range(analyzed_data['frame_num'] -1): 
    if abs(derived_data[i]) < 0.012: # if the derived data is in the noise threshold
        derived_data[i] = 0 #floor the data
    elif abs(derived_data[i]) > 0.15: # if the derived data exceedes threshold
        if derived_data[i] < 0:
            derived_data[i] = -1 #highlight decreasing change, if negative
        else:
            derived_data[i] = 1 #highlight increasing change, if positive
'''
        
                  
threshold = 0.3 #set a threshold for change detection, can be adjusted in the GUI later
lookahead_frames = 7 #set the number of frames to look ahead for detecting ongoing changes, can be adjusted in the GUI later
release_frames = 5 #set the number of frames to look ahead for releasing ongoing changes, can be adjusted in the GUI later


changes = detect_changes(analyzed_data, threshold, lookahead_frames, release_frames) # perform change detection on the analyzed data with the specified threshold


plot_data = analyzed_data['Y_median_smooth'] # get the Y median data from the analyzed data
fig, ax = plt.subplots() # create a figure and axis for plotting
ax.plot(plot_data) # plot the Y median data
ax.set_xlabel('Frame Number') # set the x-axis label
ax.set_ylabel('Y Median') # set the y-axis label
ax.set_title('Y Median Over Time') # set the title of the plot

ax2 = ax.twinx() # create a second y-axis for plotting the derivative
ax2.plot(derived_data.get(), color='orange') # plot the derivative of the Y median data on the second y-axis
ax2.set_ylabel('Derivative of Y Median') # set the y-axis label for the second y-axis

if changes: # if there are detected changes, add vertical lines to the plot to indicate the start and end of the detected changes
    for change in changes[0]:
            plt.axvline(x=change, color='g', linestyle='--') # add a vertical line to indicate the start of the detected change
    for change in changes[1]:
            plt.axvline(x=change, color='r', linestyle='--') # add a vertical line to indicate the end of the detected change
plt.show() # display the plot