import sys, os 
import re


def parse(line):
   
#    print "parse(line)"
    pattern="(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{6})[+-]\d{2}:\d{2}.*swptracer::(.*):(\d+):(.*)\(\)(.*)=(.*)\((.*)\)"
    matched = re.compile(pattern).search(line)
    if matched is None:
       return None

    timestamp = matched.group(1)
    fname = matched.group(2)
    nu = int(matched.group(3),0)
    func = matched.group(4)
    var = matched.group(5)
    address = int(matched.group(6),0)
    size = int(matched.group(7),0) 
    area = [address, address + size]
    
    print line
    print " file name : %s"%fname
    print " line number : %d "%nu
    print " function name :%s "%func
    print " variable name :%s "%var
    print " address area : [%d, %d]"%(area[0], area[1]) 



with open(sys.argv[1] , "r") as src:  
     for line in src:
         parse(line)


# (\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{6})[+-]\d{2}:\d{2}.*swptracer::(.*):(\d+):(.*)\(\)(.*)=(.*)\((.*)\)
 



