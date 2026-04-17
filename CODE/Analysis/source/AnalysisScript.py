

#### !!!!! RUNS ON PYTHON 3.12 !!!!!

import sys # sys for system functions
import cupy as cp #CuPy for GPU acceleration
import time #this is fucking obvious
import customtkinter as ctk #custom tkinter, pretty
import keyboard #keyboard input
import matplotlib.pyplot as plt #plotting
import os #os
import torch #pytorch
import ffmpeg #ffmpeg for video processing
import json #json for saving and loading analysis results
#import CODE.Gui_TopLevel as Gui_TopLevel #import the GUI code to integrate with the analysis script



class Analysis:
    def __init__(self, shot_path):
        self.shot_path = shot_path #path to the selected shot
        self.analysis_data = None #variable to store the analysis data for use in the GUI

    
    def opendata(self, analysis_path):
        self.analysis_path = analysis_path #path to the selected analysis results file
        with open(self.analysis_path, 'r') as f: #open the selected analysis results file
            self.analysis_data = json.load(f) #load the analysis data from the file and store it in a variable for use in the GUI
        return self.analysis_data #return the analysis data for use in the GUI