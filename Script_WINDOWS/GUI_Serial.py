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
This is the main script to define the GUI aimed to download the data and calibrate.
the MEGA hardware. First: the definition of the GUI without actions. Second: the 
definition of the events to bind. Third: the main that makes the link between the 
events and the GUI
"""   

###############################################################################
#################### Importation of the main librairies #######################
###############################################################################

from Tkinter import *
from tkFileDialog import asksaveasfilename
from tkMessageBox import *
import serial
import serial.tools.list_ports
import csv
import binascii

###############################################################################
####################### Creation of the GUI template ##########################
###############################################################################

################ Creation of the main windows (i.e. "Tk()") ###################

Serial = Tk()
Serial.title('SoilExp 1.0 : Serial USB Communication')
global width
width = Serial.winfo_screenwidth()
global height
height = Serial.winfo_screenheight() # Dimensions of the screen, keep global to place correctly the plots in each corner

####### Creation of the containers (i.e. "Frames") in the main windows ########

Part1 = Frame(Serial,bg="white", highlightbackground="black", highlightthickness=1)
Part2 = Frame(Serial,bg="white", highlightbackground="black", highlightthickness=1)

################# Disposition of the containers on a grid #####################

Part1.grid(row=0, sticky = W+E+N+S)
Part1.grid_columnconfigure(0, weight=1)

Part2.grid(row=0, column=1, sticky = W+E+N+S)
Part2.grid_columnconfigure(0, weight=1)

####### Create and layout the widgets for the first container "Part1" #######

Title1 = Label(Part1, bg="white",text="DOWNLOAD & CLEAN MEMORY",font="-weight bold")
Title1.grid(row=0, column=0, columnspan=3, sticky = W+E+N+S)

variable0 = StringVar(Part1) 
variable0.set('COM3')
Root = Label(Part1, bg="white",text="Port")
Root.grid(row=1, column=0, sticky = W+E+N+S)
Port = Entry(Part1, textvariable=variable0, width=5)
Port.grid(row=1, column=1,sticky = W+E+N+S) 

Connect = Button(Part1, bg="white",text="Connect")
Connect.grid(row=2, sticky = W+E+N+S, columnspan=3)

ReadMemory = Button(Part1, bg="white",text="Read Memory")
ReadMemory.grid(row=3, sticky = W+E+N+S, columnspan=3)

SP = Label(Part1, bg="white",text="Starting Point")
SP.grid(row=4, column=0, sticky = W+E+N+S)
EP = Label(Part1, bg="white",text="Ending Point")
EP.grid(row=4, column=1,sticky = W+E+N+S)

variable1 = StringVar(Part1) # variable 1 is the initial row of the aquisition file
Starting_Point = Entry(Part1, textvariable=variable1, width=5)
Starting_Point.grid(row=5, column=0,sticky = W+E+N+S)
variable2 = StringVar(Part1) # variable 2 is the final row of the aquisition file
Ending_Point = Entry(Part1, textvariable=variable2, width=5)
Ending_Point.grid(row=5, column=1,sticky = W+E+N+S)

Download = Button(Part1, bg="white",text="Download")
Download.grid(row=6, sticky = W+E+N+S, columnspan=3)

Clean_Memory = Button(Part1, bg="white",text="Clean Memory")
Clean_Memory.grid(row=7, sticky = W+E+N+S, columnspan=3)

Disconnect = Button(Part1, bg="white",text="Disconnect")
Disconnect.grid(row=8, sticky = W+E+N+S, columnspan=3)

####### Create and layout the widgets for the first container "Part2" #######

Title2 = Label(Part2, bg="white",text="CALIBRATION",font="-weight bold")
Title2.grid(row=0, column=0, columnspan=4, sticky = W+E+N+S)

variable00 = StringVar(Part1) 
variable00.set('COM3')
Root2 = Label(Part2, bg="white",text="Port")
Root2.grid(row=1, column=0, columnspan=2, sticky = W+E+N+S)
Port2 = Entry(Part2, textvariable=variable00, width=5)
Port2.grid(row=1, column=2,columnspan=2, sticky = W+E+N+S) 

Connect2 = Button(Part2, bg="white",text="Connect")
Connect2.grid(row=2, sticky = W+E+N+S, columnspan=4)

Channel = Label(Part2, bg="white",text="Channel")
Channel.grid(row=3, column=0, sticky = W+E+N+S)
NameChannel = Label(Part2, bg="white",text="Sensor")
NameChannel.grid(row=3, column=2, sticky = W+E+N+S)
MinCount = Label(Part2, bg="white",text="Min Count")
MinCount.grid(row=4, column=0, sticky = W+E+N+S)
MaxCount = Label(Part2, bg="white",text="Max Count")
MaxCount.grid(row=4, column=2, sticky = W+E+N+S)
MinVal = Label(Part2, bg="white",text="Min Val")
MinVal.grid(row=5, column=0, sticky = W+E+N+S)
MaxVal = Label(Part2, bg="white",text="Max Val")
MaxVal.grid(row=5, column=2, sticky = W+E+N+S)
OffsetVal = Label(Part2, bg="white",text="Offset Val")
OffsetVal.grid(row=6, column=0, sticky = W+E+N+S)

variable10 = StringVar(Part2) # variable 10 is the numero of the channel
Ch = Entry(Part2, textvariable=variable10, width=5)
Ch.grid(row=3, column=1, sticky = W+E+N+S)
variable11 = StringVar(Part2) # variable 11 is the name of the sensor
NCh = Entry(Part2, textvariable=variable11, width=5)
NCh.grid(row=3, column=3, sticky = W+E+N+S)
variable12 = StringVar(Part2) # variable 12 is the count minimum (calibration)
MinC = Entry(Part2, textvariable=variable12, width=5)
MinC.grid(row=4, column=1, sticky = W+E+N+S)
variable13 = StringVar(Part2) # variable 13 is the count max (calibration)
MaxC = Entry(Part2, textvariable=variable13, width=5)
MaxC.grid(row=4, column=3, sticky = W+E+N+S)
variable14 = StringVar(Part2) # variable 14 is the value min (calibration)
MinV = Entry(Part2, textvariable=variable14, width=5)
MinV.grid(row=5, column=1, sticky = W+E+N+S)
variable15 = StringVar(Part2) # variable 15 is the value max (calibration)
MaxV = Entry(Part2, textvariable=variable15, width=5)
MaxV.grid(row=5, column=3, sticky = W+E+N+S)
variable16 = StringVar(Part2) # variable 16 is the offset (calibration)
Off = Entry(Part2, textvariable=variable16, width=5)
Off.grid(row=6, column=1, sticky = W+E+N+S)

Calib = Button(Part2, bg="white",text="Calibrate")
Calib.grid(row=7, column=0, sticky = W+E+N+S, columnspan=4)

Kchamber = Label(Part2, bg="white",text="Coefficient K")
Kchamber.grid(row=8, column=0, sticky = W+E+N+S)

variable17 = StringVar(Part2) # variable 17 is the K of the accumulation chamber
Kval = Entry(Part2, textvariable=variable17, width=5)
Kval.grid(row=8, column=1, sticky = W+E+N+S)

ChangeK = Button(Part2, bg="white",text="Modify Accumulation Chamber")
ChangeK.grid(row=9, column=0, sticky = W+E+N+S,columnspan=4)

Disconnect2 = Button(Part2, bg="white",text="Disconnect")
Disconnect2.grid(row=10, column=0, sticky = W+E+N+S, columnspan=4)

################################################################################
##################### Definition of the operator's events ######################
################################################################################

def connect(event): # TO DOWNLOAD AND RESET THE MEMORY
    """ This function is used to create the connexion between the hardware and
    the laptop through an USB-serial connexion. Here the baudrate is defined
    by default and fixed as the best value to correctly download the data. The
    root to access to the serial is here reported and may be modified by the user """
    try:
        global ser
        v0=str(variable0.get())
        ser = serial.Serial(v0, baudrate=115200) # Root to the serial and baudrate
        ser.flushInput() # Remove the past commands
        showinfo("Connexion","Success connexion") # Print a success message
    except:
        showerror("Connexion","Failed") # Print an error message highlighting the potential issues
        return
    
def connect2(event): # TO CALIBRATE THE MEGA HARDWARE
    """ This function is used to create the connexion between the hardware and
    the laptop through an USB-serial connexion. Here the baudrate is defined
    by default and fixed as the best value to correctly download the data. The
    root to access to the serial is here reported and may be modified by the user """
    try:
        global ser1
        v00=str(variable00.get())
        ser1 = serial.Serial(v00, baudrate=115200) # Root to the serial and baudrate
        ser1.flushInput() # Remove the past commands
        showinfo("Connexion","Success connexion") # Print a success message
    except:
        showerror("Connexion","Failed") # Print an error message highlighting the potential issues
        return
    
def read_memory(event):
    """ This function is used to read the memory and automatically write the 
    number of the last row of the dataset available: R_MEM on independent serial com """
    ser.flushInput() # Remove the past commands
    try:
        try:
            hex_string = "525F4D454D13" # Command send to the Arduino to read the memory e.g. R_MEM
            download = bytearray.fromhex(hex_string) # Conversion in bytes
            ser.write(download) # Sending the command
            ser_bytes = ser.readline() # Read the response
            decoded_bytes = ser_bytes[0:len(ser_bytes)-2].decode("utf-8") # Convert the response in utf-8
            last = decoded_bytes.encode('utf-8') 
            a = int(filter(str.isdigit, last)) # Keep in memory only digital caracters
            variable1.set(int(1)) # Set first row
            variable2.set(int(a)) # Set last row
        except:
            hex_string = "0A525F4D454D13" # Command send to the Arduino to read the memory e.g. R_MEM
            download = bytearray.fromhex(hex_string) # Conversion in bytes
            ser.write(download) # Sending the command     
            ser_bytes = ser.readline() # Read the response
            decoded_bytes = ser_bytes[0:len(ser_bytes)-2].decode("utf-8") # Convert the response in utf-8
            last = decoded_bytes.encode('utf-8') 
            a = int(filter(str.isdigit, last)) # Keep in memory only digital caracters
            variable1.set(int(1)) # Set first row
            variable2.set(int(a)) # Set last row
    except:
        showerror("Memory","Empty memory") # Print an error message highlighting the potential issues
        return

def download(event):
    """ This function is used to download the data between the first row and
    the last row as defined in the labels (automatically or computed by the
    user. Data are exported in a .csv file """
    try:
        finalfile = asksaveasfilename(filetypes = [("csv files","*.csv")]) # Saved file
        ser_bytes = ser.readline()
        decoded_bytes = ser_bytes[0:len(ser_bytes)-2].decode("utf-8") # Ask for the initial row
        v1=variable1.get() # Record the first row from the label
        V1 = binascii.b2a_hex(v1) # Convert ascii to hex
        start = bytearray.fromhex(V1+'0D0A') # Convert hex to bytes - Last caracters for the return
        ser.write(start) # Send the command
        ser_bytes = ser.readline()
        decoded_bytes = ser_bytes[0:len(ser_bytes)-2].decode("utf-8") 
        v2=variable2.get() # Record the last row from the label
        v2=str(int(v2))
        V2 = binascii.b2a_hex(v2)##############################################
        end = bytearray.fromhex(V2+'0D0A')
        ser.write(end) # Send the command
        for i in range (1,int(v2)+6):
            try: # Write each line in the .csv file delimited by ";"
                ser_bytes = ser.readline()
                decoded_bytes = ser_bytes[0:len(ser_bytes)-2].decode("utf-8")
                with open(finalfile,"a") as f:
                    writer = csv.writer(f,delimiter=";")
                    writer.writerow([decoded_bytes])
                    f.close() ####################################################
            except:
                print("Keyboard Interrupt")
                break
        showinfo("Download","Data saved!") # Print a success message
    except:
        showerror("Download","Impossible to save the data!") # Print an error message highlighting the potential issues
        return
        
def reset_mem(event):
    """ This function is used to reset the memory: M_CLR on independent serial com """
    ser.flushInput() # Remove the past commands
    try:
        try:
            hex_string = "4D5F434C5213" # Command send to the Arduino to reset the memory e.g. M_CLR
            download = bytearray.fromhex(hex_string) 
            ser.write(download) 
        except:
            hex_string = "0A4D5F434C5213" # Command send to the Arduino to reset the memory e.g. M_CLR
            download = bytearray.fromhex(hex_string) 
            ser.write(download) 
        ser.flushInput() #########################################################
        showinfo("Reset","Success clean memory !") # Print a success message 
    except:
        showerror("Reset","Error") # Print an error message highlighting the potential issues
        return

def calib(event):
    """ This function is used to set the calibration values and change the name
    of the headers according the channel: CAL_1 on independent serial com """
    ser1.flushInput() # Remove the past commands
    try:
        try:
            hex_string = "43414C49425F5313" # Command send to the Arduino to calibrate the hardware e.g. CAL_S (may be subsituted by CAL_1 on independent serial communication)
            download = bytearray.fromhex(hex_string) 
            ser1.write(download)  
        except:
            hex_string = "0A43414C49425F5313" # Command send to the Arduino to calibrate the hardware e.g. CAL_S (may be subsituted by CAL_1 on independent serial communication)
            download = bytearray.fromhex(hex_string) 
            ser1.write(download)             
        ser_bytes = ser1.readline()
        decoded_bytes = ser_bytes[0:len(ser_bytes)-2].decode("utf-8")  
        ch = variable10.get()
        CH = binascii.b2a_hex(ch) # Convert ascii to hex
        start = bytearray.fromhex(CH+'0D0A') # Convert hex to bytes - Last caracters for the return      
        ser1.write(start) # Send the command                
        NCh = variable11.get()
        NCH = binascii.b2a_hex(NCh) # Convert ascii to hex
        start = bytearray.fromhex(NCH+'0D0A') # Convert hex to bytes - Last caracters for the return      
        ser1.write(start) # Send the command          
        ctmin = variable12.get()
        CTMIN = binascii.b2a_hex(ctmin) # Convert ascii to hex
        start = bytearray.fromhex(CTMIN+'0D0A') # Convert hex to bytes - Last caracters for the return
        ser1.write(start) # Send the command       
        vmin = variable14.get()
        VMIN = binascii.b2a_hex(vmin) # Convert ascii to hex
        start = bytearray.fromhex(VMIN+'0D0A') # Convert hex to bytes - Last caracters for the return
        ser1.write(start) # Send the command       
        ctmax = variable13.get()
        CTMAX = binascii.b2a_hex(ctmax) # Convert ascii to hex
        start = bytearray.fromhex(CTMAX+'0D0A') # Convert hex to bytes - Last caracters for the return
        ser1.write(start) # Send the command       
        vmax = variable15.get()
        VMAX = binascii.b2a_hex(vmax) # Convert ascii to hex
        start = bytearray.fromhex(VMAX+'0D0A') # Convert hex to bytes - Last caracters for the return
        ser1.write(start) # Send the command      
        off = variable16.get()
        OFFS = binascii.b2a_hex(off) # Convert ascii to hex
        start = bytearray.fromhex(OFFS+'0D0A') # Convert hex to bytes - Last caracters for the return
        ser1.write(start) # Send the command
        showinfo("Calibration","Change updated in the file and on the screen !") # Print a success message
    except:
        showerror("Calibration","Error") # Print an error message highlighting the potential issues
        return
    
def change(event):
    """ This function is used to change the coefficient K of the accumulation
    chamber that is fundamental in the soil gas flux equation: K_PEN on independent 
    serial com """
    ser1.flushInput() # Remove the past commands
    try:
        try:
            hex_string = "4B5F50454E13" # Command send to the Arduino to calibrate the coefficient K of the accumulation chamber e.g. K_PEN             
            download = bytearray.fromhex(hex_string) 
            ser1.write(download)  
        except:
            hex_string = "04B5F50454E13" # Command send to the Arduino to calibrate the coefficient K of the accumulation chamber e.g. K_PEN             
            download = bytearray.fromhex(hex_string) 
            ser1.write(download) 
        ser_bytes = ser1.readline()
        decoded_bytes = ser_bytes[0:len(ser_bytes)-2].decode("utf-8") # Ask for the initial row
        ser_bytes = ser1.readline()
        decoded_bytes = ser_bytes[0:len(ser_bytes)-2].decode("utf-8") # Ask for the initial row
        ch = variable17.get()
        CH = binascii.b2a_hex(ch) # Convert ascii to hex
        start = bytearray.fromhex(CH+'0D0A') # Convert hex to bytes - Last caracters for the return
        ser1.write(start) # Send the command  
        showinfo("Accumulation chamber","Change updated for the coefficient K of the accumulation chamber !") # Print a success message
    except:
        showerror("Calibration","Error") # Print an error message highlighting the potential issues
        return
          
def disconnect(event): # TO DISCONNECT THE COMMUNICATION REGARDING DOWNLOAD/RESET
    """ This function is used to close the connexion """
    try:
        ser.close()
        showinfo("Disconnexion","Success disconnexion") # Print a success message
    except:
        showerror("Disconnexion","Failed") # Print an error message highlighting the potential issues
        return        

def disconnect2(event): # TO DISCONNECT THE COMMUNICATION REGARDING CALIBRATION
    """ This function is used to close the connexion """
    try:
        ser1.close()
        showinfo("Disconnexion","Success disconnexion") # Print a success message
    except:
        showerror("Disconnexion","Failed") # Print an error message highlighting the potential issues
        return  
    
################################################################################
###################################### MAIN ####################################
################################################################################
        
Connect.bind('<Button-1>', connect) # Bind all the buttons
Connect2.bind('<Button-1>', connect2) # Bind all the buttons
ReadMemory.bind('<Button-1>', read_memory)
Download.bind('<Button-1>', download)
Clean_Memory.bind('<Button-1>', reset_mem)
Calib.bind('<Button-1>', calib)
ChangeK.bind('<Button-1>', change)
Disconnect.bind('<Button-1>', disconnect)
Disconnect2.bind('<Button-1>', disconnect2)

Serial.update() # To get the updated size of the windows
ws = Serial.winfo_reqwidth()
hs = Serial.winfo_reqheight()
x = (width/2) - (ws/2)
y = (height/2) - (hs/2)
Serial.geometry('%dx%d+%d+%d' % (ws, hs, x, y)) # Put the windows in the middle of the screen

Serial.mainloop() # Show 
