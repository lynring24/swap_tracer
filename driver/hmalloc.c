#include <stdio.h>
#include <stdlib.h>
#include "hmalloc.h"
#include <time.h>
#include <sys/time.h>
#include <assert.h>
//#include <syslog.h> 
#include <unistd.h>

#define  PATH_MAX 50 

void* hmalloc(const char * filen, const int line, const char * funcn, char * argn, size_t size) {
	void * res = malloc (size);
	struct timeval tv;
	struct tm * localTime;
	time_t t = time(NULL);
        
        char cwd[PATH_MAX];
        FILE *pFile;
        getcwd(cwd, sizeof(cwd));

	gettimeofday(&tv, NULL);
	localTime = localtime(&t);
        

        pFile = fopen(cwd+"/hook.log", "a+"); 
        fprintf(pFile, "%s", info);
        fclose(pFile);
	return res;
}

//	printf("%04d-%02d-%02dT%02d:%02d:%02d.%06ld::", localTime->tm_year + 1900, localTime->tm_mon + 1, localTime->tm_mday, localTime->tm_hour, localTime->tm_min, localTime->tm_sec, tv.tv_usec);
//	printf("%s:%u:%s() %s=%p(%lu)\n", filen , line , funcn, argn, res, size);
//      openlog("Logs", LOG_NDELAY, LOG_DAEMON);
//	syslog(LOG_DEBUG, "swptracer::%s:%u:%s() %s=%p(%lu)\n", filen , line , funcn, argn, res, size); 
//      closelog();
