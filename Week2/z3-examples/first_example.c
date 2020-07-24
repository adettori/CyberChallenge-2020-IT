#include <stdio.h>
#include <stdlib.h>


int main(int argc, char** argv){
	
	if(argc <= 1 || argc > 2){
		printf("usage: ./first_example <password>\n");
		exit(1);
	}

	
	int x = atoi(argv[1]);

	if( x % 7 == 0 )
		if( x % 5 == 0)
			if( x / 1000 == 5) 
				if((( x / 100) % 10) == 3) {
					printf("Good Job!\n");
					return 0;
			}
	
	printf("Fail !\n");			
	return 0;
}
