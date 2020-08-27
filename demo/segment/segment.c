#include <stdio.h>
#include <unistd.h>

static int array[1835008]={0,};
int main(int argc, char *argv)
{
	static int loop=0, idx=0;
	printf("%p %p\n", array, &array[1835007]);
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
