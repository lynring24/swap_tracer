import os 
import time
import subprocess
from utility import *

def exec_mem_limit(command, limit):
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

    if limit != 0:
        command='sudo sh $SWPTRACE/exec_mem_lim.sh {} \"{}\"'.format(str(limit), command)
   
    command = "(cd {}; {})".format(pwd, command)

    # child process 
    start_time = time.time()
    child_process= subprocess.Popen(command, stdin=None, stdout=None, shell=True)

    # wait for the grand child comes up
    time.sleep(10)
    
    os.system('$SWPTRACE/swptrace {} {}'.format(child_process.pid, 1));
    target_process = subprocess.Popen('echo $(pgrep -P $(pgrep -P $(pgrep -P {})))'.format(child_process.pid), stdout=subprocess.PIPE,shell=True)
    target_pid, err = target_process.communicate()
    target_pid = target_pid.strip()

    os.system('cat /proc/{}/maps > maps'.format(target_pid))
    child_process.wait()

    print "[Exec] {} sec".format(time.time() - start_time)
    os.system('$SWPTRACE/swptrace {} {}'.format(0, 0));
    set_pid(int(target_pid))




