#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <sys/time.h>
#include <time.h>
#include <unistd.h>

#define MEGABYTE 1024*1024

void fooD() ;
void fooC() ;

void fooA() {
	char * d;

	printf("%s\n",__FUNCTION__);
	d = (char*) malloc (256 * MEGABYTE);
	printf("%s\n",__FUNCTION__);
}


void fooB() {
	char * d;

	fooC();
    d = (char*) malloc (256 * MEGABYTE);
}

void fooC() {
	char * d;
    fooD();
	d = (char*) malloc (256 * MEGABYTE);
}


void fooD() {
	char * d;
	d = (char*) malloc (256 * MEGABYTE);
}

int main() {
	printf("start main\n");
	int cnt = 0;
        while (cnt < 10) {
	     cnt += 1;
             fooA();
             fooB();
        } 
   return 1;  
}
