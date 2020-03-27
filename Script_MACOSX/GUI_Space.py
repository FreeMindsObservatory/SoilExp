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
from Space import *
from tkFileDialog import askopenfilename
from tkFileDialog import askdirectory
from tkMessageBox import *

###############################################################################
####################### Creation of the GUI template ##########################
###############################################################################

################ Creation of the main windows (i.e. "Tk()") ###################

Space = Tk()
Space.title('SoilExp 1.0 : Space')
global width
width = Space.winfo_screenwidth()
global height
height = Space.winfo_screenheight() # Dimensions of the screen, keep global to place correctly the plots in each corner

####### Creation of the containers (i.e. "Frames") in the main windows ########

Part1 = Frame(Space,bg="white", highlightbackground="black", highlightthickness=1)
Rawfile = Frame(Space, bg="white", highlightbackground="black", highlightthickness=1)
Calibration = Frame(Space, bg="white", highlightbackground="black", highlightthickness=1)
Treatment = Frame(Space, bg="white", highlightbackground="black", highlightthickness=1)

Part2 = Frame(Space,bg="white", highlightbackground="black", highlightthickness=1)
Formatted = Frame(Space,bg="white", highlightbackground="black", highlightthickness=1)
Init = Frame(Space, bg="white", highlightbackground="black", highlightthickness=1)
Stats = Frame(Space, bg="white", highlightbackground="black", highlightthickness=1)
Process = Frame(Space, bg="white", highlightbackground="black", highlightthickness=1)

Part3 = Frame(Space, bg="white", highlightbackground="black", highlightthickness=1)
Correlation = Frame(Space, bg="white", highlightbackground="black", highlightthickness=1)
Statistics = Frame(Space, bg="white", highlightbackground="black", highlightthickness=1)
Maps = Frame(Space, bg="white", highlightbackground="black", highlightthickness=1)

Part4 = Frame(Space, bg="white", highlightbackground="black", highlightthickness=1)
SaveP = Frame(Space, bg="white", highlightbackground="black", highlightthickness=1)
Save = Frame(Space, bg="white", highlightbackground="black", highlightthickness=1)

################# Disposition of the containers on a grid #####################

Part1.grid(row=0, sticky = W+E+N+S)
Rawfile.grid(row=1, sticky = W+E+N+S)
Calibration.grid(row=2, sticky = W+E+N+S)
Treatment.grid(row=3, rowspan=2, sticky = W+E+N+S)

Part2.grid(row=0, column=1, sticky = W+E+N+S)
Formatted.grid(row=1, column=1, sticky = W+E+N+S)
Init.grid(row=2, column=1, sticky = W+E+N+S)
Stats.grid(row=3, column=1, sticky = W+E+N+S)
Process.grid(row=4, column=1, sticky = W+E+N+S)

Part3.grid(row=0, column=2, sticky = W+E+N+S)
Correlation.grid(row=1, rowspan=2, column=2, sticky = W+E+N+S)
Statistics.grid(row=3, column=2, sticky = W+E+N+S)
Maps.grid(row=4, column=2, sticky = W+E+N+S)

Part4.grid(row=5, column=0, columnspan=3, sticky = W+E+N+S)
Save.grid(row=6, column=0, columnspan=2, sticky = W+E+N+S)
SaveP.grid(row=6, column=2, sticky = W+E+N+S)


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

variable4 = StringVar(Treatment) # variable 4 is the interval in seconds that separates two series
variable4.set('60')
Splittime = Label(Treatment, bg="white",text="TimeLag")
Splittime.grid(row=1, column=0, sticky = W+E+N+S)
Svalue = Entry(Treatment, textvariable=variable4, width=5)
Svalue.grid(row=1, column=1,sticky = W+E+N+S)

variable4a = StringVar(Treatment) # variable 7 is the interval in seconds that separates two series
variable4a.set('1')
SamplingRa = Label(Treatment, bg="white",text="Sampling Rate")
SamplingRa.grid(row=2, column=0, sticky = W+E+N+S)
SampVal = Entry(Treatment, textvariable=variable4a, width=5)
SampVal.grid(row=2, column=1,sticky = W+E+N+S)

