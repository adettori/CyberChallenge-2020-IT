#include <stdio.h>
#include <stdlib.h>

void safe_gets( long * buf, int len) {
    int n;
    puts("Tell me a number");
    scanf("%d", &n);

    if (n < len) {
        long x;
        puts("I liked it! You can tell me another number!");
        scanf("%ld", &x);
        buf[n] = x;
    } else {
        puts("Nahhh you are trying to BoF me, i know it");
    }
}

void safe_printf( long * buf, int len) {
    int n;
    puts("What do you want to read?");
    scanf("%d", &n);

    if (n < len) 
        printf("Here it is what you were looking for: %ld\n", buf[n]);
    else 
        puts("NaN");
}

void menu() {
    puts("1) Write a number");
    puts("2) Read a number");
    puts("0) Exit");   
}

int main(int argc, char ** argv) {
    struct {
        volatile int len;
        long buf[64];
    } s;
    s.len = 64;
    int choice;
    while (1) {
        menu();
        scanf("%d", &choice);
        if (choice == 1)
            safe_gets(s.buf, s.len);
        else if (choice == 2)
            safe_printf(s.buf, s.len);
        else
            break;
    }    
}