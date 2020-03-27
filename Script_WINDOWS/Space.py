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

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from sklearn import mixture
import collections
from collections import OrderedDict
from matplotlib.pyplot import cm
import matplotlib.mlab as mlab
import requests
import math
from scipy.misc import imread
import matplotlib.cbook as cbook
import os, sys

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
        
    def clean_flux (self,control,controlmin,controlmax): # Input the parameter to check and the interval of definition to clean the dataframe        
        """ This method cleans the dataframe according to a parameter and its
        interval of definition. It puts np.nan values in the checked parameter 
        column for values out of the interval of definition """ 
        L=np.isnan(list(self.df[control]))
        index=[]
        for i in range(0,len(L)):
            if L[i]==True:
                None
            else:
                index.append(i)
        for j in index:
            if controlmin <= float(self.df[control].iloc[j]) <= controlmax:
                None
            else:
                self.df.iloc[j]=0
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
        self.df['DATE'] = self.df['DATE'].interpolate().ffill().bfill() # Interpolate also the first and last lines with np.nan values if required
        self.df.set_index('DATE', inplace=True) # Put the DATA column as index column
        for i in range (0,len(self.df.index)-1):
            self.tdelta.append((self.df.index[i+1]-self.df.index[i]).total_seconds()) # Calculate the delay in second between two dates
        self.tdelta.append((self.df.index[-1]-self.df.index[-2]).total_seconds())
        self.df['TIMELAG'] = pd.Series(self.tdelta,index=self.df.index)        
        return self.df
        
    def split(self,name, interval): # Define the interval in seconds that separes two distincts series of measurement 
        """ This method allows to split the initial and corrected dataframe in
        one unique intermediate file with median values. The split is based on the 
        TIMELAG column, meaning if a the interval between two successive measurements 
        is important, the median starts for another serie """
        k = -1
        j = 0
        l = 1
        datelist=[]
        labellist=[]
        medianlist=[]
        dicosum=collections.OrderedDict() # Create a dictionnary to record in the order the median of each serie
        for i in range (0,len(self.df.index)-1):
            if 0 <= float(self.df['TIMELAG'].iloc[i]) <= interval: # Define the number of rows in the same serie
                j = j
                k = k + 1
                l = l 
            else:
                datepoint = self.df.index[j] # Distinguish date (as date) from index column
                labelpoint = self.df.ix[j,0] # Distinguish label point (as str) from column O
                medianpoint = self.df.ix[j:k+2,1:].median() # Distinguish median (as float) from column 1:
                datelist.append(datepoint)
                labellist.append(labelpoint)
                medianlist.append(medianpoint)
                j = k + 2
                k = k + 1    
                l = l + 1 # Next time serie
        headers = list(self.df.columns.values)
        datelist.append(self.df.index[j])
        labellist.append(self.df.ix[j,0])
        medianlist.append(self.df.ix[j:-1,1:].median())
        dicosum.update({'DATE':datelist}) # Fill the dictionnary with dates
        dicosum.update({'POINT':labellist}) # Fill the dictionnary with label points
        for m in range (1,len(headers)):
            L=[]
            for n in range (0,len(medianlist)):
                L.append(medianlist[n][m-1])
            dicosum.update({headers[m]:L}) # Fill the dictionnary with median
        dg = pd.DataFrame(dicosum) # Convert the dictionnary in dataframe
        dg.to_csv(name+'/SpatialSerie_'+str(l)+'.csv',sep=";") # Save the file with a record of the number of measurement points in the filename
 
#################################### Test #####################################
        
#rawfile = pd.read_csv("C:/Users/Marco Liuzzo/Desktop/SoilExp/Input/Space/Test.csv",sep=";", engine='python')
#df = calibration(rawfile,12)
#a = df.getcalib(7)
#dg = df.applycalib(a[0][0],a[1][0],a[2][0])
#df1 = initialize(dg)
#df1.clean_parameter('V_BAT',12,14)
#df1.clean_parameter('HDOP',1,200)
#df1.clean_parameter('PUMP_FLUX',-1,1)
#df1.clean_flux('R-squared',0,1)
#df1.clean_time()
#df1.split('/Users/Guillaume/Desktop/SoilExp/Intermediate/Space/SpatialSerie',60)