variable5 = StringVar(Treatment) # variable 5 is the Vmin battery
variable5.set('12')
variable6 = StringVar(Treatment) # variable 6 is the Vmax battery
variable6.set('14')
Voltage = Label(Treatment, bg="white",text="Battery")
Voltage.grid(row=3, column=0, sticky = W+E+N+S)
Vmin = Entry(Treatment, textvariable=variable5, width=5)
Vmin.grid(row=3, column=1, sticky = W+E+N+S)
Vmax = Entry(Treatment, textvariable=variable6, width=5)
Vmax.grid(row=3, column=2, sticky = W+E+N+S)

variable7 = StringVar(Treatment) # variable 7 is the min pump flux
variable7.set('-15')
variable8 = StringVar(Treatment) # variable 8 is the max pump flux
variable8.set('15')
Flux = Label(Treatment, bg="white",text="Pump")
Flux.grid(row=4, column=0, sticky = W+E+N+S)
Fmin = Entry(Treatment, textvariable=variable7, width=5)
Fmin.grid(row=4, column=1, sticky = W+E+N+S)
Fmax = Entry(Treatment, textvariable=variable8, width=5)
Fmax.grid(row=4, column=2, sticky = W+E+N+S)

variable9 = StringVar(Treatment) # variable 9 is the min satellites
variable9.set('1')
variable10 = StringVar(Treatment) # variable 10 is the max satellites
variable10.set('200')
Satellite = Label(Treatment, bg="white",text="HDOP")
Satellite.grid(row=5, column=0, sticky = W+E+N+S)
Smin = Entry(Treatment, textvariable=variable9, width=5)
Smin.grid(row=5, column=1, sticky = W+E+N+S)
Smax = Entry(Treatment, textvariable=variable10, width=5)
Smax.grid(row=5, column=2, sticky = W+E+N+S)

variable11 = StringVar(Treatment) # variable 11 is the min R2 for fitting flux with the accumulation chamber
variable11.set('0.9')
variable12 = StringVar(Treatment) # variable 12 is the max R2 for fitting flux with the accumulation chamber
variable12.set('1.0')
R2 = Label(Treatment, bg="white",text="R-squared")
R2.grid(row=6, column=0, sticky = W+E+N+S)
R2min = Entry(Treatment, textvariable=variable11, width=5)
R2min.grid(row=6, column=1, sticky = W+E+N+S)
R2max = Entry(Treatment, textvariable=variable12, width=5)
R2max.grid(row=6, column=2, sticky = W+E+N+S)

Apply = Button(Treatment, bg="white",text="Clean & Create")
Apply.grid(row=7, sticky = W+E+N+S, columnspan=3)

####### Create and layout the widgets for the first container "Part2" #######
    
Part2.grid_columnconfigure(0, weight=1)

Title5 = Label(Part2, bg="white",text="2. DATA PROCESSING",font="-weight bold")
Title5.grid(row=0, column=0, columnspan=3, sticky = W+E+N+S)

####### Create and layout the widgets for the first container "Formatted" #######
    
Formatted.grid_columnconfigure(0, weight=1)

Title6 = Label(Formatted, bg="white",text="2a. Formatted file",font="-weight bold")
Title6.grid(row=0, column=0, columnspan=3, sticky = W+E+N+S)

Input6 = Button(Formatted, bg="white",text="Load & Init")
Input6.grid(row=1, column=0, columnspan=3, sticky = W+E+N+S)

##### Create and layout the widgets for the fourth container "Init" #####

Init.grid_columnconfigure(0, weight=1)

Title7 = Label(Init, bg="white",text="2b. Subset",font="-weight bold")
Title7.grid(row=0, column=0, columnspan=3, sticky = W+E+N+S)

Zoom = Label(Init, bg="white",text="Start")
Zoom.grid(row=1, column=0, sticky = W+E+N+S)
Zoom = Label(Init, bg="white",text="End")
Zoom.grid(row=1, column=2, sticky = W+E+N+S)

variable13 = StringVar(Init) # variable 13 is the min of the zoom
variable13.set('0')
variable14 = StringVar(Init) # variable 14 is the max of the zoom
variable14.set('-1')
Zoommin = Entry(Init,textvariable=variable13,width=5)
Zoommin.grid(row=2, column=0, sticky = W+E+N+S)
Zoomm = Label(Init, bg="white",text="Subset")
Zoomm.grid(row=2, column=1, sticky = W+E+N+S)
Zoommax = Entry(Init,textvariable=variable14,width=5)
Zoommax.grid(row=2, column=2, sticky = W+E+N+S)

Apply1 = Button(Init, bg="white",text="Zoom")
Apply1.grid(row=3, sticky = W+E+N+S, columnspan=3)

