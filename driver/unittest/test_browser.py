from pprint import pprint 
from common import * 
from extract import extract
from split import split
import subprocess
from requests import get

def config_input():
    if len(sys.argv) > 1: 
       set_mem_limit(sys.argv[1])
       set_command(sys.argv[2])
  

def exe_cmd():
    try:
	rsyslog = open('/etc/rsyslog.conf').read()
	if "# $ActionFileDefaultTemplate RSYSLOG_TraditionalFileFormat" in rsyslog:
	    print "rsyslog timestamping in RFC 3339 format"
	else: 
	    print "rsyslog timestamp traditional file format "
	    os.system('cp /etc/rsyslog.conf /etc/rsyslog.conf.default')
	    os.system('cp ./rsyslog.conf.rfc3339 /etc/rsyslog.conf')

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
	parse_pattern = '(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\,\d{6})\+\d{4} swptrace\((.+)\): map (\(swpentry: \d+, uaddr: \d+\))'
	set_pattern('DATE', date_pattern)
	set_pattern('LOG', parse_pattern)
    except BaseException as ex:
        print ex
	clean_up_and_exit(get_path('head'), 'awk_log')



def run_flask():
    os.environ['SWPTRACE_LOG'] = '/home/leto/Downloads/deneb/swp_log/2019-12-30T17:59:06.552257'
    #os.environ['COMMAND'] = get_command()
    os.environ['FLASK_APP']='app.py'
    ip = get('https://api.ipify.org').text
    os.system('cd $SWPTRACE ; flask run --host=0.0.0.0')
     

if __name__ == '__main__':
   run_flask() 