######### Processing the part of the dataset of interest (zoom, flux) #########

class processing:
    """ Class that aims to process the intermediate cleaned file in order to set
    the initial conditions, i.e. zoom on a part of the file (for example to see
    the result of one transect only), and say if you want to convert the CO2 values
    from all or point per point using a different k soil permeability parameter"""
    
    def __init__(self,dataframe,zoomin,zoomax):
        self.df = dataframe[zoomin:zoomax] # Zoom on the good windows
    
    def nothing(self):
        """ This method is used to return the dataframe without changes """
        return self.df

    def get_list_point(self):
        """ This method gets an ordered dictionnary POINT:index """
        self.df.is_copy = False
        List = OrderedDict()
        for site in range(0,len(self.df.index)):
            List[self.df['POINT'].iloc[site]]=site
        return List
        
    def CO2_convert_alone(self,position,permeability):
        """ Convert point per point the molar concentration in flux thanks to 
        the equation of Camarda et al. (2006) """
        self.df.is_copy = False
        self.df['CO2_100%'].iloc[position]=float(((32-5.8*(permeability**0.24))*(self.df['CO2_100%'].iloc[position])*(10**(-2))+6.3*(permeability**0.6)*(((self.df['CO2_100%'].iloc[position])*(10**(-2)))**3))*1000)
        self.df['CO2_10%'].iloc[position]=float(((32-5.8*(permeability**0.24))*(self.df['CO2_10%'].iloc[position])*(10**(-2))+6.3*(permeability**0.6)*(((self.df['CO2_10%'].iloc[position])*(10**(-2)))**3))*1000)
        return self.df

    def CO2_convert_all(self,permeability):
        """ Convert for all the points the molar concentration in flux thanks to 
        the equation of Camarda et al. (2006) """
        self.df.is_copy = False
        self.df['CO2_100%']=self.df['CO2_100%'].apply(lambda x: ((32-5.8*(permeability**0.24))*x*(10**(-2))+6.3*(permeability**0.6)*((x*(10**(-2)))**3))*1000)
        self.df['CO2_10%']=self.df['CO2_10%'].apply(lambda x: ((32-5.8*(permeability**0.24))*x*(10**(-2))+6.3*(permeability**0.6)*((x*(10**(-2)))**3))*1000)
        return self.df
        
#################################### Test #####################################
    
#rawfile2 = pd.read_csv("C:/Users/Marco Liuzzo/Desktop/SoilExp/Intermediate/Space/SpatialSerie__13.csv", sep=";", engine='python')
#dq = processing(rawfile2,2,-1)
#dr = dq.get_list_point()
##print dr
#dr = dq.CO2_convert_all(35)
#dr = dq.date()

#### Analyse a measurements serie: stat, corr, population, map, reg, compa ####

