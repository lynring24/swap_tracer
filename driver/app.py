from flask import Flask, render_template
from flask import response
import json
import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys, os, glob
import csv
from utility import *


app = Flask(__name__)


def read_csv(side):
    data=[]
    n_class = int(os.environ['CLASS'])
    for item in range (0, n_class):
        item = dict()
        item['hoverinfo']='all'
        item['mode']='markers+text'
        item['type']='scatter'

    with open(get_path_of(side)) as csvfile:
	 plots = csv.reader(csvfile, delimiter=',')
         for row in plots:    
             label = row[0]
	     sec  = row[1]
	     vpn = row[2]
             text= '/'.join(str(elem) for elem in row[3:])
             data[label].get('x').append(sec)
             data[label].get('y').append(vpn)
             data[label].get('text').append(text) 
    return data
	         

def get_path_of(loc):
    head = os.environ['SWPTRACE_LOG']
    return head+'/'+loc+ '.csv'


def get_cmd():
    return 'Swap Timestamps of %s'%os.environ['SWPTRACE_CMD']

@app.route('/')
def index():

    head = os.environ['SWPTRACE_LOG']
    swp =  sum(1 for line in open(get_path_of('labeled'))) 
    data = read_csv('labeled') 
    layout =dict(grid=dict(title='title', font=dict(size=18)))
    head = dict(count = swp, command=get_cmd())
    chart = dict(data=data, layout=layout)
    graphJSON = json.dumps(chart, cls=plotly.utils.PlotlyJSONEncoder)
  
    dirpath = os.path.dirname(os.path.abspath(__file__))
    #return render_template('index.html', head=head, graphJSON=graphJSON)
    rendered = render_template('index.html', head=head, graphJSON=graphJSON)
    pdf = pdfkit.from_url(rendered, head+'/plot.pdf')

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename='+head+'/plot.pdf'
    return response


if __name__ =='__main__':
   try:
     #app.index()
     app.run(debug=True)
   except socket.error as err:
     print '[error] socket.error : [error %s]'%str(err.errno)
