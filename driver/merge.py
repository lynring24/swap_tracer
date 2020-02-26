import fileinput
import re
from time import strptime
from common import *

#		t_fmt = '%Y-%m-%dT%H:%M:%S.%f'
#		t_pat = re.compile('(%Y-%m-%dT%H:%M:%S.%f).*' ) # pattern to extract timestamp
#		with open('test2.txt', 'w') as f:
#		     for l in sorted(lines, key=lambda l: strptime(t_pat.search(l).group(1), t_fmt)):
#			 f.write("%s\n"%l)
def merge():
        with open(get_path('merge'),'r') as merge:
                lines = merge.readlines()
                lines.sort()
		with open('test.txt', 'w') as f:
		     for line in lines: 
			 f.write("%s\n"%line)

