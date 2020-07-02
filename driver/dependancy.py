import csv
import pandas as pd
from datetime import datetime 

def get_path(x):
    return '/home/hrchung/benchmarks/random/2020-07-01T16:42:56.977715/awk.csv'

def get_pattern():
    return '%Y-%m-%dT%H:%M:%S.%f' 

def string_to_date(timestamp):
    return datetime.strptime(timestamp[:-6], get_pattern())


def extract_swap():
    global area_subs
    START_TIME = string_to_date('2020-07-01T16:42:56.868135+09:00') 
    print "$ extract ryslog log"
    columns = pd.read_csv(get_path('awk'), header=None, delimiter='\s+', nrows=1)
    max_column = columns.shape[1]
    rsyslog = pd.read_csv(get_path('awk'), header=None, delimiter='\s+', usecols=[0, max_column-4, max_column-3, max_column-2, max_column-1])

    rsyslog.columns = ['timestamp', 'cmd', 'mode', 'swpentry', 'address']
    rsyslog['address'] = rsyslog['address'].apply(lambda x: int(x, 16)/4096)
    rsyslog['timestamp'] = rsyslog['timestamp'].apply(lambda x: (string_to_date(x) - START_TIME).total_seconds()) 
    
    # anchor the related timestamp
    print "$ extract duplicated address"
    swap_in = rsyslog[rsyslog['mode']=='in'][['timestamp', 'address']]
    page_write = rsyslog[rsyslog['mode']=='out'][['timestamp', 'address']]
    joined = pd.merge(swap_in, page_write, on='address', how='outer').dropna()
    joined[joined['timestamp_x'] < joined['timestamp_y']].to_csv('./duplicated_address.csv')



extract_swap()

        
          


