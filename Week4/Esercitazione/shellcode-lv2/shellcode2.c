#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

char shbig[100] = {0};

int main(int argc, char ** argv) {
    char buf[0x40] = {0};
    gid_t gid = getegid();
	setresgid(gid,gid,gid);

    puts("Level2: 19 bytes is not so much..");    
    fgets(buf, 19, stdin);
    fgets(shbig, 100, stdin);
    int (*ret)() = (int (*)()) buf;
    ret();
}
