from utility import * 
import subprocess
from extract import extract
import subprocess
from requests import get
from scan import scan_malloc
from plot import plot_out
from exec_mem_lim import exec_mem_limit


configures = {'target' : False, 'mem' : False, 'cmd' : False, 'dir':False, 'log': False, 'heatmap' : False, 'area': False, 'fault' : False}

def config_option():
    global hasTarget
    hasTarget = False
    if len(sys.argv) > 1: 
       NOTEXIST = -1
       for arg in sys.argv[1:]:
          pos = arg.find('=')+1
          item = arg[pos:]
          if arg.find('--mem') > NOTEXIST:
             configures['mem'] = True
      	     set_mem_limit(item)
          elif arg.find('--cmd') > NOTEXIST:
             configures['cmd'] = True
       	     set_command('%s'%item) 
          elif arg.find('--dir') > NOTEXIST:
             configures['dir'] = True
             set_path('dir', item) 
          elif arg.find('--heatmap') > NOTEXIST:
              configures['heatmap'] = True
          elif arg.find('--fault') > NOTEXIST:
              configures['fault'] = True
          elif arg.find('--area') > NOTEXIST:
              configures['area'] = True
          else:
             print '[error] invalid option %s'%arg
             print "usage : python $SWPTARCE/exec.py --target=/ABSOLUTE_PATH/ --cmd=\"COMMAND\"  <--mem=Mib>  <--log=/ABSOLUTE_PATH/> <--heatmap>  <--exact=True>" 
             sys.exit(1)


def check_option():
    print "\n---------------------------------------------------------------"
    if configures['dir'] == True:
       print " * dir         : %s "%get_path('target')
    print " * command        : %s "%get_command()
    print " * mem lim(Mib)   : %s "%get_mem_limit()
    print "---------------------------------------------------------------\n"


def __awk_log(logfile, option, error): 
    	awk_part = logfile + ' | ' + option + ' > '+ get_path('awk')
    	print "\n$ "+ awk_part+'\n'
        os.system(awk_part)
	if is_false_generated(get_path('awk')):
		raise error


def awk_log():
    # awk parts from log only after the execution
    try:
	__awk_log('cat /var/log/syslog', 'awk -v start='+ datetime_to_string(get_time()) +' -F, \'/swptrace/ {if($1>start){print $0}}\'' , IOError)
    except IOError:
        print "rsyslog miss message, try dmesg"
	__awk_log( 'dmesg --time-format iso', 'grep swptrace', RuntimeError)
    except:
        print "[Failure] fail to extract log" 
	clean_up_and_exit(get_path('head'), 'awk_log')

     

if __name__ == '__main__': 
   initialize()
   config_option()
   check_option()
   exec_mem_limit(get_command(), get_mem_limit())
   create_directory() 
   awk_log()
   os.system('mv {}/maps {}'.format(get_path('root'), get_path('head')))
   extract(configures['fault'])
