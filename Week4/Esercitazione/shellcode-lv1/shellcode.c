#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main(int argc, char ** argv) {
    char buf[0x1000];
    gid_t gid = getegid();
    setresgid(gid,gid,gid);

    puts("Level1: try there your shellcode");
    fgets(buf, 0x100, stdin);
    int (*ret)() = (int (*)()) buf;
    ret();
}
