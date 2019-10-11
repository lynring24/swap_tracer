import plotly.graph_objects as go
import pandas as pd 
import sys
import csv
from configure import *

x = []
y = []

with open(sys.argv[1]) as csvfile:
     plots  =csv.reader(csvfile, delimeter=' ')
     for row in plots:
	 x.append(row[0])
	 y.append(row[1])
data = pd.read_csv(sys.argv[1], sep=' ', names=['sec', 'pvn'], header=None)
print data['sec']
#fig = go.Figure(data=go.Bar(y=[2, 3, 1]))
#fig.write_html('first_figure.html', auto_open=True)
#fig.add_trace(go.Scatter(x=data['sec'], y=data['pvn'],
#              mode='markers',
#              name='markers'))

#fig.show()
