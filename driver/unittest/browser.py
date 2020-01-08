from pprint import pprint 
from common import * 
from extract import extract
from split import split
import subprocess
from requests import get

def config_input():
    if len(sys.argv) > 1: 
       NOTEXIST = -1
       #print sys.argv[1:]
       for arg in sys.argv[1:]:
          if arg.find('--mem=') > NOTEXIST:
      	     set_mem_limit(arg[arg.find('=')+1:])
          elif arg.find('--cmd') > NOTEXIST:
       	     set_command('"%s"'%arg[arg.find('=')+1:]) 
          elif arg.find('--ip') > NOTEXIST:
       	     set_ip(arg[arg.find('=')+1:])
          elif arg.find('--port') > NOTEXIST:
       	     set_port(arg[arg.find('=')+1:])
          else:
             print '[error] invalid option %s'%arg
             print "usage : python $SWPTARCE/exec.py <--mem=Mib > <--cmd=\"COMMAND\"> <--ip=PUBLIC_IP> <--port=PORT_TO_USE>"
             sys.exit(1)



def check_option():
    print "\n---------------------------------------------------------------"
    print " * command        :%s "%get_command()
    print " * mem lim(Mib)   :%s "%get_mem_limit()
    print " * public IP      :%s "%get_ip()
    print " * port           :%s "%str(get_port())
    print "---------------------------------------------------------------\n"


def exe_cmd():
    try:
	rsyslog = open('/etc/rsyslog.conf').read()
	if "# $ActionFileDefaultTemplate RSYSLOG_TraditionalFileFormat" in rsyslog:
	    print "rsyslog timestamping in RFC 3339 format"
	else: 
	    print "rsyslog timestamp traditional file format "
	    os.system('cp /etc/rsyslog.conf /etc/rsyslog.conf.default')
	    os.system('cp ./rsyslog.conf.rfc3339 /etc/rsyslog.conf')
        print 'mem :%s'%str(get_mem_limit())
	exe_instr='sudo sh $SWPTRACE/exec_mem_lim.sh '+ str(get_mem_limit()) +' \"'+ get_command() + '\"'
	print "\n$"+ exe_instr
	eval_result = os.system(exe_instr)
        if eval_result != 0:
           raise OSError
    except OSError:
        print '[Debug] execution failed.'
	sys.exit(1)



def __awk_log(head, error): 
    	awk_part = head + ' | '+'awk -v start='+ datetime_to_string(get_time()) +' -F, \'/swptrace\(.*\)/ {if($1>start){print $0}}\' > '+ get_path('awk')
    	print "\n$ "+ awk_part+'\n'
    	os.system(awk_part)
	if is_false_generated(get_path('awk')):
		raise error


def awk_log():
    # awk parts from log only after the execution
    try:
	__awk_log('cat '+get_path('rsyslog'),IOError)
    except IOError:
        print "rsyslog miss message, try dmesg"
	clean_up(get_path('rsyslog'))
       #__awk_log('dmesg -T', BaseException)
        instr ='dmesg --time-format iso | grep swptrace > '+get_path('awk')
        os.system(instr)
	print "\n$ "+instr+"\n"
	date_pattern= '%Y-%m-%dT%H:%M:%S,%f'
	parse_pattern = '(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\,\d{6})[\+-]\d{4} swptrace\((.+)\): map (\(swpentry: \d+, uaddr: \d+\))'
	set_pattern('DATE', date_pattern)
	set_pattern('LOG', parse_pattern)
    except BaseException as ex:
        print ex
	clean_up_and_exit(get_path('head'), 'awk_log')



def run_flask():
    os.environ['SWPTRACE_LOG'] = '../demo/log/2020-01-08T03:07:31.958102'
    os.environ['FLASK_APP']='app.py'
    os.environ['SWPTRACE_CMD']='$ TEST DATA OF CFD'
    #ip = get('https://api.ipify.org').text
    try: 
      result = os.system('cd $SWPTRACE ; flask run --host=%s --port=%s'%(get_ip(), get_port()))
      if result != 0:
         raise OSError
    except OSError:
      print "[warning] invalid IP or port try 0.0.0.0:5000"
      os.system('cd $SWPTRACE ; flask run')
     

if __name__ == '__main__':
   set_up()
   config_input()
   check_option()
   #exe_cmd()
   #set_up_path()
   #awk_log()
   #extract()
   run_flask() 
