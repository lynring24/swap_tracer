from extract import extract
import subprocess
import os, sys, platform
import re, traceback
import time, calendar
import shutil
from uptime import uptime
from datetime import datetime, timedelta
import json
import resource


PATTERN = dict() 
PATTERN['rsyslog']='%Y-%m-%dT%H:%M:%S.%f'
PATTERN['dmesg']='%Y-%m-%dT%H:%M:%S,%f'
#PATTERN['rsyslog']='%Y-%m-%dT%H:%M:%S.%f'
#PATTERN['dmesg']='%Y-%m-%dT%H:%M:%S,%f'
PATTERN['date']='%Y-%m-%dT%H:%M:%S[,.]%f'

COMMAND="sleep 20"
USE_FAULT = False

def config_option():
    global hasTarget
    hasTarget = False
    if len(sys.argv) > 1: 
       NOTEXIST = -1
       for arg in sys.argv[1:-1]:
          #pos = arg.find('=')+1
          #item = arg[pos:]
          if arg.find('--fault') > NOTEXIST:
              USE_FAULT = True
          else:
             print '[error] invalid option %s'%arg
             print "usage : python $SWPTARCE/exec.py --fault \"COMMAND\""
             sys.exit(1)

       global COMMAND
       COMMAND = sys.argv[-1]
    print "\n---------------------------------------------------------------"
    print " * command   : %s "%COMMAND
    print "---------------------------------------------------------------\n"


def execute(command):
    rsyslog = open('/etc/rsyslog.conf').read()
    if "# $ActionFileDefaultTemplate RSYSLOG_TraditionalFileFormat" in rsyslog:
        print "rsyslog timestamping in RFC 3339 format"
    else:
        print "rsyslog timestamp traditional file format "
        os.system('cp /etc/rsyslog.conf /etc/rsyslog.conf.default')
        os.system('cp ./rsyslog.conf.rfc3339 /etc/rsyslog.conf')

    pwd = os.getcwd() 
    if os.path.exists('./clone'):
        pwd='{}/clone'.format(pwd)
   
    try:
        command = "(cd {}; {})".format(pwd, command)
        # child process 
        start_time = time.time()
        child_process= subprocess.Popen(command, stdin=None, stdout=None, shell=True)
        # wait for the grand child comes up
        time.sleep(10)
        os.system('$SWPTRACE/swptrace {} {}'.format(child_process.pid, 1));
        target_pid = None
        target_process = subprocess.Popen('echo $(pgrep -P {})'.format(child_process.pid), stdout=subprocess.PIPE,shell=True)
        target_pid, err = target_process.communicate()
        target_pid = target_pid.strip() 

        if target_pid != "":
            os.system('cat /proc/{}/maps > maps'.format(target_pid))
        else:
            print "\n[Debug] Skipped mmap"
        child_process.wait()
        #print "[Exec] {} sec".format(time.time() - start_time)
        os.system('$SWPTRACE/swptrace {} {}'.format(0, 0));
    except:
        print "\n[Debug] Execution Abort"
        os.system("python $SWPTRACE/off.py")
        return 


def awk_log(start_time):
    try:
        RSYSLOG = None
        if platform.dist()[0] == 'Ubuntu':
            RSYSLOG = "/var/log/syslog"
        else:
            RSYSLOG = "/var/log/messages"
        
        awk_command = "cat %s | awk -v start=%s -F, '/swptrace/ {if($1>start) {print $0}}' > awk.csv"%(RSYSLOG, datetime_to_string(start_time))
        print "$ %s\n"%awk_command
        os.system(awk_command)
        if is_false_generated("./awk.csv"):
           raise IOError
    except IOError:
        print "rsyslog miss message, try dmesg"
        awk_command = "dmesg --time-format iso | awk -v start=%s -F, '/swptrace/ {if($1>start) {print $0}}' > ./awk.csv"%datetime_to_string(start_time)
        print "$ %s\n"%awk_command
        os.system(awk_command)
        if is_false_generated("./awk.csv"):
            print "[DEBUG] Swap trace not exists" 
            exit(1)


def datetime_to_string(x):
    # needed for path, will print in rsyslog format
    return x.strftime(PATTERN["rsyslog"])


def is_false_generated(x, fname=None):
    return (os.path.isfile(x) == False or os.stat(x).st_size == 0)
 

def clean_up_and_exit(path):
    print "[Error] clean up directory"
    if os.path.exists(path): 
       print "Drop %s"%path
       if os.path.isfile(path):
          os.remove(path)
       else: 
          shutil.rmtree(path, ignore_errors=True)
    sys.exit(1)
 

if __name__ == '__main__': 
   config_option()
   START_TIME = datetime.now()
   execute(COMMAND)
   LOG_DIR = os.getcwd()+'/'+datetime_to_string(START_TIME)
   os.system('sudo mkdir -p {}'.format(LOG_DIR))
   # TODO: if file exists
   MAPS = '{}/maps'.format(os.getcwd())
   if os.path.isfile(MAPS):
       os.system('mv {} {}'.format(MAPS, LOG_DIR))
   os.chdir(LOG_DIR)
   awk_log(START_TIME)
   extract(USE_FAULT)



