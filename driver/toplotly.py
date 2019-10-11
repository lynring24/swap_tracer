import plotly.graph_objects as go
import pandas as pd 
import sys

data = pd.read_csv(sys.argv[1], delimiter=' ')
print data[0]
#fig = go.Figure(data=go.Bar(y=[2, 3, 1]))
#fig.write_html('first_figure.html', auto_open=True)
#fig.add_trace(go.Scatter(x=data['sec'], y=data['pvn'],
#              mode='markers',
#              name='markers'))

#fig.show()
