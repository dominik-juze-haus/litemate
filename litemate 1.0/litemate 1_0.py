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

        self.selected_analyses = [False, False] #variable to store the selected analyses for use in the GUI, default is both analyses selected

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
    def show_analysis_data_page(self, changes, avg_values):

        self.changes, self.avg_values = changes, avg_values #store the analysis results in instance variables for use in the update graph function when adjusting the analysis parameters with the analysis settings widgets for quick adjustments to the analysis parameters and re-running the analysis without having to navigate back to the project setup page        
        self.selected_analyses = [var.get() for var in self.analysis_selection_tkvar] #get the values of the analysis selection checkboxes

         # CLEAR THE HOME FRAME
        self.clear_home_frame() #call the function to clear the home frame before displaying the analysis results, will be replaced with a function to clear the home frame when navigating between pages in the GUI
        self.geometry('1280x1000') #resize the window to better fit the analysis results page layout
        
        self.show_analysis_data_page_frame = ctk.CTkFrame(master = self.home) #frame for the show analysis data page, master is the home frame
        self.show_analysis_data_page_frame.configure(bg_color=default_bg_color, fg_color=default_fg_color) #configure the background color of the show analysis data page frame
        self.show_analysis_data_page_frame.pack(side="top", fill="both", expand=True, anchor="center") #pack the show analysis data page frame to fill the entire home frame and allow it to expand
        
           
        # PREPARE SUBPLOT
        self.results_plot_fig, self.graph = plt.subplots() #create a figure for the analysis results plot

        # PREPARE THE GRAPH CANVAS
        self.graph_canvas = FigureCanvasTkAgg(self.results_plot_fig, master=self.show_analysis_data_page_frame) #create a canvas to display the analysis results plot in the GUI
        self.graph_canvas.get_tk_widget().pack(side="top", fill="both", expand=True) #pack the canvas to fill the entire home frame and allow it to expand
        
       
       

        self.analysis_settings_widgets(self.show_analysis_data_page_frame) #call the function to create the analysis settings widgets in the show analysis data page frame for quick adjustments to the analysis parameters and re-running the analysis without having to navigate back to the project setup page

        # Control buttons frame ----
        self.control_buttons_frame = ctk.CTkFrame(master = self.show_analysis_data_page_frame) #frame for the control buttons
        self.control_buttons_frame.configure(bg_color=default_bg_color, fg_color=default_fg_color) #configure the background color of the control buttons frame
        self.control_buttons_frame.pack(side="top") #pack the control buttons frame to fill the entire show analysis data page frame and allow it to expand

        #  New analysis button -----------------------------
        def btncmd_new_analysis():
            self.clear_home_frame() #call the function to clear the home frame before starting a new analysis, will be replaced with a function to clear the home frame when navigating between pages in the GUI
            self.project_setup_page() #call the project setup page function to return to the project setup page and start a new analysis

        self.new_analysis_button = ctk.CTkButton(master = self.control_buttons_frame, 
                                                 text="New Analysis", 
                                                 font=ctk.CTkFont(size=20), 
                                                 fg_color=default_widget_color,
                                                 command=btncmd_new_analysis) #button to start a new analysis, will be replaced with a function to clear the analysis data and return to the project setup page
        self.new_analysis_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew") #grid the new analysis button in the control buttons frame
        
        # PLOT THE ANALYSIS RESULTS 
        self.plot_graph() #call the function to plot the analysis results on the graph
        #self.after(100, lambda: self.graph_canvas.draw()) #add a short delay before drawing the plots on the canvas to ensure that the canvas is fully initialized before drawing, for better performance and to avoid potential issues with the canvas not updating correctly when the analysis results are first displayed in the GUI
        # ---------------------------------------------------

        # Send to Resolve button -----------------------------
        def btncmd_send_to_resolve():
            try:
                DaVinci().send(self.changes, self.selected_analyses) #function to send the analysis results to DaVinci Resolve, will be replaced with a function to actually send the results to Resolve and create timeline markers or other indicators based on the detected changes in the analysis data
                tk.messagebox.showinfo("Success", "Analysis results sent to DaVinci Resolve successfully.") #show a success message box if the analysis results were sent to Resolve successfully   
            except Exception as e:
                tk.messagebox.showerror("Error", f"An error occurred while sending analysis results to DaVinci Resolve: {str(e)}") #show an error message box if there was an error sending the analysis results to Resolve, with the error message for debugging purposes
        
        self.send_to_resolve_button = ctk.CTkButton(master = self.control_buttons_frame,
                                                    text="Send Results to Resolve", 
                                                    font=ctk.CTkFont(size=20), 
                                                    fg_color=default_widget_color,
                                                    command=btncmd_send_to_resolve) #button to send the analysis results to DaVinci Resolve, will be replaced with a function to actually send the results to Resolve and create timeline markers or other indicators based on the detected changes in the analysis data

        self.send_to_resolve_button.grid(row=0, column=1, padx=10, pady=10, sticky="ew") #grid the send to resolve button in the control buttons frame
        # ---------------------------------------------------

        # Export analysis results button -----------------------------
        def btncmd_export_analysis():
            try:
                Analysis.export_analysis_json(self.changes, self.avg_values) #function to export the analysis results to a JSON file, will be replaced with a function to actually export the results to a JSON file for later use or sharing
                tk.messagebox.showinfo("Success", "Analysis results exported successfully.") #show a success message box if the analysis results were exported successfully
            except Exception as e:
                tk.messagebox.showerror("Error", f"An error occurred while exporting analysis results: {str(e)}") #show an error message box if there was an error exporting the analysis results, with the error message for debugging purposes

        self.export_analysis_button = ctk.CTkButton(master = self.control_buttons_frame,
                                                    text="Export Analysis Results", 
                                                    font=ctk.CTkFont(size=20), 
                                                    fg_color=default_widget_color,
                                                    command=btncmd_export_analysis) #button to export the analysis results to a JSON file, will be replaced with a function to actually export the results to a JSON file for later use or sharing
        self.export_analysis_button.grid(row=0, column=2, padx=10, pady=10, sticky="ew") #grid the export analysis button in the control buttons frame
        # ---------------------------------------------------
        
        
        


