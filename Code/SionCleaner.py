# -*- coding: utf-8 -*-
"""
Created on Fri Nov 30 19:47:13 2018

@author: Andy
"""
import datetime
from datetime import datetime
import pandas as pd

def SionCleaner(df, tdf, ddf, wdf, num):
    
    #Reformatting datetimes to y-m-d
    df["game_date"] = df["game_date"].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))
    df["game_date"] = df["game_date"].apply(lambda x: datetime.date(x))
    
    
    #grouping by killer id, which gives deaths per day
    newtdf = df
    newtdf = newtdf.groupby(['game_date']).agg({'killer_id':'count'})
    newddf = df.groupby(['game_date']).agg({'matchid':pd.Series.nunique})
    
    newtdf = newtdf.reset_index(drop = False)
    newddf = newddf.reset_index(drop = False)
    
    #merging with previous cumulative dataframe
    newtdf = newtdf.merge(tdf, on = 'game_date', how = 'outer')
    newddf = newddf.merge(ddf, on = 'game_date', how = 'outer')
    
    newtdf.fillna(0, inplace = True)
    newddf.fillna(0, inplace = True)
    #Combining columns, dropping unncessary stuff
    newtdf["killer_id"] = newtdf["killer_id_x"] + newtdf["killer_id_y"]
    newddf["matchid"] = newddf["matchid_x"] + newddf["matchid_y"]
    
    newtdf = newtdf.drop(["killer_id_x", "killer_id_y"], 1)
    newddf = newddf.drop(["matchid_x", "matchid_y"], 1)
        
    #Getting winrates for each day
    windf = df.groupby(['game_date']).agg({'win':'mean'})
    windf = windf.reset_index(drop = False)
    
    windf = windf.merge(wdf, on = 'game_date', how = 'outer')
    windf.fillna(0, inplace = True)
    
    windf["win"] = ((windf["win_x"] * (num - 1)) + windf["win_y"])/num
    windf = windf.drop(["win_x","win_y"], 1)
    return newtdf, newddf, windf