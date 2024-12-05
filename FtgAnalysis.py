import sys
import cv2 as cv #OpenCV CPU only, for preview (only)
import numpy as np #nom nom pie
import ffmpeg #ffmpeg
import av #PyAV ffmpeg wrapper
import time #this is fucking obvious
import customtkinter as ctk #custom tkinter, pretty
from CTkListbox import * #listbox for custom tkinter


ctk.set_appearance_mode("system")
ctk.set_default_color_theme("green")
root = ctk.CTk()
root.title("Shot Architect")
root.geometry("1280x720")
#list of test footage:
#_____________________
#ESN BOAT PARTY:
#JUZE0300.mxf
#JUZE0295.mxf
#JUZE0327.mxf


class img_proc:
    def __init__(self, file_path): #Initialize
        self.file_path = file_path #assign the variable to the class variable
        self.clip = cv.VideoCapture(self.file_path) #open the footage file
        frame_count = int(self.clip.get(cv.CAP_PROP_FRAME_COUNT))
        framerate = self.clip.get(cv.CAP_PROP_FPS)
        dur_in_sec = frame_count / framerate
        
        def clip_duration_TC(dur_in_sec, framerate):
            TimeCode = {}  # 0 - hours, 1 - minutes, 2 - seconds, 3 - frames
            TimeCode[0] = int(dur_in_sec // 3600)  # hours
            TimeCode[1] = int((dur_in_sec % 3600) // 60)  # minutes
            TimeCode[2] = int(dur_in_sec % 60)  # seconds
            TimeCode[3] = int((dur_in_sec % 1) * framerate)  # frames
            return TimeCode
        
        TimeCode = clip_duration_TC(dur_in_sec, framerate)

    def WB_an(self, footage)



    
    


class GUI:






