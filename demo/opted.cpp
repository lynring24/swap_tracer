# include <stdio.h>
# include <stdlib.h>
# include <sys/time.h>
# include <time.h>
# include <sys/resource.h>
# include <iostream>
# include <thread>


// long double = 8 byte, target : 128 Mib 
//unsigned long int  MAX = 1<<30; 
unsigned long int MAX = 1<<29; 
long int WINDOW = MAX/8;
struct timeval tvBegin, tvEnd, tvDiff;

using std::thread;

thread prefetcher;

void prefetch(double * target, long offset) {
	double load;
	printf("range : %ld - %ld \n", offset, (WINDOW+ offset)%MAX);
	for ( long index = 0; index < WINDOW-1 ; index++) {
		load = target[(index+offset)%MAX];
	}
}


void start_thread(double *target, long offset) {
     prefetcher = thread(prefetch, target, offset);

}


int timeval_subtract(struct timeval *result, struct timeval *t2, struct timeval *t1)
{
	long int diff = (t2->tv_usec + 1000000 * t2->tv_sec) - (t1->tv_usec + 1000000 * t1->tv_sec);
	result->tv_sec = diff / 1000000;
	result->tv_usec = diff % 1000000;
	return (diff<0);
}



void timeval_print(struct timeval *tv)
{
	char buffer[30];
	time_t curtime;

	printf("%ld.%06ld", tv->tv_sec, tv->tv_usec);
	curtime = tv->tv_sec;
	strftime(buffer, 30, "%m-%d-%Y 	%T", localtime(&curtime));
	printf(" = %s.%06ld\n", buffer, tv->tv_usec);
}


int main(int argc, char * argv []) {
	double * array = (double*) malloc(sizeof(double)*MAX);

	int DELAY = 0;
	int SLIP = MAX/8;

	gettimeofday(&tvBegin, NULL);
	timeval_print(&tvBegin);
	for ( long i=0; i < MAX ; i++ ) 
		array[i] = 0; 
	for ( int loop = 0; loop < 3; loop++) {		
		if ( loop ==1) {
			start_thread(array, SLIP);
			prefetcher.detach();
		}
		printf("loop : %d\n",loop);
		for ( long i=0; i < MAX ; i++ ) {
			array[i] = (array[i] + rand())*1.0;
		}
	}

	gettimeofday(&tvEnd, NULL);
	timeval_print(&tvEnd);

	timeval_subtract(&tvDiff, &tvEnd, &tvBegin);
	printf("%ld.%06ld sec \n", tvDiff.tv_sec, tvDiff.tv_usec);

	free(array);
	return 0;
}