Point = Label(Init, bg="white",text="Point")
Point.grid(row=4, column=0, sticky = W+E+N+S)
Permea = Label(Init, bg="white",text="Permeability")
Permea.grid(row=4, column=1, sticky = W+E+N+S)
Allpoints = Label(Init, bg="white",text="All")
Allpoints.grid(row=4, column=2, sticky = W+E+N+S)

variable15 = StringVar(Init) 
variable15.set('') # variable 15 is the label of the measurement point
CalParameterval2 = OptionMenu(Init, variable15, "...")
CalParameterval2.grid(row=5, column=0, sticky = W+E+N+S)
variable16 = StringVar(Init) 
variable16.set('0') # variable 16 is the soil permeability
Permsolo = Entry(Init,textvariable=variable16,width=5)
Permsolo.grid(row=5, column=1, sticky = W+E+N+S)
variable17 = IntVar(Init)  # variable 17 is a checkbutton
Cocher = Checkbutton(Init, variable=variable17)
Cocher.grid(row=5, column=2, sticky = W+E+N+S)

Apply2 = Button(Init, bg="white",text="Convert CO2")
Apply2.grid(row=6, sticky = W+E+N+S, columnspan=3)

#### Create and layout the widgets for the fourth container "Statistics" ######

Stats.grid_columnconfigure(0, weight=1)

Title8 = Label(Stats, bg="white",text="2c. Parameter",font="-weight bold")
Title8.grid(row=0, column=0, columnspan=3, sticky = W+E+N+S)

Title8 = Label(Stats, bg="white",text="Choose the parameter to study")
Title8.grid(row=1, column=0, columnspan=3, sticky = W+E+N+S)

variable18 = StringVar(Stats) # variable 18 is the parameter to study
variable18.set('')
Serie = OptionMenu(Stats, variable18, "...")
Serie.grid(row=2, column=0, columnspan=3, sticky = W+E+N+S)

Apply3 = Button(Stats, bg="white",text="Statistics")
Apply3.grid(row=3, column=0, columnspan=3, sticky = W+E+N+S)


###### Create and layout the widgets for the fourth container "Process" #######
Process.grid_columnconfigure(0, weight=1)

Title9 = Label(Process, bg="white",text="2d. Regression",font="-weight bold")
Title9.grid(row=0, column=0, columnspan=3, sticky = W+E+N+S)

Sl = Label(Process, bg="white",text="Slope")
Sl.grid(row=1, column=0, sticky = W+E+N+S)
Pr = Label(Process, bg="white",text="Param")
Pr.grid(row=1, column=1, sticky = W+E+N+S)
Of = Label(Process, bg="white",text="Offset")
Of.grid(row=1, column=2, sticky = W+E+N+S)

variable19 = StringVar(Process) # variable 19 is the slope of the regression
variable19.set('0')
variable20 = StringVar(Process) # variable 20 is the offset of the regression
variable20.set('0')
variable21 = StringVar(Process) # variable 21 is the parameter used for the regression
variable21.set('')
Slope = Entry(Process,textvariable=variable19,width=5)
Slope.grid(row=2, column=0, sticky = W+E+N+S)
ParamReg = OptionMenu(Process, variable21, "...")
ParamReg.grid(row=2, column=1, sticky = W+E+N+S)
Constant = Entry(Process,textvariable=variable20,width=5)
Constant.grid(row=2, column=2, sticky = W+E+N+S)

Apply4 = Button(Process, bg="white",text="Correct")
Apply4.grid(row=3, column=0, columnspan=3, sticky = W+E+N+S)

######## Create and layout the widgets for the fifth container "Part3" #########

Part3.grid_columnconfigure(0, weight=1)

Title10 = Label(Part3, bg="white",text="3. DATA ANALYSIS",font="-weight bold")
Title10.grid(row=0, column=0, columnspan=8, sticky = W+E+N+S)

##### Create and layout the widgets for the output container "Correlation" #####

Correlation.grid_rowconfigure(0, weight=1)

Title11 = Label(Correlation, bg="white",text="3a. Correlations",font="-weight bold")
Title11.grid(row=0, column=0, columnspan=8, sticky = W+E+N+S)

