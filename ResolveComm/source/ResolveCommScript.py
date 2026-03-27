#### !!!!! RUNS ON PYTHON 3.6 !!!!!

import lib.Resolve.python_get_resolve as pyResolve #import the python_get_resolve script to get the DaVinci Resolve object
import lib.Resolve.DaVinciResolveScript as ResolveScript #import the DaVinci Resolve scripting module
import Analysis.source.AnalysisScript as AnalysisScript #import the AnalysisScript to use the Analysis class and Playback class
import numpy as np
import time
import tkinter as tk



class ApplyMarkers:
    ###Placeholder!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    def __init__(self, resolve):
        self.resolve = resolve
        self.project_manager = self.resolve.GetProjectManager()
        self.project = self.project_manager.GetCurrentProject()
        self.timeline = self.project.GetCurrentTimeline()
        self.markers = self.timeline.GetMarkers()

    ###Placeholder!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    def apply_markers(self, frame_number):
        if frame_number in self.markers:
            marker = self.markers[frame_number]
            color = marker['color']
            name = marker['name']
            note = marker['note']
            print(f"Marker at frame {frame_number}: Color: {color}, Name: {name}, Note: {note}")


class RequestAnalysis:
    ###Placeholder!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    def __init__(self, resolve):
        self.resolve = resolve
        self.project_manager = self.resolve.GetProjectManager()
        self.project = self.project_manager.GetCurrentProject()
        self.timeline = self.project.GetCurrentTimeline()
        self.playback = AnalysisScript.Playback() #initialize the Playback class from the AnalysisScript
    
