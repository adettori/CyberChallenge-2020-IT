#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/mman.h>
#include <openssl/sha.h>

#define SHA1_SIZE	20
#define MAX_SIZE	30
#define HASH_LOGIN	"22ced300842e468ad2d5449158708b18dc1f6d66"
#define HASH_PASS	"7280ffe5d72b47186f62ef575bfc4dd42c92d053"

#define stackguard_check(canary) do { \
		if ((canary) != stackguard) { \
			stackguard_fail();        \
		}                             \
    } while (0);

static char creds[MAX_SIZE * 2 + 1] = {0};

static int pad1[4096]; /* unused data */
static int stackguard;
static int pad2[4096]; /* unused data */

int stackguard_get(void)
{
	static int initialized = 0;

	if (initialized) {
		return stackguard;
	}

	srand(getpid());
	stackguard = rand();
	*((char*)&stackguard + (rand() % 4)) = '\x00';

	/*
	 * prevent tampering with the canary (patent pending)
	 * added padding around it to avoid changing memory permission of other
	 * data that reside nearby
	 */
	mprotect((int)(&stackguard) & ~0xfff, 0x1000, PROT_READ);

	initialized = 1;

	return stackguard;
}

void stackguard_fail(void)
{
	puts("Stack Smashing detected !");
	exit(1);
}

int check(const char *login, const char *password)
{
	int canary = stackguard_get();
	char hashlog[SHA1_SIZE + 1] = {0};
	char hashpass[SHA1_SIZE + 1] = {0};
	char goodlog[] = HASH_LOGIN;
	char goodpass[] = HASH_PASS;
	int res;

	SHA1(login, strlen((char*)login), hashlog);
	SHA1(password, strlen((char*)password), hashpass);

	res = (strcmp(hashlog, goodlog) == 0 && strcmp(hashpass, goodpass) == 0);
	stackguard_check(canary);

	return res;
}

void read_secret(void)
{
	int canary = stackguard_get();
	char secret[1024];

	puts("What is your secret?");
	gets(secret); /* safe to use with stackguard! */
	puts("Ok, I'll keep it safe!");

	stackguard_check(canary);
}

int check_creds(void)
{
	int canary = stackguard_get();
	int i;
	int len;
	int ret;
	char login[MAX_SIZE + 1];
	char password[MAX_SIZE + 1];

	/* read credentials */

	gets(creds); /* safe to use with stackguard! */
	len = strlen(creds);

	/* extract login / password */

	for (i = 0; i < len && creds[i] && creds[i] != ':'; i++);

	if (creds[i] != ':') {
		puts("Invalid format, expected 'login:password'");
		exit(1);
	}
	creds[i++] = 0;

	strcpy(password, &creds[i]);
	strcpy(login, creds);

	/* check login / password */
	ret = check(login, password);

	stackguard_check(canary);

	return ret;
}

int main(int argc, char **argv)
{
	if (check_creds()) {
		puts("Good Boy =)");
		read_secret();
	} else {
		puts("Bad Boy =(");
	}

	return 0;
}
