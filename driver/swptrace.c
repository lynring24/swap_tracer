#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>

#define __NR_swptrace 335
int main(int argc, char ** argv)
{
	pid_t pid; 
	int mode; 
	int result;

	pid = atoi(argv[1]);
	mode = atoi(argv[2]);
	result = syscall(__NR_swptrace, pid, mode); 
	return 0;
}

