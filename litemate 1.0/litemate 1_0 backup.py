#!/usr/bin/env python

# PREPARE RESOLVE SCRIPT ENVIRONMENT
import DaVinciResolveScript as dvr_script


resolve = dvr_script.scriptapp("Resolve")
fusion = resolve.Fusion()


# IMPORT LIBRARIES
import customtkinter as ctk #customtkinter is a library for creating modern and customizable GUIs in Python, built on top of the standard tkinter library
import tkinter as tk #standard tkinter library for creating GUIs in Python, used for some additional functionality such as message boxes and file dialogs
import ffmpeg #ffmpeg is a library for video processing and analysis, used for analyzing the footage in the Analysis class
import re #re is a library for working with regular expressions in Python, used for parsing the output of ffmpeg to extract the analysis data in the Analysis class
import av #PyAV is a Pythonic binding for the FFmpeg libraries, used for video processing and analysis in the Analysis class
import cupy as cp #CuPy is a library for GPU-accelerated computing with a NumPy-like API
from tkinter import filedialog #file dialog module from tkinter for opening file dialogs to select shots and analysis results files in the GUI
import matplotlib.pyplot as plt #matplotlib is a library for creating static, animated, and interactive visualizations in Python, used for plotting the analysis results in the GUI
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg #matplotlib backend for embedding plots in Tkinter applications, used for displaying the analysis results plot in the GUI
import keyboard #keyboard is a library for detecting and simulating keyboard events in Python, used for implementing keyboard shortcuts in the GUI (not yet implemented)
import json #json is a library for working with JSON data in Python, used for loading and saving analysis results in JSON format in the Analysis class
import os #os is a library for interacting with the operating system in Python, used for file path manipulations and other OS-related functionality in the GUI and Analysis class
import colorsys #colorsys is a library for converting between different color systems in Python, used for converting CCT values to RGB values in the Analysis class (not yet implemented)

default_bg_color = "#001523"
default_fg_color = "#001523"
default_widget_color = "#0082A5"
version = "0.1.0"




### ________________G U I   T O P L E V E L   C L A S S________________ ###

class GuiBuild(ctk.CTk):
# ---- Initialization and project setup page setup
    def __init__(self):
        super().__init__() #initialize the parent class (CTk)

        ## --------UPDATE WINDOW ICON PATH!!!!!!!!!!!!!--------
        #self.after(201, lambda :self.iconbitmap(r'C:\ZCoding\litemate\icon.ico')) #set the window icon after a short delay to ensure it loads correctly
        # ---- DEFAULT VARIABLES ----
        
        self.shot_path, self.reference_frame_num = DaVinci().getvideo() #variable to store the selected shot path    
        self.analysis_data = None #variable to store the analysis data for use in the GUI

        self.geometry('600x400')
        self.configure(bg_color=default_bg_color, fg_color=default_fg_color) #configure the background color of the window

        self.home = ctk.CTkFrame(self) #create a frame for the home page
        self.home.pack(fill="both", expand=True) #pack the frame to fill the entire window and allow it to expand
        self.home.configure(bg_color=default_bg_color, fg_color=default_fg_color) #configure the background color of the home frame

        self.title(f"LiteMate {version}") #set the title of the window
        self.project_setup_page()

