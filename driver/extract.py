from utility import *

def isNumber(s):
  try:
    float(s)
    return True
  except ValueError:
    return False


def extract_swap():
    global area_subs
    try:
	print "$ extract swap"
        merge = open(get_path('merge'), 'a+')
	with open(get_path('awk'), 'r') as src:
	      for line in src:
		  extracted = parse_swap(line)
		  if extracted is not None:
		     merge.write("%s, %s \n"%(str(extracted[0]), extracted[1]))
	#if ISABSTRACT is used, release last tracked state
	merge.close()
    except BaseException as ex:
           print ex
           clean_up_and_exit(get_path('head'), 'extract')
          

def parse_swap(line):
# if matches pattern, name and generated after(time)
    regex = re.compile(get_pattern('log'))
    matched = regex.search(line)
  
    if matched is None:
       return None
   
    comm = matched.group(2).strip()
    if comm not in get_command():
       return None
    vma = matched.group(3)
    vma =  vma[ vma.rfind(':')+1 : vma.find(')')].strip()
    #vma = int(vma)/get_page_size()
    vma = int(vma)
    date = matched.group(1)
    time = string_to_date(date)
    delta_t = time - get_time()
    if delta_t < timedelta(0):
       return None
    ustime = delta_t.total_seconds()
    return [ustime, vma]



def parse_malloc(line): 
    pattern="(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{6})::(.*):(\d+):(.*)\(\)(.*)=(.*)\((.*)\)"
    matched = re.compile(get_pattern('hook')).search(line)
    if matched is None:
       return None

    timestamp = matched.group(1)
    time = string_to_date(timestamp)
    delta_t = time - get_time()
    if delta_t < timedelta(0):
       return None
    ustime = delta_t.total_seconds()
    fname = matched.group(2)
    nu = int(matched.group(3),0)
    func = matched.group(4)
    var = matched.group(5)
    address = int(matched.group(6),0)
    size = int(matched.group(7),0) 
    area = [address, address + size]
    return [ustime, area[0], area[1], fname, func, var] 


def extract_malloc():
    print "$ extract malloc"
    merge = open(get_path('merge'), 'a+')
    with open(get_path('hook'), 'r') as hook:
         for line in hook:
             res = parse_malloc(line)
             if res is not None: 
                merge.write("%s, %d, %d, %s, %s, %s\n"%(res[0], res[1], res[2], res[3], res[4], res[5]))



