# -*- coding: utf-8 -*-
"""
Created on Fri Nov 30 00:17:32 2018

@author: Andy
"""
import pandas as pd
from sqlalchemy import create_engine
from SionCleaner import SionCleaner
from SionPlot import SionPlot
from SionWRPlot import SionWRPlot
#SQL query code and conversion to Excel file
wk_dir  = 'C:\\Users\\MSI\\Documents\\Github\\Execute-Analysis\\'
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
    for j in range(36, n_split):
        print(j)
        query_str_part = query_str.replace('snafu', str(j))
        df = run_query(query_str_part, engine, to_replace, replace)
        df.to_csv(savepath + 'Data\\' + 'sion_query' + str(j) + '.csv')

n_split = 50
engine = create_engine(db_str)
to_replace = [] 
replace = []
#split_queries(wk_dir + 'Code\\sionquery.txt', engine, n_split, to_replace, replace, wk_dir)
#with open(wk_dir + 'Code\\avgquery.txt') as f:
#    query_str = f.read()

#Getting daily avgs
'''dfavg = pd.read_sql(query_str, engine)
dfavg = dfavg[0:70]
dfavg.to_csv(wk_dir + 'Data\\avgquery.csv')'''
#dfavg = pd.read_csv(wk_dir + 'Data\\avgquery.csv')
data_dir = 'D:\\query_data\\executeanalysis\\'
#Reading csvs, getting death counts
totdf = pd.DataFrame(columns = ["game_date", "killer_id"])
daydf = pd.DataFrame(columns = ["game_date", "matchid"])
wrtdf = pd.DataFrame(columns = ["game_date", "win"])
for s in range(n_split):
    print(s)
    df = pd.read_csv(data_dir + 'sion_query' + str(s) + '.csv')
    df = df.drop(['Unnamed: 0', 'championid', 'champion', 'timestamp'], 1)
    [totdf, daydf, wrtdf] = SionCleaner(df, totdf, daydf, wrtdf, s + 1)
    


wrtdf.columns = ["game_date", "winrate"]
totdf.columns = ["game_date", "deaths"]
daydf.columns = ["game_date", "games"]
totdf["rate"] = totdf["deaths"]/daydf["games"]
totdf["games"] = daydf["games"]
totdf.to_csv(wk_dir + 'Data\\siondata.csv')
wrtdf.to_csv(wk_dir + 'Data\\winratedata.csv')

SionPlot(totdf, dfavg)
SionWRPlot(wrtdf)