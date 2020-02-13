# include <stdio.h>
# include <stdlib.h>
# include "hmalloc.h"

void* hmalloc(size_t size) {
	void * res = malloc (size);
	printf("%s:%u:%s:%p:%lu\n",__FILE__, __LINE__, __FUNCTION__, res, size);
	return res;
}
