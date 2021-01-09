from flask import Flask, render_template
from flask import Response, make_response
import json
import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys, os, glob
import pandas
import pdfkit 
from utility import *


app = Flask(__name__)


def read_csv(side):
    data=[]
    n_class = int(os.environ['CLASS'])
    
    for idx in range (0, n_class*2):
        item = dict()
        item['x']=[]
        item['y']=[]
        item['text']=[]
        item['mode']='markers'
        item['type']='scatter'
        item['hovertemplate']='<b>%{text}</b>'
        if idx < n_class: 
           item['name']= 'Alloc'
        else:
           item['name']= 'Swap'
        data.append(item)
    
    cnt = 0 
    with open(get_path_of(side)) as csvfile:
	 plots = csv.reader(csvfile, delimiter=',')
         for row in plots:    
             label = int(row[0])
	     sec  = float(row[1])
	     vpn = int(row[2])
             #text= '/'.join(str(elem) for elem in row[2:])
             text = 'Addr : {} <br>'.format(row[2])
             if len(row) > 5:
                text = text+"File :{}<br>Function : {}<br>Variable : {}".format(row[3],row[4],row[5])
             isSWP = int(row[-1])
             cnt=cnt+isSWP
             label = n_class * isSWP + label 
             data[label]['x'].append(sec)
             data[label]['y'].append(vpn)
             data[label]['text'].append(text) 

    return data, cnt 
	         

def get_path_of(loc):
    head = os.environ['SWPTRACE_LOG']
    return head+'/'+loc+ '.csv'


def get_cmd():
    return 'Swap Timestamps of {}'.format(os.environ['SWPTRACE_CMD'])

@app.route('/')
def index():
    print("$ flask run")
    data, cnt = read_csv('labeled') 
    layout = dict(grid=dict(title='title', font=dict(size=18)), yaxis=dict(type='log'))
    head = dict(count = cnt, command=get_cmd())
    chart = dict(data=data, layout=layout)
    graphJSON = json.dumps(chart, cls=plotly.utils.PlotlyJSONEncoder)
  
    dirpath = os.path.dirname(os.path.abspath(__file__))
    #return render_template('index.html', head=head, graphJSON=graphJSON)
    rendered = render_template('index.html', head=head, graphJSON=graphJSON)
    return rendered


if __name__ =='__main__':
   try:
     #app.index()
     app.run(debug=True)
   except socket.error as err:
     print( '[error] socket.error : [error {}]'.format(str(err.errno))
