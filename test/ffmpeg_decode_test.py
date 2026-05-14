import av
import cupy as cp #CuPy for GPU acceleration
import keyboard #keyboard input
import matplotlib.pyplot as plt #plotting
import re

import ffmpeg #ffmpeg for video processing

import json #json for saving and loading analysis results
from tkinter import filedialog

footage_path = filedialog.askopenfilename(title="Select Footage", filetypes=[("Video files", "*.mov *.mp4 *.avi *.mkv *.wmv *.flv *.mxf")]) # open file dialog to select footage

class Analysis:
    ## ________ FFMPEG-PYTHON VERSION ________ ##
        
    def __init__(self, shot_path):
        self.shot_path = shot_path #path to the selected shot
        self.analysis_data = None #variable to store the analysis data for use in the GUI
        self.probe = ffmpeg.probe(self.shot_path)
        self.video_stream = next((stream for stream in self.probe['streams'] if stream['codec_type'] == 'video'), None)
        self.width = int(self.video_stream['width'])
        self.height = int(self.video_stream['height'])
        self.container = av.open(self.shot_path) # open the selected footage with PyAV
        self.stream = self.container.streams.video[0] # get the first video stream from the container

        self.frame_count = int(self.video_stream['nb_frames'])
        self.bit_depth = int(self.video_stream[''])
        
    def decoder_signalstats(self):
        out = (
            ffmpeg
            .input(self.shot_path)
            .filter('scale', 320, -1)
            .filter('signalstats')
            .filter("metadata", "print")
            .output("null", f="null")
            .run_async(pipe_stderr=True)
        )
        
        
        pattern = r'YAVG=([\d\.]+)'
        yavg_values = []

        for line in out.stderr:
            line = line.decode("utf-8")

            match = re.search(pattern, line)

            if match:
                yavg_values.append(float(match.group(1)))

        if len(yavg_values) == self.frame_count: # if the number of Y average values matches the total frame count of the video, return the Y average values for use in the GUI, otherwise show an error message
            return yavg_values
        else:
            print("Error: Inconsistent frame count.")
            return None

plot_data = Analysis(footage_path).decoder_signalstats()
plt.plot(plot_data) # plot the Y median data
plt.xlabel('Frame Number') # set the x-axis label
plt.ylabel('Y Median') # set the y-axis label
plt.title('Y Median Over Time') # set the title of the plot
""" if changes: # if there are detected changes, add vertical lines to the plot to indicate the start and end of the detected changes
    for change in changes[0]:
            plt.axvline(x=change, color='r', linestyle='--') # add a vertical line to indicate the start of the detected change
    for change in changes[1]:
            plt.axvline(x=change, color='g', linestyle='--') # add a vertical line to indicate the end of the detected change
"""
plt.show() # display the plot