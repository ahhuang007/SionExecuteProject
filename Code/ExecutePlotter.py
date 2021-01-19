# -*- coding: utf-8 -*-
"""
Created on Mon Sep 10 17:18:02 2018

@author: Andy
"""
from bokeh.plotting import Figure, reset_output
from bokeh.models import ColumnDataSource, HoverTool, Div, CustomJS
from bokeh.io import output_file, show, output_notebook
from bokeh.layouts import widgetbox, row, layout
from bokeh.models.widgets import CheckboxGroup, CheckboxButtonGroup
import numpy as np


#Plotting executes
def ExecutePlot(df):
    #Let's have low file sizes shall we
    
    reset_output(state = None)
    
    output_notebook()
    #Creating plot figure
    plot = Figure(x_axis_label = "Deaths per Game", y_axis_label = "Executes per 100 Games", plot_width = 600, plot_height = 700, tools = [], x_range = [4.75, 7.6], y_range = [0.3, 13.6])
    plot.xaxis.axis_label_text_font = "arial"
    plot.xaxis.axis_label_text_font_size = "10pt"
    plot.xaxis.axis_label_text_font_style = "bold"
    plot.yaxis.axis_label_text_font = "arial"
    plot.yaxis.axis_label_text_font_size = "10pt"
    plot.yaxis.axis_label_text_font_style = "bold"
    plot.min_border_left = 0
    #Getting circle sizes based on # of games a champion was in
    rangeo = max(df["Total Games"]) - min(df["Total Games"])

    df["radSize"] = np.zeros(len(df))
    df["radSize"] = ((df["Total Games"] - min(df["Total Games"]))/ rangeo) * 25 + 7
    
    df["alpha"] = np.zeros(len(df))
    
    arangeo = max(df["radSize"]) - min(df["radSize"])
    
    df["alpha"] = .8 - (((df["radSize"] - min(df["radSize"]))/ arangeo)*0.6 + 0.2)
    
    
    
    #Loading source dataframe
    source = ColumnDataSource(df)
    sourceDF = ColumnDataSource(df)
    
    #Plotting points
    classes = list(df.Class.unique())
    circ = plot.circle(x = "DRate", y = "Rate", source = source, size = "radSize", alpha = "alpha", color = "Color", line_width = 1, line_color = "black", line_alpha = 1, hover_fill_alpha = 0.9, hover_color = "Color", hover_line_color = "black", hover_line_alpha = 1)
   
    #Spooky update functions
    '''def ClassUpdate(attr, old, new):
        index = [0,1,2,3,4,5,6]
        sels = classselect.active
        for q in range(len(sels)):
            index.remove(sels[q])
        update = [classes[i] for i in index]
        startdf = df
        for cla in range(len(update)):
            startdf = startdf[startdf["Class"] != update[cla]]
        onoff = hidetrolls.active
        if len(onoff) != 0:
            startdf = startdf[startdf["Champion"] != "Singed"]
            startdf = startdf[startdf["Champion"] != "Sion"]
        source1.data = dict(startdf)
    def HideUpdate(attr, old, new):
        index = [0,1,2,3,4,5,6]
        sels = classselect.active
        for q in range (len(sels)):
            index.remove(sels[q])
        update = [classes[i] for i in index]
        startdf = df
        for cla in range(len(update)):
            startdf = startdf[startdf["Class"] != update[cla]]
        onoff = hidetrolls.active
        if len(onoff) != 0:
            startdf = startdf[startdf["Champion"] != "Singed"]
            startdf = startdf[startdf["Champion"] != "Sion"]
        source1.data = dict(startdf)
    '''
    #Even spookier CustomJS functions
    
    WinLoseUpdateJS =  """
    var index = [0,1,2,3,4,5,6];           
    var newdf = JSON.parse(JSON.stringify(sourceDF));    
        
    var sels = classselect.active;    
    for (var i=0; i<sels.length; i++) {
        var pos = index.indexOf(sels[i]);
        if (pos > -1) {
            index.splice(pos,1);
        }
    }    
    var update = [];    
    for (var i=0; i<index.length; i++) {
        update.push(classes[index[i]]);
    }
        
    var tempdf = newdf;
    var onoff = hidetrolls.active.length;    
    var count = Object.keys(newdf["Class"]).length;  
    for (var i=0; i<count; i++) {                
        for (var j=0; j<update.length; j++) {                        
            if ( newdf["Class"][String(i)] == update[j] ) {                
                delete tempdf["Champion"][String(i)];
                delete tempdf["Executes"][String(i)];
                delete tempdf["Total Deaths"][String(i)];
                delete tempdf["Total Games"][String(i)];
                delete tempdf["Rate"][String(i)];
                delete tempdf["DRate"][String(i)];
                delete tempdf["Class"][String(i)];
                delete tempdf["Color"][String(i)]; 
                delete tempdf["radSize"][String(i)]; 
                delete tempdf["index"][String(i)]; 
                var found = 1;
            }                                     
        }        
    }        
    newdf = tempdf;            
    if (onoff == 1) {                
        for (var i=0; i<count; i++) {            
            if ( newdf["Champion"][String(i)] === "Singed" || newdf["Champion"][String(i)] === "Sion" ) {                
                delete tempdf["Champion"][String(i)];
                delete tempdf["Executes"][String(i)];
                delete tempdf["Total Deaths"][String(i)];
                delete tempdf["Total Games"][String(i)];
                delete tempdf["Rate"][String(i)];
                delete tempdf["DRate"][String(i)];
                delete tempdf["Class"][String(i)];
                delete tempdf["Color"][String(i)]; 
                delete tempdf["radSize"][String(i)]; 
                delete tempdf["index"][String(i)];
            } 
        }
        ploty.end = 8;
        hidetrolls.labels = ["Show Sion and Singed"];
    } else {
        ploty.end = 13.6;
        hidetrolls.labels = ["Hide Sion and Singed"];
    }
        
    source.data = tempdf;    
    ploty.change.emit()
    source.change.emit();
            
    """
    
    
    #Hiding certain classes
    classselect = CheckboxGroup(labels = classes, active = [0,1,2,3,4,5,6])
    
    #Hiding Sion/Singed
    hidetrolls = CheckboxButtonGroup(labels = ["Hide Sion and Singed"])
    
    winlose_callback = CustomJS(
    args=dict(plot = plot, ploty = plot.y_range, source = source, classselect = classselect, hidetrolls = hidetrolls, classes=classes, sourceDF = sourceDF.data),
    code=WinLoseUpdateJS)
    classselect.js_on_click(winlose_callback)
    hidetrolls.js_on_click(winlose_callback)
    
    #Aesthetics
    hover = HoverTool(renderers = [circ],tooltips=[("Champion",'@Champion'),("Executes/100","@Rate{0.0}"),("Deaths/game","@DRate{0.0}")], mode = "mouse", point_policy = "follow_mouse", show_arrow = False)
    plot.add_tools(hover)
    plot.toolbar_location = None
    plot.toolbar.logo = None
    
    
    widget = widgetbox([classselect, hidetrolls])
    
    content = row([plot, widget])
    layoutt = layout([[content]])
    output_file("html_plot.html", mode = 'cdn')
    
    
    show(layoutt)