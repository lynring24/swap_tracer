import sys, platform, os
import re, traceback
from datetime import datetime, timedelta
from configure import *

def isNumber(s):
  try:
    float(s)
    return True
  except ValueError:
    return False


def is_nearby(vma):
   recent_vma = tracked[-1][1] 
   return abs ( recent_vma - vma) < BLOCK 

US_TO_SEC = 1000000
def print_line(time, vma):
    vma = int (vma/BLOCK)
    blank ="%"+str(vma)+"s"
    time = time/US_TO_SEC
    outfile.write("%s, %s \n"%(str(time), vma))


def print_mean_state():
    global tracked 
    if len(tracked)==0:
	return 
    delta_t = 0 
    sum_p = 0
    
    for row in tracked:
       delta_t += row[0] - tracked[0][0]
       sum_p += row[1]

    delta_t = delta_t / len(tracked)
    mtime = delta_t + tracked[0][0]
    mvma = sum_p / len(tracked)
    print_line(mtime, mvma)
    tracked= []



def __parse(line):
# if matches pattern, name and generated after(time)
    pattern =  "(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6})\+\d{2}:\d{2} .*swptrace\((.+)\): map (\(swpentry: \d+, uaddr: \d+\))" 
    regex = re.compile(pattern)
    matched = regex.search(line)
    if matched is None:
       return None
    comm = matched.group(2).strip()
    if comm not in command:
       return None
 
    vma = matched.group(3)
    vma =  vma[ vma.rfind(':')+1 : vma.find(')')].strip()
 
    
    if ISTHRESHOLD and DIGIT_THRESHOLD > len(vma):
       return 
    vma = int(vma)/PAGE_SIZE
# if line is generated after wards 
    date = matched.group(1)
    time = datetime.strptime(date, DATE_PATTERN)
    delta_t = time - start_time
    if delta_t < timedelta(0):
       return None
    ustime = delta_t.total_seconds() * 1000000

    if ISABSTRACT == False:
       print_line(ustime, vma)
    else:
       if len(tracked) != 0 and is_nearby(vma) is False:
         print_mean_state()
    tracked.append([ustime, vma])



def setup():
    if len(sys.argv) < 2 or len(sys.argv) > 6:          
       raise SystemExit
    
    global infile, command, start_time, ISABSTRACT, ISTHRESHOLD, outfile, tracked
    
    if platform.dist()[0] == "Ubuntu":
       infile = "/var/log/syslog"
    else:
       infile = "/var/log/messages"
    
    command = sys.argv[-1].strip()
    start_time = datetime.strptime(sys.argv[-2].strip(), DATE_PATTERN)
    ISABSTRACT = False
    ISTHRESHOLD= False
    print get_current_log_path()
    OUTPUTFILENAME = get_current_log_path() + "/extracted"
    for idx in range(1, len(sys.argv)-2):
        if sys.argv[idx] == '--abstract': 
           ISABSTRACT=True
           OUTPUTFILENAME=OUTPUTFILENAME+'_abs'
        elif sys.argv[idx] == '--threshold':
           ISTHRESHOLD=True
           OUTPUTFILENAME=OUTPUTFILENAME+'_th'
        else : 
           infile = sys.argv[idx]

    outfile = open (OUTPUTFILENAME+".csv", 'w')
    #outfile.write("# Trace : %s \n"%command)
    tracked=[]




if __name__ == '__main__':
   try:
       setup()
       with open(infile, 'r') as src:
            for line in src:
                __parse(line)
    # if ISABSTRACT is used, release last tracked state
       if ISABSTRACT == True:
          print_mean_state()
       outfile.close()
   except BaseException as ex:
       print ex
       print "usage : python trace.py [--abstract] [--threshold] [src file path]  <datetime(+%Y-%m-%dT%H:%M:%S.%6N)> <command>"
   except:
      traceback.print_exc()
      if os.path.exists(LOG_DIR_PATH+"/extracted.csv"):
         os.remove(LOG_DIR_PATH+extraced+"/extracted.csv")
      else: 
	 if os.path.exists(LOG_DIR_PATH+'/extracted_th.csv'):
            os.remove(LOG_DIR_PATH+'/extracted_th.csv')

