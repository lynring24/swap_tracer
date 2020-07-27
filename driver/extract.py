from utility import *
import csv
import pandas as pd
import numpy as np
from math import ceil, isnan


def get_swap_extracted():
    print "$ extract ryslog log"
    columns = pd.read_csv(get_path('awk'), header=None, delimiter='\s+', nrows=1)
    max_column = columns.shape[1]
    rsyslog = pd.read_csv(get_path('awk'), header=None, delimiter='\s+', usecols=[0, max_column-4, max_column-3, max_column-2, max_column-1])

    rsyslog.columns = ['timestamp', 'cmd', 'mode', 'swpentry', 'address']
    rsyslog['timestamp'] = rsyslog['timestamp'].apply(lambda x: (string_to_date(x[:-6]) - get_time()).total_seconds())
    rsyslog = rsyslog[rsyslog.timestamp>= 0.0]
    rsyslog['address'] = rsyslog['address'].apply(lambda x : int(x, 16)/get_page_size())
    
    print "$ generate extracted file [%s, %s] "%(rsyslog.shape[0], rsyslog.shape[1])
    rsyslog.to_csv(get_path('merge'))
    # for map.timestamp faster than in.timestamp && map.swpentry == in.swpentry in[anchor] = map.timestamp
    # anchor the related timestamp

    print "$ extract duplicated address"
    swap_in = rsyslog[rsyslog['mode']=='in'][['timestamp', 'address']]
    page_write = rsyslog[rsyslog['mode']=='out'][['timestamp', 'address']]
    joined = pd.merge(swap_in, page_write, on='address', how='outer').dropna()
    joined = joined[joined['timestamp_x'] < joined['timestamp_y']]
    joined.to_csv('{}/duplicated_address.csv'.format(get_path('head')))

    # timestamp_x, address , timstamp_y
    print "\n[ Summary ]"
    mean = joined.apply(lambda row: row['timestamp_y'] - row['timestamp_x'], axis=1)
    mean_time = mean.mean()
    if np.isnan(mean_time):
        mean_time = 0
    print "> memory swap in# : {}".format(len(rsyslog[rsyslog['mode']=='in'].index))
    print "> memory page out # : {}".format(len(rsyslog[rsyslog['mode']=='out'].index))
    print "> memory write back # : {}".format(len(rsyslog[rsyslog['mode']=='pageout'].index))
    print "> average exist time in memory (usec) : {} ".format(mean_time)
    return mean_time 
        


         

def extract_malloc():
    # TODO 
    # check if hook exists
    if os.path.isfile('{}/hook.csv'.format(get_path('clone'))) == False:
        print "[Skip] Memory allocation not found"
        return 

    print "$ extract memory allocation"
    allocations = pd.read_csv('{}/hook.csv'.format(get_path('clone')), header=None,  delimiter='\s+')

    allocations.columns = ['timestamp', 'file','line','func','var', 'address', 'end']
    allocations['timestamp'] = allocations['timestamp'].apply(lambda x: (string_to_date(x) - get_time()).total_seconds())
    allocations = allocations[allocations.timestamp>= 0.0]
    allocations['address'] = allocations['address'].apply(lambda x : int(int(x, 16)/get_page_size()))
    allocations['end'] = allocations['end'].apply(lambda x : int (int(x, 16)/get_page_size()))
    allocations.to_csv(get_path('head')+'/hook.csv')
    




