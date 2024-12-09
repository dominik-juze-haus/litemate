import av
import av.video
import cv2
import numpy as np
import time

# List of test footage:
# _____________________
# ESN BOAT PARTY:
# JUZE0300.mxf
# JUZE0295.mxf
# JUZE0327.mxf

container = av.open('H:/ESN/2024-10-03 Boat Party/Footage/ProRes transcode/JUZE0300.mxf')
stream = container.streams.video[0]
frame_count = stream.frames
print(f"Frame count: {frame_count}")
framerate = stream.base_rate
dur_in_sec = frame_count / framerate
waitkey = int(1000/framerate-10)


def clip_duration_TC(dur_in_sec, framerate):
    TimeCode = {}  # 0 - hours, 1 - minutes, 2 - seconds, 3 - frames
    TimeCode[0] = int(dur_in_sec // 3600)  # hours
    TimeCode[1] = int((dur_in_sec % 3600) // 60)  # minutes
    TimeCode[2] = int(dur_in_sec % 60)  # seconds
    TimeCode[3] = int((dur_in_sec % 1) * framerate)  # frames
    return TimeCode

TimeCode = clip_duration_TC(dur_in_sec, framerate)
print(f"TC: {TimeCode[0]:02}:{TimeCode[1]:02}:{TimeCode[2]:02}:{TimeCode[3]:02}")

for frame in container.decode(video=0):
    img = frame.to_ndarray(format='bgr24')
    height, width = img.shape[:2]
    resized_img = cv2.resize(img, (int(width/2), int(height/2)))



    cv2.imshow('Frame', resized_img)
    if cv2.waitKey(waitkey) & 0xFF == ord('q'):
        break


