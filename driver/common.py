import os, sys, platform
import re, traceback
import time, calendar
import shutil
from uptime import uptime
from datetime import datetime, timedelta
import json


def set_up_json() :
    global configure
    with open ('configure.json') as file:
    # JSON can't unescape the so replace with the actual character 
          configure = json.load(file)

    if platform.dist()[0] == 'Ubuntu':
       configure['PATH']['rsyslog'] = "/var/log/syslog"
    else:
       configure['PATH']['rsyslog'] = "/var/log/messages"
    configure["TIME"] = {'rsyslog' : datetime.now().strftime(configure["PATTERN"]["DATE"]),
                        'dmesg':str(uptime())}


def set_up_path():
    EXE_LOG = configure['PATH']["LOG_ROOT"]+'/'+configure["TIME"]['rsyslog']
    configure['PATH']['awk'] = EXE_LOG +'/awk.log'
    configure['PATH']['extracted'] = EXE_LOG +'/extracted.log'
    configure['PATH']['block'] = EXE_LOG+'/block/'
    os.system('mkdir -p ' + configure['PATH']["LOG_ROOT"] )
    os.system('mkdir -p ' + EXE_LOG)
    os.system('mkdir -p ' + EXE_LOG +'/block/')


def set_path(path, value):
    configure['PATH'][path] = value
    

def set_pattern(key, value):
    configure['PATTERN'][key] = value


def set_time(key, value):
    configure["TIME"]['rsyslog'] = value


def is_valid_ms(line):
    matched= re.compile(configure["PATTERN"].get("BLOCK")).search(line)
    return matched


def get_time(key):
    return configure["TIME"].get(key)


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
    print "clean up %s"%path
    if os.path.exists(path):
       shutil.rmtree(path, ignore_errors=True)

def clean_up_and_exit(ex, path, func):
    print "[DEBUG] Failure in %s()"%func
    clean_up(path)
    sys.exit(1)
