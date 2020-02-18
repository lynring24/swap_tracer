hookPageTable = [address, size, address info ] 
key = address 


prev hook
prev swap 


def add_page_table(line):











f_names = [hlog, log]
lines  = list(fileinput.input(f_names))
t_fmt = '%a %b %d %H:%M:%S %Y' # format of time stamps
t_pat = re.compile(r'\[(.+?)\]') # pattern to extract timestamp
#for l in sorted(lines, key=lambda l: strptime(t_pat.search(l).group(1), t_fmt)):
lines =  sorted(lines, key=lambda l: strptime(t_pat.search(l).group(1), t_fmt)):
for line in lines: 
    if isHook :
       add_page_table(line) 
    else : 
       classify swap(line) 

