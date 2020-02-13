#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <dlfcn.h>
#include <time.h>
#include <sys/time.h>
#include <assert.h>

static void * (*real_malloc)(size_t) = NULL;

__attribute__((constructor))
static void init(void)
{
	real_malloc = dlsym(RTLD_NEXT, "malloc");
	if (NULL == real_malloc) {
		fprintf(stderr, "Error in 'dlsym' :  %s\n", dlerror());
	}
}

void getISOTime() {
	struct timeval tv;
	struct tm * localTime;
	time_t t = time(NULL);

	gettimeofday(&tv, NULL);
	localTime = localtime(&t);
	printf("local: %04d-%02d-%02d %02d:%02d:%02d.%06ld\n", localTime->tm_year + 1900, localTime->tm_mon + 1, localTime->tm_mday, localTime->tm_hour, localTime->tm_min, localTime->tm_sec, tv.tv_usec);
}


void *malloc(size_t size)
{
	void *res = NULL;
	
	if(!real_malloc)
		init();
//	printf("%s\n",__FUNCTION__);
//	getISOTime();
	res=real_malloc(size);
	printf("[%s:%s] %p (%lu)", __FILE__, __LINE__, res);
	return res;
}

