#include <errno.h>
#include <stdio.h>
#include <sys/mman.h>
#include <unistd.h>
#include <time.h>
#include <stdlib.h>
#include <unistd.h>
#include <ctype.h>

void err_sys(const char* x) 
{ 
	    perror(x); 
	        exit(1); 
}


static long long * list_bot;
static long long * list_top;
static long long * list_pos;
static long long list_siz;

int list_init(long len) {
	list_top = (long long *) mmap(NULL, len *sizeof(long long), PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, -1 ,0);
	if (list_top == MAP_FAILED) 
		return -1;
	list_bot = list_top;
	list_siz = len;
	printf("list_init: top=%p, len=%ld\n", list_top, len);
	return 0;
}



long long *list_add(long long *l, int val) {
	long long *elt;
	elt = l;
	*elt = val;
	elt = elt++;
	return elt;
}


int main(void) {
	long long *l = NULL;
	pid_t pid;
	long long MAX = (1<<29);

	if (list_init(MAX) < 0) 
		err_sys("list_init error");

	l = list_bot;
	for (long long idx = 0; idx < MAX; idx++) 
		l = list_add(l, rand()%MAX);

	for( int iter = 0 ; iter < 5 ; iter++  ) { 
		printf("iter : %d\n", iter);
		l = list_bot;
		for (long long idx = 0; idx < MAX; idx++) { 
			long long temp = *(l+idx);	
			*(l+idx)=temp+1;
		}
	}

	return 0;
}