L1 = Label(Correlation, bg="white",text="Slope")
L1.grid(row=1, column=1, sticky = W+E+N+S)
L2 = Label(Correlation, bg="white",text="Offset")
L2.grid(row=1, column=2, sticky = W+E+N+S)
L3 = Label(Correlation, bg="white",text="R2")
L3.grid(row=1, column=3, sticky = W+E+N+S)
L4 = Label(Correlation, bg="white",text="Slope")
L4.grid(row=1, column=5, sticky = W+E+N+S)
L5 = Label(Correlation, bg="white",text="Offset")
L5.grid(row=1, column=6, sticky = W+E+N+S)
L6 = Label(Correlation, bg="white",text="R2")
L6.grid(row=1, column=7, sticky = W+E+N+S)

V1 = StringVar(Correlation) # V1-V16 are the names of the parameters records on all the channels (13 with calib and 2 without + FLUX CO2)
V1.set('')
P1 = Label(Correlation, textvariable=V1, width=10)
P1.grid(row=2, column=0, sticky = W+E+N+S)
V2 = StringVar(Correlation)
V2.set('')
P2 = Label(Correlation, textvariable=V2, width=10)
P2.grid(row=3, column=0, sticky = W+E+N+S)
V3 = StringVar(Correlation)
V3.set('')
P3 = Label(Correlation, textvariable=V3, width=10)
P3.grid(row=4, column=0, sticky = W+E+N+S)
V4 = StringVar(Correlation)
V4.set('')
P4 = Label(Correlation, textvariable=V4, width=10)
P4.grid(row=5, column=0, sticky = W+E+N+S)
V5 = StringVar(Correlation)
V5.set('')
P5 = Label(Correlation, textvariable=V5, width=10)
P5.grid(row=6, column=0, sticky = W+E+N+S)
V6 = StringVar(Correlation)
V6.set('')
P6 = Label(Correlation, textvariable=V6, width=10)
P6.grid(row=7, column=0, sticky = W+E+N+S)
V7 = StringVar(Correlation)
V7.set('')
P7 = Label(Correlation, textvariable=V7, width=10)
P7.grid(row=8, column=0, sticky = W+E+N+S)
V8 = StringVar(Correlation)
V8.set('')
P8 = Label(Correlation, textvariable=V8, width=10)
P8.grid(row=9, column=0, sticky = W+E+N+S)
V9 = StringVar(Correlation)
V9.set('')
P9 = Label(Correlation, textvariable=V9, width=10)
P9.grid(row=2, column=4, sticky = W+E+N+S)
V10 = StringVar(Correlation)
V10.set('')
P10 = Label(Correlation, textvariable=V10, width=10)
P10.grid(row=3, column=4, sticky = W+E+N+S)
V11 = StringVar(Correlation)
V11.set('')
P11 = Label(Correlation, textvariable=V11, width=10)
P11.grid(row=4, column=4, sticky = W+E+N+S)
V12 = StringVar(Correlation)
V12.set('')
P12 = Label(Correlation, textvariable=V12, width=10)
P12.grid(row=5, column=4, sticky = W+E+N+S)
V13 = StringVar(Correlation)
V13.set('')
P13 = Label(Correlation, textvariable=V13, width=10)
P13.grid(row=6, column=4, sticky = W+E+N+S)
V14 = StringVar(Correlation)
V14.set('')
P14 = Label(Correlation, textvariable=V14, width=10)
P14.grid(row=7, column=4, sticky = W+E+N+S)
V15 = StringVar(Correlation)
V15.set('')
P15 = Label(Correlation, textvariable=V15, width=10)
P15.grid(row=8, column=4, sticky = W+E+N+S)
V16 = StringVar(Correlation)
V16.set('')
P16 = Label(Correlation, textvariable=V16, width=10)
P16.grid(row=9, column=4, sticky = W+E+N+S)

for j in range (8):
    for i in range (3):
      Data = Entry(Correlation, width=5)
      Data.grid(row=2+j, column=1+i, sticky = W+E+N+S)   
      Data2 = Entry(Correlation, width=5)
      Data2.grid(row=2+j, column=5+i, sticky = W+E+N+S)

##### Create and layout the widgets for the fourth container "Statistics" #####

Statistics.grid_columnconfigure(0, weight=1)

Title12 = Label(Statistics, bg="white",text="3b. Statistics",font="-weight bold")
Title12.grid(row=0, column=0, columnspan=8, sticky = W+E+N+S)

Lmean = Label(Statistics, bg="white",text="Mean")
Lmean.grid(row=1, column=0, sticky = W+E+N+S)
variable22 = StringVar(Statistics) # variable 22 is the mean
variable22.set('')
Mean = Entry(Statistics,textvariable=variable22,width=5)
Mean.grid(row=1, column=1, sticky = W+E+N+S)

