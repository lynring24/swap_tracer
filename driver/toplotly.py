import plotly.graph_objects as go
import pandas as pd 
import sys
import csv

sec = []
pvn = []

with open(sys.argv[1]) as csvfile:
     plots = csv.reader(csvfile, delimiter=',')
     for row in plots:
         sec.append(row[0])
	 pvn.append(row[1])

fig = go.Figure(data=go.Bar(y=[2, 3, 1]))
fig.write_html('first_figure.html', auto_open=True)
fig.add_trace(go.Scatter(x=sec, y=pvn,
	      mode='markers',
              name='markers'))

fig.show()