## ----- WIDGETS COMMANDS AND FUNCTIONS FOR THE GUI -----

# Function to start the frame by frame analysis
    def start_analysis(self):
        self.get_current_settings() #call the function to get the current settings from the analysis settings widgets before starting the analysis, to ensure that the analysis is performed with the most up-to-date settings
        changes, avg_values = Analysis(self.shot_path).detect_changes(self.selected_analyses, self.change_threshold, self.lookahead_frames, self.release_frames) #call the detect_changes function from the Analysis class to perform change detection on the analyzed data with a specified threshold and store the results in a variable for use in the GUI
        print("Analysis completed. Displaying results...") #placeholder for displaying the analysis results
        
        self.changes = changes
        self.avg_values = avg_values
        self.show_analysis_data_page(self.changes, self.avg_values) #call the show_analysis_data function to display the

# Analysis import
    def import_analysis(self):
        print("Importing analysis results...") #placeholder for importing analysis results
        analysis_path = filedialog.askopenfilename() #open a file dialog to select the analysis results file
        analysis_path = os.path.normpath(analysis_path) #normalize the selected analysis results file path
        print(f"Selected analysis results file: {analysis_path}") #print the selected analysis results file path
        #self.show_analysis_data_page(self.changes, self.avg_values) #call the show_analysis_data function to display the analysis data in the GUI


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
        try:
            self.threshold_textbox.insert(0, str(self.change_threshold)) #insert a default value of 0.3 in the threshold textbox for testing purposes, will be removed in the final version of the GUI
        except:
            self.threshold_textbox.insert(0, "0.3") #insert the default value of 0.3 in the threshold textbox
        self.threshold_textbox.bind("<Return>", lambda event: self.update_graph()) #bind the Enter key to the threshold textbox to update the graph with the new threshold value when the user presses Enter after entering a new threshold value, for quick adjustments to the analysis parameters and re-running the analysis without having to navigate back to the project setup page

        # LOOKAHEAD
        self.lookahead_label = ctk.CTkLabel(master = self.parameters_frame,
                                            text="Lookahead Frames:",
                                            font=ctk.CTkFont(size=16)) #label for the lookahead entry
        self.lookahead_label.grid(row=1, column=0, padx=20, pady=10, sticky=labelsalignment) #grid the lookahead label in the parameters frame with padding

        self.lookahead_textbox = ctk.CTkEntry(master = self.parameters_frame,
                                                        font=ctk.CTkFont(size=16),
                                                        fg_color=default_widget_color) #textbox to enter the lookahead frames for the analysis
        self.lookahead_textbox.grid(row=1, column=1, padx=20, pady=10, sticky=labelsalignment) #grid the lookahead textbox in the parameters frame with padding
        try:
            self.lookahead_textbox.insert(0, str(self.lookahead_frames)) #insert a default value of 7 in the lookahead textbox for testing purposes, will be removed in the final version of the GUI
        except:
            self.lookahead_textbox.insert(0, "7") #insert the default value of 7 in the lookahead textbox
        self.lookahead_textbox.bind("<Return>", lambda event: self.update_graph()) #bind the Enter key to the lookahead textbox to update the graph with the new lookahead value when the user presses Enter after entering a new lookahead value, for quick adjustments to the analysis parameters and re-running the analysis without having to navigate back to the project setup page

        # RELEASE 
        self.release_label = ctk.CTkLabel(master = self.parameters_frame, 
                                            text="Release Frames:",
                                            font=ctk.CTkFont(size=16)) #label for the release entry
        self.release_label.grid(row=2, column=0, padx=20, pady=10, sticky=labelsalignment) #grid the release label in the parameters frame with padding

        self.release_textbox = ctk.CTkEntry(master = self.parameters_frame,
                                                        font=ctk.CTkFont(size=16),
                                                        fg_color=default_widget_color) #textbox to enter the release frames for the analysis
        self.release_textbox.grid(row=2, column=1, padx=20, pady=10, sticky=labelsalignment) #grid the release textbox in the parameters frame with padding
        try:
            self.release_textbox.insert(0, str(self.release_frames)) #insert a default value of 5 in the release textbox for testing purposes, will be removed in the final version of the GUI
        except:
            self.release_textbox.insert(0, "5") #insert the default value of 5 in the release textbox
        self.release_textbox.bind("<Return>", lambda event: self.update_graph()) #bind the Enter key to the release textbox to update the graph with the new release value when the user presses Enter after entering a new release value, for quick adjustments to the analysis parameters and re-running the analysis without having to navigate back to the project setup page
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
        if self.selected_analyses[0]: #if white balance analysis is selected, check the white balance analysis checkbox
            self.wb_analysis_checkbox.select() #select the white balance analysis checkbox
        self.wb_analysis_checkbox.grid(row=0, column=0, padx=20, pady=10) #alignment

        #exp analysis checkbox ----
        self.exp_analysis_checkbox = ctk.CTkCheckBox(master = self.analysis_selections_frame, 
                                                     text="Exposure Analysis", 
                                                     font=ctk.CTkFont(size=20), 
                                                     fg_color=default_widget_color,
                                                     variable=self.analysis_selection_tkvar[1]) #checkbox for exposure analysis
        if self.selected_analyses[1]: #if exposure analysis is selected, check the exposure analysis checkbox
            self.exp_analysis_checkbox.select() #select the exposure analysis checkbox
        self.exp_analysis_checkbox.grid(row=0, column=1, padx=20, pady=10) #alignment

