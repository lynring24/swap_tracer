#include <stdio.h>

int main(int argc, char *argv)
{
	int array[1835008]={0,};
	for (int loop=0; loop<5; loop++ )
	{
		for (int idx = 0 ; idx <1835008; idx ++) 
		{
			array[idx] = idx;
		}
	}
	return 0;
}
