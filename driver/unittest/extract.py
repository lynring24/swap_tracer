import csv
import pandas as pd
import numpy as np
from math import ceil, isnan

import os, sys, platform
import re, traceback
import time, calendar
import shutil
from uptime import uptime
from datetime import datetime, timedelta
import json
import resource


MICROSECOND = 1000000

def extract():
    # TODO 
    print "$ extract ryslog log"
    columns = pd.read_csv('./awk.csv', header=None, delimiter='|', nrows=1)
    max_column = columns.shape[1]
    rsyslog = pd.read_csv('./awk.csv', header=None, delimiter='|', usecols=[0, max_column-4, max_column-3, max_column-2, max_column-1])
    

    rsyslog.columns = ['timestamp', 'cmd', 'mode', 'swpentry', 'address']
    rsyslog['timestamp'] = rsyslog['timestamp'].apply(lambda x: (string_to_date(x[:-7]) - get_time()).total_seconds() * MICROSECOND)
    rsyslog = rsyslog[rsyslog.timestamp>= 0.0] 
    
    #rsyslog['address'] = rsyslog['address'].apply(lambda x : int(x, 16)/get_page_size())
    # TODO : %lu is used for map, need to fix kernel

    #rsyslog['address'] = rsyslog['address'].apply(lambda x : int(x,16))
    rsyslog['address'] = rsyslog.apply(lambda row: int(row['address']) if row['mode']=='map' else int(row['address'],16), axis=1)

    print "$ extract duplicated address"
    swap_in = rsyslog[rsyslog['mode']=='in'][['timestamp', 'address']]
    page_write = rsyslog[rsyslog['mode']=='out'][['timestamp', 'address']]
    joined = pd.merge(swap_in, page_write, on='address', how='outer').dropna()
    joined = joined[joined['timestamp_x'] < joined['timestamp_y']]
    joined.to_csv('./duplicated_address.csv')

    # check if hook exists
    if os.path.isfile('./hook.csv'):
	    print "$ extract memory allocation"
	    allocations = pd.read_csv('./hook.csv', header=None,  delimiter='|')
	    allocations.columns = ['timestamp', 'file','line','func','var', 'address', 'size']
	    allocations['timestamp'] = allocations['timestamp'].apply(lambda x: (string_to_date(x) - get_time()).total_seconds() * MICROSECOND) 
	    allocations = allocations[allocations.timestamp>= 0.0]
	    #allocations['address'] = allocations['address'].apply(lambda x : int(int(x, 16)/get_page_size()))
	    allocations['address'] = allocations['address'].apply(lambda x : int(x, 16))

	    #allocations['end'] = allocations['end'].apply(lambda x : int (int(x, 16)/get_page_size()))
	    allocations.sort_values(by=['timestamp'], ascending=False)
    	    print "$ generate extracted file [%s, %s] "%(allocations.shape[0], allocations.shape[1])
	    def get_var_info(timestamp, address):
		info=''
		for index, row in allocations.iterrows():
		    #if row['timestamp'] < timestamp and row['address'] <= address and (address <= row['address'] + row['size']):
		    if  row['timestamp'] < timestamp and row['address'] <= address and address <= (row['address'] + row['size']):
		       # info=row.to_string(header=False,index=False)
		       info='/'.join([row['file'],str(row['line']),row['func'],row['var']])
		       break;
		return info
	    rsyslog['info']=rsyslog.apply(lambda row: get_var_info(row['timestamp'], row['address']), axis=1)
	    #rsyslog['info']=rsyslog.apply(lambda row: get_var_info(row['timestamp'], row['address']), axis=1)
				 


    #TODO : abstract data by msec instead of usec and get mean address value instead
    print "$ generate extracted file [%s, %s] "%(rsyslog.shape[0], rsyslog.shape[1])
    rsyslog.to_csv('./rsyslog.csv', index=False) 
    
    print "\n[ Summary ]"
    mean = joined.apply(lambda row: row['timestamp_y'] - row['timestamp_x'], axis=1)
    mean_time = mean.mean()
    if mean_time.dtype != np.float64: 
        mean_time = 0
    print "> memory swap in# : {}".format(len(rsyslog[rsyslog['mode']=='in'].index))
    print "> memory page out # : {}".format(len(rsyslog[rsyslog['mode']=='out'].index))
    print "> memory write back # : {}".format(len(rsyslog[rsyslog['mode']=='pageout'].index))
    print "> average exist time in memory (usec) : {} ".format(mean_time)
    return mean_time 
        


         