Lmed = Label(Statistics, bg="white",text="Median")
Lmed.grid(row=1, column=2, sticky = W+E+N+S)
variable23 = StringVar(Statistics) # variable 23 is the median
variable23.set('')
Median = Entry(Statistics,textvariable=variable23,width=5)
Median.grid(row=1, column=3, sticky = W+E+N+S)

Lmin = Label(Statistics, bg="white",text="Min")
Lmin.grid(row=1, column=4, sticky = W+E+N+S)
variable24 = StringVar(Statistics) # variable 24 is the min
variable24.set('')
Min = Entry(Statistics,textvariable=variable24,width=5)
Min.grid(row=1, column=5, sticky = W+E+N+S)

Lmax = Label(Statistics, bg="white",text="Max")
Lmax.grid(row=1, column=6, sticky = W+E+N+S)
variable25 = StringVar(Statistics) # variable 25 is the max
variable25.set('')
Max = Entry(Statistics,textvariable=variable25,width=5)
Max.grid(row=1, column=7, sticky = W+E+N+S)

Lstd = Label(Statistics, bg="white",text="Stdev")
Lstd.grid(row=2, column=0, sticky = W+E+N+S)
variable26 = StringVar(Statistics) # variable 26 is the standard deviation
variable26.set('')
Std = Entry(Statistics,textvariable=variable26,width=5)
Std.grid(row=2, column=1, sticky = W+E+N+S)

Lkurt = Label(Statistics, bg="white",text="Kurtosis")
Lkurt.grid(row=2, column=2, sticky = W+E+N+S)
variable27 = StringVar(Statistics) # variable 27 is the kurtosis
variable27.set('')
Kurt = Entry(Statistics,textvariable=variable27,width=5)
Kurt.grid(row=2, column=3, sticky = W+E+N+S)

Lskew = Label(Statistics, bg="white",text="Skewness")
Lskew.grid(row=2, column=4, sticky = W+E+N+S)
variable28 = StringVar(Statistics) # variable 28 is the skewness
variable28.set('')
Skew = Entry(Statistics,textvariable=variable28,width=5)
Skew.grid(row=2, column=5, sticky = W+E+N+S)

Lpop = Label(Statistics, bg="white",text="N° Populations")
Lpop.grid(row=2, column=6, sticky = W+E+N+S)
variable29 = StringVar(Statistics) # variable 29 is the number of populations
variable29.set('')
Pop = Entry(Statistics,textvariable=variable29,width=5)
Pop.grid(row=2, column=7, sticky = W+E+N+S)

Apply5 = Button(Statistics, bg="white",text="Distribution")
Apply5.grid(row=3, column=0, columnspan=4, sticky = W+E+N+S)

Apply6 = Button(Statistics, bg="white",text="Cumulative")
Apply6.grid(row=3, column=4, columnspan=4, sticky = W+E+N+S)

######## Create and layout the widgets for the fourth container "Maps" ########

Maps.grid_columnconfigure(0, weight=1)

Title13 = Label(Maps, bg="white",text="3c. Maps",font="-weight bold")
Title13.grid(row=0, column=0, columnspan=8, sticky = W+E+N+S)

API = Label(Maps, bg="white",text="Google API")
API.grid(row=1, column=0, columnspan=4, sticky = W+E+N+S)
variablekey = StringVar(Maps)
variablekey.set('API_KEY')
API_KEY = Entry(Maps,textvariable=variablekey,width=5)
API_KEY.grid(row=1, column=4, columnspan=4, sticky = W+E+N+S)

Lzmap = Label(Maps, bg="white",text="Zoom (5-16)")
Lzmap.grid(row=2, column=0, columnspan=4, sticky = W+E+N+S)
variable31 = StringVar(Maps)  # variable 31 is the zoom to download the map from Google
variable31.set('15')
Zmap = Entry(Maps,textvariable=variable31,width=5)
Zmap.grid(row=2, column=4, columnspan=4, sticky = W+E+N+S)

Apply7 = Button(Maps, bg="white",text="Scatter Map (gradient)")
Apply7.grid(row=3, column=0, columnspan=4, sticky = W+E+N+S)

Apply8 = Button(Maps, bg="white",text="Scatter Map (populations)")
Apply8.grid(row=3, column=4, columnspan=4, sticky = W+E+N+S)
   
