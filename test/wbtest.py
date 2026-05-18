import sys
#import cv2 as cv #OpenCV CPU only, for preview (only)
import numpy as np #nom nom pie
import scipy as sp #scipy
import cupy as cp #CuPy for GPU acceleration
import ffmpeg #ffmpeg
import av #PyAV ffmpeg wrapper
import time #this is fucking obvious
import customtkinter as ctk #custom tkinter, pretty
import keyboard #keyboard input
import matplotlib.pyplot as plt #plotting
import os #os
#import torch #pytorch
import json #json
#from CTkListbox import * #listbox for custom tkinter


CCT_to_RGB_table = json.load(open(r"I:\CODING\LiteMate\litemate\test\CODE\Analysis\lib\CCT\kelvin_table.json")) #CCT to RGB values
table_temps = np.array(list(CCT_to_RGB_table.keys()), dtype=int) #CCT values as integers
table_rgb_vals = np.array(list(CCT_to_RGB_table.values())) #RGB values



container = av.open(r'I:\CODING\LiteMate\Footage\pyxis_temp_change.mov')
stream = container.streams.video[0]
fps = float(stream.average_rate)
time_base = stream.time_base
frame_count = stream.frames
print(f"Frame count: {frame_count}")


#curent_frame
#frame_number = stream.frames - 10
frame_number = 277
frame_t = int(frame_number / fps / time_base)
container.seek(frame_t, any_frame=False, stream=stream)

for frame in container.decode(stream):
    if frame.pts is not None and frame.pts >= frame_number: 
        frame_array = frame.to_ndarray(format='rgb24')
        break

#reference_frame
frame_number = 72
#frame_number = stream.frames - 50
frame_t = int(frame_number / fps / time_base)
container.seek(frame_t, any_frame=False, stream=stream)

for frame in container.decode(stream):
    if frame.pts is not None and frame.pts >= frame_number: 
        reference_frame_array = frame.to_ndarray(format='rgb24')
        break


#Mean and median calculation
#Frame array:
mean_frame_array = np.mean(frame_array, axis=(0, 1)) #axis 0 is for rows, axis 1 is for columns
median_frame_array = np.median(frame_array, axis=(0, 1)) 
#Reference frame array:
mean_reference_frame_array = np.mean(reference_frame_array, axis=(0, 1))
median_reference_frame_array = np.median(reference_frame_array, axis=(0, 1))

print(f"Mean of frame_array (R, G, B): {mean_frame_array}")
print(f"Median of frame_array (R, G, B): {median_frame_array}")
print(f"Mean of reference_frame_array (R, G, B): {mean_reference_frame_array}")
print(f"Median of reference_frame_array (R, G, B): {median_reference_frame_array}")

mean_diff = mean_frame_array - mean_reference_frame_array
median_diff = median_frame_array - median_reference_frame_array
print(f"Mean difference (R, G, B): {mean_diff}")
print(f"Median difference (R, G, B): {median_diff}")

#CCT calculation
#CIE XYZ calculation
#Frame array:
X_CIE_frame_array = (-0.14282 * median_frame_array[0] + 1.54924 * 
                     median_frame_array[1] - 0.95641 * median_frame_array[2])
Y_CIE_frame_array = (-0.32466 * median_frame_array[0] + 1.57837 * 
                     median_frame_array[1] - 0.73191 * median_frame_array[2])
Z_CIE_frame_array = (-0.68202 * median_frame_array[0] + 0.77073 *
                        median_frame_array[1] + 0.56332 * median_frame_array[2])
#Reference frame array:
X_CIE_reference_frame_array = (-0.14282 * median_reference_frame_array[0] + 1.54924 *
                                 median_reference_frame_array[1] - 0.95641 * median_reference_frame_array[2])
Y_CIE_reference_frame_array = (-0.32466 * median_reference_frame_array[0] + 1.57837 *
                                 median_reference_frame_array[1] - 0.73191 * median_reference_frame_array[2])
