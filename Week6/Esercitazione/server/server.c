#define _POSIX_SOURCE
#include <signal.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <errno.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#define MAX_SIZE	4096
#define MAX_CONNECT	20
#define PREFIX      "The string that you just sent me is : "

void cleararray(char **array)
{
	unsigned int i = 0;

	while(array[i]) {
		memset(array[i], 0, strlen(array[i]) + 1);
		i++;
	}
}

ssize_t recv_until(int fd, char *buf, size_t n, char stop)
{
	size_t size = 0;
	char c;
	ssize_t rc;

	while (size < n)
	{
		rc = recv(fd, &c, 1, 0);

		if (rc == -1) {
			if (errno == EAGAIN || errno == EINTR) {
				continue;
			}
			return -1;
		}

		buf[size] = c;

		if (c == stop) {
			buf[size] = '\0';
			break;
		}

		size++;
	}

	return size;
}

ssize_t sendlen(int fd, const char *buf, size_t n)
{
	ssize_t rc;
	size_t nsent = 0;

	while (nsent < n)
	{
		rc = send(fd, buf + nsent, n - nsent, 0);

		if (rc == -1) {
			if (errno == EAGAIN || errno == EINTR) {
				continue;
			}
			return -1;
		}

		nsent += rc;
	}
	return nsent;
}

void handle_client(int client)
{
	char received[MAX_SIZE] = {0};

	strcpy(received, PREFIX);

	if (recv_until(client, received + strlen(received), MAX_SIZE, '\n') == -1) {
		close(client);
		exit(1);
	}

	sendlen(client, received, strlen(received));
}

void handle_signal(int signal)
{
	signal = signal;
	waitpid(-1, NULL, WNOHANG);
}

int main(int argc, char **argv, char **envp)
{
	int server, client, port, opt;
	unsigned int clientlen;
	struct sockaddr_in structserver, structclient;
	struct sigaction sig;
	pid_t pid;

	if (argc != 2) {
		printf("[-] Usage : %s <port>\n", argv[0]);
		exit(1);
	}

	if ((port = atoi(argv[1])) < 1024) {
		puts("[-] Port must be > 1024");
		exit(1);
	}

	cleararray(argv);
	cleararray(envp);

	sig.sa_handler = handle_signal;
	sigemptyset(&sig.sa_mask);
	sig.sa_flags = SA_NOCLDSTOP;

	if (sigaction(SIGCHLD, &sig, NULL) == -1) {
		perror("[-] Sigaction Fail ");
		exit(1);
	}

	if ((server = socket(PF_INET, SOCK_STREAM, 0)) == -1) {
		perror("[-] Socket Fail ");
		exit(1);
	}

	puts("[+] Socket created.");

	opt = 1;

	if (setsockopt(server, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt)) != 0) {
		perror("setsockopt");
		exit(1);
	}

	memset(&structserver, 0, sizeof(structserver));
	structserver.sin_family = AF_INET;
	structserver.sin_addr.s_addr = inet_addr("0.0.0.0");
	structserver.sin_port = htons(port);

	if (bind(server, (struct sockaddr *)&structserver, sizeof(structserver)) == -1) {
		perror("[-] Bind Fail ");
		exit(1);
	}

	if (listen(server, MAX_CONNECT) == -1) {
		perror("[-] Listen Fail ");
		exit(1);
	}

	printf("[+] Listening on %d.\n", port);

	for(;;)
	{
		memset(&structclient, 0, sizeof(structclient));
		clientlen = sizeof(structclient);
		client = accept(server, (struct sockaddr *)&structclient, &clientlen);

		if (client == -1) {
			if (errno != EINTR) {
				perror("[-] Accept Fail ");
			}
			continue;
		}

		printf("[+] New client : %s\n", inet_ntoa(structclient.sin_addr));

		if ((pid = fork()) == -1) {
			perror("[-] Fork Fail ");
			continue;
		}

		if (!pid) { /* child */
			close(fileno(stdin));
			close(fileno(stdout));
			close(fileno(stderr));

			if ((pid = fork()) == -1) {
				perror("[-] Fork Fail ");
				continue;
			}

			if (!pid) { /* child's child; prevents zombies */
				alarm(60);
				handle_client(client);
			}

			exit(0);
		} else { /* parent */
			close(client);
		}
	}

	close(server);
	return 0;
}
