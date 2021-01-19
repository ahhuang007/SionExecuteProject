# -*- coding: utf-8 -*-
"""
Created on Mon Dec 24 01:53:55 2018

@author: Andy
"""

import numpy as np
import matplotlib.pyplot as plt


#Plotting histogram of Sion executes
def DistPlot(df):
    fig, ax = plt.subplots(1,1, figsize = (8, 5))
    #Bins
    bins = np.linspace(0, 40, 41)
    #Plotting data
    ax.hist(df["min"], bins = bins, histtype = 'bar', ec = 'black', color = '#496BB9', alpha = 0.7)
    #Setting tick marks
    ax.xaxis.set_ticks(np.arange(0, 50, 3))
    #Labeling
    plt.xlabel("Time (min.)")
    plt.ylabel("Executes")
    plt.title("Total Singed Executes Each Minute for Patch 8.20")
    
    plt.show()