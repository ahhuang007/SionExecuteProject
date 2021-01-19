# -*- coding: utf-8 -*-
"""
Created on Sat Dec  1 18:48:09 2018

@author: Andy
"""
from bokeh.plotting import Figure, reset_output
from bokeh.models import ColumnDataSource, HoverTool, BasicTickFormatter, Range1d, LinearAxis, FixedTicker, Label, Arrow, NormalHead
from bokeh.io import output_file, show
from bokeh.layouts import layout
import numpy as np
import pandas as pd
import datetime
from datetime import datetime

def SionPlot(totdf, avgdf):
    
    reset_output(state = None)
    
    #Getting rolling averages
    rolling = pd.DataFrame()
    rolling["game_date"] = np.zeros(len(totdf) - 6)
    rolling["avg"] = np.zeros(len(totdf) - 6)
    for x in range(6, len(totdf)):
        rolling.loc[x - 6, "game_date"] = totdf["game_date"][x]
        subset = totdf["games"][x - 6:x + 1]
        rolling.loc[x - 6, "avg"] = sum(subset)/7
    
    #Making figure, aesthetics
    plot = Figure(title = "Sion Death Rate Over Time (in Ranked NA Solo Queue)", x_axis_label = "Date", x_axis_type = "datetime", y_axis_label = "Deaths per Game", y_axis_type = "linear", tools = [], plot_height= 400, plot_width = 700, y_range = (5, 7.5))
    plot.title.text_font = "arial"
    plot.title.text_font_style = "bold"
    plot.title.text_font_size = "12pt"
    plot.title.align = "center"
    plot.yaxis[0].formatter = BasicTickFormatter(use_scientific = False)
    plot.xaxis.axis_label_text_font = "arial"
    plot.xaxis.axis_label_text_font_size = "10pt"
    plot.xaxis.axis_label_text_font_style = "bold"
    plot.yaxis.axis_label_text_font = "arial"
    plot.yaxis.axis_label_text_font_size = "10pt"
    plot.yaxis.axis_label_text_font_style = "bold"
    plot.yaxis.minor_tick_line_color= None
    
    days = ['2018-09-15', '2018-10-01', '2018-10-15', '2018-11-01', '2018-11-15']
    dates = pd.to_datetime(days).astype(int) / 10**6
    avgdf["t_day"] = pd.to_datetime(avgdf["t_day"])
    plot.xaxis.ticker = FixedTicker(ticks = list(dates))
    
    plot.xgrid.grid_line_color = None
    plot.ygrid.grid_line_color = None
        
    #Making 2nd y axis
    plot.extra_y_ranges = {"Play-Rate": Range1d(start = min(totdf.games), end = max(totdf.games))}
    
    #Data sources
    sourcen = ColumnDataSource(totdf)
    sourcet = ColumnDataSource(rolling)
    sourcea = ColumnDataSource(avgdf)
    
    #Plotting vertical bars
    plot.vbar(x = totdf.game_date[18], bottom = 5, top = 7.5, width = 86400000/25, color = "black", alpha = 0.4, line_color = "black")
        
    
    plot.vbar(x = totdf.game_date[58], bottom = 5, top = 7.5, width = 86400000/25, color = 'black', alpha = 0.4, line_color = 'black')
    
    #Plotting plot lines
    plot.line(x = "game_date", y = "avg", source = sourcet, color = "gray", alpha = 0.6, y_range_name = "Play-Rate", line_dash = "dashed", line_width = 3, legend = "Sion Games Played")              
              
    plot.add_layout(LinearAxis(y_range_name = "Play-Rate", axis_label = "Games Played"), 'right')
    plot.yaxis[1].axis_label_text_font = "arial"
    plot.yaxis[1].axis_label_text_font_size = "10pt"
    plot.yaxis[1].axis_label_text_font_style = "bold"
    plot.yaxis[1].minor_tick_line_color = None
    #Invis lines help hover range
    plot.line(x = "t_day", y = "avg_deaths_overalls", source = sourcea, color ="#496BB9", alpha = 0.7, line_width = 3, legend = "Overall Death Rate")
    invis2 = plot.line(x = "t_day", y = "avg_deaths_overalls", source = sourcea, color ="white", alpha = 0.0, line_width = 30, legend = "Overall Death Rate")    
    
    plot.line(x = "game_date", y = "rate", source = sourcen, color = "#BA3F5D", line_width = 3, legend = "Sion Death Rate")
    invis = plot.line(x = "game_date", y = "rate", source = sourcen, color = "white", line_width = 30, alpha = 0)
    
    #Adding hovers
    hovern = HoverTool(renderers = [invis], tooltips = [("Date", "@game_date{%F}"), ("Avg. Deaths","@rate{0.0}"), ("Games", "@games")], mode = "mouse")
    hovern.formatters = {"game_date" : "datetime"}
    hoverd = HoverTool(renderers = [invis2], tooltips = [("Date", "@t_day{%F}"), ("Avg. Deaths","@avg_deaths_overalls{0.0}")], mode = "mouse")
    hoverd.formatters = {"t_day" : "datetime"}
    
    #Adding labels
    label1 = Label(x = totdf.game_date[45], y = 5.4, x_units = 'data', y_units = 'data', text = 'End of Season', text_font_size = '9pt')
    label2 = Label(x = totdf.game_date[4], y = 5.15, x_units = 'data', y_units = 'data', text = 'Inting Sion Post', text_font_size = '9pt')
    plot.add_layout(label1)
    plot.add_layout(label2)
    plot.add_layout(Arrow(end = NormalHead(fill_color = 'black', size = 6, fill_alpha = 0.6, line_alpha = 0.6), line_alpha = 0, x_start = totdf.game_date[56], y_start = 5.45, x_end = totdf.game_date[57], y_end = 5.45))
    plot.add_layout(Arrow(end = NormalHead(fill_color = 'black', size = 6, fill_alpha = 0.6, line_alpha = 0.6), line_alpha = 0, x_start = totdf.game_date[16], y_start = 5.2, x_end = totdf.game_date[17], y_end = 5.2))
    
    plot.add_tools(hoverd)
    plot.add_tools(hovern)
    
    #Final aesthetics
    plot.toolbar_location = None
    plot.toolbar.logo = None
    plot.legend.location = "top_left"
    plot.legend.label_text_font_size = "9pt"
    plot.legend.glyph_width = 15
    temp = plot.legend[0].items[2]
    plot.legend[0].items[2] = plot.legend[0].items[0]
    plot.legend[0].items[0] = temp
    
    output_file("sionplot.html")
    layoutt = layout([plot])
    show(layoutt)