#define _GNU_SOURCE 
#include <time.h>
#include <sys/time.h>
#include <string.h>
#include <stdio.h>
#include <unistd.h>
#define  PATH_MAX 200 



static int array[1835008]={0,};

void hmalloc(int * address, int index) {
	struct timeval tv;
	struct tm * localTime;
	time_t t = time(NULL);
        
        char cwd[PATH_MAX];
	long size;

        FILE *pFile;
        getcwd(cwd, sizeof(cwd));


	gettimeofday(&tv, NULL);
	localTime = localtime(&t);

        //hook.log under /moddir
        strcat(cwd, "/hook.csv");
        pFile = fopen(cwd, "a+");
	if (pFile == NULL)
	   perror("[Error] while creating hook.csv");
        	
   	unsigned int converted = (unsigned int)(address) &  0xFFFFFFFF;
  	if (converted & 0x80000000)
		converted = -((~converted & 0xFFFFFFFF) + 1);

	size = sizeof(int)*index;
  	// timestamp, filename, line_number, function, variable, address, size
        fprintf(pFile, "%04d-%02d-%02dT%02d:%02d:%02d.%06ld linear.c 4 main array %p %ld\n",
			localTime->tm_year + 1900, localTime->tm_mon + 1, localTime->tm_mday, localTime->tm_hour, 
			localTime->tm_min, localTime->tm_sec, tv.tv_usec, converted, size);        
        fclose(pFile);
}



int main(int argc, char *argv)
{
	static int loop=0, idx=0;
	//printf("%p %p %p\n", array, &array[1835007], convertto32(&array[1835007]));
	hmalloc(array, 1835008);
	for (loop=0; loop<5; loop++ )
	{
		printf("loop : %ld\n", loop);
		for (idx = 0 ; idx <1835008; idx ++) 
		{
		//	if (idx < 5)
		//		printf("%p ", &array[idx]);
			array[idx] = idx;
		}
		sleep(60);
	}
	return 0;
}
