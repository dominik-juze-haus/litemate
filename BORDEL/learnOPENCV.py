import av
import cv2
import numpy as np
import time
import customtkinter as ctk
from CTkListbox import *

# List of test footage:
# _____________________
# ESN BOAT PARTY:
# JUZE0300.mxf
# JUZE0295.mxf
# JUZE0327.mxf

container = av.open('E:/ESN/2024-10-03 Boat Party/Footage/ProRes transcode/JUZE0327.mxf')
stream = container.streams.video[0]
frame_count = stream.frames
framerate = stream.base_rate
dur_in_sec = frame_count / framerate
waitkey = 1000/framerate



def rescale_frame(frame, percent=75):
    width = int(frame.width * percent / 100)
    height = int(frame.height * percent / 100)
    return frame.reformat(width=width, height=height)

def clip_duration_TC(dur_in_sec, framerate):
    TimeCode = {}  # 0 - hours, 1 - minutes, 2 - seconds, 3 - frames
    TimeCode[0] = int(dur_in_sec // 3600)  # hours
    TimeCode[1] = int((dur_in_sec % 3600) // 60)  # minutes
    TimeCode[2] = int(dur_in_sec % 60)  # seconds
    TimeCode[3] = int((dur_in_sec % 1) * framerate)  # frames
    return TimeCode

TimeCode = clip_duration_TC(dur_in_sec, framerate)
for frame in container.decode(video=0):
    img = frame.to_ndarray(format='bgr24')

    cv2.imshow('Frame', img)
    if cv2.waitKey(waitkey) & 0xFF == ord('q'):
        break

print(f"TC: {TimeCode[0]:02}:{TimeCode[1]:02}:{TimeCode[2]:02}:{TimeCode[3]:02}")