# ---- MAIN PAGE AND FUNCTION DEFINITIONS ----
    def project_setup_page(self):
        self.project_setup_page_frame = ctk.CTkFrame(master = self.home) #frame for the project setup page, master is the home frame
        self.project_setup_page_frame.configure(bg_color=default_bg_color, fg_color=default_fg_color) #configure the background color of the project setup page frame
        self.project_setup_page_frame.pack(side="top", fill="both", expand=True, anchor="center") #pack the project setup page frame to fill the entire home frame and allow it to expand

        # --- Shot selection from files ---
        
        #selected shot path label ----
        self.selected_shot_path_label = ctk.CTkLabel(master = self.project_setup_page_frame, 
                                                     text=self.shot_path, font=ctk.CTkFont(size=16)) #label to display the selected shot path
        self.selected_shot_path_label.pack(side="top", padx=20, pady=10) #pack the selected shot path label to the top of the project setup page frame with padding
        
        """
        #shot selection button ----
        self.select_shot_button = ctk.CTkButton(master = self.project_setup_page_frame, 
                                                text="Manually Select Shot", 
                                                font=ctk.CTkFont(size=20), 
                                                fg_color=default_widget_color,
                                                command=self.select_shot_path) #button to open a project
        self.select_shot_button.pack(side="top", padx=20, pady=10) #pack the open project button to the top of the project setup page frame with padding
        """
        self.analysis_settings_widgets(self.project_setup_page_frame) #call the function to create the analysis settings widgets in the project setup page frame
        
        
        # Analysis button frame ----
        self.analysis_button_frame = ctk.CTkFrame(master = self.project_setup_page_frame) #frame for the analysis button
        self.analysis_button_frame.configure(bg_color=default_bg_color, fg_color=default_fg_color) #configure the background color of the analysis button frame
        self.analysis_button_frame.pack(side="top") #pack the analysis button frame to fill the entire project setup page frame and allow it to expand
        
        # Import analysis results button ----
        self.import_analysis_results_button = ctk.CTkButton(master = self.analysis_button_frame, 
                                                            text="Import Analysis", 
                                                            font=ctk.CTkFont(size=20), 
                                                            fg_color=default_widget_color,
                                                            command=self.import_analysis) #button to import analysis results, will be replaced with a function to import the actual analysis results
        self.import_analysis_results_button.grid(row=0, column=1, padx=10, pady=10, sticky="ew") #grid the import analysis results button in the analysis button frame
        
        # --- Start analysis button ---
        self.start_analysis_button = ctk.CTkButton(master = self.analysis_button_frame, 
                                                  text="Start Analysis", 
                                                  font=ctk.CTkFont(size=20), 
                                                  fg_color=default_widget_color,
                                                  command=self.start_analysis) #button to start the analysis
        self.start_analysis_button.grid(row=0, column=2, padx=10, pady=10, sticky="ew") #grid the start analysis button in the analysis button frame


# ----- SHOW ANALYSIS DATA PAGE -----
    def show_analysis_data_page(self, Y_changes, RGB_changes, Y_avg_values, RGB_avg_values):
        
        
        selected_analyses = [var.get() for var in self.analysis_selection_tkvar] #get the values of the analysis selection checkboxes
        
        print(Y_avg_values)


        # CLEAR THE HOME FRAME
        self.clear_home_frame() #call the function to clear the home frame before displaying the analysis results, will be replaced with a function to clear the home frame when navigating between pages in the GUI
        
        # PREPARE SUBPLOT
        results_plot_fig, graph = plt.subplots() #create a figure for the analysis results plot

        # PREPARE THE GRAPH CANVAS
        self.graph_canvas = FigureCanvasTkAgg(results_plot_fig, master=self.home) #create a canvas to display the analysis results plot in the GUI
        self.graph_canvas.get_tk_widget().pack(side="top", fill="both", expand=True) #pack the canvas to fill the entire home frame and allow it to expand
        
       
        if selected_analyses[0]: #if white balance analysis is selected, plot the white balance analysis results
            graph.plot(range(len(RGB_avg_values)), RGB_avg_values[:, 1], label='Red', color='red') #plot the red channel median values from the analysis data
            graph.plot(range(len(RGB_avg_values)), RGB_avg_values[:, 2], label='Green', color='green') #plot the green channel median values from the analysis data
            graph.plot(range(len(RGB_avg_values)), RGB_avg_values[:, 3], label='Blue', color='blue') #plot the blue channel median values from the analysis data

        if selected_analyses[1]: #if exposure analysis is selected, plot the exposure analysis results
            graph.plot(range(len(Y_avg_values)), Y_avg_values, label='Y Median', color='orange') #plot the Y channel median values from the analysis data
            for change in Y_changes[0]: #if there are detected changes in the Y channel, add vertical lines to the plot to indicate the start of the detected changes
                graph.axvline(x=change, color='g', linestyle='--') #add a vertical line to indicate the start of the detected change

        
        graph.axvline(x=self.reference_frame_num, color='k', linestyle='--', label='Reference Frame') #plot a vertical line to indicate the reference frame based on the reference frame flag in the analysis data


        
        self.graph_canvas.draw() #draw the analysis results plot on the canvas
        


## ----- WIDGETS COMMANDS AND FUNCTIONS FOR THE GUI -----

