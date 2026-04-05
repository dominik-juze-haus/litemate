#### !!!!! RUNS ON PYTHON 3.12 !!!!!

import sys # sys for system functions
import cupy as cp #CuPy for GPU acceleration
import time #this is fucking obvious
import customtkinter as ctk #custom tkinter, pretty
import keyboard #keyboard input
import matplotlib.pyplot as plt #plotting
import os #os
import torch #pytorch
from torchcodec.decoders import VideoDecoder #pytorch video decoder
import lib.guibuild as gui #import the guiBuild class from the guibuild script


gui.guiBuild().mainloop() #start the GUI main loop

decoder = VideoDecoder(gui.guiBuild().shot_path) #initialize the video decoder with the path to the video file