Z_CIE_reference_frame_array = (-0.68202 * median_reference_frame_array[0] + 0.77073 *
                                    median_reference_frame_array[1] + 0.56332 * median_reference_frame_array[2])


#CIE chromaticity coordinates calculation
#Frame array:
x_frame_array = X_CIE_frame_array / (X_CIE_frame_array + Y_CIE_frame_array + Z_CIE_frame_array)
y_frame_array = Y_CIE_frame_array / (X_CIE_frame_array + Y_CIE_frame_array + Z_CIE_frame_array)
#Reference frame array:
x_reference_frame_array = X_CIE_reference_frame_array / (X_CIE_reference_frame_array + Y_CIE_reference_frame_array + Z_CIE_reference_frame_array)
y_reference_frame_array = Y_CIE_reference_frame_array / (X_CIE_reference_frame_array + Y_CIE_reference_frame_array + Z_CIE_reference_frame_array)


#n calculation
#Frame array:
n_frame_array = (((0.23881 * median_frame_array[0]) + (0.25499 * median_frame_array[1]) - 0.58291 * median_frame_array[2]) / 
                ((0.11109 * median_frame_array[0]) + (0.81399 * median_frame_array[1]) + 0.02091 * median_frame_array[2]))
#Reference frame array:
n_reference_frame_array = (((0.23881 * median_reference_frame_array[0]) + (0.25499 * median_reference_frame_array[1]) - 0.58291 * median_reference_frame_array[2]) / 
                ((0.11109 * median_reference_frame_array[0]) + (0.81399 * median_reference_frame_array[1]) + 0.02091 * median_reference_frame_array[2]))


#CCT calculation
#Frame array:
CCT_frame_array = 449 * n_frame_array ** 3 + 3525 * n_frame_array ** 2 - 6823.3 * n_frame_array + 5520.33
#Reference frame array:
CCT_reference_frame_array = 449 * n_reference_frame_array ** 3 + 3525 * n_reference_frame_array ** 2 - 6823.3 * n_reference_frame_array + 5520.33


print(f"CCT of frame_array: {CCT_frame_array}")                     #CCT of frame_array
print(f"CCT of reference_frame_array: {CCT_reference_frame_array}") #CCT of reference_frame_array

#CCT difference calculation
CCT_diff = CCT_frame_array - CCT_reference_frame_array
print(f"CCT difference: {CCT_diff}")



#Obtain the RGB gain values of the CCT difference
interp_red = sp.interpolate.interp1d(table_temps, table_rgb_vals[:, 0], kind='cubic')
interp_green = sp.interpolate.interp1d(table_temps, table_rgb_vals[:, 1], kind='cubic')
interp_blue = sp.interpolate.interp1d(table_temps, table_rgb_vals[:, 2], kind='cubic')

CCT_diff_red = np.ceil(interp_red(np.round(np.abs(CCT_diff)/10)*10))
CCT_diff_green = np.ceil(interp_green(np.round(np.abs(CCT_diff)/10)*10))
CCT_diff_blue = np.ceil(interp_blue(np.round(np.abs(CCT_diff)/10)*10))

#print(f"CCT difference RGB values (interpolation): {CCT_diff_red}, {CCT_diff_green}, {CCT_diff_blue}")


#Chromatic adaptation
m_bradford = np.array([[0.8951, 0.2664, -0.1614],
                        [-0.7502, 1.7135, 0.0367],
                        [0.0389, -0.0685, 1.0296]])

#WB gain values
gain_red = median_reference_frame_array[0] / median_frame_array[0]
gain_green = median_reference_frame_array[1] / median_frame_array[1]
gain_blue = median_reference_frame_array[2] / median_frame_array[2]