####### Create and layout the widgets for the output container "Part4" #######
      
Part4.grid_columnconfigure(0, weight=1)

Title14 = Label(Part4, bg="white",text="4. SAVE ",font="-weight bold")
Title14.grid(row=0, column=0, sticky = W+E+N+S)     

###### Create and layout the widgets for the output container "Save" #######

Save.grid_columnconfigure(0, weight=1)

SavBut = Button(Save, bg="white",text="Save Spatial Survey")
SavBut.grid(row=0, column=0, sticky = W+E+N+S)

###### Create and layout the widgets for the output container "Save" #######

SaveP.grid_columnconfigure(0, weight=1)

Sav2But = Button(SaveP, bg="white",text="Save Populations")
Sav2But.grid(row=0, column=0, sticky = W+E+N+S)
        
################################################################################
##################### Definition of the operator's events ######################
################################################################################

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
    parameters (here number of satellites, pump flux,voltage, R2 CO2 flux). Then it 
    creates different series according to the Timestamp and uses the median to
    represent the measurements points. The intermediate file is thus a file with
    all median """
    try:
        v4=float(variable4.get()) # All these parameters are defined above as filtered thresholds, soil permeability and time interval between successive records for the splitting
        v5=float(variable5.get())
        v6=float(variable6.get())
        v7=float(variable7.get())
        v8=float(variable8.get())
        v9=float(variable9.get())
        v10=float(variable10.get())
        v11=float(variable11.get())
        v12=float(variable12.get())
        df1 = initialize(dg)
        df1.clean_parameter('V_BAT',v5,v6) # Clean on the battery tension
        df1.clean_parameter('HDOP',v9,v10) # Clean on the number of satellites
        df1.clean_parameter('PUMP_FLUX',v7,v8) # Clean on the pump flux
        df1.clean_flux('R-squared',v11,v12) # Clean on the R-square of CO2 flux
        df1.clean_time() # Clean on the date
        showinfo("Clean","Your file was correctly cleaned and interpolated") # Print a message to say that everything works finely  
        dir_name = askdirectory()
        df1.split(dir_name,v4) # Split the dataset
        showinfo("Treatment","Your file was correctly splitted in intermediate files") # Print a message to say that everything works finely
    except:
        showerror("Error Treatment", "Impossible to clean and/or split the dataset: please check the raw file or make at least one calibration before cleaning") # Print an error message highlighting the potential issues
        return

def set_filename2(event):
    """ This function asks to open a formatted file from the previous operations
    then identify the name of the parameters to record them in memory, adding 
    the two parameters without calibration and the CO2 flux. These parameters 
    are then set in listboxs and in the correlations table """
    try:
        file = askopenfilename(filetypes = [("csv files","*.csv")]) # Open the file
        global rawfile2 # Global is required to transmit between functions and keep in memory the operations
        rawfile2 = pd.read_csv(file, sep=";", engine='python')
        global df2
        df2 = calibration(rawfile2,12)
        calib2 = df2.getcalib(8) # Get the calibration as an array (name,slope,offset)
        global nameparam2
        nameparam2 = calib2[0]
        nameparam2.extend([rawfile2.columns[34],rawfile2.columns[35],rawfile2.columns[39]]) # List of the 13 parameters with calibration and the 2 without calibrations (based on the position of the columns so it is important to preserve the format) 
        Serie['menu'].delete(0,END) # Initialize the listboxs
        ParamReg['menu'].delete(0,END)
        for val in nameparam2:    
            Serie['menu'].add_command(label=val,command=lambda v=variable18,l=val:v.set(l)) # Add the name of the paramters in the listboxs
            ParamReg['menu'].add_command(label=val,command=lambda v=variable21,l=val:v.set(l))
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
        V16.set(nameparam2[15])
        variable18.trace("w",lambda *pargs: selection2(variable18,*pargs)) # Get in memory the choice of the parameters used for calculations
        variable21.trace("w",lambda *pargs: selection2(variable21,*pargs)) 
        showinfo("Formatted file","Your file was correctly imported") # Print a message to say that everything works finely
    except:
        showerror("Error Formatted file","1. Please select .csv file \n\n"  "OR \n\n"  "2. Check if your formatted file is correctly formated for the software\n\n") # Print an error message highlighting the potential issues
        return 

def zoom(event):
    """ This function initializes the dataset recording the windows to consider (zoom) """
    try:
        v13=int(variable13.get()) # Zoom min
        v14=int(variable14.get()) # Zoom max
        global dtf # The dataframe considered (with the parameter of interest and resized)
        dtf = processing(rawfile2,v13,v14)
        global points
        points=dtf.get_list_point() # Put the date as index of the dataframe
        CalParameterval2['menu'].delete(0,END) # Initialize the listboxs
        for val in points.keys():    
            CalParameterval2['menu'].add_command(label=val,command=lambda v=variable15,l=val:v.set(l))
        variable15.trace("w",lambda *pargs: selection2(variable15,*pargs))
        global dtr
        dtr = dtf.nothing()
        showinfo("Initialization","Successful") 
    except:
        showerror("Error Initialization", "Impossible to initialize the dataset") # Print an error message highlighting the potential issues
        return  
       
def convert(event):
    """ This function transfors the molar concentration of CO2 in flux according
    the choice of the user (all the dataset or point per point) """
    try:
        v16=float(variable16.get())
        v17=float(variable17.get())
        global dtr
        if v17==0: # Convert CO2 concentration in flux if the CheckButton is activated
            try:
                v15=variable15.get()
                position = points[v15]
                dtr = dtf.CO2_convert_alone(position,v16) # Convert one point
                showinfo("Conversion","This point was correctly converted")
            except:
                None
        else:
            dtr = dtf.CO2_convert_all(v16) # Convert all points
            showinfo("Conversion","Whole dataset converted")
    except:
        showerror("Error Conversion", "Impossible to convert CO2 flux") # Print an error message highlighting the potential issues
        return 

def statsserie(event):
    """ This function initializes the dataset recording the name of the parameter
    of interest and calculates all statistics """
    try:
        v18=variable18.get()
        global dtq
        dtq=analysis(dtr,v18) # Parameter of interest
        dicoc=dtq.correlation() # Create the dictionnary linked to the correlation (slope, offset, R2)
        L=[]
        for i in nameparam2:
            L.append(float(dicoc[i][0])) # Create a dictionnary to fill the table
            L.append(float(dicoc[i][1]))
            L.append(float(dicoc[i][2]))
        new_L = ["{:.2f}".format(val) for val in L] # Cut with two decimals
        l = -1
        for j in range(8): # Fill the table   
            for k in range (3):
                l = l+1
                value = StringVar(Correlation)
                value.set(new_L[l])
                Data = Entry(Correlation, width=5, textvariable=value)
                Data.grid(row=2+j, column=1+k, sticky = W+E+N+S) 
        for j in range(8): # Fill the table   
            for k in range (3):
                l = l+1
                value = StringVar(Correlation)
                value.set(new_L[l])
                Data2 = Entry(Correlation, width=5, textvariable=value)
                Data2.grid(row=2+j, column=5+k, sticky = W+E+N+S)
        statvalue=dtq.statistics()
        variable22.set(float(statvalue[0]))
        variable23.set(float(statvalue[1]))
        variable24.set(float(statvalue[2]))
        variable25.set(float(statvalue[3]))
        variable26.set(float(statvalue[4]))
        variable27.set(float(statvalue[5]))
        variable28.set(float(statvalue[6]))
        variable29.set(float(statvalue[7]))  
    except:
        showerror("Error Statistics", "Not possible to show the statistics: not enough data probably")
        return

def reg(event):
    """ This function allows making a linear regresion on the serie of the
    parameter of interest. Then it recalculates the statistics """
    try:
        try:
            v19=float(variable19.get())
            v20=float(variable20.get())
            v21=variable21.get()
            dtq.lin_reg(v21, v19, v20) # Try the linear regression
        except:
            pass
        dicoc=dtq.correlation() # Create the dictionnary linked to the correlation (slope, offset, R2)
        L=[]
        for i in nameparam2:
            L.append(float(dicoc[i][0])) # Create a dictionnary to fill the table
            L.append(float(dicoc[i][1]))
            L.append(float(dicoc[i][2]))
        new_L = ["{:.2f}".format(val) for val in L] # Cut with two decimals
        l = -1
        for j in range(8): # Fill the table   
            for k in range (3):
                l = l+1
                value = StringVar(Correlation)
                value.set(new_L[l])
                Data = Entry(Correlation, width=5, textvariable=value)
                Data.grid(row=2+j, column=1+k, sticky = W+E+N+S) 
        for j in range(8): # Fill the table   
            for k in range (3):
                l = l+1
                value = StringVar(Correlation)
                value.set(new_L[l])
                Data2 = Entry(Correlation, width=5, textvariable=value)
                Data2.grid(row=2+j, column=5+k, sticky = W+E+N+S)
        statvalue=dtq.statistics()
        variable22.set(float(statvalue[0]))
        variable23.set(float(statvalue[1]))
        variable24.set(float(statvalue[2]))
        variable25.set(float(statvalue[3]))
        variable26.set(float(statvalue[4]))
        variable27.set(float(statvalue[5]))
        variable28.set(float(statvalue[6]))
        variable29.set(float(statvalue[7])) 
    except:
        showerror("Error Correction", "Not possible to apply the linear regression")
        return

def dist(event):
    """ This function creates the distribution plot in the upper left """
    try:
        v18=variable18.get() # Name of the parameter (for the title)
        dtq.distribution(v18,width,height)
    except:
        showerror("Error Plot", "Not possible to see the distribution") # Print an error message highlighting the potential issues
        return    

def cum(event):
    """ This function creates the cumulative plot in the upper right getting the
    number of populations from the label """
    try: 
        v18=variable18.get() # Name of the parameter (for the title)
        v29=float(variable29.get()) # Number of populations
        vi29=int(v29)
        global dicopop # Dictionnary of populations and mixing values
        dicopop = dtq.popul(vi29)
        dtq.graph_combi(v18,dicopop,width,height)
    except:
        showerror("Error Plot", "Not possible to see the cumulative plot") # Print an error message highlighting the potential issues
        return 

def mapall(event):
    """ This function creates the gradient map in the lower left """
    try:
        v18=variable18.get() # Name of the parameter (for the title)
        v31=float(variable31.get()) # Get the zoom to download the map
        vi31=int(v31)
        vkey=str(variablekey.get())
        corners = dtq.download_map(vi31,vkey)
        dtq.plot_campaign_all(v18,corners,width,height)
    except:
        showerror("Error Map", "Choose a correct zoom for the map") # Print an error message highlighting the potential issues
        return   

def mappop(event):
    """ This function creates the populations map in the lower right. It is based 
    on the number of populations from the label """
    try:
        v18=variable18.get() # Name of the parameter (for the title)
        v31=float(variable31.get())  # Get the zoom to download the map
        vi31=int(v31)
        vkey=str(variablekey.get())
        corners = dtq.download_map(vi31,vkey)
        dtq.plot_campaign_pop(v18,dicopop,corners,width,height)
    except:
        showerror("Error Map", "Press 'Cumulative before' or Choose a correct zoom for the map") # Print an error message highlighting the potential issues
        return  

def export(event):
    """ This function allow to export the final file with the name of the parameter 
    of interest and the thrid row correponding to the treated data (if regression applied) """
    try:
        dire_t = askdirectory()
        dtq.record(dire_t)
        showinfo("Export","Successful")
    except:
        showerror("Error Export", "Impossible to save the file")
        return

def save_pop(event):
    """ This function allow to export the final file with the name of the parameter 
    of interest and data distribution between populations """
    try: 
        dir_name2 = askdirectory()
        dtq.savpop(dicopop,dir_name2)
        showinfo("Save Populations","Successful")
    except:
        showerror("Error Export", "Not possible to save the populations statistics") # Print an error message highlighting the potential issues
        return 
        
################################################################################
###################################### MAIN ####################################
################################################################################
    
Input2.bind('<Button-1>', set_filename) # Bind all the buttons
Recalculate.bind('<Button-1>', recalculate_newcalib)
Apply.bind('<Button-1>', clean_the_dataset)
Input6.bind('<Button-1>', set_filename2)
Apply1.bind('<Button-1>', zoom)
Apply2.bind('<Button-1>', convert)
Apply3.bind('<Button-1>', statsserie)
Apply4.bind('<Button-1>', reg)
Apply5.bind('<Button-1>', dist)
Apply6.bind('<Button-1>', cum)
Apply7.bind('<Button-1>', mapall)
Apply8.bind('<Button-1>', mappop)
SavBut.bind('<Button-1>', export)
Sav2But.bind('<Button-1>', save_pop)

Space.update() # To get the updated size of the windows
ws = Space.winfo_reqwidth()
hs = Space.winfo_reqheight()
x = (width/2) - (ws/2)
y = (height/2) - (hs/2)
Space.geometry('%dx%d+%d+%d' % (ws, hs, x, y)) # Put the windows in the middle of the screen

Space.mainloop() # Show 







































