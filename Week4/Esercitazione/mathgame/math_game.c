#include "stdio.h"
#include "stdlib.h"
#include "time.h"
#include "string.h"

#define MAX_SIZE_USERNAME 64
#define MAX_ROUNDS 100
#define BANNER  " _____ _                            _   _                                  \n|_   _| |                          | | | |                                 \n  | | | |__   ___   _ __ ___   __ _| |_| |__     __ _  __ _ _ __ ___   ___ \n  | | | '_ \\ / _ \\ | '_ ` _ \\ / _` | __| '_ \\   / _` |/ _` | '_ ` _ \\ / _ \\\n  | | | | | |  __/ | | | | | | (_| | |_| | | | | (_| | (_| | | | | | |  __/\n  \\_/ |_| |_|\\___| |_| |_| |_|\\__,_|\\__|_| |_|  \\__, |\\__,_|_| |_| |_|\\___|\n                                                 __/ |                     \n                                                |___/                      \n"              

char username[MAX_SIZE_USERNAME+1];

void greetings() {
    puts(BANNER);
    puts("Nobody has ever made 100 points, will you be the first?\n\n");
}

void getUsername() {
    puts("Whats your name?");
    // idk rick, it seems safe to me...
    fgets(username, MAX_SIZE_USERNAME, stdin);

    // remove trailing newline
    char *pos;
    if ((pos=strchr(username, '\n')) != NULL) *pos = '\0';
    puts("");
}

void playTheGame() {
    int score = 0;

    int r1, r2;
    int user_answer, correct_answer;

    int round_n;

    // Always seed your random number generators, nobody wants to be hacked
    srand(time(NULL));

    puts("Are you ready for some math?");
    
    for (round_n = 1; round_n <= MAX_ROUNDS; ++round_n) {

        r1 = rand() % 100;
        r2 = rand() % 100;

        printf("[Round number %d] Whats %d + %d ?\n", round_n, r1, r2);
        scanf("%d", &user_answer);

        // Machine learing stuff
        correct_answer = r1 + r2;

        if (user_answer == correct_answer) {
            printf("Correct, your score is now %d\n", ++score);
        }
        else {
            printf("Wrong, your score is now %d\n", --score);
        }
    }

    printf("\nOk %s, the game is over, your total score is: %d/%d\n\n", username, score, MAX_ROUNDS);
}

void getUserFeedback() {
    int feedback;
    char response;

    do {
        puts("Heeey, before you go, do you want to leave a feedback? [y/n] ");
        scanf(" %c", &response); 

    } while( response != 'y' && response != 'n');

    if ( response == 'y') {
        puts("Ok cool, give us a score between 0 and 10\n");
        scanf("%d", &feedback);

        while (feedback < 0 || feedback > 10) {
            puts("Must be between 0 and 10, i don't make the rules i'm sorry... enter again");
            scanf("%d", &feedback);
        }
        puts("Wery nice, thanks for playing with us :)");
    }
    else {
        puts("What is wrong with you?");
    }
    

    if (feedback == 42) {
        puts("\033[1;31mWhait what? Did you hack us? How did you do it?\033[0m");
        system("/bin/sh");
    }
}

int main(int argc, char ** argv) {
    greetings();
    getUsername();
    playTheGame();
    getUserFeedback();
    
    return 0;
}
