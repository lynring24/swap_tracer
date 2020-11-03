import os
import pandas as pd
import matplotlib as mpl
import numpy as np
from multiprocess import Pool, cpu_count

if os.environ.get('DISPLAY','') == '':
    print('no display found. Using non-interactive Agg backend')
    mpl.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

MICROSECOND = 1000000
MILLISECOND = 1000

def string_to_date(timestamp):
    try: 
        timestamp = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%f')
    except ValueError:
        timestamp = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S,%f')                                       
    return timestamp



def draw_heatmap(dir_path):
    rsyslog = pd.read_csv(dir_path+"/rsyslog.csv")
    rsyslog['hex'] = rsyslog['address'].apply(lambda x : hex(x)[:6])
    print rsyslog.head(5)
    rsyslog['timestamp'] = rsyslog['timestamp'].astype(int)
    rsyslog['timestamp'] = rsyslog['timestamp'].apply(lambda x : x/MILLISECOND)
    rsyslog = rsyslog.groupby(['timestamp', 'hex']).size().to_frame('count').reset_index()
    #print rsyslog.head(5)
    histogram = pd.DataFrame({'total': rsyslog.groupby('timestamp')['count'].sum()}).reset_index()
    rsyslog = pd.merge(rsyslog, histogram, how="left")
    del histogram

    rsyslog['count'] = rsyslog.apply(lambda row : round(1.0*row['count']/row['total'], 2), axis=1)
    pivot = rsyslog.pivot(index='hex', columns='timestamp', values='count').fillna(0.0)

    print pivot.head(5)
    del rsyslog

    print "set plots"

    fig = plt.figure(figsize=(20, 5))
    plt.pcolor(pivot)
    plt.xticks(np.arange(0.5, len(pivot.columns), 1), pivot.columns)
    plt.yticks(np.arange(0.5, len(pivot.index), 1), pivot.index, rotation=45)
    plt.title('Memory access # (timstamp x virtual address space)', fontsize=20)
    plt.xlabel('timestamp', fontsize=14)
    plt.ylabel('Virtual Address Space', fontsize=10)

    plt.colorbar()

    plt.tight_layout()

    # output
    print "$ save plot"
    plt.savefig(dir_path+"/heatmap.png", format='png')
    if os.environ.get('DISPLAY','') != '':
    	plt.show()

draw_heatmap('.')
