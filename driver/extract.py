from utility import *
import csv
import pandas as pd
import numpy as np
from math import ceil, isnan

MICROSECOND = 1000000

def get_swap_extracted(EXACT_ONLY):
    # swap rsyslog cluster -> [ start  end ] : if start, end -> draw as a cluster 
    

    print "$ extract ryslog log"
    columns = pd.read_csv(get_path('awk'), header=None, delimiter=get_delimeter(), nrows=1)
    max_column = columns.shape[1]
    rsyslog = pd.read_csv(get_path('awk'), header=None, delimiter=get_delimeter(), usecols=[0, max_column-5, max_column-4, max_column-3, max_column-2, max_column-1])

    rsyslog.columns = ['timestamp', 'pid', 'cmd', 'mode', 'swpentry', 'address']

    if EXACT_ONLY:
        rsyslog["pid"] = rsyslog["pid"].apply(lambda x : x==get_pid())
        rsyslog = rsyslog[rsyslog.pid==True]

    rsyslog['timestamp'] = rsyslog['timestamp'].apply(lambda x: (string_to_date(x[:-7]) - get_time()).total_seconds() * MICROSECOND)
    rsyslog = rsyslog[rsyslog.timestamp>= 0.0] 
    
    MODE_QUERY = get_mode_query()
    if MODE_QUERY != None:
        rsyslog = rsyslog.query(MODE_QUERY)

 

    print "$ extract duplicated address"
    page_fault = rsyslog[rsyslog['mode']=='fault'][['timestamp', 'address']]
    swap_in = rsyslog[rsyslog['mode']=='map'][['timestamp', 'address']]
    joined = pd.merge(page_fault, swap_in, on='address', how='outer').dropna()
    joined = joined[joined['timestamp_x'] < joined['timestamp_y']]
    joined.to_csv('{}/duplicated_address.csv'.format(get_path('head')))

    #TODO : abstract data by msec instead of usec and get mean address value instead
    print "$ generate extracted file [%s, %s] "%(rsyslog.shape[0], rsyslog.shape[1])
    rsyslog.to_csv(get_path('rsyslog'), index=False) 
    
    print "\n[ Summary ]"
    mean = joined.apply(lambda row: row['timestamp_y'] - row['timestamp_x'], axis=1)
    mean_time = mean.mean()
    if mean_time.dtype != np.float64: 
        mean_time = 0
    print "> memory swap in# : {}".format(len(rsyslog[rsyslog['mode']=='map'].index))
    print "> memory page out # : {}".format(len(rsyslog[rsyslog['mode']=='out'].index))
    print "> memory page fault # : {}".format(len(rsyslog[rsyslog['mode']=='fault'].index))
    if np.isnan(mean_time).any() != True:
        print "> average exist time in memory (usec) : {} ".format(mean_time)
        set_meantime(mean_time)

    with open('{}/summary.dat'.format(get_path('head')), 'w') as tag:
        tag.write("> memory swap in# : {}\n".format(len(rsyslog[rsyslog['mode']=='map'].index)))
        tag.write("> memory page out # : {}\n".format(len(rsyslog[rsyslog['mode']=='out'].index)))
        tag.write("> memory page fault # : {}\n".format(len(rsyslog[rsyslog['mode']=='fault'].index)))
        if np.isnan(mean_time).any() != True:
            tag.write("> average exist time in memory (usec) : {} \n".format(mean_time))
    tag.close()
        


         

def extract_malloc():
    # TODO 
    # check if hook exists
    if os.path.isfile('{}/hook.csv'.format(get_path('root'))) == False:
        print "\n$ [Skip] hook.csv not found"
        return 

    print "$ extract memory allocation"
    hook = pd.read_csv('{}/hook.csv'.format(get_path('root')), header=None,  delimiter=get_delimeter())

    hook.columns = ['timestamp', 'file','line','func','var', 'address', 'size']
    hook['timestamp'] = hook['timestamp'].apply(lambda x: (string_to_date(x) - get_time()).total_seconds() * MICROSECOND) 
    hook = hook[hook.timestamp>= 0.0]
    hook['address'] = hook['address'].apply(lambda x : int(x, 16))
    hook['timestamp'] = hook['timestamp'].astype(int)
    hook.to_csv(get_path('head')+'/hook.csv')