def initialize() :
    global configure
    configure = dict()
    # configure pattern
    configure['PATTERN'] = dict() 
    configure['PATTERN']['rsyslog']='%Y-%m-%dT%H:%M:%S.%f'
    configure['PATTERN']['dmesg']='%Y-%m-%dT%H:%M:%S,%f'
    configure['PATTERN']['date']='%Y-%m-%dT%H:%M:%S[,.]%f'
    
    configure['PATTERN']['block']='(\d+.\d{6}) (.+)'
    configure['PATTERN']['MICROSEC']='(\d+:\d{2}:\d{2}[,\.]\d{6}) (.+)'
    # configure size
    configure['SIZE'] =  resource.getpagesize()
    # configure path 
    configure['PATH'] = dict()
    configure['PATH']['root'] = os.getcwd()
    configure['PATH']['target'] = os.getcwd()
    if platform.dist()[0] == 'Ubuntu':
       configure['PATH']['rsyslog'] = "/var/log/syslog"
    else:
       configure['PATH']['rsyslog'] = "/var/log/messages"

    # configure mem limit
    configure['MEM_LIMIT'] = 1024
    configure['COMMAND'] = "python $SWPTRACE/../demo/code/increment.py"
    # configre public ip
    configure['PUBLIC'] = dict()
    configure['PUBLIC']['IP'] = '0.0.0.0'
    configure['PUBLIC']['PORT'] = 5000

    # configure time
    configure["TIME"] = datetime.now()
   
    
    

# area = ['total','rsyslog', 'labeled']
# area = ['total', 'code', 'ram', 'peripheral', 'ex_ram', 'ex_device', 'private_peripheral_bus', 'vendor']


def get_sub_path_by_id(id):
    return get_path(area[id])


def create_directory():
    configure['PATH']['clone'] = configure['PATH']['target']+"/clone"
    configure['PATH']['head'] = configure['PATH']["root"]+'/'+datetime_to_string(configure["TIME"])
    configure['PATH']['awk'] = configure['PATH']['head'] +'/awk.csv'
    configure['PATH']['rsyslog'] = configure['PATH']['head'] +'/rsyslog.csv'

    os.system('sudo mkdir -p ' + configure['PATH']['head'])
    with open(get_path('head')+'/option.dat','w') as tag:
        tag.write('[Option]\n %s, %s, %s, %s, %s\n' %(get_command(), get_mem_limit(), get_path('head'), get_ip(), str(get_port())) )
    tag.close()


def set_ip(value):
    configure['PUBLIC']['IP'] = value

def get_ip():
    return configure['PUBLIC']['IP'] 

def set_port(value):
    configure['PUBLIC']['PORT'] = value

def get_port():
    return configure['PUBLIC']['PORT']

def set_command(value):
    configure['COMMAND'] = value
 

def set_mem_limit(value):
    configure['MEM_LIMIT'] = value


def set_path(path, value):
    configure['PATH'][path] = value


def set_class(num):
    configure['CLASS'] = num
    

def get_class():
    return configure['CLASS']


def set_pattern(key, value):
    configure['PATTERN'][key] = value


def set_time():
    configure["TIME"]


def is_log_path(line):
    matched= re.compile('*{}*'.format(get_pattern('rsyslog'))).search(line)
    return matched


def get_time():
    #return string_to_date('2020-07-29T21:04:29.316294')
    return string_to_date('2020-07-29T22:13:23.845396')


def datetime_to_string(x):
    # needed for path, will print in rsyslog format
    return x.strftime(configure["PATTERN"]["rsyslog"])


def get_path(x):
    return configure['PATH'].get(x)


def get_command():
    return configure["COMMAND"]

# TODO 
# threshold for vpn
def get_threshold():
    return configure["THRESHOLD"]


def do_abstract():
    return configure['ABSTRACT']


def do_threshold():
    return configure["THRESHOLD"] != -1


def get_threshold():
    return configure["THRESHOLD"] 


def get_page_size():
    return configure['SIZE']


def get_mem_limit():
    return configure['MEM_LIMIT']

def get_pattern(x):
    return configure['PATTERN'].get(x)
 

def is_false_generated(x, fname=None):
    return (os.path.isfile(x) == False or os.stat(x).st_size == 0)
 

def string_to_date(timestamp):
    try: 
        timestamp = datetime.strptime(timestamp, get_pattern('rsyslog'))
    except ValueError:
        timestamp = datetime.strptime(timestamp, get_pattern('dmesg'))
       
    return timestamp

initialize()
extract()
