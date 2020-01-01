from flask import Flask, render_template
import json
import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys, os, glob
import csv
from common import *


app = Flask(__name__)
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

def count_swap():
    return sum(1 for line in open(get_path_of('total'))) 

def get_cmd():
    return 'Swap Timestamps of %s'%os.environ['SWPTRACE_CMD']

@app.route('/')
def index():

    global logs
    head = os.environ['SWPTRACE_LOG']
    logs = glob.glob(head+'/*.log')

    data=[]
    for side in reversed(area): 
         if side != 'total' and get_path_of(side) in logs:
	    sec, vpn = read_csv(side) 
            data.append(dict( x= sec, y=vpn, mode='markers', type='scatter')) 

    layout=dict(grid=dict(title='title', font=dict(size=18)))
    
    info = dict(count = count_swap(), command=get_cmd())
      
    chart = dict(data=data, layout=layout)
    graphJSON = json.dumps(chart, cls=plotly.utils.PlotlyJSONEncoder)
  
    dirpath = os.path.dirname(os.path.abspath(__file__))
    return render_template('index.html', info=info, 
                           graphJSON=graphJSON)

if __name__ =='__main__':
   app.index()