#White balance correction
corr_frame_array = (np.zeros_like(frame_array)).astype(np.uint32)
corr_frame_array[:,:,0] = frame_array[:,:,0] * gain_red
corr_frame_array[:,:,1] = frame_array[:,:,1] * gain_green
corr_frame_array[:,:,2] = frame_array[:,:,2] * gain_blue

#Clipping the values to 0-255
frame_array = np.clip(frame_array, 0, 255)
corr_frame_array = np.clip(corr_frame_array, 0, 255)

#Plotting
#plot dimensions (number of rows and columns)
ploth = 3   #plot height
plotw = 4   #plot width

colors = ('r', 'g', 'b') #colors for the histograms

#frame_array
fig = plt.figure(figsize=(10, 5))
ax1 = fig.add_subplot(ploth, plotw, 1)
ax1.axis('off')
ax1.set_title('Footage')
ax1.imshow(frame_array)

#frame array rgb histograms
for i, color in enumerate(colors):
    ax = fig.add_subplot(ploth, plotw, 2 + i)
    ax.set_title(f'{color.upper()} Channel')
    ax.hist(frame_array[:, :, i].ravel(), bins=256, range=(0, 256), color=color, alpha=0.5)
    ax.set_xlim([0, 256])
    ax.set_ylim([0, 80000])  # Adjust the y-axis limit to see higher value spikes
    ax.yaxis.set_visible(False)
    ax.grid(False)  # Turn off the grid

#corrected_frame_array
ax4 = fig.add_subplot(ploth, plotw, 5)
ax4.axis('off')
ax4.set_title('Corrected Footage')
ax4.imshow(corr_frame_array)

#corrected frame array rgb histograms
for i, color in enumerate(colors):
    ax = fig.add_subplot(ploth, plotw, 6 + i)
    ax.hist(corr_frame_array[:, :, i].ravel(), bins=256, range=(0, 256), color=color, alpha=0.5)
    ax.set_xlim([0, 256])
    ax.set_ylim([0, 80000])  # Adjust the y-axis limit to see higher value spikes
    ax.yaxis.set_visible(False)
    ax.grid(False)  # Turn off the grid

#reference_frame_array
ax7 = fig.add_subplot(ploth, plotw, 9)
ax7.axis('off')
ax7.set_title('Reference Frame')
ax7.imshow(reference_frame_array)

#reference frame array rgb histograms
for i, color in enumerate(colors):
    ax = fig.add_subplot(ploth, plotw, 10 + i)
    ax.hist(reference_frame_array[:, :, i].ravel(), bins=256, range=(0, 256), color=color, alpha=0.5)
    ax.set_xlim([0, 256])
    ax.set_ylim([0, 80000])  # Adjust the y-axis limit to see higher value spikes
    ax.yaxis.set_visible(False)
    ax.grid(False)  # Turn off the grid



#Checking if the image changed
if np.array_equal(frame_array, corr_frame_array):
    print('no change')
else:
    print('image changed')

#Displaying the plots
plt.show()


## DUMPING ALGS FROM THE MAIN CODE

"""
def RGB_analyze(self):
        RGB_avg_values = cp.zeros((self.frame_count, 3)) #create an array to store the RGB average values for each frame


        for frame, i in zip(self.container.decode(self.stream), range(self.frame_count)):
            frame_array = cp.frombuffer(frame.to_ndarray(format='rgb24'), cp.uint8).reshape([self.height, self.width, 3]) # convert the frame to a CuPy array in RGB format

            #RGB_histogram = cp.histogramdd(frame_array.reshape(-1, 3), bins=256, range=((0, 255), (0, 255), (0, 255))) # calculate the histogram of the RGB values for the current frame


            #Y_histogram, _ = cp.histogram(Y_plane, bins=256, range=(0, 255)) # calculate the histogram of the Y plane for the current frame


            RGB_avg_values[i, 0:] = cp.median(frame_array, axis=(0, 1)) #RGB median of the current frame           

        
        return RGB_avg_values # return the analyzed data for use in the GUI
"""
