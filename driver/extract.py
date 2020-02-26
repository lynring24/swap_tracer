from common import *

def isNumber(s):
  try:
    float(s)
    return True
  except ValueError:
    return False


def extract():
    global area_subs
    try:
	print "$ extract.py"
	area_subs = []
	for side in area: 
	    area_subs.append(open(get_path(side) , 'w'))
	with open(get_path('awk'), 'r') as src:
	      for line in src:
		  extracted = parse(line)
		  if extracted is not None:
		     print_line(extracted[0], extracted[1])
	#if ISABSTRACT is used, release last tracked state
	for side in area:
	    area_subs[area.index(side)].close()
	    if is_false_generated(get_path(side)):
	       clean_up(get_path(side))
    	
        if is_false_generated(get_path('total')) == True:
	   raise BaseException
    except BaseException as ex:
           clean_up_and_exit(get_path('head'), 'extract')
          

def parse(line):
# if matches pattern, name and generated after(time)
    regex = re.compile(get_pattern('LOG'))
    matched = regex.search(line)
  
    if matched is None:
       return None
   
    comm = matched.group(2).strip()
    if comm not in get_command():
       return None
    vma = matched.group(3)
    vma =  vma[ vma.rfind(':')+1 : vma.find(')')].strip()
    vma = int(vma)/get_page_size()
    date = matched.group(1)
    time = string_to_date(date, get_pattern("DATE"))
    delta_t = time - get_time()
    if delta_t < timedelta(0):
       return None
    ustime = delta_t.total_seconds()
    return [ustime, vma]



def parse_malloc(line): 
    pattern="(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{6})[+-]\d{2}:\d{2}.*swptracer::(.*):(\d+):(.*)\(\)(.*)=(.*)\((.*)\)"
    matched = re.compile(pattern).search(line)
    if matched is None:
       return None

    timestamp = matched.group(1)
    time = string_to_date(timestamp, get_pattern("DATE"))
    delta_t = time - get_time()
    if delta_t < timedelta(0):
       return None
    fname = matched.group(2)
    nu = int(matched.group(3),0)
    func = matched.group(4)
    var = matched.group(5)
    address = int(matched.group(6),0)
    size = int(matched.group(7),0) 
    area = [address, address + size]
    return [time, fname, nu, func, var, area[0], area[1]] 


def trace_malloc():
    print "trace_malloc"
    merge = open(get_path('merge'), 'w')
    with open(get_path('hook'), 'r') as hook:
         for line in hook:
             res = parse_malloc(line)
             if res is not None: 
                merge.write("%s, %s, %s, %s, %s, %s \n"%(res[0], res[1], res[2], res[3], res[4], res[5], res[6]))


borders = ['0x2000000', '0x40000000', '0x60000000',  '0xA0000000', '0xE0000000', '0xE0100000']
def print_line(duration, vma):
    vpn = int (vma/get_size('BLOCK'))
    area_num = 1
    for border in borders:
        if vma < int(border, 16):
           break
        area_num+=1  
    area_subs[area_num].write("%s, %s \n"%(str(duration), vpn))
    area_subs[0].write("%s, %s \n"%(str(duration), vpn))


 



