import sys
import cv2 as cv #OpenCV CPU only, for preview (only)
import numpy as np #nom nom pie
import cupy as cp #CuPy for GPU acceleration
<<<<<<< HEAD
import ffmpeg #ffmpeg
=======
>>>>>>> 7cc73a0 (DEV 2026-03-26)
import av #PyAV ffmpeg wrapper
import time #this is fucking obvious
import customtkinter as ctk #custom tkinter, pretty
import keyboard #keyboard input
import matplotlib.pyplot as plt #plotting
import os #os
import torch #pytorch
from CTkListbox import * #listbox for custom tkinter


container = av.open(r'I:\CODING\LiteMate\Footage\pyxis_exposure_change.mov')
stream = container.streams.video[0]
fps = float(stream.average_rate)
time_base = stream.time_base
frame_count = stream.frames
print(f"Frame count: {frame_count}")


#curent_frame
#frame_number = stream.frames - 10
frame_number = 340
frame_t = int(frame_number / fps / time_base)
container.seek(frame_t, any_frame=False, stream=stream)

for frame in container.decode(stream):
    if frame.pts is not None and frame.pts >= frame_number: 
        frame_array = frame.to_ndarray(format='rgb24')
        break

#reference_frame
#frame_number = 30
frame_number = 500
frame_t = int(frame_number / fps / time_base)
container.seek(frame_t, any_frame=False, stream=stream)

for frame in container.decode(stream):
    if frame.pts is not None and frame.pts >= frame_number: 
        reference_frame_array = frame.to_ndarray(format='rgb24')
        break


mean_frame_array = np.mean(frame_array)
median_frame_array = np.median(frame_array)

mean_reference_frame_array = np.mean(reference_frame_array)
median_reference_frame_array = np.median(reference_frame_array)

print(f"Mean of frame_array: {mean_frame_array}")
print(f"Median of frame_array: {median_frame_array}")
print(f"Mean of reference_frame_array: {mean_reference_frame_array}")
print(f"Median of reference_frame_array: {median_reference_frame_array}")

mean_diff = mean_frame_array - mean_reference_frame_array
median_diff = median_frame_array - median_reference_frame_array
print(f"Mean difference: {mean_diff}")
print(f"Median difference: {median_diff}")

lift = 50 #vals from 0 to 100
gamma = 50
gain = 50 #vals from 0 to 100

#median version
gamma = np.log10(median_reference_frame_array) / np.log10(median_frame_array)
#mean version
#gamma = np.log10(mean_reference_frame_array) / np.log10(mean_frame_array)
if np.abs(median_diff) <= 10:
    gamma = 0
    

    

bit_lift = 0 +((2*lift-100) / 100)
#bit_gamma = 1 + ((2*gamma-100) / 100)
bit_gamma = 2
bit_gain = 1 + ((2*gain-100) / 100)
if bit_gamma == 0:  
    bit_gamma = 0.01

#print(frame_array)
corr_frame_array = ((((frame_array / 255.0) + bit_lift * (1-(frame_array / 255.0))) * bit_gain) ** (1.0 / bit_gamma) * 255.0).astype(np.uint32)  # Apply the correction and convert to integers
#print(corr_frame_array)

frame_array = np.clip(frame_array, 0, 255)
corr_frame_array = np.clip(corr_frame_array, 0, 255)

ploth = 3
plotw = 2

fig = plt.figure(figsize=(15, 10))  # Increased the figure size
ax1 = fig.add_subplot(ploth, plotw, 1)
ax1.axis('off')
ax1.set_title('Footage')
ax1.imshow(frame_array)

ax2 = fig.add_subplot(ploth, plotw, 2)
ax2.set_title('Histogram')
ax2.hist(frame_array.ravel(), bins=256, range=(0, 256), color='gray', alpha=0.5)
ax2.set_xlim([0, 256])
ax2.set_ylim([0, 200000])  # Adjust the y-axis limit to see higher value spikes
ax2.yaxis.set_visible(False)
ax2.grid(False)  # Turn off the grid

ax3 = fig.add_subplot(ploth, plotw, 3)
ax3.axis('off')
ax3.set_title('Corrected Footage')
ax3.imshow(corr_frame_array)

ax4 = fig.add_subplot(ploth, plotw, 4)
ax4.set_title('Corrected Histogram')
ax4.hist(corr_frame_array.ravel(), bins=256, range=(0, 256), color='gray', alpha=0.5)
ax4.set_xlim([0, 256])
ax4.set_ylim([0, 200000])  # Adjust the y-axis limit to see higher value spikes
ax4.yaxis.set_visible(False)
ax4.grid(False)  # Turn off the grid

ax5 = fig.add_subplot(ploth, plotw, 5)
ax5.axis('off')
ax5.set_title('Reference Footage')
ax5.imshow(reference_frame_array)

ax6 = fig.add_subplot(ploth, plotw, 6)

ax6.set_title('Reference Histogram')
ax6.hist(reference_frame_array.ravel(), bins=256, range=(0, 256), color='gray', alpha=0.5)
ax6.set_xlim([0, 256])
ax6.set_ylim([0, 200000])  # Adjust the y-axis limit to see higher value spikes
ax6.yaxis.set_visible(False)
ax6.grid(False)  # Turn off the grid

if np.array_equal(frame_array, corr_frame_array):
    print('no change')
else:
    print('image changed')

plt.show()
