from pprint import pprint 
from utility import * 
import subprocess
from extract import get_swap_extracted, extract_malloc
import subprocess
from requests import get
from scan import scan_malloc
from plot import draw_view
from run import exec_mem_limit


enable_argv = {'target' : False, 'mem' : False, 'cmd' : False, 'ip': False, 'port':False, 'log': False,              'heatmap' : False, 'mode': False, 'exact' : False}

def config_option():
    global hasTarget
    hasTarget = False
    if len(sys.argv) > 1: 
       NOTEXIST = -1
       #print sys.argv[1:]
       for arg in sys.argv[1:]:
          pos = arg.find('=')+1
          item = arg[pos:]
          if arg.find('--mem') > NOTEXIST:
             enable_argv['mem'] = True
      	     set_mem_limit(item)
          elif arg.find('--cmd') > NOTEXIST:
             enable_argv['cmd'] = True
       	     set_command('%s'%item) 
          elif arg.find('--ip') > NOTEXIST:
             enable_argv['ip'] = True
       	     set_ip(item)
          elif arg.find('--port') > NOTEXIST:
             enable_argv['port'] = True
       	     set_port(item)
          elif arg.find('--target') > NOTEXIST:
             enable_argv['target'] = True
             set_path('target', item) 
          elif arg.find('--log') > NOTEXIST:
             enable_argv['log'] = True
             set_path('root', item)
          elif arg.find('--heatmap') > NOTEXIST:
              enable_argv['heatmap'] = True
          elif arg.find('--mode') > NOTEXIST:
              set_mode(item)
          elif arg.find('--exact') > NOTEXIST:
              enable_argv['exact'] = True
          else:
             print '[error] invalid option %s'%arg
             print "usage : python $SWPTARCE/exec.py --target=/ABSOLUTE_PATH/ --cmd=\"COMMAND\"  <--mem=Mib>  <--log=/ABSOLUTE_PATH/> <--heatmap>  <--exact=True>" 
             sys.exit(1)



def check_option():
    print "\n---------------------------------------------------------------"
    if enable_argv['target'] == True:
       print " * target         : %s "%get_path('target')
    print " * command        : %s "%get_command()
    if enable_argv['mem']:
        print " * mem lim(Mib)   : %s "%get_mem_limit()
    if enable_argv['exact']:
        print "* exact target only : True"
    if enable_argv['heatmap']:
        print "* heatmap : True"

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
         os1G.system('cd $SWPTRACE ; flask run')
     

if __name__ == '__main__': 
   initialize()
   config_option()
   check_option()
   if enable_argv['target']:
       scan_malloc()
   exec_mem_limit(get_command(), get_mem_limit() )
   create_directory() 
   awk_log()
   extract_malloc()
   get_swap_extracted(enable_argv['exact'])
   #if enable_argv['heatmap']:
   #    draw_heatmap(get_path('head'))
   #else:
   #    os.system('mv {}/maps {}'.format(get_path('root'), get_path('head')))
   #    os.system('mv {}/labelized.csv {}'.format(get_path('root'), get_path('head')))
   #    draw_view(get_path('head'), get_meantime())
   #os.system('rm {}/hook.csv'.format(get_path('clone')))
