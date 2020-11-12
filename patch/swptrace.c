#include <linux/kernel.h>
#include <linux/syscalls.h>
#include <linux/uaccess.h>
#include <linux/swptrace.h>
#include <linux/linkage.h>
#include <linux/sched.h>

#define SWPON 1
#define SWPOFF 0

int SWPTRACE=SWPOFF;
pid_t SWPTARGET=0;

MODULE_LICENSE("GPL");

SYSCALL_DEFINE2(swptrace, pid_t, pid, int , mode)  
{
	long pid_l = (long) pid;

	SWPTRACE = mode; 
	SWPTARGET = pid; 
	printk("[SWPTRACE] target(%ld) %s\n", pid_l, (SWPTRACE==SWPON)?"ON":"OFF");
	return 0;
}

int is_child(pid_t child)
{
	int is_child = 0;
	static struct task_struct *curr;
	
	if (child == SWPTARGET) 
		is_child = 1;
	else {
		curr = pid_task(find_get_pid(child), PIDTYPE_PID); 
		if(!curr)
			return -EINVAL;
		
		while( curr->pid != 0) {
			if ( curr->pid == SWPTARGET ) {
				is_child = 1;
				break;
			}
			curr = curr->parent;
		}
	}
	return is_child;
}


