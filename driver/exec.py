from pprint import pprint 
from utility import * 
from extract import extract_swap, extract_malloc
import subprocess
from requests import get
from scan import scan_malloc
from merge import merge
from model import cluster
#from split import split

def config_input():
    global hasTarget
    hasTarget = False
    if len(sys.argv) > 1: 
       NOTEXIST = -1
       #print sys.argv[1:]
       for arg in sys.argv[1:]:
          pos = arg.find('=')+1
          item = arg[pos:]
          if arg.find('--mem=') > NOTEXIST:
      	     set_mem_limit(item)
          elif arg.find('--cmd') > NOTEXIST:
       	     set_command('%s'%item) 
          elif arg.find('--ip') > NOTEXIST:
       	     set_ip(item)
          elif arg.find('--port') > NOTEXIST:
       	     set_port(item)
          elif arg.find('--target') > NOTEXIST:
             hasTarget = True
             set_path('target', item) 
          elif arg.find('--log') > NOTEXIST:
             set_path('root', item)
          else:
             print '[error] invalid option %s'%arg
             print "usage : python $SWPTARCE/exec.py --target=/ABSOLUTE_PATH/ --cmd=\"COMMAND\"  <--mem=Mib>  <--log=/ABSOLUTE_PATH/> <--ip=PUBLIC_IP> <--port=PORT_TO_USE>"
             sys.exit(1)



def check_option():
    print "\n---------------------------------------------------------------"
    if hasTarget == True:
       print " * target         :%s "%get_path('target')
    print " * command        :%s "%get_command()
    print " * mem lim(Mib)   :%s "%get_mem_limit()
    print " * log            :%s "%get_path('root')
    print " * public IP      :%s "%get_ip()
    print " * port           :%s "%str(get_port())
    print "---------------------------------------------------------------\n"


def exe_cmd():
    rsyslog = open('/etc/rsyslog.conf').read()
    if "# $ActionFileDefaultTemplate RSYSLOG_TraditionalFileFormat" in rsyslog:
       print "rsyslog timestamping in RFC 3339 format"
    else: 
       print "rsyslog timestamp traditional file format "
       os.system('cp /etc/rsyslog.conf /etc/rsyslog.conf.default')
       os.system('cp ./rsyslog.conf.rfc3339 /etc/rsyslog.conf')

    exe_instr='cd %s; sudo sh $SWPTRACE/exec_mem_lim.sh %s \"%s\"'%( get_path('root')+"/mod", str(get_mem_limit()) , get_command() )
    print "\n$ "+ exe_instr
    eval_result = os.system(exe_instr)


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
        instr ='dmesg --time-format iso | grep swptrace > '+get_path('awk')
        os.system(instr)
	print "\n$ %s \n"%instr
    except BaseException as ex:
        print ex
	clean_up_and_exit(get_path('head'), 'awk_log')



def run_flask():
    os.environ['SWPTRACE_LOG'] = get_path('head')
    os.environ['FLASK_APP']='app.py'
    os.environ['SWPTRACE_CMD']='$ %s %s'%(str(get_mem_limit()), get_command())
    os.environ['CLASS']=str(get_class())
    #ip = get('https://api.ipify.org').text
    try: 
      result = os.system('cd $SWPTRACE ; flask run --host=%s --port=%s'%(get_ip(), get_port()))
      if result != 0:
         raise OSError
    except OSError:
      if get_ip() != '0.0.0.0' and get_port() != '5000':
         print "[warning] invalid IP or port try 0.0.0.0:5000"
         os.system('cd $SWPTRACE ; flask run')
     

if __name__ == '__main__':
   
   set_up()
   config_input()
   check_option()
   if hasTarget == True :
      scan_malloc()
   exe_cmd()
   set_up_path()
   awk_log()
   if hasTarget == True :
      extract_malloc()
   extract_swap()
   merge()
   cluster()
   run_flask() 
