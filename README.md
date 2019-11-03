#####################################################################################################

SoilExp 1.0
-
Spatiotemporal analysis of physico-chemical soil records

Authors: Guillaume Boudoire*, Marco Liuzzo, Santino Cappuzzo, Giovanni Giuffrida, Paolo Cosenza, Allan Derrien, Edda Elisa Falcone

ISTITUTO NAZIONALE DI GEOFISICA E VULCANOLOGIA 
SEZIONE DI PALERMO

#####################################################################################################
 
*For questions, comments, and feedback please contact Guillaume Boudoire at guillaume.boudoire@gmail.com

The software accompanies the following manuscript, which should be cited when using it:

Boudoire, G., Liuzzo, M., Cappuzzo, S., Giufridda, G., Cosenza, P., Derrien, A. and Falcone, E.E. (2019). Easy-deployable kit for spatial and temporal electro-gas records on the field: the MEGA instrument and the SoilExp software. Computers & Geosciences.

#####################################################################################################

User instructions for the SoilExp 1.0 distribution:

1) The SoilExp 1.0 software distribution is written in Python 2.7 and can be run either on MacOS and Windows distributions. The source code was successfully tested on OS X Mojave and on Windows 10.

2) The SoilExp 1.0 software distribution is provided as a .zip file composed of the present « README file » (.txt), an « user manual » (.pdf) and five folders: two folders hosting the Python 2.7 scripts (« Script_MacOSX » and « Script_Windows ») and three folders containing test files (« Input » for the formatting of rawfiles downloaded from the MEGA hardware, « Intermediate » for the formatting of cleaned files able to be processed for the spatial or temporal analysis and, « Output » for the final .csv files that may be produced by the user using the software)

3) Python scripts require the use of Pandas, Numpy, SciPy, Matplotlib, Scikit-Learn, PySerial libraries. Actually to use the SoilExp 1.0 software distribution we have used the Spyder 2 or 3 open source cross-platform integrated development environment (IDE) with the Anaconda distribution in order to benefit from the integration of scientific libraries. Even if it should be possible to use the software by a manual installation of the required libraries, we only guarantee the use of the software under the same test conditions we have performed.

To run the SoilExp 1.0 distribution:

1) Install the Anaconda distribution (Python 2.7) available for your MacOS or Windows machine (https://www.anaconda.com/download) and set the PySerial library from the Anaconda « Environments ».

2) Run the Spyder open source cross-platform integrated development environment (IDE). 

3) Go in Spyder Tools > Preferences > IPython console > Graphics and select « Tkinter » > OK.

4) Go in Spyder Tools > Preferences > Run > Execute in a new dedicated Python console > OK.

5) Check that input (if starting from rawfiles from the MEGA hardware) or intermediate files respect the file formatting described in the user manual.

6) Go in Spyder File > Open and select the script you need (in « Script_MacOSX » and « Script_Windows » according to your machine): « GUI_Serial.py » to download the data and calibrate the MEGA hardware, « GUI_Space.py » to process spatial surveys or « GUI_Time.py » to process time series.

7) Press the « Run » green button to execute the selected script and follow the instructions of the user manual to process your dataset.

NB: In case of issues to see the Matplotlib plots, close the Graphical User Interface (GUI) and press the « Run » green button to execute the script in a new console with a reset of all the parameters.

#####################################################################################################
