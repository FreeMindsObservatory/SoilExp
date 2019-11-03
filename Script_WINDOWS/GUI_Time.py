#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on Fri Jan 26 09:32:57 2018
@author: Guillaume Boudoire - INGV Palermo

"""

###############################################################################
############################# INTERFACE TIME ##################################
###############################################################################

""" 
This is the main script to define the GUI related to Time analysis of the data.
Here, are imported the classes and functions from Time.py used to define the 
operator's events. First: the definition of the GUI without actions. Second:
the definition of the events to bind based on Time.py. Third: the main that 
makes the link between the event and the GUI
"""   

###############################################################################
#################### Importation of the main librairies #######################
###############################################################################

from Tkinter import *
import pandas as pd
from Time import *
from tkFileDialog import askopenfilename
from tkFileDialog import askdirectory
from tkMessageBox import *

###############################################################################
####################### Creation of the GUI template ##########################
###############################################################################

################ Creation of the main windows (i.e. "Tk()") ###################

Time = Tk()
Time.title('SoilExp 1.0 : Time')
global width
width = Time.winfo_screenwidth()
global height
height = Time.winfo_screenheight() # Dimensions of the screen, keep global to place correctly the plots in each corner


####### Creation of the containers (i.e. "Frames") in the main windows ########

Part1 = Frame(Time,bg="white", highlightbackground="black", highlightthickness=1)
Rawfile = Frame(Time, bg="white", highlightbackground="black", highlightthickness=1)
Calibration = Frame(Time, bg="white", highlightbackground="black", highlightthickness=1)
Treatment = Frame(Time, bg="white", highlightbackground="black", highlightthickness=1)

Part2 = Frame(Time,bg="white", highlightbackground="black", highlightthickness=1)
Formatted = Frame(Time,bg="white", highlightbackground="black", highlightthickness=1)
Init = Frame(Time, bg="white", highlightbackground="black", highlightthickness=1)
Process = Frame(Time, bg="white", highlightbackground="black", highlightthickness=1)

Part3 = Frame(Time, bg="white", highlightbackground="black", highlightthickness=1)
Correlation = Frame(Time, bg="white", highlightbackground="black", highlightthickness=1)

Part4 = Frame(Time, bg="white", highlightbackground="black", highlightthickness=1)
Save = Frame(Time, bg="white", highlightbackground="black", highlightthickness=1)

################# Disposition of the containers on a grid #####################

Part1.grid(row=0, sticky = W+E+N+S)
Rawfile.grid(row=1, sticky = W+E+N+S)
Calibration.grid(row=2, sticky = W+E+N+S)
Treatment.grid(row=3, sticky = W+E+N+S)

Part2.grid(row=0, column=1, sticky = W+E+N+S)
Formatted.grid(row=1, column=1, sticky = W+E+N+S)
Init.grid(row=2, column=1, sticky = W+E+N+S)
Process.grid(row=3, column=1, sticky = W+E+N+S)

Part3.grid(row=0, column=2, sticky = W+E+N+S)
Correlation.grid(row=1, rowspan=3, column=2, sticky = W+E+N+S)

Part4.grid(row=4, column=0, columnspan=3, sticky = W+E+N+S)
Save.grid(row=5, column=0, columnspan=4, sticky = W+E+N+S)

####### Create and layout the widgets for the first container "Part1" #######
    
Part1.grid_columnconfigure(0, weight=1)

Title1 = Label(Part1, bg="white",text="1. FILE TREATMENT",font="-weight bold")
Title1.grid(row=0, column=0, columnspan=3, sticky = W+E+N+S)

####### Create and layout the widgets for the first container "Rawfile" #######
    
Rawfile.grid_columnconfigure(0, weight=1)

Title2 = Label(Rawfile, bg="white",text="1a. Raw file",font="-weight bold")
Title2.grid(row=0, column=0, columnspan=3, sticky = W+E+N+S)

Input2 = Button(Rawfile, bg="white",text="Load")
Input2.grid(row=1, column=0, columnspan=3, sticky = W+E+N+S)

#### Create and layout the widgets for the second container "Calibration" #####

Calibration.grid_columnconfigure(0, weight=1)

Title3 = Label(Calibration, bg="white",text="1b. Linear Calibration",font="-weight bold")
Title3.grid(row=0, column=0, columnspan=3, sticky = W+E+N+S)

CalParameter = Label(Calibration, bg="white",text="Parameter")
CalParameter.grid(row=1, column=0, sticky = W+E+N+S)
CalSlope = Label(Calibration, bg="white",text="Slope")
CalSlope.grid(row=1, column=1,sticky = W+E+N+S)
CalOffset = Label(Calibration, bg="white",text="Offset")
CalOffset.grid(row=1, column=2,sticky = W+E+N+S)

variable1 = StringVar(Calibration) # variable 1 is the name of the parameter to calibrate
variable1.set('')
CalParameterval = OptionMenu(Calibration, variable1, "...")
CalParameterval.grid(row=2, column=0, sticky = W+E+N+S)
variable2 = StringVar(Calibration) # variable 2 is the slope of the parameter to calibrate
CalSlopeval = Entry(Calibration, textvariable=variable2, width=5)
CalSlopeval.grid(row=2, column=1,sticky = W+E+N+S)
variable3 = StringVar(Calibration) # variable 3 is the offset of the parameter to calibrate
CalOffsetval = Entry(Calibration, textvariable=variable3, width=5)
CalOffsetval.grid(row=2, column=2,sticky = W+E+N+S)

Recalculate = Button(Calibration, bg="white",text="Recalculate")
Recalculate.grid(row=3, sticky = W+E+N+S, columnspan=3)

###### Create and layout the widgets for the third container "Treatment" ######

Treatment.grid_columnconfigure(0, weight=1)

Title4 = Label(Treatment, bg="white",text="1c. Treatment",font="-weight bold")
Title4.grid(row=0, column=0, columnspan=3, sticky = W+E+N+S)

variable7 = StringVar(Treatment) # variable 7 is the interval in seconds that separates two series
variable7.set('60')
Splittime = Label(Treatment, bg="white",text="TimeLag")
Splittime.grid(row=1, column=0, sticky = W+E+N+S)
Svalue = Entry(Treatment, textvariable=variable7, width=5)
Svalue.grid(row=1, column=1,sticky = W+E+N+S)

variable7a = StringVar(Treatment) # variable 7 is the interval in seconds that separates two series
variable7a.set('1')
SamplingRa = Label(Treatment, bg="white",text="Sampling Rate")
SamplingRa.grid(row=2, column=0, sticky = W+E+N+S)
SampVal = Entry(Treatment, textvariable=variable7a, width=5)
SampVal.grid(row=2, column=1,sticky = W+E+N+S)

variable8 = StringVar(Treatment) # variable 8 is the Vmin battery
variable8.set('12')
variable9 = StringVar(Treatment) # variable 9 is the Vmax battery
variable9.set('14')
Voltage = Label(Treatment, bg="white",text="Battery")
Voltage.grid(row=3, column=0, sticky = W+E+N+S)
Vmin = Entry(Treatment, textvariable=variable8, width=5)
Vmin.grid(row=3, column=1, sticky = W+E+N+S)
Vmax = Entry(Treatment, textvariable=variable9, width=5)
Vmax.grid(row=3, column=2, sticky = W+E+N+S)

variable10 = StringVar(Treatment) # variable 10 is the min pump flux
variable10.set('-15')
variable11 = StringVar(Treatment) # variable 11 is the max pump flux
variable11.set('15')
Flux = Label(Treatment, bg="white",text="Pump")
Flux.grid(row=4, column=0, sticky = W+E+N+S)
Fmin = Entry(Treatment, textvariable=variable10, width=5)
Fmin.grid(row=4, column=1, sticky = W+E+N+S)
Fmax = Entry(Treatment, textvariable=variable11, width=5)
Fmax.grid(row=4, column=2, sticky = W+E+N+S)

variable12 = StringVar(Treatment) # variable 12 is the min hdop
variable12.set('1')
variable13 = StringVar(Treatment) # variable 13 is the max hdop
variable13.set('200')
Satellite = Label(Treatment, bg="white",text="HDOP")
Satellite.grid(row=5, column=0, sticky = W+E+N+S)
Smin = Entry(Treatment, textvariable=variable12, width=5)
Smin.grid(row=5, column=1, sticky = W+E+N+S)
Smax = Entry(Treatment, textvariable=variable13, width=5)
Smax.grid(row=5, column=2, sticky = W+E+N+S)

variable14 = StringVar(Treatment) # variable 14 is the soil permeabilty (k in micrometersquared)
variable14.set('35')
Convflux = Label(Treatment, bg="white",text="Soil Permeability")
Convflux.grid(row=6, column=0, sticky = W+E+N+S)
Convfluxval = Entry(Treatment, textvariable=variable14, width=5)
Convfluxval.grid(row=6, column=1, sticky = W+E+N+S)
variable15 = IntVar(Treatment) # variable 15 is '0' if none or '1' if checked
Cocher = Checkbutton(Treatment, variable=variable15)
Cocher.grid(row=6, column=2, sticky = W+E+N+S)

Apply = Button(Treatment, bg="white",text="Clean & Split")
Apply.grid(row=7, sticky = W+E+N+S, columnspan=3)

####### Create and layout the widgets for the first container "Part2" #######
    
Part2.grid_columnconfigure(0, weight=1)

Title5 = Label(Part2, bg="white",text="2. DATA PROCESSING",font="-weight bold")
Title5.grid(row=0, column=0, columnspan=4, sticky = W+E+N+S)

####### Create and layout the widgets for the first container "Formatted" #######
    
Formatted.grid_columnconfigure(0, weight=1)

Title6 = Label(Formatted, bg="white",text="2a. Formatted file",font="-weight bold")
Title6.grid(row=0, column=0, columnspan=4, sticky = W+E+N+S)

Input6 = Button(Formatted, bg="white",text="Load")
Input6.grid(row=1, column=0, columnspan=4, sticky = W+E+N+S)

##### Create and layout the widgets for the fourth container "Init" #####

Init.grid_columnconfigure(0, weight=1)

Title7 = Label(Init, bg="white",text="2b. Initialize",font="-weight bold")
Title7.grid(row=0, column=0, columnspan=4, sticky = W+E+N+S)

variable4 = StringVar(Init) # variable 4 is the parameter to study
variable4.set('')
Choice = Label(Init, bg="white",text="Time Serie")
Choice.grid(row=2, column=0, sticky = W+E+N+S)
Serie = OptionMenu(Init, variable4, "...")
Serie.grid(row=2, column=1, columnspan=3, sticky = W+E+N+S)

variable16 = StringVar(Init) # variable 16 is the min of the zoom
variable16.set('0')
variable17 = StringVar(Init) # variable 17 is the max of the zoom
variable17.set('-1')
Zoom = Label(Init, bg="white",text="Zoom")
Zoom.grid(row=3, column=0, sticky = W+E+N+S)
Zoommin = Entry(Init,textvariable=variable16,width=5)
Zoommin.grid(row=3, column=1, sticky = W+E+N+S)
Zoomlab = Label(Init, bg="white",text="start / stop", font="-slant italic")
Zoomlab.grid(row=3, column=2, sticky = W+E+N+S)
Zoommax = Entry(Init,textvariable=variable17,width=5)
Zoommax.grid(row=3, column=3, sticky = W+E+N+S)

Input7 = Button(Init, bg="white",text="Initialize")
Input7.grid(row=4, column=0, columnspan=4, sticky = W+E+N+S)

##### Create and layout the widgets for the fourth container "Process" #####

Process.grid_columnconfigure(0, weight=1)

Title8 = Label(Process, bg="white",text="2c. Process",font="-weight bold")
Title8.grid(row=0, column=0, columnspan=4, sticky = W+E+N+S)

variable18 = StringVar(Process) # variable 18 is the slope of the regression
variable18.set('0')
variable19 = StringVar(Process) # variable 19 is the offset of the regression
variable19.set('0')
variable5 = StringVar(Process) # variable 5 is the parameter used for the regression
variable5.set('')
Regression = Label(Process, bg="white",text="Regression")
Regression.grid(row=1, column=0, sticky = W+E+N+S)
Slope = Entry(Process,textvariable=variable18,width=5)
Slope.grid(row=1, column=1, sticky = W+E+N+S)
ParamReg = OptionMenu(Process, variable5, "...")
ParamReg.grid(row=1, column=2, sticky = W+E+N+S)
Constant = Entry(Process,textvariable=variable19,width=5)
Constant.grid(row=1, column=3, sticky = W+E+N+S)

variable20 = StringVar(Process) # variable 20 is the windows of the moving average
variable20.set('0')
Moving = Label(Process, bg="white",text="MovAverage")
Moving.grid(row=2, column=0, sticky = W+E+N+S)
Average = Entry(Process,textvariable=variable20,width=5)
Average.grid(row=2, column=1, sticky = W+E+N+S)
Movlab = Label(Process, bg="white",text="time window", font="-slant italic")
Movlab.grid(row=2, column=2, sticky = W+E+N+S)

variable21 = StringVar(Process) # variable 21 is the fmin for the FFT cut-off
variable21.set('1')
variable22 = StringVar(Process) # variable 22 is the fmax for the FFT cut-off
variable22.set('1')
Filter = Label(Process, bg="white",text="CutBand")
Filter.grid(row=3, column=0, sticky = W+E+N+S)
FFTmin = Entry(Process,textvariable=variable21,width=5)
FFTmin.grid(row=3, column=1, sticky = W+E+N+S)
FFTlab = Label(Process, bg="white",text="min / max", font="-slant italic")
FFTlab.grid(row=3, column=2, sticky = W+E+N+S)
FFTmax = Entry(Process,textvariable=variable22,width=5)
FFTmax.grid(row=3, column=3, sticky = W+E+N+S)

variable6 = StringVar(Process) # variable 6 is the compared parameter
variable6.set('')
ChoiceCompa = Label(Process, bg="white",text="Comparison")
ChoiceCompa.grid(row=4, column=0, sticky = W+E+N+S)
SerieCompa = OptionMenu(Process, variable6, "...")
SerieCompa.grid(row=4, column=1, columnspan=3, sticky = W+E+N+S)

Export1 = Button(Process, bg="white",text="Treated vs. Raw")
Export1.grid(row=5, column=0, columnspan=2, sticky = W+E+N+S)

Export2 = Button(Process, bg="white",text="Treated vs. Comparative")
Export2.grid(row=5, column=2, columnspan=2, sticky = W+E+N+S)

Export3 = Button(Process, bg="white",text="Spectra")
Export3.grid(row=6, column=0, columnspan=2, sticky = W+E+N+S)

Export4 = Button(Process, bg="white",text="Spectrogram")
Export4.grid(row=6, column=2, columnspan=2, sticky = W+E+N+S)

Export5 = Button(Process, bg="white",text="Correlations")
Export5.grid(row=7, column=0, columnspan=2, sticky = W+E+N+S)

Export6 = Button(Process, bg="white",text="Find Anomaly")
Export6.grid(row=7, column=2, columnspan=2, sticky = W+E+N+S)
variable6a = IntVar(Process) # variable 15 is '0' if none or '1' if checked
Cocher2 = Checkbutton(Process, variable=variable6a)
Cocher2.grid(row=8, column=0, sticky = W+E+N+S)
Anomaly = Label(Process, bg="white",text="Threshold")
Anomaly.grid(row=8, column=1, sticky = W+E+N+S)
variable6aa = StringVar(Process) # variable 22 is the fmax for the FFT cut-off
variable6aa.set('0')
Ano = Entry(Process,textvariable=variable6aa,width=5)
Ano.grid(row=8, column=2, columnspan=2, sticky = W+E+N+S)

######## Create and layout the widgets for the fifth container "Part3" #########

Part3.grid_columnconfigure(0, weight=1)

Title9 = Label(Part3, bg="white",text="3. DATA ANALYSIS",font="-weight bold")
Title9.grid(row=0, column=0, columnspan=6, sticky = W+E+N+S)

####### Create and layout the widgets for the output container "Correlation" #######

Correlation.grid_rowconfigure(0, weight=1)

V1 = StringVar(Correlation) # V1-V15 are the names of the parameters records on all the channels (13 with calib and 2 without)
V1.set('')
P1 = Label(Correlation, textvariable=V1, width=10)
P1.grid(row=1, column=0, sticky = W+E+N+S)
V2 = StringVar(Correlation)
V2.set('')
P2 = Label(Correlation, textvariable=V2, width=10)
P2.grid(row=2, column=0, sticky = W+E+N+S)
V3 = StringVar(Correlation)
V3.set('')
P3 = Label(Correlation, textvariable=V3, width=10)
P3.grid(row=3, column=0, sticky = W+E+N+S)
V4 = StringVar(Correlation)
V4.set('')
P4 = Label(Correlation, textvariable=V4, width=10)
P4.grid(row=4, column=0, sticky = W+E+N+S)
V5 = StringVar(Correlation)
V5.set('')
P5 = Label(Correlation, textvariable=V5, width=10)
P5.grid(row=5, column=0, sticky = W+E+N+S)
V6 = StringVar(Correlation)
V6.set('')
P6 = Label(Correlation, textvariable=V6, width=10)
P6.grid(row=6, column=0, sticky = W+E+N+S)
V7 = StringVar(Correlation)
V7.set('')
P7 = Label(Correlation, textvariable=V7, width=10)
P7.grid(row=7, column=0, sticky = W+E+N+S)
V8 = StringVar(Correlation)
V8.set('')
P8 = Label(Correlation, textvariable=V8, width=10)
P8.grid(row=8, column=0, sticky = W+E+N+S)
V9 = StringVar(Correlation)
V9.set('')
P9 = Label(Correlation, textvariable=V9, width=10)
P9.grid(row=9, column=0, sticky = W+E+N+S)
V10 = StringVar(Correlation)
V10.set('')
P10 = Label(Correlation, textvariable=V10, width=10)
P10.grid(row=10, column=0, sticky = W+E+N+S)
V11 = StringVar(Correlation)
V11.set('')
P11 = Label(Correlation, textvariable=V11, width=10)
P11.grid(row=11, column=0, sticky = W+E+N+S)
V12 = StringVar(Correlation)
V12.set('')
P12 = Label(Correlation, textvariable=V12, width=10)
P12.grid(row=12, column=0, sticky = W+E+N+S)
V13 = StringVar(Correlation)
V13.set('')
P13 = Label(Correlation, textvariable=V13, width=10)
P13.grid(row=13, column=0, sticky = W+E+N+S)
V14 = StringVar(Correlation)
V14.set('')
P14 = Label(Correlation, textvariable=V14, width=10)
P14.grid(row=14, column=0, sticky = W+E+N+S)
V15 = StringVar(Correlation)
V15.set('')
P15 = Label(Correlation, textvariable=V15, width=10)
P15.grid(row=15, column=0, sticky = W+E+N+S)

L1 = Label(Correlation, bg="white",text="Slope")
L1.grid(row=0, column=1, sticky = W+E+N+S)
L2 = Label(Correlation, bg="white",text="Offset")
L2.grid(row=0, column=2, sticky = W+E+N+S)
L3 = Label(Correlation, bg="white",text="R2")
L3.grid(row=0, column=3, sticky = W+E+N+S)
L4 = Label(Correlation, bg="white",text="Delay")
L4.grid(row=0, column=4, sticky = W+E+N+S)
L5 = Label(Correlation, bg="white",text="R2")
L5.grid(row=0, column=5, sticky = W+E+N+S)

for j in range (15):
    for i in range (5):
      Data = Entry(Correlation, width=5)
      Data.grid(row=1+j, column=1+i, sticky = W+E+N+S)  
       
###### Create and layout the widgets for the output container "Part4" #######
      
Part4.grid_columnconfigure(0, weight=1)

Title10 = Label(Part4, bg="white",text="4. SAVE",font="-weight bold")
Title10.grid(row=0, column=0, sticky = W+E+N+S)     

###### Create and layout the widgets for the output container "Save" #######

Save.grid_columnconfigure(0, weight=1)

SavBut = Button(Save, bg="white",text="Save Time Serie")
SavBut.grid(row=0, column=0, sticky = W+E+N+S)
        
###############################################################################
#################### Definition of the operator's events ######################
###############################################################################
def selection(dic,na,sl,of,*pargs):
    """ This function is used in the "trace" of the set_filename function in 
    order to give to variable2 and 3 the float of the slope (sl) and the offset (of)
    from the calibration dictionnary with variable1 as name (na)"""
    na.get()
    sl.set(float(dic[na.get()][0]))
    of.set(float(dic[na.get()][1]))

def selection2(na,*pargs):
    """ This function is used in the "trace" of the set_filename function in 
    order to give to variable2 and 3 the float of the slope (sl) and the offset (of)
    from the calibration dictionnary with variable1 as name (na)"""
    na.get()
    
def set_filename(event):
    """ This function open the file, get the calibration values to show and
    return a dataframe without the calibration rows. Modify manually the number
    of parameters that have a calibration (e.g. 12 by default and deb 7) """
    try: # If the file is correctely formated
        file = askopenfilename(filetypes = [("csv files","*.csv")]) # Open the file
        rawfile = pd.read_csv(file, sep=";", engine='python')
        global df
        df = calibration(rawfile,12) # Number of parameter with a calibration
        calib = df.getcalib(7) # Get the calibration as an array (name,slope,offset)
        diction = {}
        nameparam = calib[0]
        slope = calib[1]
        offset = calib[2]
        for i in range(0,len(nameparam)):
            diction[nameparam[i]]=[slope[i],offset[i]] # Create a dictionnary from the array (name:[slope,offset])
        CalParameterval['menu'].delete(0,END) # Reinitialize the menu of all the OptionMenu
        for val in nameparam:
            CalParameterval['menu'].add_command(label=val,command=lambda v=variable1,l=val:v.set(l)) # Add the new menu with the name from the calibrated sensors (variablei are StringVar() that allow further modifications, see the GUI)
        variable1.trace("w",lambda *pargs: selection(diction,variable1,variable2,variable3,*pargs)) # Record the name selected (trace) and apply the function to the other variables (slope,offset) writting them in the Entry buttons
        showinfo("Raw file","Your file was correctly opened and the calibration imported") # Print a message to say that everything works finely
    except:
        showerror("Error Raw file","1. Please select .csv file \n\n"  "OR \n\n"  "2. Check if your raw file is correctly formated for the software\n\n"  "OR \n\n"  "3. Check any wrong characters in the calibration lines") # Print an error message highlighting the potential issues
        return

def recalculate_newcalib(event):
    """ This function allows the recalibration of the data and remove the calibration
    lines """
    try:
        v1=variable1.get() # Name of the parameter
        v2=float(variable2.get()) # Slope of the parameter
        v3=float(variable3.get()) # Offset of the parameter
        global dg
        dg = df.applycalib(v1,v2,v3) # Apply the calibration from COUNT to VAL
        showinfo("Recalibration","Your file was correctly recalibrated") # Print a message to say that everything works finely
    except:
        showerror("Error Recalibration", "Impossible to recalibrate this parameter: please check the raw file") # Print an error message highlighting the potential issues
        return

def clean_the_dataset(event):
    """ This function cleans the dataframe on the time, on mistakes and on controlled
    parameters (here number of satellites, pump flux and voltage). Then it interpolates
    the dataframe for missing values (linear) and creates a new column recording the
    rows that were interpolated. Finally the dataframe is splitted in intermediate files.
    It is possible to convert CO2 concentration in flux here """
    try:
        v7=float(variable7.get()) # All these parameters are defined above as filtered thresholds, soil permeability and time interval between successive records for the splitting
        v8=float(variable8.get())
        v9=float(variable9.get())
        v10=float(variable10.get())
        v11=float(variable11.get())
        v12=float(variable12.get())
        v13=float(variable13.get())
        v14=float(variable14.get())
        v15=float(variable15.get())
        df1 = initialize(dg)
        df1.clean_time() # Clean on the date
        df1.clean_all() # Clean on badrows and mistakes
        df1.clean_parameter('V_BAT',v8,v9) # Clean on the battery tension
        df1.clean_parameter('HDOP',v12,v13) # Clean on the number of satellites
        df1.clean_parameter('PUMP_FLUX',v10,v11) # Clean on the pump flux
        df1.missing_values() # Back-up of the rows where missing values are present
        df1.interpolate() # Interpolate the dataframe
        showinfo("Clean","Your file was correctly cleaned and interpolated") # Print a message to say that everything works finely
        if v15==0: # Convert CO2 concentration in flux if the CheckButton is activated
            None
        else:
            df1.flux_convert(v14)    
        dir_name = askdirectory()
        df1.split(dir_name,v7) # Split the dataset
        showinfo("Treatment","Your file was correctly splitted in intermediate files") # Print a message to say that everything works finely
    except:
        showerror("Error Treatment", "Impossible to clean and/or split the dataset: please check the raw file or make at least one calibration before cleaning") # Print an error message highlighting the potential issues
        return

def set_filename2(event):
    """ This function asks to open a formatted file from the previous operations
    then identify the name of the parameters to record them in memory, adding 
    the two parameters without calibration. These parameters are then set in 
    listboxs and in the correlations table """
    try:
        file = askopenfilename(filetypes = [("csv files","*.csv")]) # Open the file
        global rawfile2 # Global is required to transmit between functions and keep in memory the operations
        rawfile2 = pd.read_csv(file, sep=";", engine='python')
        global df2
        df2 = calibration(rawfile2,12)
        calib2 = df2.getcalib(6) # Get the calibration as an array (name,slope,offset)
        global nameparam2
        nameparam2 = calib2[0]
        nameparam2.extend([rawfile2.columns[32],rawfile2.columns[33]]) # List of the 13 parameters with calibration and the 2 without calibrations (based on the position of the columns so it is important to preserve the format) 
        Serie['menu'].delete(0,END) # Initialize the listboxs
        ParamReg['menu'].delete(0,END)
        SerieCompa['menu'].delete(0,END)
        for val in nameparam2:    
            Serie['menu'].add_command(label=val,command=lambda v=variable4,l=val:v.set(l)) # Add the name of the paramters in the listboxs
            ParamReg['menu'].add_command(label=val,command=lambda v=variable5,l=val:v.set(l))
            SerieCompa['menu'].add_command(label=val,command=lambda v=variable6,l=val:v.set(l))
        V1.set(nameparam2[0]) # Add the name of the parameters in the correlations table
        V2.set(nameparam2[1])
        V3.set(nameparam2[2])
        V4.set(nameparam2[3])
        V5.set(nameparam2[4])
        V6.set(nameparam2[5])
        V7.set(nameparam2[6])
        V8.set(nameparam2[7])
        V9.set(nameparam2[8])
        V10.set(nameparam2[9])
        V11.set(nameparam2[10])
        V12.set(nameparam2[11])
        V13.set(nameparam2[12])
        V14.set(nameparam2[13])
        V15.set(nameparam2[14])
        variable4.trace("w",lambda *pargs: selection2(variable4,*pargs)) # Get in memory the choice of the parameters used for calculations
        variable5.trace("w",lambda *pargs: selection2(variable5,*pargs)) 
        variable6.trace("w",lambda *pargs: selection2(variable6,*pargs))
        showinfo("Formatted file","Your file was correctly imported") # Print a message to say that everything works finely
    except:
        showerror("Error Formatted file","1. Please select .csv file \n\n"  "OR \n\n"  "2. Check if your formatted file is correctly formated for the software\n\n") # Print an error message highlighting the potential issues
        return 

def initia(event):
    """ This function initialize the dataset recording the name of the parameter
    of interest and the windows to consider (zoom). The parameters of treatment are
    also reinitialize here """
    try:
        v4=variable4.get() # Name of the parameter of interest
        v16=int(variable16.get()) # Zoom min
        v17=int(variable17.get()) # Zoom max
        variable18.set('0')
        variable19.set('0')
        variable20.set('0')
        variable21.set('1')
        variable22.set('1')
        global dtf # The dataframe considered (with the parameter of interest and resized)
        dtf = analysis(rawfile2,v4,v16,v17)
        dtf.date() # Put the date as index of the dataframe
        showinfo("Initialization","Successful") 
    except:
        showerror("Error Initialization", "Impossible to initialize the dataset") # Print an error message highlighting the potential issues
        return         
        
def transform1(event):
    """ This function allows to compare raw with treated data. All methods are 
    applied depending on the values computed by the operator, then they are
    reinitialize to avoid any secondments """
    try:
        v4=variable4.get() # Name of the parameter of interest
        v5=variable5.get() # Get the values used to treat the signal
        v18=float(variable18.get())
        v19=float(variable19.get())
        v20=float(variable20.get())
        v21=float(variable21.get())
        v22=float(variable22.get())
        vtc=float(variable6a.get())
        vth=float(variable6aa.get())
        try:
            dtf.lin_reg(v5, v18, v19) # Try the linear regression
        except:
            pass
        dtf.mov_average(v20) # Moving average
        dtf.filtering(v21, v22) # Cut band
        dtf.plot_graphraw(vtc,vth,rawfile2.columns[2],width,height,v4) # Show the plot in the good corner
        variable18.set('0') # Reinitialize
        variable19.set('0')
        variable20.set('0')
        variable21.set('1')
        variable22.set('1')
    except:
        showerror("Error Processing", "Verify if all labels are filled") # Print an error message highlighting the potential issues
        return 
        
def transform2(event):
    """ This function allows to compare treated with other data. All methods are 
    applied depending on the values computed by the operator, then they are
    reinitialize to avoid any secondments """
    try:
        v4=variable4.get() # Name of the parameter of interest
        v5=variable5.get() # Get the values used to treat the signal
        v6=variable6.get()
        v18=float(variable18.get())
        v19=float(variable19.get())
        v20=float(variable20.get())
        v21=float(variable21.get())
        v22=float(variable22.get())
        try:
            dtf.lin_reg(v5, v18, v19) # Try the linear regression
        except:
            pass
        dtf.mov_average(v20) # Moving average
        dtf.filtering(v21, v22) # Cut band
        dtf.plot_graphcompa(v6,rawfile2.columns[2],width,height,v4) # Show the plot in the good corner
        variable18.set('0') # Reinitialize
        variable19.set('0')
        variable20.set('0')
        variable21.set('1')
        variable22.set('1')
    except:
        showerror("Error Processing", "Verify if all labels are filled") # Print an error message highlighting the potential issues
        return 
        
def transform3(event):
    """ This function allows to show the FFT spectra with the main 3 frequencies.
    All methods are applied depending on the values computed by the operator,
    then they are reinitialize to avoid any secondments """
    try:
        v5=variable5.get() # Get the values used to treat the signal
        v18=float(variable18.get())
        v19=float(variable19.get())
        v20=float(variable20.get())
        v21=float(variable21.get())
        v22=float(variable22.get())
        v7a=float(variable7a.get())
        try:
            dtf.lin_reg(v5, v18, v19) # Try the linear regression
        except:
            pass
        dtf.mov_average(v20) # Moving average
        dtf.filtering(v21, v22) # Cut band
        dtf.spectrum(3,v7a,width,height) # Show the plot in the good corner
        variable18.set('0') # Reinitialize
        variable19.set('0')
        variable20.set('0')
        variable21.set('1')
        variable22.set('1')
    except:
        showerror("Error Processing", "Verify if all labels are filled") # Print an error message highlighting the potential issues
        return 

def transform4(event):
    """ This function allows to show the spectrogram. All methods are 
    applied depending on the values computed by the operator, then they are
    reinitialize to avoid any secondments """
    try:
        v5=variable5.get() # Get the values used to treat the signal
        v18=float(variable18.get())
        v19=float(variable19.get())
        v20=float(variable20.get())
        v21=float(variable21.get())
        v22=float(variable22.get())
        v7a=float(variable7a.get())
        try:
            dtf.lin_reg(v5, v18, v19) # Try the linear regression
        except:
            pass
        dtf.mov_average(v20) # Moving average
        dtf.filtering(v21, v22) # Cut band
        dtf.plot_specgram(v7a,256,128,width,height) # Show the plot in the good corner
        variable18.set('0') # Reinitialize
        variable19.set('0')
        variable20.set('0')
        variable21.set('1')
        variable22.set('1')
    except:
        showerror("Error Processing", "Verify if all labels are filled") # Print an error message highlighting the potential issues
        return 

def transform5(event):
    """ This function allows to calculate and show the results of the correlations
    and of the cross-correlations. All methods are applied depending on the values
    computed by the operator, then they are reinitialize to avoid any secondments """
    try:
        v5=variable5.get() # Get the values used to treat the signal
        v18=float(variable18.get())
        v19=float(variable19.get())
        v20=float(variable20.get())
        v21=float(variable21.get())
        v22=float(variable22.get())
        try:
            dtf.lin_reg(v5, v18, v19) # Try the linear regression
        except:
            pass
        dtf.mov_average(v20) # Moving average
        dtf.filtering(v21, v22) # Cut band
        dicoc=dtf.correlation() # Create the dictionnary linked to the correlation (slope, offset, R2)
        dicocc=dtf.cross_correlation(1) # Create the dictionnary of the cross-correlation (time delay, R2). The number (here 1) highlights that between two measurements there is one second of delay in our case to reconstruct the final time in s and not in number of measurements
        L=[]
        for i in nameparam2:
            L.append(float(dicoc[i][0])) # Create a dictionnary to fill the table
            L.append(float(dicoc[i][1]))
            L.append(float(dicoc[i][2]))
            L.append(float(dicocc[i][1]))
            L.append(float(dicocc[i][0]))
        new_L = ["{:.2f}".format(val) for val in L] # Cut with two decimals
        l = -1
        for j in range(15): # Fill the table   
            for k in range (5):
                l = l+1
                value = StringVar(Correlation)
                value.set(new_L[l])
                Data = Entry(Correlation, width=5, textvariable=value)
                Data.grid(row=1+j, column=1+k, sticky = W+E+N+S) 
        variable18.set('0') # Reinitialize
        variable19.set('0')
        variable20.set('0')
        variable21.set('1')
        variable22.set('1')
    except:
        showerror("Error Processing", "Verify if all labels are filled") # Print an error message highlighting the potential issues
        return 

def transform6(event):
    """ This function allows to set the minimum value of the anomalous population """
    thres=float(dtf.number_pop())
    variable6aa.set(thres) 
    
def export(event):
    """ This function allow to export the final file with the name of the parameter 
    of interest and the first two rows correponding to the raw and treated data """
    try:
        dire_t = askdirectory()
        dtf.record(dire_t)
        showinfo("Export","Successful")
    except:
        showerror("Error Export", "Impossible to save the file")
        return
        
###############################################################################
##################################### MAIN ####################################
###############################################################################
    
Input2.bind('<Button-1>', set_filename) # Bind all the buttons
Recalculate.bind('<Button-1>', recalculate_newcalib)
Apply.bind('<Button-1>', clean_the_dataset)
Input6.bind('<Button-1>', set_filename2)
Input7.bind('<Button-1>', initia)
Export1.bind('<Button-1>', transform1)
Export2.bind('<Button-1>', transform2)
Export3.bind('<Button-1>', transform3)
Export4.bind('<Button-1>', transform4)
Export5.bind('<Button-1>', transform5)
Export6.bind('<Button-1>', transform6)
SavBut.bind('<Button-1>', export)

Time.update() # To get the updated size of the windows
ws = Time.winfo_reqwidth()
hs = Time.winfo_reqheight()
x = (width/2) - (ws/2)
y = (height/2) - (hs/2)
Time.geometry('%dx%d+%d+%d' % (ws, hs, x, y)) # Put the windows in the middle of the screen

Time.mainloop() # Show 







































