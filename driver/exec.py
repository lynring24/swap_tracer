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
            child_process.wait()
            print "[Exec] {} sec".format(time.time() - start_time)
            os.system('$SWPTRACE/swptrace {} {}'.format(0, 0));
        else:
            print "\n[Debug] Skipped mmap"
    except:
        print "\n[Debug] Execution Abort"
        return 


def __awk_log(logfile, time_to_str, error): 
    	awk_part = logfile +'{} | awk -v start={} -F, \'/swptrace/  {if($1>start){print $0}}\' > ./awk.csv'.format(logfile, time_to_str)
    	print "\n$ "+ awk_part+'\n'
        os.system(awk_part)
	if is_false_generated('./awk.csv'):
		raise error


def awk_log(start_time):
    # awk parts from log only after the execution
    try:
        RSYSLOG = None
        if platform.dist()[0] == 'Ubuntu':
           RSYSLOG = "/var/log/syslog"
        else:
           RSYSLOG = "/var/log/messages"

	__awk_log('cat {}'.format(RSYSLOG),  datetime_to_rsyslog(start_time), IOError)
    except IOError:
        print "rsyslog miss message, try dmesg"
	__awk_log( 'dmesg --time-format iso', datetime_to_dmesg(start_time), RuntimeError)
    except:
        print "[Failure] fail to extract log" 
	clean_up_and_exit(os.getcwd())


def create_directory():
    configure['PATH']['awk'] = configure['PATH']['head'] +'/awk.csv'


def datetime_to_rsyslog(x):
    # needed for path, will print in rsyslog format
    return x.strftime(PATTERN["rsyslog"])

def datetime_to_dmesg(x):
    # needed for path, will print in rsyslog format
    return x.strftime(PATTERN["dmesg"])


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
   print COMMAND
   execute(COMMAND)
   LOG_DIR = os.getcwd()+'/'+datetime_to_rsyslog(START_TIME)
   os.system('sudo mkdir -p {}'.format(LOG_DIR))
   os.system('mv {}/maps {}'.format(os.getcwd(), LOG_DIR))
   os.chdir(LOG_DIR)
   awk_log(START_TIME)
   extract(USE_FAULT)



