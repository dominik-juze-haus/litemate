import sys
import cv2 as cv #OpenCV CPU only, for preview (only)
import numpy as np #nom nom pie
import cupy as cp #CuPy for GPU acceleration
import ffmpeg #ffmpeg
import av #PyAV ffmpeg wrapper
import time #this is fucking obvious
import customtkinter as ctk #custom tkinter, pretty
import keyboard #keyboard input
import matplotlib.pyplot as plt #plotting
import os #os
import torch #pytorch
from CTkListbox import * #listbox for custom tkinter


#ctk.set_appearance_mode("system")
#ctk.set_default_color_theme("green")
#root = ctk.CTk()
#root.title("Shot Architect")
#root.geometry("1280x720")



paused = False
quit = False

fig = plt.figure(figsize=(10, 5))
ax1 = fig.add_subplot(1, 3, 1)
ax1.axis('off')
ax1.set_title('Footage')
ax2 = fig.add_subplot(1, 3, 2)
ax2.set_title('Histogram')
ax3 = fig.add_subplot(1, 3, 3)
ax3.set_title('Corrected Footage')




class Keybinds:
    def __init__(self):
        keyboard.on_press(self.toggle_pause)
        
    def toggle_pause(self, event):
        global paused
        if event.name == 'space':
            paused = not paused
    
    def quit(self, event):
        global quit
        if event.name == 'q':
            quit = True

class LoadFootage:
    def __init__(self, file_path): #Initialize
        self.file_path = file_path #assign the variable to the class variable
        self.container = av.open(r'I:\CODING\LiteMate\Footage\jarosovci_exposure_change.mov')
        self.stream = self.container.streams.video[0]
        self.fps = float(self.stream.average_rate)
        self.frame_count = self.stream.frames
        self.duration = self.stream.duration
    
        def classify_bit_depth(stream):
            stream = stream
            if stream.pix_fmt[-4:] == '10le':
                bit_depth = 10
            elif stream.pix_fmt[-4:] == '12le':
                bit_depth = 12

            return bit_depth
        
        #self.bit_depth = classify_bit_depth(self.stream)       ##The bit depth is set manually for now until the function is fixed
        self.bit_depth = 8
            




        """
        def clip_duration_TC(dur_in_sec, framerate):
            TimeCode = {}  # 0 - hours, 1 - minutes, 2 - seconds, 3 - frames
            TimeCode[0] = int(dur_in_sec // 3600)  # hours
            TimeCode[1] = int((dur_in_sec % 3600) // 60)  # minutes
            TimeCode[2] = int(dur_in_sec % 60)  # seconds
            TimeCode[3] = int((dur_in_sec % 1) * framerate)  # frames
            return TimeCode
        
        TimeCode = clip_duration_TC(dur_in_sec, framerate)
        """
    #def WB_an(self, footage)
"""
class Histogram_analysis:
    def __init__ (self, footage_array, resolution, bit_depth):
        self.footage_array = footage_array
        self.hist = plt.hist(np.zeros((resolution.height * resolution.width * 3,)), bins=2^bit_depth, range=(0, 2^bit_depth), color='r', alpha=0.5)
"""

LoadFootage_inst = LoadFootage(r'I:\CODING\LiteMate\Footage\jarosovci_exposure_change.mov')






class Analysis:
    def __init__(self, bit_depth, res_height, res_width, frame_count, fps):
        self.bit_depth = bit_depth
        self.res_height = res_height
        self.res_width = res_width
        self.frame_count = frame_count
        self.fps = fps

    def histogram(self, frame_array):
        self.frame_array = frame_array
        ax2.cla()
        ax2.set_title('Histogram')
        ax2.hist(self.frame_array.ravel(), bins = 2 ** self.bit_depth, range = (0, 2 ** self.bit_depth), color='r', alpha = 0.5)
        ax2.set_xlim(0, 2 ** self.bit_depth)
        ax2.set_ylim(0, self.res_height * self.res_width / 3 / 8)
        ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x / (self.res_height * self.res_width / 3 / 8) * 100)}%'))
        colors = ('r', 'g', 'b')
        for i, color in enumerate(colors):
            ax2.hist(self.frame_array[:, :, i].ravel(), bins=2 ** self.bit_depth, range=(0, 2 ** self.bit_depth), color=color, alpha=0.5, label=f'{color.upper()} channel')
        ax2.legend(loc='upper right')
        plt.pause(1 / self.fps)

"""       
    def normalize(self):
        self.frame_array = self.frame_array / 2**LoadFootage_inst.bit_depth
        return self.frame_array
    
    def get_luminance(self):
        self.luminance = 0.2126 * self.frame_array[0] + 0.7152 * self.frame_array[1] + 0.0722 * self.frame_array[2]
        return self.luminance
    
    def get_chrominance(self):
        self.chrominance = self.frame_array - self.luminance
        return self.chrominance
    
    def get_histogram(self):
        self.histogram = torch.histc(self.luminance, bins=2**LoadFootage_inst.bit_depth, min=0, max=1)
        return self.histogram
    
    def get_mean(self):
        self.mean = torch.mean(self.luminance)
        return self.mean
    
    def get_std(self):
        self.std = torch.std(self.luminance)
        return self.std
    
    def get_variance(self):
        self.variance = torch.var(self.luminance)
        return self.variance
    
    def get_skewness(self):
        self.skewness = torch.mean((self.luminance - self.mean) ** 3) / self.std ** 3
        return self.skewness
    
    def get_kurtosis(self):
        self.kurtosis = torch.mean((self.luminance - self.mean) ** 4) / self.std ** 4
        return self.kurtosis
"""  

Analysis_inst = Analysis(LoadFootage_inst.bit_depth, LoadFootage_inst.stream.height,
                         LoadFootage_inst.stream.width, LoadFootage_inst.frame_count, 
                         LoadFootage_inst.fps)



class Playback:
    def __init__(self):
        self.container = LoadFootage_inst.container
        
    def get_frame(self, frame_number): #Get specific frame from the footage
        frame_t = int(frame_number / LoadFootage_inst.fps / LoadFootage_inst.stream.time_base) #Calculate the time of the frame precisely on the timebase
        self.container.seek(frame_t, any_frame=True, stream=LoadFootage_inst.stream) #Seek to the frame

        for frame in self.container.decode(video=0): #Iterate through the frames
            if frame.pts is not None and frame.pts >= frame_number: 
                frame_array = frame.to_ndarray(format='rgb24') #Convert the frame to an array
                Analysis_inst.histogram(frame_array)
                ax1.cla()
                ax1.axis('off')
                ax1.set_title('Footage')
                ax1.imshow(frame_array)
                return frame_array #Return the frame array
            
    def play_forward(self): #Play the footage
        
        for frame in self.container.decode(video=0): # !!!! Untested CODE !!!!
            global paused
            global quit
            if quit:
                break                
            while paused:
                plt.pause(0.1)
            frame_array = frame.to_ndarray(format='rgb24')
            Analysis_inst.histogram(frame_array)
            ax1.cla()
            ax1.axis('off')
            ax1.set_title('Footage')
            ax1.imshow(frame_array)
            plt.pause(1 / LoadFootage_inst.fps)

keybings_instance = Keybinds()        
playback_instance = Playback()


#analysis_instance = Analysis(playback_instance.get_frame(300))
#playback_instance.play_forward()
playback_instance.get_frame(300)

plt.show()




#Histogram_analysis_inst = Histogram_analysis(, LoadFootage_inst.stream, LoadFootage_inst.bit_depth)


"""
class GUI:

"""




