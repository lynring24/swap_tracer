#ifndef HMALLOC_H
#define HMALLOC_H
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

void* hmalloc(const char * filen, const int line, const char * funcn, char * argn, size_t size) ;

#ifdef __cplusplus
}
#endif 

#endif /*HMALLOC_H*/ 
