#define _GNU_SOURCE 
#include <time.h>
#include <sys/time.h>
#include <string.h>
#include <dlfcn.h>
#include "hmalloc.h"
//#include <stdio.h>
//#include <stdlib.h>
//#include <stdint.h>
//#include <unistd.h>

#define  PATH_MAX 200 


void* hmalloc(const char * filen, const int line, const char * funcn, char * argn, size_t size) {
	void *(*libc_malloc)(size_t) = dlsym(RTLD_NEXT, "malloc");

	struct timeval tv;
	struct tm * localTime;
	time_t t = time(NULL);
        
        char cwd[PATH_MAX];
        FILE *pFile;
        getcwd(cwd, sizeof(cwd));


	gettimeofday(&tv, NULL);
	localTime = localtime(&t);

        //hook.log under /moddir
        strcat(cwd, "/hook.csv");
        pFile = fopen(cwd, "a+");
	if (pFile == NULL)
	   perror("[Error] while creating hook.csv");
        	
	void * res = libc_malloc(size);
  	// timestamp, filename, line_number, function, variable, address, size
        fprintf(pFile, "%04d-%02d-%02dT%02d:%02d:%02d.%06ld %s %u %s %s %p %p\n",
			localTime->tm_year + 1900, localTime->tm_mon + 1, localTime->tm_mday, localTime->tm_hour, localTime->tm_min, localTime->tm_sec, tv.tv_usec, 
                        filen , line , funcn, argn, res, res+size);        
        fclose(pFile);
	//return libc_malloc(size);
	return res;
}

