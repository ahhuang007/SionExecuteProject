# -*- coding: utf-8 -*-
"""
Created on Tue Jan 22 17:07:18 2019

@author: Andy
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def SionWRPlot(df):
    rolling = pd.DataFrame()
    rolling["game_date"] = np.zeros(len(df) - 3)
    rolling["winrate"] = np.zeros(len(df) - 3)
    for x in range(3, len(df)):
        rolling.loc[x - 3, "game_date"] = df["game_date"][x]
        subset = df["winrate"][x - 3:x + 1]
        rolling.loc[x - 3, "winrate"] = sum(subset)/4
    
    fig, ax = plt.subplots(1,1, figsize = (8, 5))
    ax.plot(rolling["game_date"], rolling["winrate"])
    #Labeling
    plt.xlabel("Date")
    
    plt.ylabel("Win Rate")
    plt.title("Sion's Win Rate in NA Ranked Solo Queue from 9/15 to 11/23")
    
    plt.show()