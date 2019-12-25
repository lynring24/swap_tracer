import plotly.graph_objects as go
import pandas as pd 
import sys, os
import csv


sec = []
pvn = []

def to_plot():
     log_path = sys.argv[1]
     png_path = log_path[:log_path.rfind('/')]+'plot.png' 
     with open(log_path) as csvfile:
	  plots = csv.reader(csvfile, delimiter=',')
	  for row in plots:
	      sec.append(row[0])
	      pvn.append(row[1])
     #data = pd.read_csv(sys.argv[1], sep=' ', names=['sec', 'pvn'], header=None )


     fig = go.Figure(data=go.Scatter(x=sec, y=pvn,
		   mode='markers',
		   name=sys.argv[1]))
#     if not os.path.exists(png_path):
#        fig.write_image(png_path)

     fig.show()




to_plot()