# Function to start the frame by frame analysis
    def start_analysis(self):
        selected_analyses = [var.get() for var in self.analysis_selection_tkvar] #get the values of the analysis selection checkboxes
        
        if not any([self.shot_path]): #if no shot is selected, show a warning message
            tk.messagebox.showwarning("No Shot Selected", "Please select a shot to start the analysis.")
            return

        if not any(selected_analyses): #if no analyses are selected, show a warning message
            tk.messagebox.showwarning("No Analysis Selected", "Please select at least one analysis to start.")
            return
        
        if selected_analyses[0] and selected_analyses[1]: #if both analyses are selected, print messages (placeholder for starting the analyses)
            print("Selected WB and Exposure...") #placeholder for starting the white balance analysis
        elif selected_analyses[0]: #if only white balance analysis is selected, print a message (placeholder for starting the white balance analysis)
            print("Selected WB...") #placeholder for starting the white balance analysis
        elif selected_analyses[1]: #if only exposure analysis is selected, print a message (placeholder for starting the exposure analysis)
            print("Selected Exposure...") #placeholder for starting the exposure analysis
        
               
        # Get the parameter values from the entry boxes and validate them
        threshold_text = self.threshold_textbox.get().strip()
        if threshold_text == "":
            tk.messagebox.showwarning("No Threshold Value", "Please enter a threshold value.")
            return
        try:
            self.change_threshold = float(threshold_text)
        except ValueError:
            tk.messagebox.showwarning("Invalid Threshold Value", "Please enter a valid float threshold value.")
            return
        

        lookahead_text = self.lookahead_textbox.get().strip()
        if lookahead_text == "":
            tk.messagebox.showwarning("No Lookahead Value", "Please enter a lookahead value.")
            return
        try:            
            self.lookahead_frames = int(lookahead_text)
        except ValueError:
            tk.messagebox.showwarning("Invalid Lookahead Value", "Please enter a valid integer lookahead value.")
            return
        

        release_text = self.release_textbox.get().strip()
        if release_text == "":
            tk.messagebox.showwarning("No Release Value", "Please enter a release value.")
            return
        try:
            self.release_frames = int(release_text)
        except ValueError:
            tk.messagebox.showwarning("Invalid Release Value", "Please enter a valid integer release value.")
            return
        
        
        
        


        Y_changes, RGB_changes, Y_avg_values, RGB_avg_values = Analysis(self.shot_path).detect_changes(selected_analyses, self.change_threshold, self.lookahead_frames, self.release_frames) #call the detect_changes function from the Analysis class to perform change detection on the analyzed data with a specified threshold and store the results in a variable for use in the GUI
        print("Analysis completed. Displaying results...") #placeholder for displaying the analysis results, will be replaced with the actual function to display the analysis results in the GUI
        
        self.show_analysis_data_page(Y_changes, RGB_changes, Y_avg_values, RGB_avg_values) #call the show_analysis_data function to display the

