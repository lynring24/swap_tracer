import os 
import subprocess


def exec_mem_lim(command, limit):

    MEMLIM=limit * 1024 * 10224

    MEMCG_ORIG_DIR='/sys/fs/cgroup/memory/'

    MEMCG_DIR='/sys/fs/cgroup/memory/run_mem_lim_$USER'
    os.system('mkdir -p {}'.format(MEMCG_DIR))
    os.system("echo $$ >> {}/cgroup.procs".format(MEMCG_DIR))
    os.system("echo $MEMLIM > {}/memory.limit_in_bytes".format(MEMCG_DIR)) 
    
    #pid = os.fork()
    #if pid == 0:
    #else:

    # child process 
    try: 
        p = subprocess.Popen(command, stdin=None, stdout=None, shell=True)
        print "pid : {}\n".format(p.pid)
        os.system('cat /proc/$(pgrep -P {})/maps > maps'.format(p.pid))
        out, err = p.communication()
    except: 
        pass

    
    #clean_up='while read -r pid; do sudo bash -c "echo $pid > {}/tasks" done < {}/tasks'.format(MEMCG_ORIG_DIR, MEMCG_DIR)

    #os.system(clean_up)

    #os.system("sudo rmdir {}".format(MEMCG_DIR))


exec_mem_lim('./linear', 3*1024)
