from flask import Flask, render_template
from flask import Response, make_response
import json
import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys, os, glob
import csv
import pdfkit 
from utility import *


app = Flask(__name__)


def read_csv(side):
    data=[]
    n_class = int(os.environ['CLASS'])
    for item in range (0, n_class):
        item = dict()
        item['x']=[]
        item['y']=[]
        item['text']=[]
        item['mode']='markers'
        item['type']='scatter'
        item['hovertemplate']='<b>%{text}</b>'
        data.append(item)
    
    with open(get_path_of(side)) as csvfile:
	 plots = csv.reader(csvfile, delimiter=',')
         for row in plots:    
             label = int(row[0])
	     sec  = float(row[1])
	     vpn = int(row[2])
             text= '/'.join(str(elem) for elem in row[2:])
             data[label]['x'].append(sec)
             data[label]['y'].append(vpn)
             data[label]['text'].append(text) 
    return data
	         

def get_path_of(loc):
    head = os.environ['SWPTRACE_LOG']
    return head+'/'+loc+ '.csv'


def get_cmd():
    return 'Swap Timestamps of %s'%os.environ['SWPTRACE_CMD']

@app.route('/')
def index():
    print "$ flask run"
    swp =  sum(1 for line in open(get_path_of('labeled'))) 
    data = read_csv('labeled') 
    layout = dict(grid=dict(title='title', font=dict(size=18)), yaxis=dict(type='log', autorange=True))
    head = dict(count = swp, command=get_cmd())
    chart = dict(data=data, layout=layout)
    graphJSON = json.dumps(chart, cls=plotly.utils.PlotlyJSONEncoder)
  
    dirpath = os.path.dirname(os.path.abspath(__file__))
    #return render_template('index.html', head=head, graphJSON=graphJSON)
    rendered = render_template('index.html', head=head, graphJSON=graphJSON)
    return rendered

    #path = os.environ['SWPTRACE_LOG']
    #pdf = pdfkit.from_url(rendered, path+'/plot.pdf')

   # response = make_response(pdf)
   # response.headers['Content-Type'] = 'application/pdf'
   # response.headers['Content-Disposition'] = 'attachment; filename='+path+'/plot.pdf'
   # return response


if __name__ =='__main__':
   try:
     #app.index()
     app.run(debug=True)
   except socket.error as err:
     print '[error] socket.error : [error %s]'%str(err.errno)
