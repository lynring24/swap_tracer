from flask import Flask, render_template
<<<<<<< HEAD
from flask import response
=======
from flask import Response, make_response
>>>>>>> 026724062b5c2746723de2fd013f16cde949a1a3
import json
import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys, os, glob
import csv
<<<<<<< HEAD
=======
import pdfkit 
>>>>>>> 026724062b5c2746723de2fd013f16cde949a1a3
from utility import *


app = Flask(__name__)


def read_csv(side):
    data=[]
    n_class = int(os.environ['CLASS'])
<<<<<<< HEAD
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
=======
    print n_class
    
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
             text = 'Addr : %s <br>'%row[2]
             if len(row) > 5:
                text = text+"File : %s<br>Function : %s<br>Variable : %s"%(row[3],row[4],row[5])
             isSWP = int(row[-1])
             cnt=cnt+isSWP
             label = n_class * isSWP + label 
             data[label]['x'].append(sec)
             data[label]['y'].append(vpn)
             data[label]['text'].append(text) 

    return data, cnt 
>>>>>>> 026724062b5c2746723de2fd013f16cde949a1a3
	         

def get_path_of(loc):
    head = os.environ['SWPTRACE_LOG']
    return head+'/'+loc+ '.csv'


def get_cmd():
    return 'Swap Timestamps of %s'%os.environ['SWPTRACE_CMD']

@app.route('/')
def index():
<<<<<<< HEAD

    head = os.environ['SWPTRACE_LOG']
    swp =  sum(1 for line in open(get_path_of('labeled'))) 
    data = read_csv('labeled') 
    layout =dict(grid=dict(title='title', font=dict(size=18)))
    head = dict(count = swp, command=get_cmd())
=======
    print "$ flask run"
    data, cnt = read_csv('labeled') 
    layout = dict(grid=dict(title='title', font=dict(size=18)), yaxis=dict(type='log'))
    #layout = dict(grid=dict(title='title', font=dict(size=18)), yaxis=dict(type='log', autorange=True))
    head = dict(count = cnt, command=get_cmd())
>>>>>>> 026724062b5c2746723de2fd013f16cde949a1a3
    chart = dict(data=data, layout=layout)
    graphJSON = json.dumps(chart, cls=plotly.utils.PlotlyJSONEncoder)
  
    dirpath = os.path.dirname(os.path.abspath(__file__))
    #return render_template('index.html', head=head, graphJSON=graphJSON)
    rendered = render_template('index.html', head=head, graphJSON=graphJSON)
<<<<<<< HEAD
    pdf = pdfkit.from_url(rendered, head+'/plot.pdf')

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename='+head+'/plot.pdf'
    return response
=======
    return rendered

    #path = os.environ['SWPTRACE_LOG']
    #pdf = pdfkit.from_url(rendered, path+'/plot.pdf')

   # response = make_response(pdf)
   # response.headers['Content-Type'] = 'application/pdf'
   # response.headers['Content-Disposition'] = 'attachment; filename='+path+'/plot.pdf'
   # return response
>>>>>>> 026724062b5c2746723de2fd013f16cde949a1a3


if __name__ =='__main__':
   try:
     #app.index()
     app.run(debug=True)
   except socket.error as err:
     print '[error] socket.error : [error %s]'%str(err.errno)
