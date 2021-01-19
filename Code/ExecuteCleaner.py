# -*- coding: utf-8 -*-
"""
Created on Mon Sep 17 23:03:28 2018

@author: Andy
"""
import numpy as np
import pandas as pd


def ExecuteCleaner(df):
    
    champions = list(df.champion.unique())
    
    #New dataframe with champions, # of executes, death count, and ratio of executes to total games
    counts = pd.DataFrame()
    
    counts["Champion"] = champions
    
    #Number of times a champion was executed
    counts["Executes"] = np.zeros(len(counts))
    df3 = df[df["killer_id"] == 0]
    df3 = df3.groupby("champion")["killer_id"].count()
    df3 = df3.reset_index(drop = True)
    counts["Executes"] = df3
    
    #Total times a champion died
    counts["Total Deaths"] = np.zeros(len(counts))
    df2 = df.groupby("champion")["killer_id"].count()
    df2 = df2.reset_index(drop = True)
    counts["Total Deaths"] = df2
    
    #Total times a champion appeared in a game
    counts["Total Games"] = np.zeros(len(counts))
    df4 = df.drop_duplicates(subset = ["matchid", "champion"])
    df4 = df4.groupby(["champion"])["champion"].count()
    df4 = df4.reset_index(drop = True)
    counts["Total Games"] = df4
    
    
    counts["Rate"] = np.zeros(len(counts))
    
    #Finding most deaths from one champion in a game
    id_counts = df['matchid'].value_counts()
    id_counts = id_counts.reset_index(drop = False)
    id_counts["id"] = id_counts["index"]
    maxdf = df[df["matchid"] == id_counts.id[0]]
    death_counts = maxdf["champion"].value_counts()
    death_counts = death_counts.reset_index(drop = False)
    death_counts["champ"] = death_counts["index"]
    countmax = pd.DataFrame()
    for q in range(3):
        part = maxdf[maxdf["champion"] == death_counts.champ[q]]
        countmax = countmax.append(part)
    
    #Finding most deaths from one game
    mostdf = df.groupby(['matchid','champion']).agg({'champion':'count'})
    maxnum = max(mostdf.champion)
    mdf = mostdf[mostdf["champion"] == maxnum]
    mdf.columns = ["Deaths"]
    mdf = mdf.reset_index(drop = False)
    topdf = df[df["matchid"] == mdf.matchid[0]]
    
    #Finding most deaths in high elo games
    highdf = df[df["rank"] >= 5.0]
    hid_counts = highdf["matchid"].value_counts()
    hid_counts = hid_counts.reset_index(drop = False)
    hid_counts["id"] = hid_counts["index"]
    hmaxdf = highdf[highdf["matchid"] == hid_counts.id[0]]
    hdeaths = hmaxdf["champion"].value_counts()
    hdeaths = hdeaths.reset_index(drop = False)
    hdeaths["champ"] = hdeaths["index"]
    highmax = pd.DataFrame()
    for r in range(3):
        portion = hmaxdf[hmaxdf["champion"] == hdeaths.champ[r]]
        highmax = highmax.append(portion)
        
        
    return [counts, countmax, topdf, highmax]
    
    