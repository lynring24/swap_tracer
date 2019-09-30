import sys, platform, os
import re, traceback
from datetime import datetime, timedelta

def isNumber(s):
  try:
    float(s)
    return True
  except ValueError:
    return False


ABSTRACT = 500 
group = []

def is_nearby(spos):
   recent_pos = group[-1][2] 
   return abs ( recent_pos - spos) < ABSTRACT 


def print_line(time, spos):
    pos = int (spos/ABSTRACT)
    blank ="%"+str(pos)+"s"
    log.write("%s %s \n"%(str(time), spos))


date_pattern = "%Y-%m-%dT%H:%M:%S.%f"
def print_mean_state():
    if len(group)==0:
	return 
    delta_t = timedelta(0) 
    sum_p = 0
    
    for row in group:
       delta_t += row[0] - group[0][0]
       sum_p += row[2]

    delta_t = delta_t / len(group)
    mtime = delta_t + group[0][0]
    mpos = sum_p / len(group)   



def get_info_of(line):
# if matches pattern, name and generated after(time)
    pattern =  "(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6})\+\d{2}:\d{2} .*swptrace\((.+)\): map (\(swpentry: \d+, uaddr: \d+\))" 
    regex = re.compile(pattern)
    matched = regex.search(line)
    if matched is None:
       return None
    comm = matched.group(2).strip()
    if comm not in command:
       return None
 
# if line is generated after wards 
    date = matched.group(1)
# compare with exectime
    time = datetime.strptime(date, date_pattern)
    delta_t = time - exectime
    if delta_t < timedelta(0):
       return None
    ustime = delta_t.total_seconds() * 1000000
    spos = matched.group(3)
    return [ustime, spos]


def get_position_of(line):
    info = get_info_of(line)
    if info is None:
       return   
    time = info[0]
    spos = info[1]

    pos = int(spos[ spos.rfind(':')+1 :spos.find(')')].strip())
    global group
    if option is None:
       print_line(time, pos)
    else:
       if len(group) != 0 and is_nearby(pos) is False:
         print_mean_state()
	 group= []
    group.append([time, pos])


if __name__ == '__main__':
   if len(sys.argv) < 2 or len(sys.argv) > 5:          
      print "usage : trace.py [-m] [log file] <datetime(+%Y-%m-%dT%H:%M:%S.%6N)> <command>"
      exit(1)

   option = None
   if platform.dist()[0] == "Ubuntu":
      fname = "/var/log/syslog"
   else:
      fname = "/var/log/messages"

   command = sys.argv[-1]
   exectime = datetime.strptime(sys.argv[-2], date_pattern)

   if len(sys.argv) == 4:
      if sys.argv[1] == "-m":
         option = True
      else:
         fname = sys.argv[1]
   elif len(sys.argv) == 5:
      option = True
      fname = sys.argv[2]

   try:
       log = open ("../log/"+exectime.strftime('%b%d%H%M%S')+".csv", 'w')
       log.write("# Trace : %s \n"%command)

       with open(fname, 'r') as src:
            for line in src:
                get_position_of(line)
    # if option is used, release last group state
       if option is True:
          print_mean_state()

       log.close()
   except:
      traceback.print_exc()
      if os.path.exists("../log/"+exectime.strftime('%b%d%H%M%S')+".csv"):
         os.remove("../log/"+exectime.strftime('%b%d%H%M%S')+".csv")
