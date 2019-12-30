from flask import Flask, render_template
import json
import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys, os, glob
import csv
from common import *


app = Flask(__name__, render_template='template')
app.debug = True


def read_csv(side):
    with open(get_path_of(side)) as csvfile:
	 sec = []
	 vpn = []
	 plots = csv.reader(csvfile, delimiter=',')
	 for row in plots:
	     sec.append(row[0])
	     vpn.append(row[1])
    return sec, vpn
	         

def get_path_of(loc):
    head = os.environ['SWPTRACE_LOG']
    return head+'/'+loc+ '.log'


@app.route('/')
def index():

    global logs
    head = os.environ['SWPTRACE_LOG']
    logs = glob.glob(head+'/*.log')

    data = []
    idx=1
    for side in reversed(area): 
         if side != 'total' and get_path_of(side) in logs:
	    sec, vpn = read_csv(side) 
            if idx == 1:
               data.append(dict( x= sec, y=vpn, type='scatter')) 
            else:
               data.append(dict( x= sec, y=vpn, xaxis='x'+idx, yaxis= 'y'+idx, type='scatter')) 
    layout=dict(grid=dict(rows=len(logs)-2, colums= 1, pattern='independent', roworder='top to bottom'))
    
    fig = []
    fig.append(data)
    fig.append(layout)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
  
    dirpath = os.path.dirname(os.path.abspath(__file__))
    return render_template('index.html',
                           graphJSON=graphJSON)

if __name__ =='__main__':
   app.run()
