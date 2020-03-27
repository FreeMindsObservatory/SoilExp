#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on Fri Jan 26 09:32:57 2018
@author: Guillaume Boudoire - INGV Palermo

"""

###############################################################################
################################## TIME #######################################
###############################################################################

""" 
This is the main class and functions used to deal with real time data from the
file when connecting on the field
"""   

###############################################################################
#################### Importation of the main librairies #######################
###############################################################################

import copy
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as md
from scipy import stats
from scipy import interpolate
from scipy.fftpack import fft, rfft, irfft, fftfreq, ifft
from sklearn import mixture
from collections import OrderedDict
import time
import datetime as dt

###############################################################################
################ Definition of the main classes and functions #################
###############################################################################

###### Create corrected and interpolated individual intermediate series #######

class calibration:
    """ Class that apply get the calibration data and then remove the 
    corresponding lines from the dataframe. The first line is the name of the
    sensors. The second line is the min calibration. The third line is the max
    calibration. The fourth line is the offset """
    
    def __init__(self,dataframe,nb_calib):
        self.df = dataframe
        self.calib=nb_calib
        
    def getcalib(self,deb):
        """ This method extracts the calibration data and define the slope of 
        the linear calibration and the offset from COUNT_ and VAL_ considering
        that there are nb_calib sensors at fixed place in the datframe. A the 
        end, the calibration data are removed. "deb" is the position of the first
        column where the calibrated parameters begin """ 
        CMIN=[]
        CMAX=[]
        VMIN=[]
        VMAX=[]
        Slope=[]
        Offset=[]
        Cnamecolumns=[]
        Vnamecolumns=[]
        for i in range(0,13):
            Cnamecolumns.append(self.df.columns[2*i+deb])
            Vnamecolumns.append(self.df.columns[(2*i+1)+deb])
        for j in range(len(Cnamecolumns)):
            CMIN.append(float(self.df[Cnamecolumns[j]][0]))
            VMIN.append(float(self.df[Vnamecolumns[j]][0]))
            CMAX.append(float(self.df[Cnamecolumns[j]][1]))
            VMAX.append(float(self.df[Vnamecolumns[j]][1]))
            Offset.append(float(self.df[Vnamecolumns[j]][2])) # Offset of the linear calibration
        for j in range (len(Cnamecolumns)):
            if CMAX[j]-CMIN[j]==0:
                Slope.append(np.nan)
            elif CMAX[j]-CMIN[j]==np.nan:
                Slope.append(np.nan)
            else:
                Slope.append((VMAX[j]-VMIN[j])/(CMAX[j]-CMIN[j])) # Slope of the linear calibration
        self.df = self.df.iloc[3:] # Remove the rows linked to the calibration
        return [Vnamecolumns, Slope, Offset]
        
    def applycalib(self,name,slope,offset): # Input the list of slopes and the list of offset for the calibration
        """ This method applies the new calibration with slope and offset on 
        the VAL_ of the sensors from the COUNT_ column that has to be just before
        (if not modify the code). It allows a first check of the data, checking 
        that all the float frame [:, 2:] is numeric, if not np.nan values 
        instead. [:, :2] corresponds to the first two columns with PUNTO & 
        DATA """
        df1=self.df.iloc[:, :2] # Str part of the dataframe
        df2=self.df.iloc[:, 2:] # Float part of the dataframe
        df2n = df2.convert_objects(convert_numeric=True) # Check if any str in the float frame and add np.nan instead
        positionVAL = df2n.columns.get_loc(name) # Identify poisition of VAL column
        positionCOUNT = positionVAL - 1 # Position of COUNT column
        nameCOUNT = df2n.iloc[:,positionCOUNT].name # Name of COUNT column
        df2n[name] = slope*df2n[nameCOUNT]+offset # Apply the linear calibration                   
        self.df=pd.concat([df1,df2n],axis=1)
        return self.df
        
class initialize:
    """ Class that aims to clean a dataframe by creating np.nan values
    for line with errors and with values not in a define range for one parameter.
    Resulted dataframe maybe interpolated for further calculations and the place
    of interpolated data recorded to be removed further. IMPORTANT: all the 
    methods provide the same input and output dataframe """
    
    def __init__ (self,dataframe): # Input the dataframe and the number of expected values per measurement
        self.df = dataframe
        self.nbvalrow = dataframe.apply(lambda x: x.count(), axis=1)
        self.missing =[]
        self.tdelta=[]
        self.missing=[]
        self.nbval = int(np.median(self.nbvalrow))
            
    def clean_all (self): # Input the parameter to check and the interval of definition to clean the dataframe
        """ This method cleans the dataframe of bad rows. It checks if the number
        of expected values per row is correct (based on the median of values per 
        row in the whole dataframe), if not np.nan on all the line """ 
        for i in range (0,len(self.df.values)):
            if self.nbvalrow.iloc[i]==self.nbval:
                None
            else:
                self.df.iloc[i]=np.nan
        return self.df
        
    def clean_parameter (self,control,controlmin,controlmax): # Input the parameter to check and the interval of definition to clean the dataframe        
        """ This method cleans the dataframe according to a parameter and its
        interval of definition. It puts np.nan values in the checked parameter 
        column for values out of the interval of definition """ 
        for i in range (0,len(self.df.values)):
            if controlmin <= float(self.df[control].iloc[i]) <= controlmax:
                None
            elif self.df[control].iloc[i]==np.nan:
                None
            else:
                self.df.iloc[i]=np.nan
        return self.df
    
    def clean_time (self):
        """ This method cleans the dataframe according to the date. If a date
        has not the format of a date, it will be replaced by pd.nat (equivalent
        np.nan for python). Then, the date is interpolated in order to check if 
        there is any bad date with a changed character. This methods involves a 
        checking of the date with respect to the one before and the one after 
        and thus involves that the first and last lines of the dataframe are good """
        badrows=[] # List of bad rows indexes  
        self.df['DATE']=pd.to_datetime(self.df['DATE'],format='%d/%m/%Y %H:%M:%S',errors='coerce') # Define the format of the date
        self.df['DATE'] = self.df['DATE'].interpolate().ffill().bfill() # Interpolate also the first and last lines with np.nan values if required
        for j in range(0,len(self.df.index)-2): # Test if a bad character is inserted in the date
            if self.df['DATE'].iloc[j] <= self.df['DATE'].iloc[j+1]:   
                None
            else:
                if self.df['DATE'].iloc[j] <= self.df['DATE'].iloc[j+2]: 
                    badrows.append(j+1)
                else:
                    badrows.append(j)
        for k in badrows:
            self.df['DATE'].iloc[k]=np.nan
        return self.df
        
    def missing_values(self):
        """ This method allows to add a column in the dataframe (MISSING) instead 
        of one (HDOP) in order to provide the value 1 if the raw is composed of
        np.nan values and thus will be interpolated. This allows further
        elimination of interpolated rows in the final dataframe """
        dp = pd.isnull(self.df) # Create a dataframe of True and False according is np.nan is present
        for i in range (0,len(dp.index)):
            if float(dp['POINT'].iloc[i])==True: # Check if a value from the PUNTO column is np.nan
                self.missing.append(1)
            else:
                self.missing.append(0)
        del self.df['NB_SATELLITE'] # Remove the NB_SATELLITE column
        self.df['MISSING'] = pd.Series(self.missing,index=self.df.index) # Add the MISSING column
        return self.df
    
    def interpolate (self):
        """ This methods interpolates all the missing values. The first and last
        lines are also interpolated with np.nan values is nothing inside. It is
        possible to choose the method of the interpolation in interpolate(). By
        default, it is a linear interpolation. This methods also create a column
        (TIMELAG) looking the difference between two successives dates and put
        instead the DATA column as index of the future dataframe """
        self.df['DATE'] = pd.to_datetime(self.df['DATE'], format='%d/%m/%Y %H:%M:%S') # Convert the DATA in a date format instead of str
        dates=[] # Code to interpolate the date
        dftime=self.df['DATE'].tolist()
        for i in range (0,len(self.df.index)): # Conversion in UTC timestamp
            if str(dftime[i]) is 'NaT':
                dates.append(np.nan)
            else:
                dates.append(time.mktime(dftime[i].timetuple()))
        Dates=np.array(dates) # Convert the list in array for the shape
        inds = np.arange(Dates.shape[0])
        good = np.where(np.isfinite(Dates))
        f = interpolate.interp1d(inds[good], Dates[good],bounds_error=False)
        B = np.where(np.isfinite(Dates),Dates,f(inds)) # Interpolate date
        C = B.tolist()
        inter_date=[]
        for j in range (0,len(C)): # Conversion in UTC datetime
            inter_date.append(dt.datetime.fromtimestamp(C[j]))
        self.df = self.df.interpolate().ffill().bfill() # Interpolation (possible to define different method of interpolation in the parenthesis)
        self.df.set_index('DATE', inplace=True) # Put the DATA column as index column
        for i in range (0,len(self.df.index)-1):
            self.tdelta.append((self.df.index[i+1]-self.df.index[i]).total_seconds()) # Calculate the delay in second between two dates
        self.tdelta.append((self.df.index[-1]-self.df.index[-2]).total_seconds())
        self.df['TIMELAG'] = pd.Series(self.tdelta,index=self.df.index)
        self.df['DATE'] = pd.Series(inter_date,index=self.df.index) # Replace the date with the interpolated date
        self.df.set_index('DATE', inplace=True)  
        return self.df
    
    def flux_convert (self,permeability):
        """ Apply the formula of Camarda etal. (2006) to convert CO2 concentration
        in flux (simplified equation valable for a pumping flux around 0.8 L/min) """
        self.df['CO2_100%']=self.df['CO2_100%'].apply(lambda x: ((32-5.8*(permeability**0.24))*x*(10**(-2))+6.3*(permeability**0.6)*((x*(10**(-2)))**3))*1000)
        self.df['CO2_10%']=self.df['CO2_10%'].apply(lambda x: ((32-5.8*(permeability**0.24))*x*(10**(-2))+6.3*(permeability**0.6)*((x*(10**(-2)))**3))*1000)
        return self.df
        
    def split(self,name, interval): # Define the interval in seconds that separes two distincts series of measurement 
        """ This method allows to split the initial and corrected dataframe in
        various intermediate files. One created file corresponds to one serie of 
        measurements. The split is based on the TIMELAG column, meaning if 
        a the interval between two successive measurements is important, the 
        dataframe is splited"""
        k = -1
        j = 0
        l = 1
        for i in range (0,len(self.df.index)-1):
            if 0 <= float(self.df['TIMELAG'].iloc[i]) <= interval:
                j = j
                k = k + 1
                l = l
            else:
                self.df.ix[j:k+2].to_csv(name+'/Intermediate_'+str(l)+'.csv',sep=";") # Implement automatically the number of the serie
                j = k + 2
                k = k + 1    
                l = l + 1
        self.df.ix[j:len(self.df.index)].to_csv(name+'/Intermediate_'+str(l)+'.csv',sep=";") # Implement automatically the last serie
        
#################################### Test #####################################
        
#rawfile = pd.read_csv("C:/Users/Marco Liuzzo/Desktop/SoilExp/Input/Time/180628 Stromboli.csv",sep=";", engine='python')
#df = calibration(rawfile,12)
#a = df.getcalib(7)
#dg = df.applycalib(a[0][0],a[1][0],a[2][0])
#df1 = initialize(dg)
#df1.clean_time()
#df1.clean_all()
#df2 = df1.flux_convert(35)
#print df2
#df1.clean_parameter('V_BAT',12,14)
#df1.clean_parameter('HDOP',1,200)
#df1.clean_parameter('PUMP_FLUX',-15,15)
#df1.missing_values()
#df1.interpolate()
#print df2
#df1.split('C:/Users/Marco Liuzzo',60)

###### Create corrected and interpolated individual intermediate series #######

class analysis:
    """ Class that aims to provide the tools in order to treat the signal for
    one parameter, providing at each time the same size of dataframe. Then this
    class provides methods to plot the data """
    
    def __init__(self,dataframe,parameter,zoomin,zoomax):
        self.raw = dataframe[zoomin:zoomax]  # Create a copy to keep the rawdata
        self.df = dataframe[zoomin:zoomax] # Zoom on the good windows
        self.parameter = parameter # Column to study

    def date(self):
        """ This function is indispensable to put the date at index with a 
        recognized pd.datetime format and define a deep copy of the raw data """
        self.raw = copy.deepcopy(self.raw)
        self.df.set_index('DATE', inplace=True) # Indexing the file with the date
        self.df.index = pd.to_datetime(self.df.index, format='%d/%m/%Y %H:%M:%S') # Convert the date in a good format for plot
        return self.df
      
    def mov_average(self,window): 
        """ This method will create an avering average with np.nan values for
        the half window borders. With respect to the other methods, this one is
        applied to the whole dataset, excepting the last two control columns """
        if window % 2 == 0: # Take into consideration the pair windows for np.nan
            window = window + 1
        else :
            None
        for k in self.df.columns[1:-2]: # Apply the moving average to all the column to be compared then for regression, except the last two used to produce final files (e.g. 'MISSING') and the first one (e.g. 'PUNTO') that is a string
            """ Define the first values where the windows is not totally filled """
            ravemin=[]
            for i in range(0,int(window/2)):
                med=0
                nn=0
                for j in range(i-int(window/2),i+int(window/2)):
                    if (j>0 and pd.isnull(self.df[k][i])==0): 
                        med=med+float(self.df[k][j])
                        nn=nn+1
                if (nn>0): 
                    ravemin.append(med/(nn))
                else: 
                    ravemin.append(np.NaN)
            """ Define the last values where the windows is not totally filled """
            ravemax=[]      
            for i in range(len(self.df[k])-int(window/2), len(self.df[k])):
                med=0
                nn=0
                for j in range(i-int(window/2),i+int(window/2)):
                    if (j<len(self.df[k]) and pd.isnull(self.df[k][i])==0): 
                        med=med+float(self.df[k][j])
                        nn=nn+1;
                if (nn>0): 
                    ravemax.append(med/(nn))
                else: 
                    ravemax.append(np.NaN)
            """ Define the rest of the serie """
            weigths = np.repeat(1.0, window)/window
            smas = np.convolve(self.df[k], weigths, 'valid')
            new = sum([ravemin, smas.tolist(), ravemax], []) # Concatenate the 3 lists
            self.df.is_copy = False # Avoid error due to possible interpretation as a copy of a dataframe
            self.df.loc[:,k] = new
        return self.df
    
    def correlation (self):
        """ This method return a dictionnary of the r2, the slope and the offset
        between each column with respect to the studied parameter """
        dictio1={}
        for k in self.df.columns[1:-2]:
            slopecorrel = stats.linregress(self.df[k],self.df[self.parameter])[0]
            offsetcorrel = stats.linregress(self.df[k],self.df[self.parameter])[1]
            rsquarecorrel = (stats.linregress(self.df[k],self.df[self.parameter])[2])**2
            dictio1[k] = [slopecorrel,offsetcorrel,rsquarecorrel]
        return dictio1
    
    def cross_correlation (self,t_time):
        """ This method return the r2 of the best cross-correlation together 
        with the time delay (if positive, it means that the comparative column
        k have a delay, i.e. arrive after. This method is based on FFT circular
        analysis """
        dictio2={}
        for k in self.df.columns[1:-2]:
            A = fft(self.df[self.parameter])
            B = fft(self.df[k])
            Ar = -A.conjugate()
            lag =np.argmax(np.abs(ifft(Ar*B)))            
            k_move = self.df[k]
            inphase = np.roll(k_move, shift=-int(np.ceil(lag)))
            rsquarecorrel = (stats.linregress(inphase,self.df[self.parameter])[2])**2
            dictio2[k] = [rsquarecorrel,lag*t_time]
        return dictio2
            
    def lin_reg (self, param_reg, sl, of):
        """ This method allows a linear regression taking into account the parameter 
        used for the regression, the slope and the offset of the correlation. The 
        value is then offset at the average """
        for i in range (0, len(self.df.index)):
            if float(self.df[self.parameter][i]) == np.nan: # Do not modify np.nan value to not create a biais
                None
            else:
                self.df.at[self.df.index[i],self.parameter] =  self.df.loc[self.df.index[i],self.parameter] - (sl * self.df.loc[self.df.index[i],param_reg] + of) + (sl * self.df[param_reg].mean() + of)
        return self.df
        
    def filtering (self,fmin,fmax):
        """ This method applies a cut-band filter to the signal based on FFT
        analysis between fmin and fmax """
        timef = np.fft.fftfreq(len(self.df[self.parameter]),d=1) # Time range normalised
        signal = np.asarray(self.df[self.parameter]) # Convert the list in array
        W = fftfreq(signal.size, d=(timef[1]-timef[0])) # convert in frequency adapted to the time range and frequential analysis
        f_signal = rfft(signal) # Spectral analysis
        cut_f_signal1 = f_signal.copy() # Cut band filter in the following lines
        cut_f_signal2 = f_signal.copy()
        cut_f_signal = f_signal.copy()
        cut_f_signal1[(np.abs(W)>=float((2*signal.size)/fmax))] = 0
        cut_f_signal2[(np.abs(W)<=float((2*signal.size)/fmin))] = 0
        for i in range(0,signal.size-1):
            if cut_f_signal[i]!=cut_f_signal1[i] and cut_f_signal[i]!=cut_f_signal2[i] :
                cut_f_signal[i]=cut_f_signal1[i]
            else:
                cut_f_signal[i]=cut_f_signal[i]
        cut_signal = irfft(cut_f_signal) # Inverse the signal
        filtered_list = np.array(cut_signal).tolist() # Convert the array in list 
        self.df.loc[:,self.parameter] = filtered_list
        return self.df

    def number_pop(self):
        """ This method allows to determine the number of populations based on the 
        same code that for statistics """
        lis=list(self.df[self.parameter].dropna())
        lis.sort()
        X=np.asarray(lis).reshape(-1,1)
        N = np.arange(1, 10)
        models = [None for i in range(len(N))]
        for i in range(len(N)):
            models[i] = mixture.GaussianMixture(N[i],max_iter=1000,tol=0.05).fit(X) # Simulating for 1 to n populations the best modelling fit with a Gaussian Mixture (see above principle)
        BIC = [m.bic(X) for m in models]
        popnb=1
        item=0
        final = True
        while final == True:
            if float(BIC[item])>float(BIC[item+1]):
                popnb = popnb + 1
                item = item + 1
                final = True
            else:
                popnb = popnb
                item = item
                final = False
        S = models[item].predict_proba(X)
        dicopop = OrderedDict() # Ordered dictionnary to update in the order Pop & Mix 
        for poptype in range(0,popnb):
            dicopop.setdefault(poptype, []) # Initialize the dictionnary for the number of populations
        for pos in range(0,len(lis)):
            for poptype in range(0,popnb): # If a value is composed at more than 95% by a population, it belongs to this population, if not it will be a mixing value
                if float(S[pos][poptype])>0.95:
                    dicopop[poptype].append(float(lis[pos]))
                else:
                    None
        threshold=[]
        for population in dicopop.keys(): # For each population determined the min and the max
            try: 
                threshold.append(min(dicopop[population]))
            except ValueError:
                pass
        threshold.sort() # Order the list of thresholds (min and max for each population)
        limit="{:.2f}".format(threshold[-1])
        return limit
        
    def plot_graphraw(self,act,lim,note,lar,lon,par):
        """ This method will plot the data with raw serie and the corrected serie
        depending on which corrections are applied. The parameter to enter
        corresponds to the column name dedicated to timestamp a special event
        to plot on the graph """
        fig1 = plt.figure(1)
        fig1.canvas.manager.window.resizable(int(lar/2), int(lon/2))
        fig1.canvas.manager.window.wm_geometry("+0+0") 
        fig1.autofmt_xdate() # Set date formatting. This is important to have dates pretty printed 
        Lim=[]
        for i in range(0,len(self.df.index)):
            Lim.append(float(lim))
        ax1 = fig1.add_subplot(111)
        ax1.plot(self.df.index,self.raw[self.parameter],'k-',linewidth=1, label = "Raw Signal")
        ax1.plot(self.df.index,self.df[self.parameter],'r-',linewidth=2, label = "Treated Signal")
        if act==0:
            None
        else:
            ax1.plot(self.df.index,Lim,'r--',linewidth=1, label = 'Threshold: '+str("{:.2f}".format(lim)))
        xfmt = md.DateFormatter('%d/%m/%Y %H:%M:%S')
        ax1.xaxis.set_major_formatter(xfmt)
        xyloc = plt.MaxNLocator(10)
        ax1.xaxis.set_major_locator(xyloc)
        plt.setp(ax1.xaxis.get_majorticklabels(), rotation=30,fontsize=15)
        ax1.legend(fontsize=12)
        for i in range (1,len(self.df[note])-1):
            if self.df[note][i]==1:
                ax1.axvspan(self.df.index[i-1], self.df.index[i-1], alpha=0.2, color='black',fontsize=12) # Timestam event
            else:
                None
        plt.xlabel('UTC Time',fontsize=15)
        plt.ylabel(str(par),fontsize=15)
        plt.yticks(fontsize=15)
        fig1.show()
      
    def plot_graphcompa(self,compa,note,lar,lon,par):
        """ This method will plot the data with the corrected serie and a 
        comparative serie. The parameter to enter corresponds to the column name
        of the comparative serie and the column name dedicated to timestamp 
        a special event to plot on the graph """
        fig2 = plt.figure(2)
        fig2.canvas.manager.window.resizable(int(lar/2), int(lon/2))
        fig2.canvas.manager.window.wm_geometry("+"+str(int(lon/2))+"+0") 
        fig2.autofmt_xdate() # Set date formatting. This is important to have dates pretty printed 
        ax1 = fig2.add_subplot(111)
        lns1 = ax1.plot(self.df.index,self.df[self.parameter],'r-',linewidth=2, label = "Treated Signal")
        xfmt = md.DateFormatter('%d/%m/%Y %H:%M:%S')
        ax1.xaxis.set_major_formatter(xfmt)
        ax11 = ax1.twinx()
        lns2 = ax11.plot(self.df.index,self.df[compa],'g-',linewidth=1, label = "Comparative Signal")
        xfmt = md.DateFormatter('%d/%m/%Y %H:%M:%S')
        ax11.xaxis.set_major_formatter(xfmt)
        xyloc = plt.MaxNLocator(10)
        ax1.xaxis.set_major_locator(xyloc)
        plt.setp(ax1.xaxis.get_majorticklabels(), rotation=30,fontsize=15)
        for i in range (1,len(self.df[note])-1):
            if self.df[note][i]==1:
                ax1.axvspan(self.df.index[i-1], self.df.index[i-1], alpha=0.2, color='black') # Timestam event
            else:
                None
        lns=lns1+lns2
        labs = [l.get_label() for l in lns]
        ax1.legend(lns, labs, fontsize=12, loc=0)
        ax1.set_xlabel('UTC Time',fontsize=15)
        ax1.set_ylabel(str(par),color='r',fontsize=15)
        ax11.set_ylabel(str(compa),color='g',fontsize=15)
        ax1.tick_params(labelsize=15)
        ax11.tick_params(labelsize=15)
        fig2.show()
   
    def spectrum(self,n,samprate,lar,lon): # Analyse spectrale du signal et renvoie les trois fréquences de plus forte amplitude, possibilité de tracer en retirant #
        """ This method provides a spectrum of the signal with a FFT analysis.
        On the spectrum (normalized between 0-1 and considering the symetrie of
        the spectrum), the "n" highest peaks are notes that corresponds to the
        main frequencies of the signal (in unit, i.e. here in s because the 
        sampling rate is in s, but if the sampling rate is 10s this means that
        the corresponding period is "n"*10 s so the real time is between parenthesis """
        fig3 = plt.figure(3)
        fig3.canvas.manager.window.resizable(int(lar/2), int(lon/2))
        fig3.canvas.manager.window.wm_geometry("+0+"+str(int(lar/2))) 
        ax1 = fig3.add_subplot(111)
        n1=len(self.df[self.parameter])
        yf=fft(self.df[self.parameter]) 
        yf=2.0/n1*np.abs(yf[0:n1/2])
        xf=np.fft.fftfreq(n1,d=1)
        ax1.plot(xf[1:n1/2],yf[1:n1/2], 'r-',linewidth=2, label = "FFT Spectrum")
        ax1.set_xlabel('Frequency (/'+str(samprate)+' $Hz$)',fontsize=15)
        ax1.set_ylabel('Amplitude [a.u.]',fontsize=15)
        ax1.tick_params(labelsize=15)
        plt.title(str(self.parameter),fontsize=20)
        ax1.legend(fontsize=12)
        """ Create a derivate of the time serie """
        n2 = len(yf[0:n1/2])
        derivate=np.zeros(n2) 
        k=0 
        d0=np.NaN 
        for i in range(0,n2-1):
            if (np.isnan(yf[0:n1/2][i])==0): 
                d0=yf[0:n1/2][i]
                k=i 
                break
        for i in range(0,n2):
            derivate[i]=np.NaN   
            if (np.isnan(yf[0:n1/2][i])==0 and i>k): 
                derivate[i]=yf[0:n1/2][i]-d0 
                d0=yf[0:n1/2][i] 
                k=i
        """ Find the peaks of the time serie based on the derivate """        
        x=[] 
        y=[]
        n3=len(derivate) 
        a=0 
        i0=0 
        i1=0
        if (derivate[1]>0): 
            x.append(-1) 
            y.append(0)
        for i in range(1,n3):
            if (derivate[i]>0):
                if (a<0): 
                    x.append(int(i1)) 
                    y.append(int(i0))
                i1=i 
                a=1
            if (derivate[i]<0): 
                i0=i 
                a=-1
        if (derivate[n3-1]>0): 
            x.append(int(n3-1))
            y.append(-1)
        """ Identify the peaks to write the value on the plot """        
        n1=len(x)
        for j in range(0,n+1): # Number of peaks to find
            p=0 
            k=-1
            for i in range(0,n1):
                if (x[i]>-1):
                    if (p<yf[x[i]]): 
                        p=yf[x[i]] 
                        k=i
            if (k>-1): # Infinite peak not view on the plot at 0 to adapt the scale to the other peaks
                if (xf[x[k]]==0): 
                    period='inf'
                    period2='inf'
                else: 
                    period=str(int(1/xf[x[k]]))
                    period2=int(1/xf[x[k]])
                ax1.text(xf[x[k]],yf[x[k]],period+' meas. ('+str(period2*int(samprate))+' s)', fontsize=12) 
                x[k]=-1
        fig3.show()
          
    def plot_specgram(self,srate,input_NFFT,input_noverlap,lar,lon):
        """ This method will plot the spectrogram of the corrected serie but let
        the user free to define which NNFT and overlap he wish. By default 256 
        and 128, respectively, are the classical values used: 256 to perform the 
        FFT on 256 measurements and 128 to smooth on a 128 windows. The mode is
        "magnitude" and we applied a linear detrend before. The absisse is the
        number of measurements (i.e. s here because 1Hz measurements) and the 
        frequency the inverse of the time delay (i.e. 1Hz here) """
        fig4 = plt.figure(4)
        fig4.canvas.manager.window.resizable(int(lar/2), int(lon/2))
        fig4.canvas.manager.window.wm_geometry("+"+str(int(lon/2))+"+"+str(int(lar/2))) 
        ax = fig4.add_subplot(111)
        ax.set_xlabel('Time (x'+str(srate)+' $s$)',fontsize=15)
        ax.set_ylabel('Frequency (/'+str(srate)+' $Hz$)',fontsize=15)
        ax.tick_params(labelsize=15)
        plt.title(str(self.parameter),fontsize=20)
        pxx,  freq, t, cax = plt.specgram(self.df[self.parameter], Fs=1, NFFT=input_NFFT, mode='magnitude', noverlap=input_noverlap, detrend='linear', cmap='rainbow')
        fig4.colorbar(cax).set_label('Intensity ($dB$)')
        fig4.tight_layout()
        fig4.show()
    
    def record(self,name):
        """ This method will save a file correctly treated by the operator,
        adding in the first two columns the raw serie and the corrected serie
        of the parameter of interest (e.g. in the name of the file and in the
        name of the column index. Then all interpolated values are set to
        np.nan values thanks to the MISSING value column """
        self.df.is_copy = False
        colr = self.raw[self.parameter].tolist()
        colc = self.df[self.parameter].tolist()
        self.df.insert(1, 'RAW_'+self.parameter, colr)
        self.df.insert(1, 'TREATED_'+self.parameter, colc)  
        for i in range (0,len(self.df.values)):
            if self.df['MISSING'].iloc[i]==1:
                self.df.iloc[i]=np.nan
            else:
                None
        self.df.to_csv(name+'/Final_'+str(self.parameter)+'.csv',sep=";")
     
#################################### Test #####################################
    
#rawfile2 = pd.read_csv("C:\Users\Marco Liuzzo\Desktop\Intermediate_1.csv", sep=";", engine='python')
#dq = analysis(rawfile2,'CO2_10',0,-1)
#dq.date()
#dq.number_pop()
#dq.spectrum(3,10,300,300)
#dq.mov_average(15)
#dq.lin_reg('CO2_100',10,4)
#dq.plot_specgram(10,256,128,300,300)
#dq.plot_graphraw(1,7.194,'MARKER',900,900,'CO2_100')
#dq.plot_graphcompa('CO2_100','MISSING',300,300,'P_atm')
#dq.correlation()
#dq.cross_correlation(1)
#dq.record('/Users/Guillaume/Desktop/')

###############################################################################


























