# -*- coding: utf-8 -*-
"""
Created on Thu Sep  6 18:41:20 2018

@author: Andy
"""
#Main function - Will read in data

#Importing necessary libraries
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from ExecuteCleaner import ExecuteCleaner
from ExecutePlotter import ExecutePlot
from ExecuteDist import ExecuteDist
from DistPlot import DistPlot
#SQL query code and conversion to Excel file
wk_dir  = 'C:\\Users\\MSI\\Documents\\GitHub\\Execute-Analysis\\'
db_str  = 'mysql+pymysql://LOLMegaRead:'+'LaberLabsLOLquery'+'@lolsql.stat.ncsu.edu/lol'

#Getting query data from database
def run_query(query, engine, to_replace, replacers): # filepath of text file that contains query
    for i in range(len(to_replace)):
        old = to_replace[i]
        new = replacers[i]
        query = query.replace(old, str(new))
    df =  pd.read_sql(query,engine)
    
    return df
def split_queries(filepath, engine, n_split, to_replace, replace, savepath):
    
    with open(filepath) as f:
        query_str = f.read()
    query_str = query_str.replace('split_num', str(n_split))
    for j in range(8,9):
        query_str_part = query_str.replace('snafu', str(j))
        df = run_query(query_str_part, engine, to_replace, replace)
        df.to_csv(savepath + 'Data\\' + 'query' + str(j) + '.csv')
        
    

dfo = pd.DataFrame()
dfp = pd.DataFrame()
dft = pd.DataFrame()
dfh = pd.DataFrame()

distdf = pd.DataFrame(columns = ["timestamp"])
engine = create_engine(db_str)

n_split = 24
to_replace = [] #things to replace in query
replace = [] #can be dataframe if replacing multiple things multiple times
#split_queries(wk_dir + 'Code\\loopquery.txt', engine, n_split, to_replace, replace, wk_dir)
champs = []
#Reading csvs and getting relevant data, then compiling into dataframes
dat_dir = 'D:\\query_data\\executeanalysis\\'
for m in range(n_split):
    print(m)
    df = pd.read_csv(dat_dir + 'query' + str(m) + '.csv')
    [part, partmax, parttop, parthigh] = ExecuteCleaner(df)
    part["Executes"].fillna(0, inplace = True)
    champs = list(part.Champion.unique())
    if m == 0:
        dfo = dfo.append(part)
    else:
        dfo = dfo + part
    dfp = dfp.append(partmax)
    dft = dft.append(parttop)
    dfh = dfh.append(parthigh)
    #Getting execute distribution for Sion
    dist = ExecuteDist(df)
    distdf = pd.concat([distdf, dist], sort = True)

#Looking for highest death counts per match in specific dataframes
for n in range(n_split):
    topdf = dft[dft["matchid"] % n_split == n]
    d_counts = topdf["champion"].value_counts()
    print(d_counts[0])
    
for o in range(n_split):
    highdf = dfh[dfh["matchid"] % n_split == o]
    h_counts = highdf["champion"].value_counts()
    print(h_counts[0])

#Further processing
dfo["Champion"] = champs

dfo["Rate"] = (dfo["Executes"] / dfo["Total Games"]) * 100


dfo["DRate"] = np.zeros(len(dfo))

    
dfo["DRate"] = (dfo["Total Deaths"] / dfo["Total Games"]) 




data_dir = 'C:\\Users\\MSI\\Documents\\GitHub\\Execute-Analysis\\Data\\'    
classes = pd.read_csv(data_dir + 'classdata.csv')
dfo = dfo.merge(classes, how = 'inner')

colors = {'Assassin':'#ED2941', 'Mage':'#25BAA4', 'Tank':'#393663', 'Fighter':'#664A40', 'Support': '#FFB733', 'Specialist':'#EB8596', 'Marksman':'#0D1F22'}
dfo["Color"] = dfo['Class'].map(colors)

dfo.to_excel(data_dir + "execute_data.xlsx")

#Plotting
ExecutePlot(dfo)
#distdf = distdf.sort_values(["bin"], ascending = True)
distdf["round"] = np.round(distdf["timestamp"])
distdf["min"] = distdf["round"]/60

distdf = distdf.reset_index(drop = True)
#Plotting histogram
DistPlot(distdf)



    





