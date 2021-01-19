# -*- coding: utf-8 -*-
"""
Created on Mon Dec 24 00:14:37 2018

@author: Andy
"""

import numpy as np 
import pandas as pd
# 0 for-loops, I'm actually 64042039 IQ
def ExecuteDist(df):
    siondf = df[df["champion"] == "Singed"]
    siondf = siondf.drop(["matchid", "win", "championid", "rank", "champion", "Unnamed: 0"], 1)
    siondf = siondf[siondf["killer_id"] == 0]
    siondf = siondf.drop(["killer_id"], 1)
    siondf["timestamp"] = siondf["timestamp"]/1000
    sdf2 = siondf
    #Getting numbers per bin - apparently these can't be used to plot, so simply for making sure I have the right plots
    siondf["bin"] = np.ceil(siondf["timestamp"]/120)
    newsdf = siondf.groupby(['bin']).agg({'bin':'count'})
    newsdf["count"] = newsdf["bin"]
    newsdf = newsdf.drop(["bin"], 1)
    newsdf = newsdf.reset_index(drop = False)
    
    return sdf2
    
    