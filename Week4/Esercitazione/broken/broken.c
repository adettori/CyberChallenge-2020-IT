#include <stdio.h>
#include <stdlib.h>

int main(int argc, char ** argv) {
    char buf[0x10];
    puts("What are you gonna do now?");
    printf("%p\n", buf);
    gets(buf);
}