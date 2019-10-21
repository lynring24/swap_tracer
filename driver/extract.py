from common import *

def isNumber(s):
  try:
    float(s)
    return True
  except ValueError:
    return False


def extract():
    global tracked, outfile 
    outfile = open (get_path('extracted'), 'w')
    tracked=[]
    with open(get_path('awk'), 'r') as src:
	 for line in src:
             __parse(line)
	     print line
       # if ISABSTRACT is used, release last tracked state
         if do_abstract():
            print_mean_state()
    outfile.close()



US_TO_SEC = 1000000
def __parse(line):
# if matches pattern, name and generated after(time)
    pattern =  "(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6})\+\d{2}:\d{2} .*swptrace\((.+)\): map (\(swpentry: \d+, uaddr: \d+\))" 
    regex = re.compile(pattern)
    matched = regex.search(line)
    if matched is None:
       return None
    
    comm = matched.group(2).strip()
    print comm
    if comm not in get_command():
       return None
 
    vma = matched.group(3)
    vma =  vma[ vma.rfind(':')+1 : vma.find(')')].strip()
    vma = int(vma)/get_page_size()
 
    #  if it is enable, mush be over threshold 
    if do_threshold() and get_threshold() > len(vma):
       return 
# if line is generated after wards 
    date = matched.group(1)
    time = datetime.strptime(date, get_pattern("DATE"))
    delta_t = time - get_start_time()
    if delta_t < timedelta(0):
       return None
#    ustime = delta_t.total_seconds() * US_TO_SEC
    ustime = delta_t.total_seconds()

    if do_abstract() == False:
       print_line(ustime, vma)
    else:
       if len(tracked) != 0 and is_nearby(vma) is False:
         print_mean_state()
    tracked.append([ustime, vma])



def is_nearby(vma):
   recent_vma = tracked[-1][1] 
   return abs ( recent_vma - vma) < get_block_size()


def print_line(time, vma):
    vma = int (vma/get_block_size())
    blank ="%"+str(vma)+"s"
    #time = time/US_TO_SEC
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


