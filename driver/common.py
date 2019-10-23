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
#   configure["TIME"] = datetime.now().strftime(configure["PATTERN"]["DATE"])
#   configure["TIME"] = datetime.now()
    configure["TIME"] = string_to_date('2019-10-23T20:47:42.850120', "%Y-%m-%dT%H:%M:%S.%f")


def set_up_path():
    EXE_LOG = configure['PATH']["LOG_ROOT"]+'/'+datetime_to_string(configure["TIME"])
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
    print "clean up %s"%path
    if os.path.exists(path):
       shutil.rmtree(path, ignore_errors=True)

def clean_up_and_exit(ex, path, func):
    print "[DEBUG] Failure in %s()"%func
    clean_up(path)
    sys.exit(1)