# ---------------------------------------------------------------------------

    def plot_graph(self):
        # PLOT THE ANALYSIS RESULTS
        # WB plots
        if self.selected_analyses[0]: #if white balance analysis is selected, plot the white balance analysis results
            self.graph.plot(range(len(self.avg_values[0])), self.avg_values[0], label='CCT', color='red') #plot the CCT channel
            for start, end in zip(self.changes[0][0], self.changes[0][1]): #add vertical lines for each detected change  
                self.graph.axvline(x=start, color='g', linestyle='--') #add a vertical line to indicate the start 
                self.graph.axvline(x=end, color='r', linestyle='--') #add a vertical line to indicate the end 
                self.graph.axvspan(start, end, color='y', alpha=0.3, label='WB Change') #highlight the change duration

        # Exposure plots
        if self.selected_analyses[1]: #if exposure analysis is selected, plot the exposure analysis results
            self.graph.plot(range(len(self.avg_values[1])), self.avg_values[1], label='Y Median', color='orange') #plot the Y channel 
            for start, end in zip(self.changes[1][0], self.changes[1][1]): #add vertical lines for each detected change 
                self.graph.axvline(x=start, color='c', linestyle='--') #add a vertical line to indicate the start 
                self.graph.axvline(x=end, color='m', linestyle='--') #add a vertical line to indicate the end 
                self.graph.axvspan(start, end, color='y', alpha=0.3, label='Exposure Change') #highlight the change duration
        
        self.graph.axvline(x=self.reference_frame_num, color='k', linestyle='--', label='Reference Frame') #plot the reference frame
        if self.graph_canvas.get_tk_widget().winfo_exists():
            self.graph_canvas.draw() #draw the plots on the canvas

