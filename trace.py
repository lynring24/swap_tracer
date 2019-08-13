import sys
import re
from datetime import datetime, timedelta

def isNumber(s):
  try:
    float(s)
    return True
  except ValueError:
    return False


ABSTRACT = 500 
group = []
#count swap
#num = -1

def is_nearby(mark, spos):
   recent_pos = group[-1][2] 
   recent_mark = group[-1][1]
   return abs ( recent_pos - spos) < ABSTRACT and recent_mark == mark 


def print_line(time, mark, spos):
    pos = int (spos/ABSTRACT)
    blank ="%"+str(pos)+"s"

    if mark == 'R':
	plots[READ].write("%s %s \n"%(str(time), spos))
    elif mark == 'W':
        plots[WRITE].write("%s %s \n"%(str(time), spos))
    else:
	plots[SWAP].write("%s %s \n"%(str(time), spos))

#    num += 1
#    print "%10s |"%str(time), "%7s |"%spos , blank%(mark)

date_pattern = "%b %d %H:%M:%S"
def print_mean_state():
    if len(group)==0:
	return 
    delta_t = timedelta(0) 
    sum_p = 0
    
    for unit in group:
       delta_t += unit[0] - group[0][0]
       sum_p += unit[2]

    delta_t = delta_t / len(group)
    mtime = (delta_t + group[0][0]).strftime('%Y-%m-%d %H:%M:%S')
    mpos = sum_p / len(group)   
     
    print_line(mtime, group[0][1], mpos) 

def get_info_of(line):
# if matches pattern, name and generated after(time)
   pattern =  "(.+)(\d{2}:\d{2}:\d{2}).+swptrace\((.+)\).*(read|map|write) (.+)" 
   regex = re.compile(pattern)
   matched = regex.search(line)
   
   if matched is None:
      return None

   comm = matched.group(3).strip()
   if comm not in command:
     return None

# if line is generated after wards 
   date = matched.group(1)
   time = matched.group(2)

# compare with exectime
   time = datetime.strptime(date+time, date_pattern)
   if time < exectime:
      return None

   exct = matched.group(4)
   spos = matched.group(5)
   return [time, exct, spos]



def get_position_of(line):
   info = get_info_of(line)

   if info is None:
     return   
   time = info[0]
   exct = info[1]
   spos = info[2]

#  if needed to count swap 
#   global num 
 
   if exct == "read":
      mark = 'R'
      pos = int(spos)
   elif exct == "write":
      mark = 'W'
      pos = int(spos)
   else: 
 #     num += 1
      mark = 'X'
      pos = int(spos[11:spos.find(',')])
      upos = spos[spos.find(',')+1:-2]  
   
   global group
   if option is None:
        print_line(time, mark, pos)
   else:
     if len(group) != 0 and is_nearby(mark, pos) is False:
     	print_mean_state()
	group= []
   	
     group.append([time, mark, pos])


if len(sys.argv) < 2 or len(sys.argv) > 5:          
  print "usage : swptrace.py [-m] [log file] <datetime(%b %d %H:%M:%S)> <command>"
  exit(1)


option = None
fname = "/var/log/messages"
command = sys.argv[-1][:15]
exectime = datetime.strptime(sys.argv[-2], date_pattern)

if len(sys.argv) == 4:
  if sys.argv[1] == "-m":
     option = True
  else:
     fname = sys.argv[1]
elif len(sys.argv) == 5:
  option = True
  fname = sys.argv[2]

READ = 0 
WRITE = 1
SWAP = 2
ftype = ["read","write","swap"]
plots =[]

for idx in range(3):
   temp = open ("swaptracer/plot/"+exectime.strftime('%H%M%S')+"-"+ftype[idx]+".plot", 'w')
   temp.write("# Trace : %s \n"%command)
   plots.append(temp)

with open(fname, 'r') as log:
   for line in log:
      get_position_of(line)
# if option is used, release last group state
if option is True:
   print_mean_state()

plots[SWAP].write( "# Number of Swap = %s"%str(num));

for plot in plots:
 plot.close()
