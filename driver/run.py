from pprint import pprint 
from common import * 
from extract import extract
from split import split


def execute():
    try:
	rsyslog = open('/etc/rsyslog.conf').read()
	if "# $ActionFileDefaultTemplate RSYSLOG_TraditionalFileFormat" in rsyslog:
	    print "rsyslog timestamping in RFC 3339 format"
	else: 
	    print "rsyslog timestamp traditional file format "
	    os.system('cp /etc/rsyslog.conf /etc/rsyslog.conf.default')
	    os.system('cp ./rsyslog.conf.rfc3339 /etc/rsyslog.conf')

	exe_instr='sudo sh exec_mem_lim.sh '+ str(get_mem_limit()) +' \"'+ get_command() + '\"'
	print "\n$"+ exe_instr
	os.system(exe_instr)
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
        instr ='dmesg -T | grep swptrace > '+get_path('awk')
        os.system(instr)
	print "\n$ "+instr+"\n"
	date_pattern= '%a %b %d %H:%M:%S %Y'
	parse_pattern = '\[([a-zA-Z]{3} [a-zA-Z]{3} \d{2} \d{2}:\d{2}:\d{2} \d{4})\] swptrace\\((.+)\\): map (\\(swpentry: \\d+, uaddr: \\d+\\))'
	set_pattern('DATE', date_pattern)
	set_pattern('LOG', parse_pattern)
    except BaseException as ex:
        print ex
	clean_up_and_exit(ex, get_path('awk'), 'awk_log')


if __name__ == '__main__':
   set_up_json()
   execute()
   set_up_path()
   awk_log()
   extract()
#   split()