# ----- Update graph function
    def update_graph(self):
        self.get_current_settings() #call the function to get the current settings from the analysis settings widgets before updating the graph, to ensure that the graph is updated with the most up-to-date settings
        self.changes, self.avg_values = Analysis(self.shot_path).detect_changes(self.selected_analyses, self.change_threshold, self.lookahead_frames, self.release_frames) #call the detect_changes function from the Analysis class to perform change detection on the analyzed data with a specified threshold and store the results in a variable for use in the GUI
        self.graph.clear() #clear the current graph before plotting the updated analysis results
        self.plot_graph() #call the function to plot the updated analysis results

# ----- Get the current settings function
    def get_current_settings(self):
        self.selected_analyses = [var.get() for var in self.analysis_selection_tkvar] #get the values of the analysis selection checkboxes
        
        if not any([self.shot_path]): #if no shot is selected, show a warning message
            tk.messagebox.showwarning("No Shot Selected", "Please select a shot to start the analysis.")
            return

        if not any(self.selected_analyses): #if no analyses are selected, show a warning message
            tk.messagebox.showwarning("No Analysis Selected", "Please select at least one analysis to start.")
            return
        
        if self.selected_analyses[0] and self.selected_analyses[1]: #if both analyses are selected, print messages (placeholder for starting the analyses)
            print("Selected WB and Exposure...") #placeholder for starting the white balance analysis

        elif self.selected_analyses[0]: #if only white balance analysis is selected, print a message (placeholder for starting the white balance analysis)
            print("Selected WB...") #placeholder for starting the white balance analysis
        elif self.selected_analyses[1]: #if only exposure analysis is selected, print a message (placeholder for starting the exposure analysis)
            print("Selected Exposure...") #placeholder for starting the exposure analysis
        
            
        
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
        self.CCT_avg_values = None # initialize a variable to store the CCT average values for use in change detection
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
    
    def export_analysis_json(self, changes, avg_values):
        json_file_path = filedialog.asksaveasfilename(title="Export Analysis Results", defaultextension=".json", filetypes=[("JSON files", "*.json")]) # open file dialog to select the location to save the analysis results file
        with open(json_file_path, 'w') as f:
            json.dump([{'changes': changes, 'avg_values': avg_values}], f) # save the analysis data to the selected JSON file

    ## PERFORM SELECTED ANALYSIS FUNCTION
    def perform_analysis(self, analysis_type):
        self.out = self.decode_with_signalstats() # call the decode_with_signalstats function to start decoding the video with the signalstats filter and store the output for processing the analysis data in the GUI
      
        self.bit_depth = None

        for line in self.out:

            if self.bit_depth is None: # if the bit depth has not been determined yet, try to determine it from the line
                bit_depth_match = re.search(r'YBITDEPTH=(\d+)', line) # search for the bit depth in the line using a regular expression pattern that looks for "bit_depth=" followed by a number and captures the number as a group for extraction
                if bit_depth_match:
                    self.bit_depth = int(bit_depth_match.group(1)) # extract the bit depth from the matched line and convert it to an integer for use in determining the expected range of the YUV values, which can vary based on the bit depth of the video (e.g., 0-255 for 8-bit, 0-1023 for 10-bit, etc.)
                    break
        
        print(f"Determined bit depth: {self.bit_depth}") # print the determined bit depth for debugging purposes, will be removed in the final version of the GUI
        
        if analysis_type[0]: # if white balance analysis is selected, call the RGB_analyze function to perform the white balance analysis and store the results in a variable for use in the GUI
            WB_avg_values = self.WB_analyze() # call the RGB_analyze function to perform the white balance analysis and store the results in a variable for use in the GUI
            self.CCT_avg_values = [] # initialize a variable to store the RGB average values for use in change detection
            for y, u, v in zip(WB_avg_values[0], WB_avg_values[1], WB_avg_values[2]): # loop through the RGB average values for each frame and perform change detection
                r, g, b = self.YUV_to_RGB_rec709(y, u, v) # convert the YUV average values to RGB values for use in change detection

                self.CCT_avg_values.append(self.RGB_to_CCT(r, g, b)) # convert the RGB average values to CCT values for use in change detection and store it in a variable for use in the GUI    
            """ self.RGB_avg_values[0].append(r) # append the converted red channel value to the list of RGB average values for change detection
                self.RGB_avg_values[1].append(g) # append the converted green channel value to the list of RGB average values for change detection
                self.RGB_avg_values[2].append(b) # append the converted blue channel value to the list of RGB average values for change detection
            """
            """ self.RGB_derived_data = [self.derivative(self.RGB_avg_values[0], self.frame_count), 
                                     self.derivative(self.RGB_avg_values[1], self.frame_count), 
                                     self.derivative(self.RGB_avg_values[2], self.frame_count)] # calculate the derivative of the RGB average values for use in change detection and store it in a variable for use in the GUI
            """ 
            print(self.CCT_avg_values) # print the CCT average values for debugging purposes, will be removed in the final version of the GUI
            self.CCT_derived_data = self.derivative(self.CCT_avg_values, self.frame_count) # calculate the derivative of the CCT average values for use in change detection and store it in a variable for use in the GUI

        if analysis_type[1]: # if exposure analysis is selected, call the Y_analyze function to perform the exposure analysis and store the results in a variable for use in the GUI
            self.Y_avg_values = self.Y_analyze() # call the Y_analyze function to perform the exposure analysis and store the results in a variable for use in the GUI
            self.Y_derived_data = self.derivative(self.Y_avg_values, self.frame_count) # calculate the derivative of the Y average values for use in change detection and store it in a variable for use in the GUI
        #print(self.RGB_avg_values[0])
        #print(self.Y_avg_values)

    ## Y ANALYZE FOOTAGE FUNCTION ##
    def Y_analyze(self):
               
        pattern = r'YAVG=([\d\.]+)' # regular expression pattern to search for the Y average value in the ffmpeg output, looks for "YAVG=" followed by a number (which can include a decimal point) and captures the number as a group for extraction   
        Y_avg_values = []

        for line in self.out: 
            match = re.search(pattern, line) # search for the Y average value in the line using the defined regular expression pattern, which looks for "YAVG=" followed by a number (which can include a decimal point) and captures the number as a group for extraction

            if match:
                Y_avg_values.append(float(match.group(1))) # extract the Y average value from the matched line, convert it to a float, and append it to the list of Y average values for each frame

        #print(Y_avg_values)
        if len(Y_avg_values) == self.frame_count: # if the number of Y average values matches the total frame count of the video, return the Y average values for use in the GUI, otherwise show an error message   
            return Y_avg_values
        else:
            GuiBuild.external_error_message(self, "Backend Error: Inconsistent frame count in Y analysis results.") # show an error message if the number of Y average values does not match the total frame count of the video
            return None
        
    ## WB ANALYZE FOOTAGE FUNCTION ##
    def WB_analyze(self):
        
        valtypes = ['YAVG', 'UAVG', 'VAVG'] #set of value types
        YUV_avg_values = [[],[],[]]

        for line in self.out: 
            for valtype, i in zip(valtypes, range(0, len(valtypes))): # loop through the HSL value types and their indices
                
                
                pattern = rf'{valtype}=([\d\.]+)' # regular expression pattern to search for the YUV values

                match = re.search(pattern, line) # search for the YUV  average value in the line using the defined regular expression pattern, which looks for "VALTYPE=" followed by a number (which can include a decimal point) and captures the number as a group for extraction

                if match:
                    YUV_avg_values[i].append(float(match.group(1))) # extract the YUV average value from the matched line, convert it to a float, and append it to the list of YUV average values for each frame
                #print(YUV_avg_values)
        
        if len(YUV_avg_values[0]) == self.frame_count: # if the number of YUV average values matches the total frame count of the video, return the YUV average values for use in the GUI, otherwise show an error message   
            return YUV_avg_values
        else:
            string = "Backend Error: Inconsistent frame count in YUV analysis results.\n" + f"Expected: {self.frame_count}, Got: {len(YUV_avg_values[0])}" # initialize an error message string to show in the error message box
            GuiBuild.external_error_message(self, string) # show an error message if the number of YUV average values does not match the total frame count of the video
            return None
        

    ## DECODE VIDEO WITH SIGNALSTATS FILTER 
    def decode_with_signalstats(self):
        out = (
            ffmpeg
            .input(self.shot_path, hwaccel='auto')
            .filter('scale', -2, 240)
            .filter("colorspace", all='bt709', range='pc', fast=0)
            .filter('signalstats')
            .filter("metadata", "print")
            .output("null", f="null")
            .run_async(pipe_stderr=True)
        )

        """ for line in out.stderr: 
            line = line.decode("utf-8") # decode the line from bytes to string format for processing
            print(line) """
        
        output_lines = []
        for line in out.stderr:
            line = line.decode("utf-8") # decode the line from bytes to string format for processing
            output_lines.append(line) # store the decoded lines in a list for processing the analysis data in the GUI, since the ffmpeg output is a generator that can only be iterated through once, we need to store the lines in a list to loop through them again for each analysis type if both analyses are selected


        return output_lines # return the ffmpeg process output for processing the signalstats data in the GUI


    # ---- function to calculate the derivative of the analyzed data
    def derivative(self, data, frame_num):
        derivative = cp.zeros(frame_num - 1) # initialize an array to store the derivative values
        for i in range(frame_num - 1): # loop through the data starting from the second frame
            derivative[i] = data[i + 1] - data[i] # calculate the difference between the current frame and the next frame and store it in the derivative array
        
        return derivative # return the calculated derivative values for use in change detection


    # ---- YUV to RGB conversion function for REC.709
    def YUV_to_RGB_rec709(self, y, u, v): 
        match self.bit_depth: # determine the expected range of the YUV values based on the determined bit depth of the video and adjust the YUV values accordingly for accurate color space conversion
            case 8:
                r = y + 1.5748 * (v - 128) # calculate the red channel value from the YUV values using the REC.709 color space conversion formula
                g = y - 0.1873 * (u - 128) - 0.4681 * (v - 128) # calculate the green channel value from the YUV values using the REC.709 color space conversion formula
                b = y + 1.8556 * (u - 128) # calculate the blue channel value from the YUV values using the REC.709 color space conversion formula

                r = float(max(0, min(255, r))) # clamp the red channel value to the range of 0-255
                g = float(max(0, min(255, g))) # clamp the green channel value to the range of 0-255
                b = float(max(0, min(255, b))) # clamp the blue channel value to the range of 0-255
            case 10:
                r = y + 1.5748 * (v - 512) # calculate the red channel value from the YUV values using the REC.709 color space conversion formula
                g = y - 0.1873 * (u - 512) - 0.4681 * (v - 512) # calculate the green channel value from the YUV values using the REC.709 color space conversion formula
                b = y + 1.8556 * (u - 512) # calculate the blue channel value from the YUV values using the REC.709 color space conversion formula

                r = float(max(0, min(1023, r))) # clamp the red channel value to the range of 0-1023
                g = float(max(0, min(1023, g))) # clamp the green channel value to the range of 0-1023
                b = float(max(0, min(1023, b))) # clamp the blue channel value to the range of 0-1023
            case _:
                GuiBuild.external_error_message(self, "Backend Error: Unsupported bit depth for YUV to RGB conversion.") # show an error message if the bit depth is not supported for the YUV to RGB conversion
                return 0, 0, 0 # return default RGB values if the bit depth is not supported for the YUV to RGB conversion



        return r, g, b # return the calculated RGB values for use in change detection on the RGB data


    # ---- RGB to CCT conversion function
    def RGB_to_CCT(self, r, g, b):
        # Convert RGB to XYZ color space
        match self.bit_depth: # determine the expected range of the RGB values based on the determined bit depth of the video and adjust the RGB values accordingly for accurate color space conversion
            case 8:                
                r = r / 255.0 # normalize the red channel value to the range of 0-1
                g = g / 255.0 # normalize the green channel value to the range of 0-1
                b = b / 255.0 # normalize the blue channel value to the range of 0-1
            case 10:                
                r = r / 1023.0 # normalize the red channel value to the range of 0-1
                g = g / 1023.0 # normalize the green channel value to the range of 0-1
                b = b / 1023.0 # normalize the blue channel value to the range of 0-1

        X = (-0.14282 * r) + (1.54924 * g) + (-0.95641 * b) # calculate the X value in the XYZ color space from the RGB values using the REC.709 color space conversion formula
        Y = (-0.32466 * r) + (1.57837 * g) + (-0.73191 * b) # calculate the Y value in the XYZ color space from the RGB values using the REC.709 color space conversion formula
        Z = (-0.68202 * r) + (0.77073 * g) + (0.56332 * b) # calculate the Z value in the XYZ color space from the RGB values using the REC.709 color space conversion formula

        # Calculate chromaticity coordinates
        x = X / (X + Y + Z)
        y = Y / (X + Y + Z)

        # Calculate n
        n = (x - 0.3320) / (0.1858 - y)

        # Calculate CCT
        CCT = 449 * n**3 + 3525 * n**2 + 6823.3 * n + 5520.33

        return CCT # return the calculated CCT value for use in change detection on the white balance data


    # ---- change detection function, which takes the analyzed data and the threshold as input and returns a list of detected changes
    def detect_changes(self, analysis_type, threshold, lookahead_frames, release_frames):
        
        def change_detection_loop(derived_data):
            zerotolerance = threshold 
            changes_list = [[], []] #list to store the detected changes, index 0 for change starts and index 1 for change ends
            change_ongoing_flag = False # initialize a flag to track whether a change is currently ongoing
            direction = 0 # initialize a variable to track the direction of the change, 0 = no change, 1 = positive change, -1 = negative change

            for i in range(self.frame_count - 1): # loop through the analyzed data starting from the second frame for change detection
                if not change_ongoing_flag and abs(derived_data[i]) > threshold: # if there is no ongoing change and threshold was exceeded
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
                        changes_list[0].append(i) #mark the change start
                    
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
                            changes_list[1].append(i) # mark the change end
                            change_ongoing_flag = False # reset the change ongoing flag
                            direction = 0 # reset the change direction variable 

                    elif (direction == 1 and derived_data[i] < 0) or (direction == -1 and derived_data[i] > 0): # if the change direction reversed
                        flip_flag = True
                        for j in range(lookahead_frames): # look ahead for the specified number of frames to confirm the change direction reversal
                            if i + j >= self.frame_count - 1: # if we have reached the end of the data during lookahead, break out of the loop
                                break
                            if (direction == 1 and derived_data[i + j] > 0) or (direction == -1 and derived_data[i + j] < 0): # if the change direction reversal is confirmed within the lookahead period, consider it to be a new change
                                flip_flag = False # reset the flip flag if the change direction reversal is confirmed during lookahead
                                break
                        if flip_flag: # if the change direction reversal is not confirmed during lookahead, consider it to be ongoing
                            changes_list[1].append(i) # if the change continues, consider it to have ended and add the current frame to the list of detected changes for the analysis
                            i += 1
                            changes_list[0].append(i) # if the change continues, consider it to have started again and add the current frame to the list of detected changes for the analysis
                            direction *= -1 # flip the change direction variable
            
            return changes_list # return the list of detected changes for the analysis to be used in the GUI
        
        
        
        
        if analysis_type[1]: # if exposure analysis is selected, use the Y median data for change detection
            if self.Y_avg_values is None: # if the Y average values are not available, show an error message and return empty change lists
                self.perform_analysis(analysis_type) # perform analysis if no data is available
            threshold = threshold * ((2 ** self.bit_depth)/100) # adjust the threshold for change detection based on the bit depth of the video, since the range of the Y values can vary based on the bit depth (e.g., 0-255 for 8-bit, 0-1023 for 10-bit, etc.)

            # Change detection loop ---------------------------------------------------------------------------------------------------
            Y_changes = change_detection_loop(self.Y_derived_data) # call the change detection loop function to detect changes in the Y average data and store the detected changes in a variable for use in the GUI
        
        if analysis_type[0]: # if white balance analysis is selected, use the RGB median data for change detection
            if self.CCT_avg_values is None: # if the RGB average values are not available, show an error message and return empty change lists
                self.perform_analysis(analysis_type) # call the RGB_analyze function to get the RGB average values for each frame and store it in a variable for use in change detection
            threshold = threshold * (19000/100) # adjust the threshold for change detection based on the bit depth of the video, since the range of the RGB values can vary based on the bit depth (e.g., 0-255 for 8-bit, 0-1023 for 10-bit, etc.)

            # Change detection loop ---------------------------------------------------------------------------------------------------
            
            

            WB_changes = change_detection_loop(self.CCT_derived_data) # call the change detection loop function to detect changes in the RGB average data and store the detected changes in a variable for use in the GUI
        

               
        if not analysis_type[0]: # if white balance analysis is not selected, set the HSL changes list to empty lists
            WB_changes = [[], []]
            self.CCT_avg_values = [[], [], []] # set the RGB average values to empty lists if white balance analysis is not selected for use in the GUI

        if not analysis_type[1]: # if exposure analysis is not selected, set the Y changes list to empty lists
            Y_changes = [[], []]
            self.Y_avg_values = [[], [], []] # set the Y average values to empty lists if exposure analysis is not selected for use in the GUI
        
        changes = [WB_changes, Y_changes] # combine the detected changes for both analyses into a single list to return to the GUI
        print(changes) # print the detected changes for debugging purposes, will be removed in the final version of the GUI
        avg_values = [self.CCT_avg_values, self.Y_avg_values] # store the average values for both analyses in a variable to be returned to the GUI for use in the visualization of the analysis data

        return changes, avg_values # return the list of detected changes and average values for use in the GUI



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

    def send(self, change_data, selected_analyses):
        if selected_analyses[0]: # if white balance analysis is selected, add markers for the detected changes in the RGB data
             for start, end in zip(change_data[0][0], change_data[0][1]): # Loop through the detected change start frame IDs and add markers to the timeline
                #print(start, end)
                self.timeline.AddMarker(start, 'Yellow', 'WB change', 'Notes', end-start, 'Secret_Word') # Add markers to the timeline at the specified frame IDs
                
        if selected_analyses[1]: # if exposure analysis is selected, add markers for the detected changes in the Y data
             for start, end in zip(change_data[1][0], change_data[1][1]): # Loop through the detected change start frame IDs and add markers to the timeline
                #print(start, end)
                self.timeline.AddMarker(start, 'Rose', 'Exposure change', 'Notes', end-start, 'Secret_Word') # Add markers to the timeline at the specified frame IDs

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

#GuiBuild().destroy() #destroy the GUI after the main loop is exited