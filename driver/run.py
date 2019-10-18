import os, sys, platform
import json
from pprint import pprint 
from configure import * 



def _init_() :         
    with open ('configure.json') as configurefile:
         configure = json.load(configurefile)
    if configure["SRC"] = "Default":
	 if platform.dist()[0] == "Ubuntu":
            configure['SRC'] = "/var/log/syslog"
         else:
	    configure['SRC'] = "/var/log/messages"
 
    start = datetime.now().strftime(DATE_PATTERN)
    os.system('mkdir -p ' + configure["LOG_ROOT"])
    os.system('mkdir -p ' + configure["LOG_ROOT"]+'/'+start)
    os.system('mkdir -p ' + configure["LOG_ROOT"]+'/'+start+'/block/')


def execute():
    rsyslog = open('/etc/rsyslog.conf').read()
    if "# $ActionFileDefaultTemplate RSYSLOG_TraditionalFileFormat" in rsyslog:
        print "rsyslog timestamping in RFC 3339 format"
    else: 
        print "rsyslog timestamp traditional file format "
        os.system('cp /etc/rsyslog.conf /etc/rsyslog.conf.default')
        os.system('cp ./rsyslog.conf.rfc3339 /etc/rsyslog.conf')

    os.system('sudo sh exec_mem_lim.sh'+configure['MEM_LIMIT']+"\""+configure['COMMAND']+"\"")


def extract():
    with open(configure["SRC"], 'r') as src:
         for line in src:
	      __parse(line)
	      # if ISABSTRACT is used, release last tracked state
         if configure["ABSTRACT"] == True: 
	    print_mean_state()
            outfile.close()


def split_by_block(): 



if __name__ == '__main__':
   __init__()
   execute()
   extract()
   split_by_block()


