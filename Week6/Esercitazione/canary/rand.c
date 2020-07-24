#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char *argv[]) {

	int seed = atoi(argv[1]);
	int rand_off;
	int stackguard;
	
	srand(seed);
	
	stackguard = rand();
	rand_off = rand()%4;
	
	*((char*)&stackguard + (rand_off % 4)) = (char) 0;

	printf("Stackguard: %d END", stackguard);

	return 0;
}
