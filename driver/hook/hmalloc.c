# include <stdio.h>
# include <stdlib.h>
# include "hmalloc.h"
#include <time.h>
#include <sys/time.h>
#include <assert.h>


void getISOTime();
void* hmalloc(const char * filen, const int line, const char * funcn, char * argn, size_t size) {
	void * res = malloc (size);
	printf("%s:%u:%s allocate %s in %p(%lu)\n", filen , line , funcn, argn, res, size);
	getISOTime();
	return res;
}

void getISOTime() {
	struct timeval tv;
	struct tm * localTime;
	time_t t = time(NULL);

	gettimeofday(&tv, NULL);
	localTime = localtime(&t);
	printf("local: %04d-%02d-%02d %02d:%02d:%02d.%06ld\n", localTime->tm_year + 1900, localTime->tm_mon + 1, localTime->tm_mday, localTime->tm_hour, localTime->tm_min, localTime->tm_sec, tv.tv_usec);
}
