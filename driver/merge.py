import fileinput
import re
from time import strptime
from common import *

def merge():
	f_names = [get_path('hook'), get_path('total')] # names of log files
        print f_names
	lines = list(fileinput.input(f_names))
        lines.sort()
	#t_fmt = '%a %b %d %H:%M:%S %Y' # format of time stamps
	t_fmt = get_pattern('DATE')
	t_pat = re.compile(get_pattern('MICROSEC')) # pattern to extract timestamp
#	with open('your_file.txt', 'w') as f:
	  #   for i in lines:
	#	 f.write("%s\n"%i)      
	for l in sorted(lines, key=lambda l: strptime(t_pat.search(l).group(1), t_fmt)):
	    print l,
