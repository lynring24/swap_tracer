import json
from pprint import pprint 
from common import * 
from extract import extract
from split import split


def execute():
    rsyslog = open('/etc/rsyslog.conf').read()
    if "# $ActionFileDefaultTemplate RSYSLOG_TraditionalFileFormat" in rsyslog:
        print "rsyslog timestamping in RFC 3339 format"
    else: 
        print "rsyslog timestamp traditional file format "
        os.system('cp /etc/rsyslog.conf /etc/rsyslog.conf.default')
        os.system('cp ./rsyslog.conf.rfc3339 /etc/rsyslog.conf')

    exe_instr='sudo sh exec_mem_lim.sh'+ get_mem_limit() +'\"'+ get_command() + '\"'
    os.system(exe_instr)

def awk_log():
    # awk parts from log only after the execution
    awk_part = 'cat '+ get_path('rsyslog') + ' | '+'awk -v date='+ get_start_time() +' -F, \'/swptrace\(.*\)/ {if($1>date){print $1}}\' > '+ get_path('log')
    print exe_instr
    print awk_part
    os.system(awk_part)


if __name__ == '__main__':
   set_up_json()
   execute()
   set_up_path()
   awk_log()
   extract()
   split()


