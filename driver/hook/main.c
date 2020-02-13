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
	char * argA;
	argA = (char*) malloc (256 * MEGABYTE);
}


void fooB() {
	char * argB;

	fooC();
        argB = (char*) malloc (256 * MEGABYTE);
}

void fooC() {
	char * argC;
        fooD();
	argC = (char*) malloc (256 * MEGABYTE);
}


void fooD() {
	char * argD = (char*) malloc (256 * MEGABYTE);
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
