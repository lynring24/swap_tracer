from utility import *
import csv
import pandas as pd

def isNumber(s):
  try:
    float(s)
    return True
  except ValueError:
    return False


def extract_swap():
    global area_subs
    print "$ extract ryslog log"
    columns = pd.read_csv(get_path('awk'), header=None, delimiter='\s+', nrows=1)
    max_column = columns.shape[1]
    rsyslog = pd.read_csv(get_path('awk'), header=None, delimiter='\s+', usecols=[0, max_column-4, max_column-3, max_column-2, max_column-1])

    rsyslog.columns = ['timestamp', 'cmd', 'mode', 'swpentry', 'address']
    rsyslog['timestamp'] = rsyslog['timestamp'].apply(lambda x: (string_to_date(x[:-6]) - get_time()).total_seconds())
    rsyslog = rsyslog[rsyslog.timestamp>= 0.0]
    rsyslog['address'] = rsyslog['address'].apply(lambda x : int(x, 16)/get_size('block'))
    
    print "$ generate extracted file [%s, %s] "%(rsyslog.shape[0], rsyslog.shape[1])
    rsyslog.to_csv(get_path('merge'))
    # for map.timestamp faster than in.timestamp && map.swpentry == in.swpentry in[anchor] = map.timestamp
    # anchor the related timestamp
    print "$ extract duplicated address"
    swap_in = rsyslog[rsyslog['mode']=='in'][['timestamp', 'address']]
    page_write = rsyslog[rsyslog['mode']=='out'][['timestamp', 'address']]
    joined = pd.merge(swap_in, page_write, on='address', how='outer').dropna()
    joined[joined['timestamp_x'] < joined['timestamp_y']].to_csv('{}/duplicated_address.csv'.format(get_path('head')))
         


def extract_malloc():
    print "$ extract memory allocation"
    alloc_log = pd.read_csv(get_path('hook'), header=None,  delimiter='\s+')
    alloc_log.columns = ['timestamp', 'file','line','func','var', 'address', 'size']
    alloc_log['timestamp'] = alloc_log['timestamp'].apply(lambda x: (string_to_date(x) - get_time()).total_seconds())
    alloc_log = alloc_log[alloc_log.timestamp>= 0.0]
    alloc_log['address'] = alloc_log['address'].apply(lambda x : str(int(x, 16)/get_size('block'))) 



