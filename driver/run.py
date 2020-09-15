import os 
import time
import subprocess


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
    p = subprocess.Popen(command, stdin=None, stdout=None, shell=True)
    time.sleep(0.05)
    os.system('echo pid # : $(pgrep -P $(pgrep -P $(pgrep -P {})))'.format(p.pid))
    os.system('cat /proc/$(pgrep -P $(pgrep -P $(pgrep -P {})))/maps > maps'.format(p.pid))
    out, err = p.communicate()
    p.wait()




