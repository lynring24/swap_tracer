#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <sys/time.h>

#define MEGABYTE 1024*1024

void main() {
	struct timeval tv;
	char *current_data;

	while(1) {
		gettimeofday(&tv, NULL);
		current_data = ( char*) malloc(MEGABYTE);
		sprintf( current_data, "%d", tv.tv_usec);
		sleep(1);
	}
	exit(0);
}
