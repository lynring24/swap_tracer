from utility import *
import csv
import pandas as pd

def isNumber(s):
  try:
    float(s)
    return True
  except ValueError:
    return False


def extract_swap():
    global area_subs
    try:
	print "$ extract ryslog log"
        rsyslog = pd.read_csv(get_path('awk'), header=None, delimiter='\s+')
        if rsyslog.shape[1] > 6 : 
            rsyslog.columns = ['timestamp', 'server', 'dtime', 'swptrace' , 'cmd', 'mode', 'swpentry', 'address']
        else:
            rsyslog.columns = ['timestamp', 'swptrace' , 'cmd', 'mode', 'swpentry', 'address']
        rsyslog['timestamp'] = rsyslog['timestamp'].apply(lambda x: (string_to_date(x) - get_time()).total_seconds())
        rsyslog = rsyslog[rsyslog.timestamp>= 0.0]
        # for map.timestamp faster than in.timestamp && map.swpentry == in.swpentry in[anchor] = map.timestamp
        group = rsyslog.groupby('swpentry')['timestamp'].unique()
        group = group[group.apply(lambda x: len(x)>1)]
        group.to_frame().to_csv(get_path('head')+'/duplicated_entries.csv')
        # anchor the related timestamp

        print "$ generate extracted file [%s, %s] "%(rsyslog.shape[0], rsyslog.shape[1])
        rsyslog[['timestamp', 'cmd', 'mode', 'swpentry', 'address']].to_csv(get_path('merge'))
        if is_false_generated(get_path('merge')):
            raise BaseException 
    except BaseException as ex:
           print ex
           clean_up_and_exit(get_path('merge'), 'extract')
          

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
    if is_false_generated(get_path('merge')):
       print "Allocation Hook False Generated"
       clean_up_and_exit(get_path('merge'),'extract allocation')



