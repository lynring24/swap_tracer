import os, sys, platform
import re, traceback
import time, calendar
import shutil
from uptime import uptime
from datetime import datetime, timedelta
import json


def set_up() :
    global configure
    configure = dict()
    configure["TIME"] = datetime.now()
    # configure pattern
    configure['PATTERN'] = dict() 
    configure['PATTERN']['LOG']= '(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6})[-\+]\d{2}:\d{2} .*swptrace\((.+)\): map (\(swpentry: \d+, uaddr: \d+\))'
    configure['PATTERN']['DATE']='%Y-%m-%dT%H:%M:%S.%f'
    configure['PATTERN']['BLOCK']='(\d+.\d{6}) (.+)'
    configure['PATTERN']['MICROSEC']='(\d+:\d{2}:\d{2}\.\d{6}) (.+)'
    # configure size
    configure['SIZE'] = dict()
    configure['SIZE']['BLOCK'] = 1024
    configure['SIZE']['PAGE'] = 4096
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
   
    
    

area = ['total', 'code', 'sram', 'peripheral', 'ex_ram', 'ex_device', 'private_peripheral_bus', 'vendor']


def set_up_path():
    EXEC_DIR = configure['PATH']["root"]+'/'+datetime_to_string(configure["TIME"])
    configure['PATH']['head'] = EXEC_DIR
    configure['PATH']['awk'] = EXEC_DIR +'/awk.log'
    configure['PATH']['pdf'] = EXEC_DIR + 'snapshot.pdf'
    for side in area:
        configure['PATH'][side] = EXEC_DIR + '/' + side + '.log'
   #configure['PATH']['extracted'] = EXEC_DIR +'/extracted.log'
   # configure['PATH']['block'] = EXEC_DIR+'/block/'
    os.system('sudo mkdir -p ' + configure['PATH']["root"] )
    os.system('sudo mkdir -p ' + EXEC_DIR)
   # os.system('mkdir -p ' + EXEC_DIR +'/block/')


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
    

def set_pattern(key, value):
    configure['PATTERN'][key] = value


def set_time():
    configure["TIME"]


def is_valid_ms(line):
    matched= re.compile(configure["PATTERN"].get("BLOCK")).search(line)
    return matched


def get_time():
    return configure["TIME"]


def datetime_to_string(x):
    return x.strftime(configure["PATTERN"]["DATE"])


def get_path(x):
    return configure['PATH'].get(x)

def get_page_size():
    return configure['SIZE']["PAGE"]

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


def get_size(x):
    return configure['SIZE'].get(x)


def get_mem_limit():
    return configure['MEM_LIMIT']


def get_pattern(x):
    return configure['PATTERN'].get(x)
 

def is_false_generated(x):
    return (os.path.isfile(x) == False or os.stat(x).st_size == 0)
 

def string_to_date(timestamp, pattern):
    return datetime.strptime(timestamp, pattern)

 
def clean_up(path):
    if os.path.exists(path): 
       print "Drop %s"%path
       if os.path.isfile(path):
          os.remove(path)
       else: 
          shutil.rmtree(path, ignore_errors=True)
       #shutil.rmtree(configure['PATH']['head'], ignore_errors=True)

def clean_up_and_exit(path, func):
    print "[DEBUG] Failure in %s()"%func
    clean_up(path)
    sys.exit(1)



