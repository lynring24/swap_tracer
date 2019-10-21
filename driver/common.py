import os, sys, platform
import re, traceback
import time, calendar
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
   # configure["START"] = datetime.now().strftime(configure["PATTERN"]["DATE"])
    configure["START"] = "2019-10-21T13:26:52.447862"


def set_up_path():
    EXE_LOG = configure['PATH']["LOG_ROOT"]+'/'+configure["START"]
    configure['PATH']['awk'] = EXE_LOG +'/awk.log'
    configure['PATH']['extracted'] = EXE_LOG +'/extracted.log'
    configure['PATH']['block'] = EXE_LOG+'/block/'
    os.system('mkdir -p ' + configure['PATH']["LOG_ROOT"] )
    os.system('mkdir -p ' + EXE_LOG)
    os.system('mkdir -p ' + EXE_LOG +'/block/')


def is_valid_ms(line):
    matched= re.compile(configure["PATTERN"].get("BLOCK")).search(line)
    return matched


def get_start_time():
    return configure['START']


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
 