# Analysis import
    def import_analysis(self):
        selected_analyses = [var.get() for var in self.analysis_selection_tkvar] #get the values of the analysis selection checkboxes

        if not any(selected_analyses): #if no analyses are selected, show a warning message
            tk.messagebox.showwarning("No Analysis Selected", "Please select at least one analysis to start.")
            return
        
        if selected_analyses[0] and selected_analyses[1]: #if both analyses are selected, print messages (placeholder for starting the analyses)
            print("Selected WB and Exposure...") #placeholder for starting the white balance analysis
        elif selected_analyses[0]: #if only white balance analysis is selected, print a message (placeholder for starting the white balance analysis)
            print("Selected WB...") #placeholder for starting the white balance analysis
        elif selected_analyses[1]: #if only exposure analysis is selected, print a message (placeholder for starting the exposure analysis)
            print("Selected Exposure...") #placeholder for starting the exposure analysis

        print("Importing analysis results...") #placeholder for importing analysis results, will be replaced with the actual function to import analysis results
        analysis_path = filedialog.askopenfilename() #open a file dialog to select the analysis results file
        analysis_path = os.path.normpath(analysis_path) #normalize the selected analysis results file path
        print(f"Selected analysis results file: {analysis_path}") #print the selected analysis results file path, will be replaced with the actual function to import and process the analysis results
        analysis_data = Analysis.load_analysis_json(self) #call the load_analysis_json function from the Analysis class to load the analysis data from the selected file and store it in a variable for use in the GUI

        detection_data = Analysis.detect_changes(self, analysis_data, threshold=self.change_threshold) #call the detect_changes function from the Analysis class to perform change detection on the loaded analysis data with a specified threshold and store the results in a variable for use in the GUI

        self.show_analysis_data_page(analysis_data, detection_data) #call the show_analysis_data function to display the analysis data in the GUI, will be replaced with the actual function to display the analysis data in the GUI


    #------ BUTTON COMMANDS ------
    """ 
    # ----- Function to select a shot path from the file system -----
    def select_shot_path(self):
        self.shot_path = filedialog.askopenfilename(title="Select Footage", filetypes=[("Video files", "*.mov *.mp4 *.avi *.mkv *.wmv *.flv *.mxf")]) #open a file dialog to select a shot
        self.shot_path = os.path.normpath(self.shot_path) #normalize the selected shot path
        self.selected_shot_path_label.configure(text=self.shot_path) #update the selected shot path label with the selected shot path
    """

    # ------ FUNCTION TO CLEAR THE HOME FRAME ------
    def clear_home_frame(self):
        for widget in self.home.winfo_children(): #loop through all the widgets in the home frame
            widget.destroy() #destroy each widget to clear the home frame, will be replaced with a function to clear the home frame when navigating between pages in the GUI

    # ----- Analysis settings widgets for quick initialization ------
    def analysis_settings_widgets(self, curr_page_frame):
        # Reference frame number entry ---
        self.reference_frame_num_label = ctk.CTkLabel(master = curr_page_frame,
                                                        text= 'Reference Frame: ' + str(self.reference_frame_num),
                                                        font=ctk.CTkFont(size=16)) #label to display the reference frame number for the analysis
        self.reference_frame_num_label.pack(side="top", padx=20, pady=10) #pack the reference frame number label to the top of the project setup page frame with padding

        # Reload reference frame number button ---
        self.reload_reference_frame_button = ctk.CTkButton(master = curr_page_frame, 
                                                        text="Reload Reference Frame", 
                                                        font=ctk.CTkFont(size=16), 
                                                        fg_color=default_widget_color,
                                                        command=self.reload_reference_frame) #button to reload the reference frame number from the timeline marker
        self.reload_reference_frame_button.pack(side="top", padx=20, pady=10) #pack the reload reference frame button to the top of the project setup page frame with padding
        
        #------------------------Parameters  frame------------------------

        labelsalignment = "e" #alignment for the parameter labels in the parameters frame, left aligned

        self.parameters_frame = ctk.CTkFrame(master = curr_page_frame) #frame for the analysis parameters
        self.parameters_frame.configure(bg_color=default_bg_color, fg_color=default_fg_color)
        self.parameters_frame.pack(side="top") #pack the parameters frame to the top of the project setup page frame, no padding


        # THRESHOLD
        self.threshold_label = ctk.CTkLabel(master = self.parameters_frame,
                                            text="Change Detection Threshold:",
                                            font=ctk.CTkFont(size=16)) #label for the threshold entry
        self.threshold_label.grid(row=0, column=0, padx=20, pady=10, sticky=labelsalignment) #grid the threshold label in the parameters frame with padding

        self.threshold_textbox = ctk.CTkEntry(master = self.parameters_frame,
                                                        font=ctk.CTkFont(size=16),
                                                        fg_color=default_widget_color,) #textbox to enter the change detection threshold for the analysis
        self.threshold_textbox.grid(row=0, column=1, padx=20, pady=10) #grid the threshold textbox in the parameters frame with padding
        self.threshold_textbox.insert(0, "0.3") #insert a default value of 0.3 in the threshold textbox for testing purposes, will be removed in the final version of the GUI


        # LOOKAHEAD
        self.lookahead_label = ctk.CTkLabel(master = self.parameters_frame,
                                            text="Lookahead Frames:",
                                            font=ctk.CTkFont(size=16)) #label for the lookahead entry
        self.lookahead_label.grid(row=1, column=0, padx=20, pady=10, sticky=labelsalignment) #grid the lookahead label in the parameters frame with padding

        self.lookahead_textbox = ctk.CTkEntry(master = self.parameters_frame,
                                                        font=ctk.CTkFont(size=16),
                                                        fg_color=default_widget_color) #textbox to enter the lookahead frames for the analysis
        self.lookahead_textbox.grid(row=1, column=1, padx=20, pady=10, sticky=labelsalignment) #grid the lookahead textbox in the parameters frame with padding
        self.lookahead_textbox.insert(0, "5") #insert a default value of 5 in the lookahead textbox for testing purposes, will be removed in the final version of the GUI
        

        # RELEASE 
        self.release_label = ctk.CTkLabel(master = self.parameters_frame, 
                                            text="Release Frames:",
                                            font=ctk.CTkFont(size=16)) #label for the release entry
        self.release_label.grid(row=2, column=0, padx=20, pady=10, sticky=labelsalignment) #grid the release label in the parameters frame with padding

        self.release_textbox = ctk.CTkEntry(master = self.parameters_frame,
                                                        font=ctk.CTkFont(size=16),
                                                        fg_color=default_widget_color) #textbox to enter the release frames for the analysis
        self.release_textbox.grid(row=2, column=1, padx=20, pady=10, sticky=labelsalignment) #grid the release textbox in the parameters frame with padding
        self.release_textbox.insert(0, "10") #insert a default value of 10 in the release textbox for testing purposes, will be removed in the final version of the GUI
        # ---------------------------------------------------------------------------

        # ----------------- Analysis selections ------------------
        #analysis selections frame ----
        self.analysis_selections_frame = ctk.CTkFrame(master = curr_page_frame) #frame for the analysis selections
        self.analysis_selections_frame.configure(bg_color=default_bg_color, fg_color=default_fg_color) #configure the background color of the analysis selections frame
        self.analysis_selections_frame.pack(side="top") #pack the analysis selections frame to the top of the project setup page frame, no padding
                
        #wb analysis checkbox ----
        self.analysis_selection_tkvar = [ctk.BooleanVar(), ctk.BooleanVar()] #variables for the analysis selection checkboxes

        self.wb_analysis_checkbox = ctk.CTkCheckBox(master = self.analysis_selections_frame, 
                                                    text="WB Analysis", 
                                                    font=ctk.CTkFont(size=20), 
                                                    fg_color=default_widget_color,
                                                    variable=self.analysis_selection_tkvar[0]) #checkbox for white balance analysis
        self.wb_analysis_checkbox.grid(row=0, column=0, padx=20, pady=10) #alignment

        #exp analysis checkbox ----
        self.exp_analysis_checkbox = ctk.CTkCheckBox(master = self.analysis_selections_frame, 
                                                     text="Exposure Analysis", 
                                                     font=ctk.CTkFont(size=20), 
                                                     fg_color=default_widget_color,
                                                     variable=self.analysis_selection_tkvar[1]) #checkbox for exposure analysis
        self.exp_analysis_checkbox.grid(row=0, column=1, padx=20, pady=10) #alignment


        
