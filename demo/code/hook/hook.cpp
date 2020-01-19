#include <dlfcn.h>
#include <iostream>
#include <cstring>
#include <sys/time.h>

using namespace std;

char* (*origin_malloc)(char* dest, const char *src);

char* malloc(char* dest, const char *src) {
      struct timeval tv;
      
      origin_malloc = ( char* (*)(char*, const char*)) dlsym(RTLD_NEXT, "malloc");
       
      return (*origin_malloc) (dest, src);
}