class analysis:
    """ Class that aims to deals with one data serie to correct, obtain statistics,
    populations, maps, correlations wit other data serie """
    
    def __init__(self,dataframe,parameter):
        self.df = dataframe # Zoom on the good windows
        self.parameter = parameter
        
    def correlation (self):
        """ This method return a dictionnary of the r2, the slope and the offset
        between each column with respect to the studied parameter """
        dictio1={}
        for k in self.df.columns[3:-1]:
            X = (self.df[self.parameter]).tolist()
            Y = (self.df[k]).tolist()
            for i in range (0,len(X)-1):
                if math.isnan(X[i]): # Need to remove np.nan value for the correlation
                    X.remove(X[i])
                    Y.remove(Y[i])
                else:
                    pass
            Xm = np.ma.masked_array(X,mask=np.isnan(Y)).compressed() # Exception to take into account np.nan value in the linear regression
            Ym = np.ma.masked_array(Y,mask=np.isnan(Y)).compressed()
            try:
                slopecorrel = stats.linregress(Ym,Xm)[0]
                offsetcorrel = stats.linregress(Ym,Xm)[1]
                rsquarecorrel = (stats.linregress(Ym,Xm)[2])**2
                dictio1[k] = [slopecorrel,offsetcorrel,rsquarecorrel]
            except:
                dictio1[k] = [np.nan,np.nan,np.nan]
                pass
        return dictio1
        
    def lin_reg (self, param_reg, sl, of):
        """ This method allows a linear regression taking into account the parameter 
        used for the regression, the slope and the offset of the correlation. The 
        value is then offset at the average """
        for i in range (0, len(self.df.index)):
            if float(self.df[self.parameter].iloc[i]) == np.nan: # Do not modify np.nan value to not create a biais
                None
            else:
                self.df.at[self.df.index[i],self.parameter] =  self.df.loc[self.df.index[i],self.parameter] - (sl * self.df.loc[self.df.index[i],param_reg] + of) + (sl * self.df[param_reg].mean() + of)
        return self.df
        
    def statistics (self):
        """ This method allows to get all classical statistics: average, median
        min, max, deviation, skewness, kurtosis and the number of populations using
        the Maximum Likehood Method (Elio et al., 2016) """
        stat=[]
        L=list(self.df[self.parameter].dropna())
        average = np.mean(L) # Average
        med = np.median(L) # Median
        mi = np.amin(L) # Minimum
        ma = np.amax(L) # Maximum
        stdev = np.std(L) # Standard Deviation
        skewness = stats.skew(L) # Skewness
        kurt = stats.kurtosis(L) # Kurosis
        X=np.asarray(L).reshape(-1,1) # Reshape the data serie for Gaussian simulations
        N = np.arange(1, 10) # Number of populations
        models = [None for i in range(len(N))]
        for i in range(len(N)):
            models[i] = mixture.GaussianMixture(N[i],max_iter=1000,tol=0.05).fit(X) # 1000 iterations (Elio et al., 2016) and 0.05 uncertainty
        BIC = [m.bic(X) for m in models] # BIC
        popnb=1
        item=0
        final = True
        while final == True: # Search the minimum BIC to compute the number of population popnb
            if float(BIC[item])>float(BIC[item+1]):
                popnb = popnb + 1
                item = item + 1
                final = True
            else:
                popnb = popnb
                item = item
                final = False
        stat.append(average)
        stat.append(med)
        stat.append(mi)
        stat.append(ma)
        stat.append(stdev)
        stat.append(skewness)
        stat.append(kurt)
        stat.append(popnb)
        return stat

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
        return popnb

    def popul(self,popnb):
        """ This methods is based on a fixed number of populations determined by
        the user. Then it builds a dictionnary with 'Pop' (population) or 'Mix'
        (mixing values between two or more populations) as keys and the corresponding 
        values """ 
        lis=list(self.df[self.parameter].dropna())
        lis.sort()
        X=np.asarray(lis).reshape(-1,1)
        N = np.arange(1, 10)
        models = [None for i in range(len(N))]
        for i in range(len(N)):
            models[i] = mixture.GaussianMixture(N[i],max_iter=1000,tol=0.05).fit(X)
        item = popnb-1
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
                threshold.append(max(dicopop[population]))
            except ValueError:
                pass
        threshold.sort() # Order the list of thresholds (min and max for each population)
        dicosort = OrderedDict()
        for thres in range (0,len(threshold)-1):
            if thres%2==0: # If the position of the threshols can be divided by 2 thus it will be a population
                dicosort.setdefault('Pop'+str(1+thres/2), [])
                for val in lis:
                    if float(threshold[thres]) <= float(val) <= float(threshold[thres+1]):
                        dicosort['Pop'+str(1+thres/2)].append(val)
                    else:
                        pass
            else: # If the position of the threshols cannot be divided by 2 thus it will be a mixing
                dicosort.setdefault('Mix'+str(1+thres/2), [])
                for val in lis:
                    if float(threshold[thres]) < float(val) < float(threshold[thres+1]):
                        dicosort['Mix'+str(1+thres/2)].append(val)
                    else:
                        pass
        for key in dicosort.keys(): # Clean the Mixing keys that are empty
            if bool(dicosort[key]) is False:
                dicosort.pop(key)
            else:
                pass
        return dicosort 
        
    def graph_combi(self,par,dico,lar,lon):
        """ This method produces a plot as a cumulative plot where the results
        of the Maximum Likehood Method are directly shown in order to allow the
        user to checked graphically (GSA) if the number of populations is adapted.
        If not he can adapt the number of populations """
        fig2 = plt.figure(2)
        fig2.canvas.manager.window.resizable(int(lar/2), int(lon/2))
        fig2.canvas.manager.window.wm_geometry("+"+str(int(lon/2))+"+0") 
        ax = fig2.add_subplot(111)
        lis=list(self.df[self.parameter].dropna())
        (quantiles, values), (slope, intercept, r) = stats.probplot(lis, dist='norm')
        index = 0
        lo = len(lis)
        plt.plot(quantiles, values,'ok') # To plot the cumulative plot
        color=cm.bwr(np.linspace(0,1,len(dico.keys()))) # Color for each population
        for key,c in zip(dico.keys(),color):
            ax.plot(quantiles[index:int(index+len(dico[key]))], values[index:int(index+len(dico[key]))],marker='o',c=c,linewidth=0) # Print the population and mixing categories
            if len(dico[key])>1:
                nb = len(values[index:int(index+len(dico[key]))])
                perc = round(100*float(nb)/float(lo),1)
                av = round(np.mean(values[index:int(index+len(dico[key])-1)]),1)
                st = round(np.std(values[index:int(index+len(dico[key])-1)]),1)
            else: # If there is one value for the key to avoid numpy Warning on the mean, deviation ...
                nb = 1
                perc = round(100*float(nb)/float(lo),1)
                av = round(values[index],1)
                st = 0
            ax.annotate(str(key)+' ('+str(perc)+'%): Mean='+str(av)+'+/-'+str(st), xy=(quantiles[int(index+len(dico[key])/2)], values[int(index+len(dico[key])/2)]), xytext=(quantiles[int(index+len(dico[key])/2)]+0.5, values[int(index+len(dico[key])/2)]),color=c,fontsize=12) # Plot the name of the key and the mean+stdev directly on the plot
            index = int(index+len(dico[key]))
        ticks_perc=[1, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 95, 99] #define ticks
        ticks_quan=[stats.norm.ppf(i/100.) for i in ticks_perc] #transfrom them from precentile to cumulative density
        plt.xticks(ticks_quan,ticks_perc,fontsize=15) #assign new ticks
        plt.xlabel('Cumulative (%)',fontsize=15)
        plt.yticks(fontsize=15)
        plt.ylabel('Parameter (values)',fontsize=15)
        plt.title(str(par),fontsize=20)
        plt.grid() #show plot
        fig2.show()   

    def distribution(self,par,lar,lon):
        """ This method produces an histogram of the data serie and computes the value
        of the Anderson-Darling normality test (the threshold to determine the normality
        depends on the number of samples: see online documentation) """
        fig1 = plt.figure(1)
        fig1.canvas.manager.window.resizable(int(lar/2), int(lon/2))
        fig1.canvas.manager.window.wm_geometry("+0+0") 
        ax = fig1.add_subplot(111)
        lis=list(self.df[self.parameter].dropna())
        a = stats.anderson(lis)[0]
        anderson = round(a*a,2)
        mu = np.mean(lis) # Mean 
        sigma = np.std(lis) # Standard Deviation
        n, bins, patches = ax.hist(lis, facecolor='grey', alpha=0.5) # Histogram of the data
        y = mlab.normpdf(bins, mu, sigma) # Add a best fit line
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)        
        plt.text(0.05, 0.95, 'Anderson-Darling normality test ($A^{2}$): '+str(anderson)+'\nIf $A^{2}$>0.752 hypothesis of normality rejected at 95% of significance level', transform=ax.transAxes, fontsize=12, verticalalignment='top', bbox=props) # Print the result of the test        
        ax.ticklabel_format(useOffset=False)
        plt.plot(bins, y, 'r--')
        plt.xlabel('Parameter (values)',fontsize=15)
        plt.xticks(fontsize=15)
        plt.ylabel('Number of samples',fontsize=15)
        plt.yticks(fontsize=15)
        plt.title(str(par),fontsize=20)
        plt.subplots_adjust(left=0.15) # Tweak spacing to prevent clipping of ylabel
        fig1.show()

    def download_map(self,zo,key):
        """ This method allows to download the map from Google and to determine
        from the pixels the corners in decimal degrees (valid only for a zoom >5
        because below it is not possible to keep the linearity on the latitude """
        w = 400 # Width map size (pixel)
        h = 400  # High map size (pixel)
        zoom = int(zo) # Zoom for the map (1: Earth to 16: max zoom / should be between 5 and 16)
        lat = float(self.df['LATITUDE'].median())
        lng = float(self.df['LONGITUDE'].median())
        f=open('Map.tif','wb') # Write the map in the scripts folder
        f.write(requests.get('http://maps.googleapis.com/maps/api/staticmap?center='+str(lat)+','+str(lng)+'&zoom='+str(zoom)+'&size='+str(w)+'x'+str(h)+'&maptype=satellite&sensor=false&key='+str(key)).content) # Download the map on internet
        f.close()
        parallelMultiplier = math.cos(lat * math.pi / 180)
        degreesPerPixelX = 360 / math.pow(2, zoom + 8) # pass pixel to degree longitude
        degreesPerPixelY = 360 / math.pow(2, zoom + 8) * parallelMultiplier # pass pixel to degree latitude
        top = lat - degreesPerPixelY * ( 0 - h / 2)
        right = lng + degreesPerPixelX * ( w - w / 2)
        bottom = lat - degreesPerPixelY * ( h - h / 2)
        left = lng + degreesPerPixelX * ( 0 - w / 2)
        coord = [left, right, bottom, top] # georeferenced (borders coordinates)
        return coord

    def plot_campaign_all(self,par,coordonnee,lar,lon):
        """ This method creates a gradient map of the data serie """
        fig3 = plt.figure() 
        fig3.canvas.manager.window.resizable(int(lar/2), int(lon/2))
        fig3.canvas.manager.window.wm_geometry("+0+"+str(int(lar/2))) 
        ax = fig3.add_subplot(111)
        try:
            dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))
            f = os.path.join(dirname, "Map.tif")
            datafile = cbook.get_sample_data(f)
            img = imread(datafile)
        except:
            pass
        value = []
        latitude = []
        longitude = []
        for i in range(0,len(self.df.values)):
            value.append(float(self.df[self.parameter].iloc[i]))
            latitude.append(float(self.df['LATITUDE'].iloc[i]))
            longitude.append(float(self.df['LONGITUDE'].iloc[i]))
        s = ax.scatter(longitude, latitude, c=value ,edgecolors='black',linewidth=1, marker='o', s=50, cmap='bwr') 
        ax = plt.gca()
        ax.ticklabel_format(useOffset=False)
        plt.xticks(rotation=70)
        try:
            plt.imshow(img, zorder=0, extent=coordonnee) 
        except:
            pass
        plt.xlim(float(coordonnee[0]),float(coordonnee[1]))
        plt.ylim(float(coordonnee[2]),float(coordonnee[3]))
        plt.xlabel('Longitude',fontsize=15) 
        plt.xticks(fontsize=15)
        plt.yticks(fontsize=15)
        plt.ylabel('Latitude',fontsize=15) 
        plt.title(str(par),fontsize=20)
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        plt.text(0.05, 0.95, 'X1: '+str(round(coordonnee[0],5))+'\n'+'X2: '+str(round(coordonnee[1],5))+'\n'+'Y1: '+str(round(coordonnee[2],5))+'\n'+'Y2: '+str(round(coordonnee[3],5)), transform=ax.transAxes, fontsize=12, verticalalignment='top', bbox=props)        
        fig3.colorbar(s).set_label('Parameter (values)')
        fig3.show()
        
    def plot_campaign_pop(self,par,dictiopopu,coordonnee,lar,lon):
        """ This method creates a map of the data serie architectured with
        populations and mixing groups as defined above """
        fig4 = plt.figure()
        fig4.canvas.manager.window.resizable(int(lar/2), int(lon/2))
        fig4.canvas.manager.window.wm_geometry("+"+str(int(lon/2))+"+"+str(int(lar/2))) 
        ax = fig4.add_subplot(111)
        try:
            dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))
            f = os.path.join(dirname, "Map.tif")
            datafile = cbook.get_sample_data(f)
            img = imread(datafile)
        except:
            pass
        dicofinal = OrderedDict()
        for key in dictiopopu.keys():
            try:
                minimum = np.min(dictiopopu[key])
                maximum = np.max(dictiopopu[key])
                dicofinal.setdefault(key, [[],[]])
                for i in range (0,len(self.df.values)):
                    if minimum <= float(self.df[self.parameter].iloc[i]) <= maximum:
                        dicofinal[key][0].append(float(self.df['LONGITUDE'].iloc[i]))
                        dicofinal[key][1].append(float(self.df['LATITUDE'].iloc[i]))
                    else:
                        None
            except ValueError:  
                pass
        colors=cm.bwr(np.linspace(0,1,len(dicofinal.keys())))
        for keyf,c in zip(dicofinal.keys(),colors): 
            ax.scatter(dicofinal[keyf][0], dicofinal[keyf][1], edgecolors='black',linewidth=1,color=c, marker='o', s=50, label=str(keyf)+': from '+str("{:.2f}".format(np.min(dictiopopu[keyf])))+' to '+str("{:.2f}".format(np.max(dictiopopu[keyf])))) 
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(reversed(handles), reversed(labels), loc='lower left',scatterpoints=1,fontsize=12)        
        ax.ticklabel_format(useOffset=False)
        plt.xticks(rotation=70)
        try:
            plt.imshow(img, zorder=0, extent=coordonnee) 
        except:
            pass
        plt.xlim(float(coordonnee[0]),float(coordonnee[1]))
        plt.ylim(float(coordonnee[2]),float(coordonnee[3]))
        plt.xlabel('Longitude',fontsize=15) 
        plt.ylabel('Latitude',fontsize=15) 
        plt.xticks(fontsize=15)
        plt.yticks(fontsize=15)
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        plt.text(0.05, 0.95, 'X1: '+str(round(coordonnee[0],5))+'\n'+'X2: '+str(round(coordonnee[1],5))+'\n'+'Y1: '+str(round(coordonnee[2],5))+'\n'+'Y2: '+str(round(coordonnee[3],5)), transform=ax.transAxes, fontsize=12, verticalalignment='top', bbox=props)
        plt.title(str(par),fontsize=20)
        fig4.show()

    def record(self,name):
        """ This method will save a file correctly treated by the operator,
        adding in the first two columns the raw serie and the corrected serie
        of the parameter of interest (e.g. in the name of the file and in the
        name of the column index. Then all interpolated values are set to
        np.nan values thanks to the MISSING value column """
        self.df.is_copy = False
        colc = self.df[self.parameter].tolist()
        self.df.insert(1, 'TREATED_'+self.parameter, colc)  
        self.df.to_csv(name+'/Final_'+str(self.parameter)+'.csv',sep=";")

    def savpop(self,dicosort,name2):
        """ This method will save a file with the data distrubutions between all
        defined populations and mixing classes """
        pd.DataFrame.from_dict(dicosort, orient='index').T.to_csv(name2+'/Populations_'+str(self.parameter)+'.csv', index=False,sep=";") # Save the file


#################################### Test #####################################  

#findat = analysis(dr,'CO2_100')
#findat.lin_reg('P_in',5,14)
#a = findat.correlation()
#print a
#findat.statistics()
#findat.distribution()
#findat.number_pop()
#dicopop = findat.popul(4)
#findat.graph_combi('CO2_100',dicopop,500,500)
#corners = findat.download_map(15)
#findat.plot_campaign_pop('CO2_100',dicopop,corners,500,500)
#findat.plot_campaign_all(corners)

###############################################################################