# ----- Function to show an error message in a message box -----
    def external_error_message(self, message):
        tk.messagebox.showerror("Error", message) #function to show an error message in a message box

# ------ Function to reload the reference frame number from the timeline marker -----
    def reload_reference_frame(self):
        reference_frame_num = DaVinci().get_reference_marker() #call the get_reference_marker function from the DaVinci class to get the reference marker ID from the timeline
        if reference_frame_num is not None: #if a reference marker ID is returned, update the reference frame number variable and label with the new reference frame number
            self.reference_frame_num = reference_frame_num
            self.reference_frame_num_label.configure(text='Reference Frame: ' + str(self.reference_frame_num)) #update the reference frame number label with the new reference frame number




### ________________A N A L Y S I S   C L A S S________________ ###
class Analysis:

    ## ________ FFMPEG-PYTHON VERSION ________ ##
    '''
    def __init__(self, shot_path):
        self.shot_path = shot_path #path to the selected shot
        self.analysis_data = None #variable to store the analysis data for use in the GUI
        self.probe = ffmpeg.probe(self.shot_path)
        self.video_stream = next((stream for stream in self.probe['streams'] if stream['codec_type'] == 'video'), None)
        self.width = int(self.video_stream['width'])
        self.height = int(self.video_stream['height'])
    '''

    ## ________ PYAV AND FFMPEG-PYTHON VERSION ________ ##
    def __init__(self, shot_path):
        self.shot_path = shot_path #path to the selected shot
        self.analysis_data = None #variable to store the analysis data for use in the GUI
        self.container = av.open(self.shot_path) # AV open the selected footage with PyAV
        self.stream = self.container.streams.video[0] # AV get the first video stream from the container
        
        self.probe = ffmpeg.probe(self.shot_path) # FFMPEG probe the selected footage to get the video stream information, used for the ffmpeg-python analysis functions
        self.video_stream = next((stream for stream in self.probe['streams'] if stream['codec_type'] == 'video'), None) # FFMPEG get the video stream information from the probed data, used for the ffmpeg-python analysis functions

        
        self.width = self.stream.width # AV get the width of the video
        self.height = self.stream.height # AV get the height of the video
        self.fps = float(self.stream.average_rate) # AV get the frame rate of the video as a float for easier calculations
        self.frame_count = self.stream.frames # AV get the total number of frames in the video
        self.stream.thread_type = "AUTO" # AV set the thread type to auto for optimal performance
        self.stream.thread_count = 0  # AV 0 = auto (use all cores)


        self.Y_avg_values = None # initialize a variable to store the Y average values for use in change detection
        self.HSL_avg_values = None # initialize a variable to store the RGB average values for use in change detection
    ## LOAD ANALYSIS FUNCTION TO LOAD ANALYSIS RESULTS FROM A JSON FILE ##
    def load_analysis_json(self):
        json_file_path = filedialog.askopenfilename(title="Load Analysis Results", filetypes=[("JSON files", "*.json")]) # open file dialog to select the analysis results file to load
        with open(json_file_path, 'r') as f:
            json_data = json.load(f) # load the analysis data from the selected JSON file and return it for use in the GUI
            analysis_data = {} # initialize a dictionary to store the loaded analysis data
            for item in json_data:
                for key, value in item.items():
                    analysis_data[key] = cp.array(value).get() # convert any lists in the loaded analysis data back to CuPy arrays for use in the GUI, while keeping other data types unchanged
        return analysis_data
    
    ## PERFORM SELECTED ANALYSIS FUNCTION
    def perform_analysis(self, analysis_type):
        self.out = self.decode_with_signalstats() # call the decode_with_signalstats function to start decoding the video with the signalstats filter and store the output for processing the analysis data in the GUI

        if analysis_type[0]: # if white balance analysis is selected, call the RGB_analyze function to perform the white balance analysis and store the results in a variable for use in the GUI
            self.WB_avg_values = self.WB_analyze() # call the RGB_analyze function to perform the white balance analysis and store the results in a variable for use in the GUI


        if analysis_type[1]: # if exposure analysis is selected, call the Y_analyze function to perform the exposure analysis and store the results in a variable for use in the GUI
            self.Y_avg_values = self.Y_analyze() # call the Y_analyze function to perform the exposure analysis and store the results in a variable for use in the GUI



    ## Y ANALYZE FOOTAGE FUNCTION ##
    def Y_analyze(self):
               
        pattern = r'YAVG=([\d\.]+)' # regular expression pattern to search for the Y average value in the ffmpeg output, looks for "YAVG=" followed by a number (which can include a decimal point) and captures the number as a group for extraction   
        Y_avg_values = []

        for line in self.out.stderr: 
            line = line.decode("utf-8") # decode the line from bytes to string format for processing
            #print(line)
            match = re.search(pattern, line) # search for the Y average value in the line using the defined regular expression pattern, which looks for "YAVG=" followed by a number (which can include a decimal point) and captures the number as a group for extraction

            if match:
                Y_avg_values.append(float(match.group(1))) # extract the Y average value from the matched line, convert it to a float, and append it to the list of Y average values for each frame

        if len(Y_avg_values) == self.frame_count: # if the number of Y average values matches the total frame count of the video, return the Y average values for use in the GUI, otherwise show an error message   
            return Y_avg_values
        else:
            GuiBuild.external_error_message(self, "Backend Error: Inconsistent frame count in Y analysis results.") # show an error message if the number of Y average values does not match the total frame count of the video
            return None
        
    ## RGB ANALYZE FOOTAGE FUNCTION ##
    def WB_analyze(self):
        
        valtypes = ['YAVG', 'HUEAVG', 'SATAVG'] #set of value types
        HSL_avg_values = []

        for valtype, i in zip(valtypes, range(len(valtypes))): # loop through the HSL value types and their indices
            pattern = rf'{valtype}=([\d\.]+)' # regular expression pattern to search for the HSL values
            HSL_avg_values.append([]) # initialize a list to store the average values for each frame for the current value type

            for line in self.out.stderr: 
                line = line.decode("utf-8") # decode the line from bytes to string format for processing
                #print(line)
                match = re.search(pattern, line) # search for the RGB average value in the line using the defined regular expression pattern, which looks for "VALTYPE=" followed by a number (which can include a decimal point) and captures the number as a group for extraction

                if match:
                    HSL_avg_values[i].append(float(match.group(1))) # extract the HSL average value from the matched line, convert it to a float, and append it to the list of HSL average values for each frame
        

        if len(HSL_avg_values[0]) == self.frame_count: # if the number of HSL average values matches the total frame count of the video, return the HSL average values for use in the GUI, otherwise show an error message   
            print(HSL_avg_values)
            return HSL_avg_values
        else:
            GuiBuild.external_error_message(self, "Backend Error: Inconsistent frame count in HSL analysis results.") # show an error message if the number of HSL average values does not match the total frame count of the video
            return None
        

    ## DECODE VIDEO WITH SIGNALSTATS FILTER 
    def decode_with_signalstats(self):
        out = (
            ffmpeg
            .input(self.shot_path)
            .filter('scale', 320, -1)
            .filter('signalstats')
            .output("null", f="null")
            .run_async(pipe_stderr=True)
        )

        for line in out.stderr: 
            line = line.decode("utf-8") # decode the line from bytes to string format for processing
            print(line)

        return out # return the ffmpeg process output for processing the signalstats data in the GUI


    # ---- function to calculate the derivative of the analyzed data
    def derivative(self, data, frame_num):
        derivative = cp.zeros(frame_num - 1) # initialize an array to store the derivative values
        for i in range(frame_num - 1): # loop through the data starting from the second frame
            derivative[i] = data[i + 1] - data[i] # calculate the difference between the current frame and the next frame and store it in the derivative array
        
        return derivative # return the calculated derivative values for use in change detection


    # ---- change detection function, which takes the analyzed data and the threshold as input and returns a list of detected changes
    def detect_changes(self, analysis_type, threshold, lookahead_frames, release_frames):
        #Y_median_smooth = analyzed_data['Y_median_smooth'] # get the smoothed Y median data from the analyzed data
        #print(Y_median_smooth) # print the smoothed Y median data for debugging purposes
        #print(Y_feed) # print the Y median data for debugging purposes
        


        if analysis_type[1]: # if exposure analysis is selected, use the Y median data for change detection
            if self.Y_avg_values is None: # if the Y average values are not available, show an error message and return empty change lists
                self.Y_avg_values = self.perform_analysis(analysis_type) # perform analysis if no data is available

            Y_changes = [[], []] #list to store the detected changes
            change_ongoing_flag = False # initialize a flag to track whether a change is currently ongoing
            derived_data = self.derivative(self.Y_avg_values, self.frame_count) # calculate the derivative of the Y average data for use in change detection
            direction = 0 # initialize a variable to track the direction of the change, 0 = no change, 1 = positive change, -1 = negative change
            i = 0

            
            # --- flooring of noise data
            '''
            for i in range(analyzed_data['frame_num'] -1):
                if abs(derived_data[i]) < 0.12:
                    derived_data[i] = 0
            '''
            
            zerotolerance = 0.012


            while i < self.frame_count - 1: # loop through the smoothed Y median data starting from the second frame
                #segment_diff = Y_median_smooth[i + 1] - Y_median_smooth[i] # calculate the absolute difference between the current frame and the next frame
                if not change_ongoing_flag and abs(derived_data[i]) > zerotolerance: # if there is no ongoing change and threshold was exceeded
                    
                    for j in range(lookahead_frames):
                        if i + j >= self.frame_count - 1: # if we have reached the end of the data during lookahead, break out of the loop
                                break
                        if abs(derived_data[i+j]) < zerotolerance: # if the change stabilizes in the lookahead, ignore the change
                            change_ongoing_flag = False
                            break
                        if abs(derived_data[i]) > threshold:
                            change_ongoing_flag = True
                    if change_ongoing_flag: #if the change occurs in the entire lookahead
                        direction = 1 if derived_data[i] > 0 else -1 # determine the direction of the change based on the sign of the derivative
                        Y_changes[0].append(i) #mark the change start
                    
                elif change_ongoing_flag: # if the change is currently ongoing
                    if abs(derived_data[i]) <= zerotolerance: # if the change seems to have stopped
                        stabilization_flag = True # initialize a flag to track whether the change has stabilized
                        for j in range(release_frames): # look ahead for the specified number of frames to see if the change stopped 
                            if i + j >= self.frame_count - 1: # if we have reached the end of the data during lookahead, break out of the loop
                                break
                            if abs(derived_data[i + j]) > threshold: # if the change continues within the lookahead period, consider it to be ongoing
                                stabilization_flag = False # reset the stabilization flag
                                break
                        if stabilization_flag: # if the value has stabilized
                            Y_changes[1].append(i) # mark the change end
                            change_ongoing_flag = False # reset the change ongoing flag
                            direction = 0 # reset the change direction variable 

                    elif (direction == 1 and derived_data[i] < 0) or (direction == -1 and derived_data[i] > 0): # if the change direction reversed
                        Y_changes[1].append(i) # if the change continues, consider it to have ended and add the current frame to the list of detected changes
                        i += 1    
                        Y_changes[0].append(i) # if the change continues, consider it to have started again and add the current frame to the list of detected changes
                        direction = -direction # flip the change direction variable to reflect the change in direction
                
                i += 1 # if there is no change, move to the next frame
        
        if analysis_type[0]: # if white balance analysis is selected, use the RGB median data for change detection, will be replaced with the actual function to perform change detection on the RGB median data
            if self.HSL_avg_values is None: # if the RGB average values are not available, show an error message and return empty change lists
                self.HSL_avg_values = self.perform_analysis(analysis_type) # call the RGB_analyze function to get the RGB average values for each frame and store it in a variable for use in change detection


            RGB_changes = [[], []] #list to store the detected changes for the RGB analysis, will be replaced with the actual function to perform change detection on the RGB median data


        if not analysis_type[0]: # if white balance analysis is not selected, set the RGB changes list to empty lists
            RGB_changes = [[], []]

        if not analysis_type[1]: # if exposure analysis is not selected, set the Y changes list to empty lists
            Y_changes = [[], []]

        return Y_changes, RGB_changes, self.Y_avg_values, self.RGB_avg_values # return the list of detected changes for use in the GUI, will be replaced with the actual function to return the detected changes based on the selected analysis type



