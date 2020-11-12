import os 
import sys
import time
import subprocess
from utility import *

limit=sys.argv[1]
command=sys.argv[2]
print '{} {}'.format(limit, command)
if limit != 0:
    command='sudo sh $SWPTRACE/exec_mem_lim.sh {} \"{}\"'.format(str(limit), command)

command = "(cd {}; {})".format(pwd, command)

# child process 
start_time = time.time()
child_process= subprocess.Popen(command, stdin=None, stdout=None, shell=True)

# wait for the grand child comes up
time.sleep(10)

os.system('$SWPTRACE/swptrace {} {}'.format(child_process.pid, 1));
print "[Exec] {} sec".format(time.time() - start_time)



