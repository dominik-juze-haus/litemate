import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
import Analysis.source.AnalysisScript as AnalysisScript
import json
import os

default_bg_color = "#001523"
default_fg_color = "#001523"
default_widget_color = "#0082A5"
version = "0.1.0"




class guiBuild(ctk.CTk):
# ---- Initialization and project setup page setup
    def __init__(self):
        super().__init__() #initialize the parent class (CTk)

        ## --------UPDATE WINDOW ICON PATH!!!!!!!!!!!!!--------
        #self.after(201, lambda :self.iconbitmap(r'C:\ZCoding\litemate\icon.ico')) #set the window icon after a short delay to ensure it loads correctly
        # ---- DEFAULT VARIABLES ----
        self.shot_path = None #variable to store the selected shot path    
        self.analysis_data = None #variable to store the analysis data for use in the GUI

        self.geometry('600x400')
        self.configure(bg_color=default_bg_color, fg_color=default_fg_color) #configure the background color of the window

        self.home = ctk.CTkFrame(self) #create a frame for the home page
        self.home.pack(fill="both", expand=True) #pack the frame to fill the entire window and allow it to expand
        self.home.configure(bg_color=default_bg_color, fg_color=default_fg_color) #configure the background color of the home frame

        self.title(f"LiteMate {version}") #set the title of the window
        self.project_setup_page()

# ---- Main page and project setup page function

    def project_setup_page(self):
        self.project_setup_page_frame = ctk.CTkFrame(master = self.home) #frame for the project setup page, master is the home frame
        self.project_setup_page_frame.configure(bg_color=default_bg_color, fg_color=default_fg_color) #configure the background color of the project setup page frame
        self.project_setup_page_frame.pack(side="top", fill="both", expand=True, anchor="center") #pack the project setup page frame to fill the entire home frame and allow it to expand

        # --- Shot selection from files ---
        #shot selection button ----
        self.select_shot_button = ctk.CTkButton(master = self.project_setup_page_frame, 
                                                text="Select Shot", 
                                                font=ctk.CTkFont(size=20), 
                                                fg_color=default_widget_color,
                                                command=self.select_shot_path) #button to open a project
        self.select_shot_button.pack(side="top", padx=20, pady=10) #pack the open project button to the top of the project setup page frame with padding
        
        #selected shot path label ----
        self.selected_shot_path_label = ctk.CTkLabel(master = self.project_setup_page_frame, 
                                                     text=" ", font=ctk.CTkFont(size=16)) #label to display the selected shot path
        self.selected_shot_path_label.pack(side="top", padx=20, pady=10) #pack the selected shot path label to the top of the project setup page frame with padding

        # --- Analysis selections ---
        #analysis selections frame ----
        self.analysis_selections_frame = ctk.CTkFrame(master = self.project_setup_page_frame) #frame for the analysis selections
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
        self.import_analysis_results_button.grid(row=0, column=1, padx=20, pady=10) #grid the import analysis results button in the analysis button frame
        
        # --- Start analysis button ---
        self.start_analysis_button = ctk.CTkButton(master = self.analysis_button_frame, 
                                                  text="Start Analysis", 
                                                  font=ctk.CTkFont(size=20), 
                                                  fg_color=default_widget_color,
                                                  command=self.start_analysis) #button to start the analysis
        self.start_analysis_button.grid(row=0, column=2, padx=20, pady=10) #grid the start analysis button in the analysis button frame

    def select_shot_path(self):
        self.shot_path = filedialog.askopenfilename() #open a file dialog to select a shot
        self.shot_path = os.path.normpath(self.shot_path) #normalize the selected shot path
        self.selected_shot_path_label.configure(text=self.shot_path) #update the selected shot path label with the selected shot path


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

        print("Starting analysis...") #placeholder for starting the analysis, will be replaced with the actual analysis function


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
        self.analysis_path = filedialog.askopenfilename() #open a file dialog to select the analysis results file
        self.analysis_path = os.path.normpath(self.analysis_path) #normalize the selected analysis results file path
        print(f"Selected analysis results file: {self.analysis_path}") #print the selected analysis results file path, will be replaced with the actual function to import and process the analysis results
        self.analysis_data = AnalysisScript.Analysis.opendata(self, self.analysis_path) #call the opendata function from the Analysis class to load the analysis data from the selected file and store it in a variable for use in the GUI

        self.show_analysis_data(self.analysis_data) #call the show_analysis_data function to display the analysis data in the GUI, will be replaced with the actual function to display the analysis data in the GUI

# ----- Plotting the Analysis Data -----
    def show_analysis_data(self, analysis_data):
        
        self.analysis_data = analysis_data #store the analysis data in a variable for use in the GUI
        

    def external_error_message(self, message):
        tk.messagebox.showerror("Error", message) #function to show an error message in a message box

guiBuild().mainloop() #start the GUI main loop