### ________________S E N D   T O   D A V I N C I   R E S O L V E   C L A S S________________ ###
class DaVinci:
    def __init__(self):        
        # Get the main objects
        self.projectManager = resolve.GetProjectManager()  # Get the project manager    
        self.project = self.projectManager.GetCurrentProject() # Get the current project
        self.timeline = self.project.GetCurrentTimeline() # Get the new timeline
        
    
    def getvideo(self):
        timeline_video = self.timeline.GetItemListInTrack("video", 1) # Get the file path of the footage in the video track of the timeline
        video_mediapool = timeline_video[0].GetMediaPoolItem() # Get the media pool item for the footage in the video track of the timeline
        footage_path = os.path.normpath(video_mediapool.GetClipProperty('File Path')) # Get the file path of the footage from the media pool item
        reference_marker_id = self.get_reference_marker() # Get the reference marker ID from the timeline for use in the analysis
        print(timeline_video[0].GetName()) # Print the file path of the footage for debugging purposes
        print(footage_path) # Print the file path of the footage for debugging purposes
        print(reference_marker_id) # Print the markers from the timeline for debugging purposes
        
        return footage_path, reference_marker_id # Return the footage path and the reference marker ID for use in the analysis

    def send(self, change_data):
        
        for frame_id in change_data: # Loop through the detected change start frame IDs and add markers to the timeline
            print(frame_id)
            self.timeline.AddMarker(frame_id[0], 'Red', 'Marker Name', 'Notes', frame_id[1]-frame_id[0], 'Secret_Word') # Add markers to the timeline at the specified frame IDs

    def get_reference_marker(self):
        markers = self.timeline.GetMarkers() # Get the markers from the timeline
        if not markers: # If no markers are found, show an error message and return None
            GuiBuild.external_error_message(self, "No markers found in the timeline. Please add a marker to the timeline to indicate the reference frame for the analysis.")
            return None
        elif len(markers) > 1: # If multiple markers are found, show an error message and return None
            GuiBuild.external_error_message(self, "Multiple markers found in the timeline. Please ensure there is only one marker in the timeline to indicate the reference frame for the analysis.")
            return None
        reference_marker_id = next(iter(markers)) # Get the first marker ID from the markers dictionary
        return reference_marker_id # Return the reference marker ID for use in the analysis

    def get_playhead_position(self):
        current_timecode = self.timeline.GetCurrentTimecode() # Get the current timecode from the timeline
        fps = self.timeline.GetSetting("timelineFrameRate") # Get the frame rate of the timeline
        hours, minutes, seconds, frames = map(int, current_timecode.split(':')) # Split the timecode into its components and convert them to integers
        total_frames = (hours * 3600 + minutes * 60 + seconds) * fps + frames # Calculate the total number of frames based on the timecode and frame rate
        return total_frames # Return the total number of frames for use in the analysis
'''
analysis = Analysis(footage_path) # create an instance of the Analysis class with the selected footage
analyzed_data = analysis.analyze_footage(reference_frame_num) # perform the analysis on the footage with the specified reference frame number
print(analyzed_data) # print the analyzed data to the console for testing purposes
'''
#__________________________________M A I N   P R O G R A M___________________________________#
##############################################################################################

# Analysis(footage_path)
DaVinci()
GuiBuild().mainloop() #start the GUI main loop