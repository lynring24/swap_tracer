from utility import *
import csv
import pandas as pd
import numpy as np
from math import ceil, isnan

MICROSECOND = 1000000

def get_swap_extracted(use_abstract=False):
    # swap rsyslog cluster -> [ start  end ] : if start, end -> draw as a cluster 
    

    print "$ extract ryslog log"
    columns = pd.read_csv(get_path('awk'), header=None, delimiter=get_delimeter(), nrows=1)
    max_column = columns.shape[1]
    rsyslog = pd.read_csv(get_path('awk'), header=None, delimiter=get_delimeter(), usecols=[0, max_column-4, max_column-3, max_column-2, max_column-1])

    rsyslog.columns = ['timestamp', 'cmd', 'mode', 'swpentry', 'address']

    def compare_command(x):
        if x in get_command():
            return True
        else: 
            return False
    rsyslog["cmd"] = rsyslog["cmd"].apply(lambda x : compare_command(x))
    rsyslog = rsyslog[rsyslog.cmd==True]
    rsyslog['timestamp'] = rsyslog['timestamp'].apply(lambda x: (string_to_date(x[:-7]) - get_time()).total_seconds() * MICROSECOND)
    rsyslog = rsyslog[rsyslog.timestamp>= 0.0] 
    
    modes = ['out', 'fault', 'map']
    MODE_QUERY = get_mode_query()
    if MODE_QUERY != None:
        rsyslog = rsyslog.query(MODE_QUERY)

    # rsyslog['address'] = rsyslog.apply(lambda row : int(row['address'], 16) if row['mode'] in modes else row['address'], axis=1)
 

    print "$ extract duplicated address"
    page_fault = rsyslog[rsyslog['mode']=='fault'][['timestamp', 'address']]
    swap_in = rsyslog[rsyslog['mode']=='map'][['timestamp', 'address']]
    joined = pd.merge(page_fault, swap_in, on='address', how='outer').dropna()
    joined = joined[joined['timestamp_x'] < joined['timestamp_y']]
    joined.to_csv('{}/duplicated_address.csv'.format(get_path('head')))

    #TODO : abstract data by msec instead of usec and get mean address value instead
    if use_abstract:
        print "$ generate abstracted file"
        rsyslog['timestamp'] = rsyslog.apply(lambda row : round(row['timestamp']*1000, 3), axis =1)
        abstract = rsyslog.groupby(['mode', 'timestamp'])['address'].mean().reset_index()
        abstract.to_csv(get_path('rsyslog'), index=False)
    else:
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
    #print "> memory write back # : {}".format(len(rsyslog[rsyslog['mode']=='pageout'].index))
    print "> average exist time in memory (usec) : {} ".format(mean_time)

    with open('{}/summary.dat'.format(get_path('head')), 'w') as tag:
        tag.write("> memory swap in# : {}\n".format(len(rsyslog[rsyslog['mode']=='map'].index)))
        tag.write("> memory page out # : {}\n".format(len(rsyslog[rsyslog['mode']=='out'].index)))
        tag.write("> memory page fault # : {}\n".format(len(rsyslog[rsyslog['mode']=='fault'].index)))
        tag.write("> average exist time in memory (usec) : {} \n".format(mean_time))
    tag.close()
    return mean_time 
        


         

def extract_malloc():
    # TODO 
    # check if hook exists
    if os.path.isfile('{}/hook.csv'.format(get_path('root'))) == False:
        print "[Skip] Memory allocation not found"
        return 

    print "$ extract memory allocation"
    hook = pd.read_csv('{}/hook.csv'.format(get_path('root')), header=None,  delimiter=get_delimeter())

    hook.columns = ['timestamp', 'file','line','func','var', 'address', 'size']
    hook['timestamp'] = hook['timestamp'].apply(lambda x: (string_to_date(x) - get_time()).total_seconds() * MICROSECOND) 
    hook = hook[hook.timestamp>= 0.0]
    hook['address'] = hook['address'].apply(lambda x : int(x, 16))
    hook['timestamp'] = hook['timestamp'].astype(int)
    hook.to_csv(get_path('head')+'/hook.csv')


