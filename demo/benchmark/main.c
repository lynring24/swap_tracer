#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <sys/time.h>
#include <time.h>
#include <unistd.h>
#define MEGABYTE 1024*1024

int fooD() ;
int fooC() ;

time_t start, end;
double elapsed;

void skim(char * list) {
     char temp;
     for (int i =0 ;  i  <strlen(list); i++) 
         temp = list[i];
}

int fooA() {
	char * argA;
	argA = (char*) malloc (256 * MEGABYTE);
        skim(argA);
       end = time(NULL);
       elapsed = difftime(end, start);
       if (elapsed >= 59.0) 
                return 0; 
       else
          return 1;
}


int fooB() {
	char * argB;

	fooC();
        argB = (char*) malloc (256 * MEGABYTE);
        skim(argB);
       end = time(NULL);
       elapsed = difftime(end, start);
       if (elapsed >= 59.0) 
                return 0; 
       else
          return 1;

}

int fooC() {
       char * argC;
       fooD();
       argC = (char*) malloc (256 * MEGABYTE);
       skim(argC);
       end = time(NULL);
       elapsed = difftime(end, start);
       if (elapsed >= 59.0) 
          return 0; 
       else
          return 1;


}


int  fooD() {
	char * argD = (char*) malloc (256 * MEGABYTE);
        skim(argD);

       end = time(NULL);
       elapsed = difftime(end, start);
       if (elapsed >= 59.0) 
          return 0; 
       else
          return 1;
}

int main() {
   int cnt = 0;
     
   printf("Malloc for 1 min\n");
   start = time(NULL);
   
   while (1) {
       if (!fooA() ) 
          break;
       if (!fooB() )
          break;
       cnt+=1;
       if (cnt > 2147483645) 
               break;
   } 
   return 0;  
}
