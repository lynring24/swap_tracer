import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd 
import sys, os, glob
import csv
from utility import *



def get_grid_all(): 
    grids = [ [{'rowspan':2}, {}]]

    for i in range (0, len(logs)-2):
        grids.append([None, {}])
    return grids




def to_browser():
    global logs
    logs = glob.glob(get_path('head')+'/*.log')

    fig = make_subplots( 
               rows = len(logs)-2, cols = 1, 
               vertical_spacing=0.02,
               shared_yaxes=True,
               shared_xaxes=True
              #   specs= get_grid()
                )
                      
    grid = 1
    for side in reversed(area): 
         if side != 'total' and get_path(side) in logs:
	    with open(get_path(side)) as csvfile:
	         sec = []
	         pvn = []
	         plots = csv.reader(csvfile, delimiter=',')
	         for row in plots:
	             sec.append(row[0])
	             pvn.append(row[1])
	         
#                 rgrid, cgrid = get_spot(side)
                 fig.add_trace( 
                          go.Scatter(
                             x=sec, y=pvn,
                             #name=side,
	                     mode='markers'),
                             row = grid,
                             col = 1
                 )
                 grid+=1
#     if not os.path.exists(png_path):
#        fig.write_image(png_path)
    
    fig.update_layout( 
               height=1000, width= 1800, 
               title_text="swap timestamps of $ %s %s"%(str(get_mem_limit()),  get_command()),
               xaxis_title='Time',
               yaxis_title='VPN (Virtual Page Number)',
               font =  dict (
                           family='Courier New, monospace',  
                           size=18,
                           color='#7f7f7f')
               )

    fig.show()
