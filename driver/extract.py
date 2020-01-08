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
#    ustime = delta_t.total_seconds() * US_TO_SEC
    ustime = delta_t.total_seconds()
    return [ustime, vma]


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
