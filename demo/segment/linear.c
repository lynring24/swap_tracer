#define _GNU_SOURCE 
#include <time.h>
#include <sys/time.h>
#include <string.h>
#include <stdio.h>
#include <unistd.h>
#define  PATH_MAX 200 



static int array[1048576]={0,};


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
        	

	size = &(address[index-1]) - address ;
  	// timestamp, filename, line_number, function, variable, address, size
        fprintf(pFile, "%04d-%02d-%02dT%02d:%02d:%02d.%06ld linear.c 4 main array %p %ld\n",
			localTime->tm_year + 1900, localTime->tm_mon + 1, localTime->tm_mday, localTime->tm_hour, 
			localTime->tm_min, localTime->tm_sec, tv.tv_usec, address, size);        
        fclose(pFile);
}



int main(int argc, char *argv)
{
	static int loop=0, idx=0;
	int * heap;
	hmalloc(array, 1048576);
	printf("total : %llu\n", 1048576 *sizeof(int) + (2*sizeof(int)));
	printf("array[0] : %p \n", array);
	printf("array[100000] : %p \n", &(array[100000]));
	printf("array[1048576] : %p \n", &(array[1048575]));
	printf("loop : %p \n", &loop);
	printf("idx : %p \n", &idx);

	for (loop=0; loop<3; loop++ )
	{
		printf("bss : %ld\n", loop);
		for (idx = 0 ; idx < 1048576; idx ++) 
		{
			array[idx] = (array[idx]+1)%1048576;
		}
	}


	heap = (int*)malloc(sizeof(int)*1048576);
	hmalloc(heap, 1048576);
	printf("heap[0] : %p \n", array);
	printf("heap[100000] : %p \n", &(heap[100000]));
	printf("heap[1048576] : %p \n", &(heap[1048575]));
	for (loop=0; loop<3; loop++ )
	{
		printf("heap : %ld\n", loop);
		for (idx = 0 ; idx < 1048576; idx ++) 
		{
			heap[idx] = (heap[idx]+1)%1048576;
		}
		sleep(5);
	}

	return 0;
}
